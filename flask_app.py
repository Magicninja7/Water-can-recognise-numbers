from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import numpy as np
import knn 

app = Flask(__name__)
CORS(app)


def convert_png_to_array(image_data_url: str):
    try:
        # decode base64 image
        if image_data_url.startswith('data:image'):
            # rm prefix
            base64_data = image_data_url.split(',')[1]
        else:
            base64_data = image_data_url
        
        # base64 2 bytes 2 pil img
        image_bytes = base64.b64decode(base64_data)
        img = Image.open(io.BytesIO(image_bytes))
        
        #since canvas size is fixed to 400x400, not needed
        #img = img.resize((400, 400), Image.Resampling.LANCZOS)

        # rgba to rgb+wh background
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        # grayscale
        img_gray = img.convert('L') # 'L' mode is for grayscale
        img_resized = img_gray.resize((40, 40), Image.Resampling.LANCZOS)
        img_array = np.array(img_resized)
        binary_array = (img_array < 128).astype(int)

        # 3. Find the bounding box of the content
        rows_with_content = np.any(binary_array == 1, axis=1)
        cols_with_content = np.any(binary_array == 1, axis=0)

        if not np.any(rows_with_content) or not np.any(cols_with_content):
            binary_array = np.zeros((20, 20), dtype=int)
        else:
            # find box
            top = np.argmax(rows_with_content)
            bottom = len(rows_with_content) - np.argmax(rows_with_content[::-1]) - 1
            left = np.argmax(cols_with_content)
            right = len(cols_with_content) - np.argmax(cols_with_content[::-1]) - 1
            
            cropped = binary_array[top:bottom+1, left:right+1]
            h, w = cropped.shape
            
                # calc max support point +-1
            max_content_size = 18
            
            # scale the mf
            if h > w:
                scale_factor = max_content_size / h
            else:
                scale_factor = max_content_size / w
            
            new_h = max(1, int(h * scale_factor))
            new_w = max(1, int(w * scale_factor))
            
                # resize (again)
            cropped_img = Image.fromarray((cropped * 255).astype(np.uint8))
            resized_img = cropped_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            resized_array = (np.array(resized_img) > 127).astype(int)
            
            final_h = new_h + 2
            final_w = new_w + 2
            
            # final matrix
            binary_array = np.zeros((final_h, final_w), dtype=int)
            
             # 1 pixel from de edge
            start_row = 1
            start_col = 1
            binary_array[start_row:start_row+new_h, start_col:start_col+new_w] = resized_array
            return binary_array

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@app.route('/')
def home():
    return "Flask server is running! Use the /predict endpoint for digit prediction."

@app.route('/predict', methods=['POST'])
def predict_digit():
    try:
        image_data_url = request.json['image']
        x = convert_png_to_array(image_data_url)        
        prediction = knn.process_drawing(x)
        print(prediction)
        return jsonify({'prediction': int(prediction)})
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure to place app.py in the root of num_w_bfs, not in the app subfolder
    app.run(debug=True, port=5000)