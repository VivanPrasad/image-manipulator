from PIL import Image, ImageFilter, ImageTk

from tkinter import *
from tkinter import ttk

import sv_ttk

root = Tk()

def toggle_theme():
    if sv_ttk.get_theme() == "dark":
        print("Setting theme to light")
        sv_ttk.use_light_theme()
    elif sv_ttk.get_theme() == "light":
        print("Setting theme to dark")
        sv_ttk.use_dark_theme()
    else:
        print("Not Sun Valley theme")

title = ttk.Label(root,font=("Times New Roman",48),text="Image Manipulator")
title.place(rely=0.05, relx=0.325)
button = ttk.Button(root, text="Toggle theme", command=toggle_theme)
button.place(relx=0.8,rely=0.9)

button = ttk.Button(root,text="Login")
button.place(rely=0.40, relx=0.50)
root.geometry("1600x900")
root.resizable(0,0)
root.title("Image Manipulator")

root.iconbitmap("icon.ico")
sv_ttk.set_theme("dark")
root.mainloop()