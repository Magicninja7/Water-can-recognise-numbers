import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk
import numpy as np
global drawn_array_tk

class DigitDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit Drawing to Binary Array")
        self.root.geometry("600x700")
        
        self.canvas_size = 400
        self.brush_size = 10
        self.drawing = False
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Draw a Digit", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.canvas = tk.Canvas(main_frame, width=self.canvas_size, height=self.canvas_size, 
                               bg='white', relief=tk.SUNKEN, borderwidth=2)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_draw)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_canvas)
        clear_btn.grid(row=0, column=0, padx=(0, 5))
        
        convert_btn = ttk.Button(button_frame, text="Convert to 20x20 Array", command=self.convert_to_array)
        convert_btn.grid(row=0, column=1, padx=(5, 0))
        
        self.text_area = tk.Text(main_frame, height=25, width=70, font=("Courier", 8))
        self.text_area.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.grid(row=3, column=2, sticky="ns", pady=(10, 0))
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        instructions = ttk.Label(main_frame, 
                                text="Instructions:\n1. Draw digit in the canvas\n2. Clear to start over",
                                justify=tk.LEFT, foreground="gray")
        instructions.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
    def start_draw(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y
        
    def draw(self, event):
        if self.drawing:
            self.canvas.create_oval(event.x - self.brush_size*1.5, event.y - self.brush_size*1.5,
                                  event.x + self.brush_size*1.5, event.y + self.brush_size*1.5,
                                  fill='black', outline='black')
            
            if hasattr(self, 'last_x') and hasattr(self, 'last_y'):
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                      width=self.brush_size, fill='black', capstyle=tk.ROUND, smooth=tk.TRUE)
            
            self.last_x, self.last_y = event.x, event.y
            
    def stop_draw(self, event):
        self.drawing = False
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.text_area.delete(1.0, tk.END)
        
    def convert_to_array(self):
        try:
            ps = self.canvas.postscript(colormode='color')
        
            img = Image.new('RGB', (self.canvas_size, self.canvas_size), 'white')
            draw = ImageDraw.Draw(img)
        
            items = self.canvas.find_all()
            for item in items:
                item_type = self.canvas.type(item)
                coords = self.canvas.coords(item)
                if item_type == 'oval' and len(coords) == 4:
                    draw.ellipse(coords, fill='black')
                elif item_type == 'line' and len(coords) >= 4:
                    width = int(float(self.canvas.itemcget(item, 'width')))
                    for i in range(0, len(coords)-2, 2):
                        x1, y1 = coords[i], coords[i+1]
                        x2, y2 = coords[i+2], coords[i+3]
                        for offset in range(-width//2, width//2 + 1):
                            draw.line([x1+offset, y1, x2+offset, y2], fill='black')
                            draw.line([x1, y1+offset, x2, y2+offset], fill='black')
        
            img_gray = img.convert('L')
            img_resized = img_gray.resize((40, 40), Image.Resampling.LANCZOS)
            img_array = np.array(img_resized)
            binary_array = (img_array < 128).astype(int)
        
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
            
                # 1 pixel from de edge btw
                start_row = 1
                start_col = 1
                binary_array[start_row:start_row+new_h, start_col:start_col+new_w] = resized_array
        
            self.drawing_array = binary_array.tolist()
        
            global drawn_array_tk
            drawn_array_tk = binary_array
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print('hihihiha')
