# Author(s): Dr. Patrick Lemoine

import tkinter as tk
#from tkinter import filedialog
from PIL import Image, ImageTk
import os
import sys
import argparse
import time

class Slideshow:
    def __init__(self, master, directory):
        self.master = master
        self.directory = directory
        self.images = self.get_images()
        self.current_image = 0
        self.setup_ui()
        self.update_clock()
        self.master.resizable(True, True)
        self.master.overrideredirect(1)  # Hide the title bar
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}") 
        self.master.bind("<Escape>", self.exit_app_key) 

  
    def get_images(self):
        files = [file for file in os.listdir(self.directory) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif','.JPG'))]
        files_sorted = sorted(files)
        return [os.path.join(self.directory, file) for file in files_sorted]


    def setup_ui(self):
        self.master.config(bg="#333333") 
        self.master.overrideredirect(False)  
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")  

        self.canvas = tk.Canvas(self.master, width=screen_width, height=screen_height-85, bg="#333333", highlightthickness=0)
        self.canvas.pack()

        # Frame pour les boutons
        button_frame = tk.Frame(self.master, bg="#333333")
        button_frame.pack(fill="x")

        #self.prev_button = tk.Button(button_frame, text="Before", command=self.prev_image, bg="#444444", fg="white")
        #self.prev_button.pack(side="left")
        #self.prev_button.pack(side="left", padx=5, pady=5)

        #self.next_button = tk.Button(button_frame, text="Next", command=self.next_image, bg="#444444", fg="white")
        #self.prev_button.pack(side="left")
        #self.next_button.pack(side="left", padx=5, pady=5)

        #self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, bg="#444444", fg="white")
        #self.prev_button.pack(side="left")
        #self.exit_button.pack(side="left", padx=5, pady=5)


        self.image_number_label = tk.Label(button_frame, text="", bg="#333333", fg="white", font=("Helvetica", 12))
        self.image_number_label.pack(side="right", padx=5, pady=5)

        # Frame pour le slider, sous les boutons
        slider_frame = tk.Frame(self.master, bg="#333333")
        slider_frame.pack(fill="x")

        self.slider = tk.Scale(slider_frame, from_=0, to=max(len(self.images)-1, 0), orient="horizontal",
                               command=self.slider_changed, length=600, bg="#333333", fg="white",
                               troughcolor="#555555", highlightthickness=0)
        self.slider.pack(padx=5, pady=5)

        self.master.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.master.bind_all("<Button-4>", self.on_mouse_wheel_up)
        self.master.bind_all("<Button-5>", self.on_mouse_wheel_down)
        
        # Label pour l'heure en bas à droite
        self.clock_label = tk.Label(self.master, bg="#333333", fg="white", font=("Helvetica", 10))
        self.clock_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # 10 pixels du bord bas droit
        #self.clock_label.pack(side="right", padx=10)

        self.show_image()

    def rgb_to_hex(self, r, g, b):
        if not (isinstance(r, int) and isinstance(g, int) and isinstance(b, int)):
            raise ValueError("RGB values ​​must be Integer.")
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values ​​must be between 0 and 255..")
        return f"#{r:02x}{g:02x}{b:02x}"

    def show_image(self):
        if self.images:
            self.canvas.delete("all")

            image_path = self.images[self.current_image]
            image = Image.open(image_path)
            width, height = image.size

            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight() - 150
            ratio = min((screen_width - 20) / width, screen_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            image = image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)

            x = (screen_width - new_width) // 2
            y = ((screen_height - 150) - new_height) // 2 + 120

            r, g, b = 30, 30, 30 
            dp = 10
            hex_color = self.rgb_to_hex(r, g, b)
            self.canvas.create_rectangle(x+dp, y+dp, x+new_width+dp, y+new_height+dp, fill=hex_color, outline=hex_color)

            r, g, b = 10, 10, 10 
            dp = 5
            hex_color = self.rgb_to_hex(r, g, b)
            self.canvas.create_rectangle(x+dp*2, y+dp*2, x+new_width+dp, y+new_height+dp, fill=hex_color, outline=hex_color)

            self.canvas.create_image(x, y, anchor="nw", image=photo)
            self.canvas.image = photo

            #self.image_number_label.config(text=f"Image {self.current_image + 1} / {len(self.images)}")
            self.slider.set(self.current_image)

    def prev_image(self):
        if self.images:
            self.current_image = (self.current_image - 1) % len(self.images)
            self.slider.set(self.current_image)
            self.show_image()

    def next_image(self):
        if self.images:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.slider.set(self.current_image)
            self.show_image()

    def slider_changed(self, value):
        index = int(value)
        if 0 <= index < len(self.images):
            self.current_image = index
            self.show_image()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.prev_image()
        else:
            self.next_image()

    def on_mouse_wheel_up(self, event):
        self.prev_image()

    def on_mouse_wheel_down(self, event):
        self.next_image()

    def exit_app(self):
        self.master.destroy()

    def exit_app_key(self, event):
        self.master.destroy()
        
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.master.after(1000, self.update_clock)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path', type=str, default='None', help='Path to image directory.')
    args = parser.parse_args()
    directory = args.Path

    if directory == 'None' or not os.path.isdir(directory):
        print("Please provide a valid path to an image file with --Path")
        sys.exit(1)

    root = tk.Tk()
    slideshow = Slideshow(root, directory)
    root.mainloop()
