# Author(s): Dr. Patrick Lemoine

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import sys
import argparse
import time

class Slideshow:
    def __init__(self, master, directory,panel_cols,panel_rows):
        self.master = master
        self.directory = directory
        self.images = self.get_images()

        self.panel_cols = panel_cols
        self.panel_rows = panel_rows
        self.panel_step = self.panel_cols * self.panel_rows

        self.current_image = 0
        self.setup_ui()
        self.update_clock()
        self.master.resizable(True, True)
        self.master.overrideredirect(1)  
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.bind("<Escape>", self.exit_app_key) 
        self.master.bind("<space>", self.next_image_key)

    
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

        button_frame = tk.Frame(self.master, bg="#333333")
        button_frame.pack(fill="x")

        self.image_number_label = tk.Label(button_frame, text="", bg="#333333", fg="white", font=("Helvetica", 12))
        self.image_number_label.pack(side="right", padx=5, pady=5)

        slider_frame = tk.Frame(self.master, bg="#333333")
        slider_frame.pack(fill="x")

        self.slider = tk.Scale(slider_frame, from_=0, to=max(len(self.images)-1, 0), orient="horizontal",
                               command=self.slider_changed, length=600, bg="#333333", fg="white",
                               troughcolor="#555555", highlightthickness=0)
        self.slider.pack(padx=5, pady=5)

        self.master.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.master.bind_all("<Button-4>", self.on_mouse_wheel_up)
        self.master.bind_all("<Button-5>", self.on_mouse_wheel_down)
        
        self.clock_label = tk.Label(self.master, bg="#333333", fg="white", font=("Helvetica", 10))
        self.clock_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  

        self.show_image()
        
    def rgb_to_hex(self, r, g, b):
        if not (isinstance(r, int) and isinstance(g, int) and isinstance(b, int)):
            raise ValueError("RGB values ​​must be Integer.")
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values ​​must be between 0 and 255..")
        return f"#{r:02x}{g:02x}{b:02x}"
    
    
    def shadow(self,x,y,w,h):
        r, g, b = 30, 30, 30 
        dp = 10
        hex_color = self.rgb_to_hex(r, g, b)
        self.canvas.create_rectangle(x+dp, y+dp, x+w+dp, y+h+dp, fill=hex_color, outline=hex_color)
        
        r, g, b = 20, 20, 20 
        dp = 8
        hex_color = self.rgb_to_hex(r, g, b)
        self.canvas.create_rectangle(x+dp*2, y+dp*2, x+w+dp, y+h+dp, fill=hex_color, outline=hex_color)  
        
        r, g, b = 10, 10, 10 
        dp = 5
        hex_color = self.rgb_to_hex(r, g, b)
        self.canvas.create_rectangle(x+dp*2, y+dp*2, x+w+dp, y+h+dp, fill=hex_color, outline=hex_color)  

             
    
    def show_image(self):
        if not self.images:
            return
    
        self.canvas.delete("all")
    
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight() - 150 
    
        cols = self.panel_cols
        rows = self.panel_rows
    
        max_img_width = screen_width // cols - 20  
        max_img_height = screen_height // rows - 20
    
        start_index = self.current_image - 4 
        start_index = self.current_image - 0 
    
        self.canvas.images = []
    
        for i in range(rows):
            for j in range(cols):
                img_index = (start_index + i * cols + j) % len(self.images)
                image_path = self.images[img_index]
                img = Image.open(image_path)
                width, height = img.size
    
                ratio = min(max_img_width / width, max_img_height / height)
                w, h = int(width * ratio), int(height * ratio)
    
                resized_img = img.resize((w, h))
                photo_img = ImageTk.PhotoImage(resized_img)
    
                x = j * (screen_width // cols) + ((screen_width // cols) - w) // 2
                y = i * (screen_height // rows) + ((screen_height // rows) - h) // 2 + 50  
    
                self.shadow(x, y, w, h)  
                self.canvas.create_image(x, y, anchor="nw", image=photo_img)
    
                self.canvas.images.append(photo_img) 
    
        self.slider.set(self.current_image)

        
    def prev_image(self):
        if self.images:
            self.current_image = (self.current_image - self.panel_step) % len(self.images)
            self.slider.set(self.current_image)
            self.show_image()

    def next_image(self):
        if self.images:
            self.current_image = (self.current_image + self.panel_step) % len(self.images)
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

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.images = self.get_images()
            self.current_image = 0
            self.show_image()
            
    def next_image_key(self, event):
        if self.images:
            self.current_image = (self.current_image + self.panel_step) % len(self.images)
            self.show_image()
            
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.master.after(1000, self.update_clock)  


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path',type=str,default='None', help='Path.')
    parser.add_argument('--Cols',type=int,default=7, help='Cols.')
    parser.add_argument('--Rows',type=int,default=5, help='Rows.')
    args = parser.parse_args()
    root = tk.Tk()
    slideshow = Slideshow(root,args.Path,args.Cols,args.Rows)
    root.mainloop()

