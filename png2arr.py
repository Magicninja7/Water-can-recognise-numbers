import numpy as np
from PIL import Image

def convert_png_to_array(image_path: str):
    """
    Loads a PNG image, processes it, and converts it into a small,
    centered, binary numpy array.

    The process involves:
    1. Loading the image and handling transparency.
    2. Binarizing the image (pixels become 0 or 1).
    3. Cropping to the bounding box of the content.
    4. Resizing the content to fit within an 18x18 box.
    5. Centering the resized content in a new array with 1-pixel padding.

    Args:
        image_path (str): The file path to the input PNG image.

    Returns:
        numpy.ndarray: The processed binary array.
    """
    try:
        # 1. Load the image from file
        img = Image.open(image_path)

        # Handle transparency (convert RGBA to RGB with a white background)
        if img.mode == 'RGBA':
            # Create a new white background image
            background = Image.new('RGB', img.size, (255, 255, 255))
            # Paste the image onto the background using the alpha channel as a mask
            background.paste(img, mask=img.split()[3])
            img = background

        # 2. Convert to grayscale and create initial binary array
        img_gray = img.convert('L') # 'L' mode is for grayscale
        # Resize to a standard size for initial processing
        img_resized = img_gray.resize((40, 40), Image.Resampling.LANCZOS)
        img_array = np.array(img_resized)
        # Binarize the array: pixels darker than 128 are 1, others are 0
        binary_array = (img_array < 128).astype(int)

        # 3. Find the bounding box of the content
        rows_with_content = np.any(binary_array == 1, axis=1)
        cols_with_content = np.any(binary_array == 1, axis=0)

        # If the image is empty, return a 20x20 array of zeros
        if not np.any(rows_with_content) or not np.any(cols_with_content):
            return np.zeros((20, 20), dtype=int)
        
        # Get the coordinates of the bounding box
        top = np.argmax(rows_with_content)
        bottom = len(rows_with_content) - np.argmax(rows_with_content[::-1]) - 1
        left = np.argmax(cols_with_content)
        right = len(cols_with_content) - np.argmax(cols_with_content[::-1]) - 1

        # 4. Crop the array to the content
        cropped = binary_array[top:bottom+1, left:right+1]
        h, w = cropped.shape

        # 5. Scale the content to fit within a target size (e.g., 18x18)
        max_content_size = 18
        if h > w:
            scale_factor = max_content_size / h
        else:
            scale_factor = max_content_size / w
        
        new_h = max(1, int(h * scale_factor))
        new_w = max(1, int(w * scale_factor))

        # Resize the cropped content using Pillow for better interpolation
        cropped_img = Image.fromarray((cropped * 255).astype(np.uint8))
        resized_img = cropped_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        resized_array = (np.array(resized_img) > 127).astype(int)

        # 6. Create final padded array
        # Add 2 for 1-pixel padding on each side
        final_h, final_w = new_h + 2, new_w + 2
        final_array = np.zeros((final_h, final_w), dtype=int)
        
        # Place the resized content into the center of the padded array
        final_array[1:1+new_h, 1:1+new_w] = resized_array

        return final_array

    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None