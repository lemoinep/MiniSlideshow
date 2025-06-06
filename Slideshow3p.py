# Author(s): Dr. Patrick Lemoine

import tkinter as tk
from tkinter import filedialog
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
        if self.images:
            self.canvas.delete("all") 
            
            
            if (True) :
                sz1 = 50 
                prev_image_path = self.images[(self.current_image - 2) % len(self.images)]
                prev_image = Image.open(prev_image_path)
                prev_width, prev_height = prev_image.size
                prev_ratio = min(sz1 / prev_width, sz1 / prev_height) 
                w = int(prev_width * prev_ratio)
                h = int(prev_height * prev_ratio)
                
                x = 15
                y =  (self.master.winfo_screenheight() - 150 - h) // 2 + 120
                
                self.shadow(x,y,w,h)
                prev_image0 = prev_image.resize((w,h))
                prev_photo0 = ImageTk.PhotoImage(prev_image0)
                self.canvas.create_image(x, (self.master.winfo_screenheight() - 150 - h) // 2 + 120, anchor="nw", image=prev_photo0)
                self.canvas.image_prev0 = prev_photo0
  
            
            if (True) :
                sz1 = 250 
                prev_image_path = self.images[(self.current_image - 1) % len(self.images)]
                prev_image = Image.open(prev_image_path)
                prev_width, prev_height = prev_image.size
                prev_ratio = min(sz1 / prev_width, sz1 / prev_height) 
                w = int(prev_width * prev_ratio)
                h = int(prev_height * prev_ratio)
                
                x = 80
                y =  (self.master.winfo_screenheight() - 150 - h) // 2 + 120
                
                self.shadow(x,y,w,h)
                prev_image1 = prev_image.resize((w,h))
                prev_photo1 = ImageTk.PhotoImage(prev_image1)
                self.canvas.create_image(x, (self.master.winfo_screenheight() - 150 - h) // 2 + 120, anchor="nw", image=prev_photo1)
                self.canvas.image_prev1 = prev_photo1 
                

            image_path = self.images[self.current_image]
            image = Image.open(image_path)
            width, height = image.size
   
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight() - 150  
            ratio = min((screen_width - 20 - 700) / width, screen_height / height)  
            w = int(width * ratio)
            h = int(height * ratio)
   
            image = image.resize((w,h))
            photo = ImageTk.PhotoImage(image)
   
            x = (screen_width - w) // 2
            y = ((screen_height - 150) - h) // 2+120 
                         
            self.shadow(x,y,w,h)
            self.canvas.create_image(x, y, anchor="nw", image=photo)
            self.canvas.image = photo  
            

            if (True) :
                sz1 = 250 
                next_image_path = self.images[(self.current_image + 1) % len(self.images)]
                next_image = Image.open(next_image_path)
                next_width, next_height = next_image.size
                next_ratio = min(sz1 / next_width, sz1 / next_height) 
                w = int(next_width * next_ratio)
                h = int(next_height * next_ratio)
                
                x = screen_width - w - 80
                y =  (self.master.winfo_screenheight() - 150 - h) // 2 + 120
                
                self.shadow(x,y,w,h)
                next_image1 = next_image.resize((w,h))
                next_photo1 = ImageTk.PhotoImage(next_image1)
                self.canvas.create_image(x, (self.master.winfo_screenheight() - 150 - h) // 2 + 120, anchor="nw", image=next_photo1)
                self.canvas.image_next1 = next_photo1  
                
            if (True) :
                sz1 = 50 
                next_image_path = self.images[(self.current_image + 2) % len(self.images)]
                next_image = Image.open(next_image_path)
                next_width, next_height = next_image.size
                next_ratio = min(sz1 / next_width, sz1 / next_height) 
                w = int(next_width * next_ratio)
                h = int(next_height * next_ratio)
                    
                x = screen_width - w - 15
                y =  (self.master.winfo_screenheight() - 150 - h) // 2 + 120
                    
                self.shadow(x,y,w,h)
                next_image0 = next_image.resize((w,h))
                next_photo0 = ImageTk.PhotoImage(next_image0)
                self.canvas.create_image(x, (self.master.winfo_screenheight() - 150 - h) // 2 + 120, anchor="nw", image=next_photo0)
                self.canvas.image_next0 = next_photo0  
            
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

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.images = self.get_images()
            self.current_image = 0
            self.show_image()
            
    def next_image_key(self, event):
        if self.images:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.show_image()
            
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.master.after(1000, self.update_clock)  


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path',type=str,default='None', help='Path.')
    args = parser.parse_args()
    directory=args.Path
    root = tk.Tk()
    slideshow = Slideshow(root, directory)
    root.mainloop()
