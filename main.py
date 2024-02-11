import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont

class PhotoEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Photo Editor")
        self.master.geometry("800x650")

        self.image = None
        self.original_image = None
        self.tk_image = None
        self.brightness_factor = 1.0
        self.crop_slider = None
        self.auto_enhanced = False  # Track whether auto enhance has been applied
        self.text_items = []
        self.drawing_tool = "pen"
        self.drawing_color = "black"
        self.start_x = None
        self.start_y = None
        self.line_width = 5

        self.initialize_gui()

    def initialize_gui(self):
        # Menus
        menu_bar = tk.Menu(self.master)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)

        filter_menu = tk.Menu(menu_bar, tearoff=0)
        filter_menu.add_command(label="Blur", command=self.apply_blur_filter)
        filter_menu.add_command(label="Sepia Tone", command=self.apply_sepia_tone)
        filter_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        filter_menu.add_command(label="Sharpen", command=self.apply_sharpen)
        filter_menu.add_command(label="Edge Enhancement", command=self.apply_edge_enhancement)
        filter_menu.add_command(label="Negative", command=self.apply_negative)
        filter_menu.add_command(label="Posterize", command=self.apply_posterize)

        text_menu = tk.Menu(menu_bar, tearoff=0)
        text_menu.add_command(label="Text Overlay", command=self.add_text_overlay)

        drawing_menu = tk.Menu(menu_bar, tearoff=0)
        drawing_menu.add_command(label="Pen", command=lambda: self.set_drawing_tool("pen"))
        drawing_menu.add_command(label="Pencil", command=lambda: self.set_drawing_tool("pencil"))
        drawing_menu.add_command(label="Spray Paint", command=lambda: self.set_drawing_tool("spray_paint"))
        drawing_menu.add_command(label="Paint Brush", command=lambda: self.set_drawing_tool("paint_brush"))
        drawing_menu.add_command(label="Marker", command=lambda: self.set_drawing_tool("marker"))
        drawing_menu.add_separator()
        drawing_menu.add_command(label="Choose Color", command=self.choose_drawing_color)

        skin_fixes_menu = tk.Menu(menu_bar, tearoff=0)
        skin_fixes_menu.add_command(label="Blemish Fix", command=self.remove_blemishes)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Filters", menu=filter_menu)
        menu_bar.add_cascade(label="Text", menu=text_menu)
        menu_bar.add_cascade(label="Drawing", menu=drawing_menu)
        menu_bar.add_cascade(label="Skin Fixes", menu=skin_fixes_menu)

        self.master.config(menu=menu_bar)

        # Canvas for displaying image
        self.canvas = tk.Canvas(self.master, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Buttons
        blur_button = tk.Button(self.master, text="Blur", command=self.apply_blur_filter)
        blur_button.pack(side=tk.LEFT, padx=10)

        # Brightness slider
        brightness_label = tk.Label(self.master, text="Brightness")
        brightness_label.pack(side=tk.LEFT)

        self.brightness_slider = tk.Scale(self.master, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(side=tk.LEFT)

        # Reset button
        reset_button = tk.Button(self.master, text="Reset", command=self.reset_image)
        reset_button.pack(side=tk.LEFT, padx=10)

        # Rotate button
        rotate_button = tk.Button(self.master, text="Rotate", command=self.rotate_image)
        rotate_button.pack(side=tk.LEFT, padx=10)

        # Resize entry
        resize_label = tk.Label(self.master, text="Resize (WxH)")
        resize_label.pack(side=tk.LEFT)

        self.resize_entry = tk.Entry(self.master, width=10)
        self.resize_entry.pack(side=tk.LEFT)

        # Resize button
        resize_button = tk.Button(self.master, text="Resize", command=self.resize_image)
        resize_button.pack(side=tk.LEFT, padx=10)

        # Crop slider
        crop_label = tk.Label(self.master, text="Crop")
        crop_label.pack(side=tk.LEFT)

        self.crop_slider = tk.Scale(self.master, from_=0, to=50, orient=tk.HORIZONTAL, command=self.crop_image)
        self.crop_slider.pack(side=tk.LEFT, padx=10)

        # Auto-enhance button
        self.auto_enhance_button = tk.Button(self.master, text="AI Enhance", command=self.auto_enhance)
        self.auto_enhance_button.pack(side=tk.LEFT, padx=10)

        # Label for author information
        author_label = tk.Label(self.master, text="Made by Charan Raavi", font=("Helvetica", 10, "italic"))
        author_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(defaultextension=".png", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()  # Keep a copy of the original image
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.auto_enhanced = False  # Reset auto-enhanced status when a new image is loaded
            self.clear_text_items()  # Clear existing text items

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.image.save(file_path)

    def apply_blur_filter(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def update_brightness(self, value):
        if self.image:
            self.brightness_factor = float(value)
            enhanced_image = ImageEnhance.Brightness(self.image).enhance(self.brightness_factor)
            self.tk_image = ImageTk.PhotoImage(enhanced_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()  # Restore the original image
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.brightness_slider.set(1.0)  # Reset brightness slider
            self.auto_enhanced = False  # Reset auto-enhanced status when image is reset
            self.clear_text_items()  # Clear existing text items

    def apply_sepia_tone(self):
        if self.image:
            sepia_image = ImageOps.colorize(self.image.convert("L"), "#704214", "#C0A080")
            self.image = sepia_image
            self.tk_image = ImageTk.PhotoImage(sepia_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def apply_grayscale(self):
        if self.image:
            grayscale_image = self.image.convert("L")
            self.image = grayscale_image
            self.tk_image = ImageTk.PhotoImage(grayscale_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def apply_sharpen(self):
        if self.image:
            sharpened_image = self.image.filter(ImageFilter.SHARPEN)
            self.image = sharpened_image
            self.tk_image = ImageTk.PhotoImage(sharpened_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def apply_edge_enhancement(self):
        if self.image:
            enhanced_image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.image = enhanced_image
            self.tk_image = ImageTk.PhotoImage(enhanced_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def apply_negative(self):
        if self.image:
            negative_image = ImageOps.invert(self.image)
            self.image = negative_image
            self.tk_image = ImageTk.PhotoImage(negative_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def apply_posterize(self):
        if self.image:
            posterized_image = ImageOps.posterize(self.image, 4)  # You can adjust the levels as needed
            self.image = posterized_image
            self.tk_image = ImageTk.PhotoImage(posterized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def rotate_image(self):
        if self.image:
            angle = 45  # You can adjust the rotation angle as needed
            rotated_image = self.image.rotate(angle)
            self.image = rotated_image
            self.tk_image = ImageTk.PhotoImage(rotated_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def resize_image(self):
        if self.image:
            dimensions = self.resize_entry.get().split("x")
            if len(dimensions) == 2 and dimensions[0].isdigit() and dimensions[1].isdigit():
                width, height = int(dimensions[0]), int(dimensions[1])
                resized_image = self.image.resize((width, height))
                self.image = resized_image
                self.tk_image = ImageTk.PhotoImage(resized_image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def crop_image(self, slider_value):
        if self.image:
            crop_percentage = int(slider_value)
            if crop_percentage > 0:
                left = crop_percentage
                top = crop_percentage
                right = self.image.width - crop_percentage
                bottom = self.image.height - crop_percentage
                cropped_image = self.image.crop((left, top, right, bottom))
                self.image = cropped_image
                self.tk_image = ImageTk.PhotoImage(cropped_image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def auto_enhance(self):
        if self.image and not self.auto_enhanced:
            enhanced_image = ImageEnhance.Contrast(self.image).enhance(1.5)
            self.image = enhanced_image
            self.tk_image = ImageTk.PhotoImage(enhanced_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.auto_enhanced = True
        elif self.auto_enhanced:
            messagebox.showinfo("Warning", "Photo already enhanced!")

    def add_text_overlay(self):
        if self.image:
            text = simpledialog.askstring("Text Overlay", "Enter text:")
            if text:
                draw = ImageDraw.Draw(self.image)
                font = ImageFont.load_default()
                draw.text((10, 10), text, font=font, fill="white")
                self.tk_image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
                self.text_items.append((text, (10, 10)))

    def clear_text_items(self):
        for text, position in self.text_items:
            draw = ImageDraw.Draw(self.image)
            font = ImageFont.load_default()
            draw.text(position, text, font=font, fill="white")
        self.text_items = []

    def start_drawing(self, event):
        if self.image:
            self.start_x = event.x
            self.start_y = event.y

    def draw(self, event):
        if self.image and self.start_x is not None and self.start_y is not None:
            if self.drawing_tool == "pen":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.drawing_color, width=self.line_width)
            elif self.drawing_tool == "pencil":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.drawing_color, width=1)
            elif self.drawing_tool == "spray_paint":
                self.canvas.create_oval(event.x, event.y, event.x + 1, event.y + 1, fill=self.drawing_color, outline="")
            elif self.drawing_tool == "paint_brush":
                self.canvas.create_oval(event.x - self.line_width, event.y - self.line_width, event.x + self.line_width, event.y + self.line_width, fill=self.drawing_color, outline="")
            elif self.drawing_tool == "marker":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.drawing_color, width=self.line_width, capstyle=tk.ROUND, smooth=tk.TRUE)

            self.start_x = event.x
            self.start_y = event.y

    def stop_drawing(self, event):
        self.start_x = None
        self.start_y = None

    def set_drawing_tool(self, tool):
        self.drawing_tool = tool

    def choose_drawing_color(self):
        color = colorchooser.askcolor(initialcolor=self.drawing_color)[1]
        if color:
            self.drawing_color = color

    def remove_blemishes(self):
        if self.image:
            # Implement your code for blemish removal here
            pass

if __name__ == "__main__":
    root = tk.Tk()
    photo_editor = PhotoEditor(root)
    root.mainloop()