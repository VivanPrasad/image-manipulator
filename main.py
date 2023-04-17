from PIL import Image, ImageFilter, ImageTk
import tkinter as tk
from tkinter import ttk
import os


# The theme is derived off of the example. I had to watch a few videos to replicate some of the features as Tkinter is extremely complex.

# You can use Ctrl and Shift key to select several files as well!

#image = Image.open('images/3.png')
#image.show()
root = tk.Tk()
root.title("Image Manipulator")
root.iconbitmap("./icon.ico")
root.option_add("*tearOff", False) # This is always a good idea

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call('source', 'forest-dark.tcl')

# Set the theme with the theme_use method
style.theme_use('forest-dark')

# Create lists for the Comboboxes
label = ttk.Label(root, text="Blur %", justify="center")
filter_option_list = ["", "None", "Black and White", "Edges","Contour"]
thumbnail_option_list = ["","Original","200x200","400x400","600x600","800x800","1200x1200"]

# File variables/parameters for saving file and presets
file_type = tk.IntVar(value=2)
filter_option = tk.StringVar(value=filter_option_list[1])
thumbnail_option = tk.StringVar(value=thumbnail_option_list[1])
blur = tk.DoubleVar(value=0) #Blur
rotation = tk.DoubleVar(value=0) #Rotation

# Separator
"""
separator = ttk.Separator(root)
separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
"""
# Create a Frame for the Radiobuttons
radio_frame = ttk.LabelFrame(root, text="Save As", padding=(20, 10))
radio_frame.grid(row=3, column=2, padx=(20, 5), pady=5, sticky="nsew")

# Radiobuttons
radio_1 = ttk.Radiobutton(radio_frame, text=".jpeg", variable=file_type, value=1)
radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
radio_2 = ttk.Radiobutton(radio_frame, text=".png", variable=file_type, value=2)
radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
radio_3 = ttk.Radiobutton(radio_frame, text=".webp",variable=file_type, value=3)
radio_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=3, column=0, padx=(25,75), pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

# Switch
switch = ttk.Checkbutton(widgets_frame, text="Situational Build Path", style="Switch")
switch.grid(row=9, column=0, padx=5, pady=10, sticky="nsew")


# Panedwindow
paned = ttk.PanedWindow(root)
paned.grid(row=0, column=0, padx=(25,0),pady=(25, 5), sticky="nsew", rowspan=3)

# Pane #1
pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=1)

# Create a Frame for the Treeview
treeFrame = ttk.Frame(pane_1)
treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")
def save_file(selection):
    file_ext = ['','.jpeg','.png','.webp'][file_type.get()]
    
    try: os.makedirs('edited-images')
    except: pass
    for file in selection:
        file_name = treeview.item(file, "text")
        image = Image.open(f'images/{file_name}')
        image.rotate(rotation.get()).save(f'edited-images/{file_name.split(".")[0]}-edited{file_ext}')
        image.filter(ImageFilter.GaussianBlur(blur.get())).save(f'edited-images/{file_name.split(".")[0]}-edited{file_ext}')
        
        if filter_option.get() == "Black and White":
            image.convert(mode="L").save(f'edited-images/{file_name.split(".")[0]}-edited{file_ext}')
        elif filter_option.get() == "Edges":
            image.filter(ImageFilter.FIND_EDGES).save(f'edited-images/{file_name.split(".")[0]}-edited{file_ext}')
        elif filter_option.get() == "Contour":
            image.filter(ImageFilter.CONTOUR).save(f'edited-images/{file_name.split(".")[0]}-edited{file_ext}')
        if thumbnail_option.get() != "Original":
            image.thumbnail(tuple(thumbnail_option.get().split("x"))).save(f'edited-images/{file_name.split(".")[0]}-edited{file_ext}')
        image.close()
    global treeview_data
    treeview_data = []
    update_treeview()
def open_file(selection_id): #Gives the selection ID for the treeview item selected
    #treeview.item(selection_id)
    for file in selection_id:
        file_name = treeview.item(file, "text")
        if file_name == "images":
            os.startfile(".")
        else:
            try:
                image = Image.open(f'edited-images/{file_name}').show()
            except:
                image = Image.open(f'images/{file_name}').show()


def update_selection(selection):
    for file in treeview.selection():
        if os.path.isdir(treeview.item(file, 'text')):
            save_button.config(state="disabled")
            
    if len(selection) > 1:
        select_label.config(text="Selected multiple files")
        button.config(text="Open Files")
        save_button.config(text="Save Files")
    elif os.path.isdir(treeview.item(treeview.selection(), 'text')):
        select_label.config(text=f"Selected folder '{treeview.item(treeview.selection(), 'text')}'")
        save_button.config(text="Save File")
        button.config(text="Open File")
    else:
        select_label.config(text=f"Selected file '{treeview.item(treeview.selection(), 'text')}'")
        save_button.config(state="normal")
        button.config(text="Open File")
        save_button.config(text="Save File")
        save_button.config(state="enabled")

