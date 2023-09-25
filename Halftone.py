
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import svgwrite

class HalftoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Halftone Art Generator")
        self.root.geometry("800x600")
        self.image = None
        self.image_preview = None
        self.halftoned_image = None
        self.halftoned_preview = None

        self.import_btn = tk.Button(self.root, text="Import Image", command=self.import_image)
        self.import_btn.pack()
        
        self.image_canvas = tk.Canvas(self.root, width=200, height=200, bg='grey')
        self.image_canvas.pack()
        
        self.info_label = tk.Label(self.root, text="Image Info:")
        self.info_label.pack()

        self.angles_label = tk.Label(self.root, text="Angles:")
        self.angles_label.pack()
        
        self.angle1_entry = tk.Entry(self.root, width=5)
        self.angle1_entry.insert(0, "15")
        self.angle1_entry.pack(side="left")
        
        self.angle2_entry = tk.Entry(self.root, width=5)
        self.angle2_entry.insert(0, "75")
        self.angle2_entry.pack(side="left")
        
        self.angle3_entry = tk.Entry(self.root, width=5)
        self.angle3_entry.insert(0, "0")
        self.angle3_entry.pack(side="left")
        
        self.angle4_entry = tk.Entry(self.root, width=5)
        self.angle4_entry.insert(0, "45")
        self.angle4_entry.pack(side="left")
        
        self.antialias = tk.BooleanVar()
        self.antialias_checkbox = tk.Checkbutton(self.root, text="Antialias", variable=self.antialias)
        self.antialias_checkbox.pack()
        
        self.percentage_label = tk.Label(self.root, text="Percentage:")
        self.percentage_label.pack()
        
        self.percentage_slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.percentage_slider.set(50)
        self.percentage_slider.pack()
        
        self.scale_label = tk.Label(self.root, text="Scale:")
        self.scale_label.pack()
        
        self.scale_slider = tk.Scale(self.root, from_=1, to=10, orient="horizontal")
        self.scale_slider.set(1)
        self.scale_slider.pack()
        
        self.style_label = tk.Label(self.root, text="Style:")
        self.style_label.pack()
        
        self.style_var = tk.StringVar()
        self.style_combobox = ttk.Combobox(self.root, textvariable=self.style_var, values=("color", "grayscale"))
        self.style_combobox.current(0)
        self.style_combobox.pack()
        
        self.convert_btn = tk.Button(self.root, text="Convert to Halftone", command=self.convert_to_halftone)
        self.convert_btn.pack()
        
        self.halftone_canvas = tk.Canvas(self.root, width=200, height=200, bg='grey')
        self.halftone_canvas.pack()
        
        self.save_btn = tk.Button(self.root, text="Save", command=self.save_image)
        self.save_btn.pack()

    def import_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image_preview = ImageTk.PhotoImage(self.image.resize((200, 200)))
            self.image_canvas.create_image(100, 100, image=self.image_preview)
            
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            self.info_label.config(text=f"Name: {file_name[:20]} | Size: {file_size} bytes | Resolution: {self.image.size}")

    def simple_halftone_conversion(self, image):
        draw = ImageDraw.Draw(image)
        for i in range(0, image.size[0], 10):
            for j in range(0, image.size[1], 10):
                pixel = image.getpixel((i, j))
                
                # Simplified halftoning logic, you can replace this with more complex algorithms
                avg = int((pixel[0] + pixel[1] + pixel[2]) / 3)
                if avg > 127:
                    draw.rectangle([i, j, i+9, j+9], fill="white")
                else:
                    draw.rectangle([i, j, i+9, j+9], fill="black")
        
        return image

    def convert_to_halftone(self):
        if self.image:
            self.halftoned_image = self.simple_halftone_conversion(self.image.copy())
            self.halftoned_preview = ImageTk.PhotoImage(self.halftoned_image.resize((200, 200)))
            self.halftone_canvas.create_image(100, 100, image=self.halftoned_preview)
            
    def save_image(self):
        if self.halftoned_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("SVG files", "*.svg"), ("All files", "*.*")])
            if file_path.endswith('.svg'):
                dwg = svgwrite.Drawing(file_path, profile='tiny')
                # SVG saving logic
                dwg.save()
            else:
                self.halftoned_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = HalftoneApp(root)
    root.mainloop()
