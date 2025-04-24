import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import sys
import argparse

class Slideshow:
    def __init__(self, master, directory):
        self.master = master
        self.directory = directory
        self.images = self.get_images()
        self.current_image = 0
        self.setup_ui()
        self.master.resizable(True, True)
        self.master.overrideredirect(1)  # Masquer la barre de titre
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.bind("<Escape>", self.exit_app_key) 
        self.master.bind("<space>", self.next_image_key)

    def get_images(self):
        # Récupérer les fichiers images dans le répertoire
        #return [os.path.join(self.directory, file) for file in os.listdir(self.directory) if file.endswith(('.jpg','.JPG', '.jpeg', '.png', '.gif'))]
        return sorted([os.path.join(self.directory, file) for file in os.listdir(self.directory) if file.endswith(('.jpg','.JPG', '.jpeg', '.png', '.gif'))])

    def setup_ui(self):
        self.master.config(bg="#333333") 
        self.master.overrideredirect(False)  
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")  

        self.canvas = tk.Canvas(self.master, width=screen_width, height=screen_height-50, bg="#333333", highlightthickness=0)
        self.canvas.pack()

        button_frame = tk.Frame(self.master)
        button_frame.pack()

        self.prev_button = tk.Button(button_frame, text="Before", command=self.prev_image, bg="#444444", fg="white")
        self.prev_button.pack(side="left")

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_image, bg="#444444", fg="white")
        self.next_button.pack(side="left")

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, bg="#444444", fg="white")
        self.exit_button.pack(side="left")

        # Lier l'événement de roulette de la souris
        self.master.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.master.bind_all("<Button-4>", self.on_mouse_wheel_up)
        self.master.bind_all("<Button-5>", self.on_mouse_wheel_down)

        self.show_image()
        
    def rgb_to_hex(self, r, g, b):
        if not (isinstance(r, int) and isinstance(g, int) and isinstance(b, int)):
            raise ValueError("Les valeurs RGB doivent être des entiers.")
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("Les valeurs RGB doivent être comprises entre 0 et 255.")
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
            y = ((screen_height - 150) - new_height) // 2+120 
             
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
            

    def prev_image(self):
        if self.images:
            self.current_image = (self.current_image - 1) % len(self.images)
            self.show_image()

    def next_image(self):
        if self.images:
            self.current_image = (self.current_image + 1) % len(self.images)
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
        
    def next_image_key(self, event):
        if self.images:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.show_image()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path',type=str,default='None', help='Path.')
    #parser.add_argument('Path', type=str, help='Path.')
    args = parser.parse_args()
    directory=args.Path
    #directory = os.path.normpath(args.Path)
    root = tk.Tk()
    slideshow = Slideshow(root, directory)
    root.mainloop()