# Treeview
treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1), height=20)
treeview.pack(expand=True, fill="both")
#treeview.bind('<Double-1>',lambda event: open_file(treeview.selection()))
treeview.bind('<ButtonRelease-1>', lambda event: update_selection(treeview.selection()))
treeScroll.config(command=treeview.yview)

select_label = ttk.Label(widgets_frame, text="No File Selected")
select_label.grid(row=3, column=0)
# Treeview columns
treeview.column("#0", width=150)

# Treeview headings
treeview.heading("#0", text="Name", anchor="center")

treeview_data = []

def update_treeview():
    global treeview
    global treeview_data
    treeview_data = [("", "end", 1, "images",())]
    i = 1
    for f in os.listdir('images'):
        i += 1
        treeview_data.append((1,"end",i,str(f),()))
    # Define treeview data
    try:
        i += 1
        treeview_data.append(("", "end", i, "edited-images",()))
        x = i
        for f in os.listdir('edited-images'):
            i += 1
            treeview_data.append((x,"end",i,str(f),()))
        
    except: pass
    for item in treeview_data:
        treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
    if item[0] == "" or item[2] in (8, 12):
        treeview.item(item[2], open=True) # Open parents


update_treeview()
# Insert treeview data
# Select and scroll
#treeview.selection_set(10)
#treeview.see(7)

# Button
button = ttk.Button(widgets_frame, text="Open File",command=lambda: open_file(treeview.selection()))
button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

# Accentbutton
save_button = ttk.Button(widgets_frame, text="Save File", style="Accent.TButton",command=lambda: save_file(treeview.selection()))
save_button.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

# Pane #2
pane_2 = ttk.Frame(paned)
paned.add(pane_2, weight=1)

# Notebook
notebook = ttk.Notebook(pane_2)

# Tab #1
tab_1 = ttk.Frame(notebook)
tab_1.columnconfigure(index=0, weight=1)
tab_1.columnconfigure(index=1, weight=1)
tab_1.rowconfigure(index=0, weight=1)
tab_1.rowconfigure(index=1, weight=1)
notebook.add(tab_1, text="Blur")

# Scale
scale = ttk.Scale(tab_1, from_=0, to=100, variable=blur, command=lambda event: blur.set(scale.get()))
scale.grid(row=0, column=0, padx=(10,0), pady=(15, 0),sticky="ew")


# Label
label = ttk.Label(tab_1, text="Blur %", justify="center")
label.grid(row=0, column=1,pady=(10,0), columnspan=1)
label_2 = ttk.Label(tab_1, text=int(blur.get()), justify="center")
label_2.grid(row=0, column=1, columnspan=1,padx=(75,0),pady=(10,0))
scale.bind('<B1-Motion>',lambda event: label_2.config(text=int(blur.get())))

# Tab #2
tab_2 = ttk.Frame(notebook)
notebook.add(tab_2,text="Rotation")

scale_2 = ttk.Scale(tab_2, from_=0, to=360, variable=rotation, command=lambda event: rotation.set(scale_2.get()))
scale_2.grid(row=0, column=0, padx=(10,0), pady=(15, 0),sticky="ew")

label_3 = ttk.Label(tab_2, text=f"{int(rotation.get())}° (Clockwise)", justify="center")
label_3.grid(row=0, column=1, columnspan=1,padx=(75,0),pady=(10,0))
scale_2.bind('<B1-Motion>',lambda event: label_3.config(text=f"{int(rotation.get())}° (Clockwise)"))
# Tab #3
tab_3 = ttk.Frame(notebook)
notebook.add(tab_3, text="Resolution")
    #Thumbnail Options
optionmenu2 = ttk.OptionMenu(tab_3, thumbnail_option, *thumbnail_option_list)
optionmenu2.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

# Tab #4
tab_4 = ttk.Frame(notebook)
notebook.add(tab_4, text="Filter")
    # OptionMenu
optionmenu = ttk.OptionMenu(tab_4, filter_option, *filter_option_list)
optionmenu.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

notebook.pack(expand=True, fill="both", padx=5, pady=5)

# Sizegrip
sizegrip = ttk.Sizegrip(root)
sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

# Center the window, and set the min-size and geometry of the app resolution
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# Start the main loop
root.mainloop()