
import tkinter as tk
import os
from tkinter import filedialog, Checkbutton, Scale
from PIL import Image, ImageDraw, ImageTk
import svgwrite

class HalftoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Halftone Art Converter")
        self.root.geometry('460x370')
        
        self.image = None
        self.halftoned_image = None
        self.vectoral = tk.BooleanVar()

        # Create buttons
        self.import_btn = tk.Button(self.root, text="Import Image", command=self.import_image)
        self.import_btn.place(x=20, y=20, width=120, height=30)

        self.convert_btn = tk.Button(self.root, text="Convert to Halftone", command=self.convert_to_halftone)
        self.convert_btn.place(x=20, y=60, width=120, height=30)
        self.convert_btn.config(state=tk.DISABLED)

        self.save_btn = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_btn.place(x=170, y=320, width=120, height=30)
        self.save_btn.config(state=tk.DISABLED)

        self.file_info_label = tk.Label(self.root, text="", bg="white", relief=tk.SUNKEN)
        self.file_info_label.place(x=280, y=20, width=160, height=50)


        # Vectoral checkbox
        
        # Dot density slider (initially hidden)
        self.dot_density_slider = Scale(self.root, from_=5, to=300, orient=tk.HORIZONTAL, label="Dot Density")
        self.dot_density_slider.set(10)  # default value
        self.dot_density_slider.place(x=170, y=100)
        self.dot_density_slider.place_forget()  # Hide initially


        self.vectoral_checkbox = Checkbutton(self.root, text="Vectoral", variable=self.vectoral, command=self.toggle_vectoral)
        self.vectoral_checkbox.place(x=170, y=70)

        # Resolution slider
        self.resolution_slider = Scale(self.root, from_=100, to=1500, orient=tk.HORIZONTAL, label="Resolution")
        self.resolution_slider.set(300)  # default value
        self.resolution_slider.place(x=170, y=100)

        # Create image display labels with a fixed size placeholder
        placeholder_image = Image.new('L', (200, 200), color=255)
        placeholder_tk = ImageTk.PhotoImage(placeholder_image)

        self.original_label = tk.Label(self.root, image=placeholder_tk, text="", compound=tk.CENTER)
        self.original_label.image = placeholder_tk
        self.original_label.place(x=20, y=110)

        self.halftone_label = tk.Label(self.root, image=placeholder_tk, text="", compound=tk.CENTER)
        self.halftone_label.image = placeholder_tk
        self.halftone_label.place(x=240, y=110)

        
        # Enable/Disable resolution slider based on vectoral checkbox
        if self.vectoral.get():
            self.resolution_slider.pack_forget()
            self.dot_density_slider.pack(pady=10)
        else:
            self.dot_density_slider.pack_forget()
            self.resolution_slider.pack(pady=10)

        # Enable/Disable resolution slider based on vectoral checkbox
        
            # Dot density adjustment
            dot_density = self.dot_density_slider.get()
            # ... apply dot_density to SVG generation logic
            # (This part needs to be filled in based on how dot_density should affect the SVG output.)
            
        
            # Get the dot density
            dot_density = self.dot_density_slider.get()
            # ... apply dot_density to SVG generation logic here (e.g., adjusting the number of horizontal pixels or dot placeholders)
        if self.vectoral.get():
            self.resolution_slider.config(state=tk.DISABLED)
        else:
            self.resolution_slider.config(state=tk.NORMAL)

        # # Enable/Disable resolution slider based on vectoral checkbox
        # if self.vectoral.get():
        #     self.resolution_slider.config(state=tk.DISABLED)
        # else:
        #     self.resolution_slider.config(state=tk.NORMAL)

    
    def toggle_vectoral(self):
        # Enable/Disable resolution slider based on vectoral checkbox
        if self.vectoral.get():
            self.resolution_slider.pack_forget()
            self.dot_density_slider.pack(pady=10)
        else:
            self.dot_density_slider.pack_forget()
            self.resolution_slider.pack(pady=10)


    def import_image(self):
        file_path = filedialog.askopenfilename(title="Select an image", filetypes=(("All files", "*.*"), ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")))
        if file_path:
            self.image = Image.open(file_path).convert("L")  # Convert to grayscale
            self.display_image(self.image, self.original_label)
            self.convert_btn.config(state=tk.NORMAL)

        # Update file info label
        file_name = file_path.split("/")[-1]
        file_size = round((os.path.getsize(file_path) / 1024), 2)  # Convert bytes to KB and round off to two decimal places
        aspect_ratio = f"{self.image.width}x{self.image.height}"
        
        # Update file info label
        file_name = file_path.split("/")[-1]
        file_size = round((os.path.getsize(file_path) / 1024), 2)  # Convert bytes to KB and round off to two decimal places
        aspect_ratio = f"{self.image.width}x{self.image.height}"
        self.file_info_label.config(text=f"Name: {file_name[:20]}\nSize: {file_size} KB\nAspect Ratio: {aspect_ratio}")



    def convert_to_halftone(self):
        if self.image:
            output_image = Image.new("L", self.image.size, 255)
            draw = ImageDraw.Draw(output_image)

            step_size = 255-self.dot_density_slider.get()
            for x in range(0, self.image.width, step_size):
                for y in range(0, self.image.height, step_size):
                    # Get average color in this square
                    average = self.average_color(x, y, step_size)
                    radius = (step_size/2) * (1 - average/255)
                    draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=0)

            self.halftoned_image = output_image
            self.display_image(self.halftoned_image, self.halftone_label)
            self.save_btn.config(state=tk.NORMAL)

    def average_color(self, x, y, step_size):
        """Compute the average color in a square region."""
        total = 0
        count = 0
        for i in range(x, min(x+step_size, self.image.width)):
            for j in range(y, min(y+step_size, self.image.height)):
                total += self.image.getpixel((i, j))
                count += 1
        return total / count

    def save_image(self):
        if self.halftoned_image:
            if self.vectoral.get():
                file_path = filedialog.asksaveasfilename(title="Save Image", defaultextension=".svg", filetypes=(("SVG files", "*.svg"), ("All files", "*.*")))
                if file_path:
                    # Convert and save as SVG using svgwrite
                    
                    dwg = svgwrite.Drawing(file_path, profile='tiny', size=(self.halftoned_image.width, self.halftoned_image.height))

                    step_size = 255-self.dot_density_slider.get()
                    for x in range(0, self.halftoned_image.width, step_size):
                        for y in range(0, self.halftoned_image.height, step_size):
                            average = self.average_color(x, y, step_size)
                            radius = (step_size/2) * (1 - average/255)
                            dwg.add(dwg.ellipse(center=(x, y), r=(radius, radius), fill='black'))
                    dwg.save()
            else:
                file_path = filedialog.asksaveasfilename(title="Save Image", defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
                if file_path:
                    # Resize based on the resolution slider and save as PNG
                    output_height = self.resolution_slider.get()
                    output_width = int(output_height * self.halftoned_image.width / self.halftoned_image.height)
                    resized_image = self.halftoned_image.resize((output_width, output_height))
                    resized_image.save(file_path, format="PNG")

    def display_image(self, img, label):
        # Resize the image for preview if it exceeds 200 pixels in either direction
        if img.width > 200 or img.height > 200:
            img = img.resize((200, int(200 * img.height / img.width))) if img.width > img.height else img.resize((int(200 * img.width / img.height), 200))
        
        # Convert the image to a format suitable for Tkinter
        tk_image = ImageTk.PhotoImage(img)
        
        # Adjust for centering images in their placeholders
        if img.width < 200:
            x_offset = (200 - img.width) // 2
        else:
            x_offset = 0

        if img.height < 200:
            y_offset = (200 - img.height) // 2
        else:
            y_offset = 0

        label.config(image=tk_image, compound=tk.CENTER, padx=x_offset, pady=y_offset)

        label.image = tk_image  # Keep a reference to the image to prevent garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = HalftoneApp(root)
    root.mainloop()
