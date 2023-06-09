from PIL import Image, ImageFilter, ImageTk
import tkinter as tk
from tkinter import ttk
import os, datetime

# The theme is derived off of the example. I had to watch a few videos to replicate some of the features as Tkinter is extremely complex.

# You can use Ctrl and Shift key to select several files as well!

#image = Image.open('images/3.png')
#image.show()

root = tk.Tk()
root.title("Image Manipulator")

root.iconbitmap(f"./icon.ico")
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
thumbnail_option_list = ["","Original","100x100","200x200","400x400","600x600","800x800","1200x1200"]

#Folder Path Names
image_folder_paths = ["images","jpeg","png","webp","blurred","rotated","black and white","edges","contour","100x100","200x200","400x400","600x600","800x800","1200x1200","edited"]

for folder in image_folder_paths:
    if folder != "images":
        try:
            for file in os.listdir(f"./{folder}"):
                os.remove(f"./{folder}/{file}")
            os.rmdir(f"./{folder}")
        except:
            pass
        
# File variables/parameters for saving file and presets
file_type = tk.IntVar(value=2)
filter_option = tk.StringVar(value=filter_option_list[1])
thumbnail_option = tk.StringVar(value=thumbnail_option_list[1])
blur = tk.DoubleVar(value=0) #Blur
rotation = tk.DoubleVar(value=0) #Rotation
combined_edit = tk.BooleanVar(value=False)
# Separator

# Create a Frame for the Radiobuttons
radio_frame = ttk.LabelFrame(root, text="Save As", padding=(10, 10))
radio_frame.grid(row=3, column=1, padx=(20, 5), pady=5, sticky="nsew")
    # Radiobuttons
radio_1 = ttk.Radiobutton(radio_frame, text=".jpeg", variable=file_type, value=1)
radio_1.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
radio_2 = ttk.Radiobutton(radio_frame, text=".png", variable=file_type, value=2)
radio_2.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")
radio_3 = ttk.Radiobutton(radio_frame, text=".webp",variable=file_type, value=3)
radio_3.grid(row=2, column=0, padx=0, pady=10, sticky="nsew")

# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=3, column=0, padx=(25,75), pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

# Combined Edits - Switch
def toggle_switch(state):
    if state.get() == True:
        switch.config(text="Combined Edits")
    else:
        switch.config(text="Separate Edits",style='Switch')

theme_switch = ttk.Checkbutton(root,text="Dark Theme", state='disabled')
theme_switch.grid(row=1,column=1, sticky="nsew")

switch = ttk.Checkbutton(widgets_frame, text="Separate Edits",style="Switch",command=lambda: toggle_switch(combined_edit),variable=combined_edit)
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

def edit_file(file_name, save_file_name):
    pass

def save_file(selection):
    file_ext = ['','jpeg','png','webp'][file_type.get()]
    
    if combined_edit.get() == True: #save as multiple edits
        try: 
            os.makedirs(f'./edited')
        except: pass
        for file in selection:
            file_name = treeview.item(file, "text")
            for folder in image_folder_paths:
                try:
                    image = Image.open(f'./{folder}/{file_name}')
                except: pass
            save_name = f'./edited/{file_name.split(".")[0]}-edited.{file_ext}'
            image.save(save_name)
            image = Image.open(save_name)
            image.rotate(int(rotation.get()),expand=True).save(save_name)
            image = Image.open(save_name)
            image.filter(ImageFilter.GaussianBlur(int(blur.get()))).save(save_name)
            image = Image.open(save_name)
            if filter_option.get() == "Black and White":
                image.convert(mode="L").save(save_name)
            elif filter_option.get() == "Edges":
                image.filter(ImageFilter.FIND_EDGES).save(save_name)
            elif filter_option.get() == "Contour":
                image.filter(ImageFilter.CONTOUR).save(save_name)
            image = Image.open(save_name)
            if thumbnail_option.get() != "Original":
                image.thumbnail(tuple([int(thumbnail_option.get().split("x")[0]),int(thumbnail_option.get().split("x")[0])]))
                image.save(save_name)
            image.close()
    else:
        #["images","jpeg","png","webp","blurred","rotated","filtered","100","200","400","600","800","1200","edited"]
        index = 0
        for data in [file_ext,int(blur.get()),int(rotation.get()) * -1,filter_option.get(),thumbnail_option.get()]:
            default_values = ["jpeg",0,0,"None","Original"]
            for file in selection:
                file_name = treeview.item(file, "text")
                for folder in image_folder_paths:
                    try:
                        image = Image.open(f'./{folder}/{file_name}').convert('RGB')
                    except: pass
                if not data in default_values:
                    if data == "png":
                        pass
                    if not index in [1,2]: #not blur or rotation
                        try: os.makedirs(f'./{str(data).lower()}')
                        except: pass
                    elif index == 1: #blur
                        try: os.makedirs(f"./blurred")
                        except: pass
                    else: #rotation
                        try: os.makedirs(f"./rotated")
                        except:pass
                    #
                    if index == 0:
                        image.save(f'./{data}/{file_name.split(".")[0]}.{data}')
                    elif index == 1:
                        image.filter(ImageFilter.GaussianBlur(data)).save(f'./blurred/{file_name.split(".")[0]}-blur{data}.{file_name.split(".")[1]}')
                    elif index == 2:
                        image.rotate(data,expand=True).save(f'./rotated/{file_name.split(".")[0]}-rotate{data}.{file_name.split(".")[1]}')
                    elif index == 3:
                        if data == "Black and White":
                            image.convert(mode="L").save(f'./{data}/{file_name}')
                        elif data == "Edges":
                            image.filter(ImageFilter.FIND_EDGES).save(f'./{data}/{file_name}')
                        elif data == "Contour":
                            image.filter(ImageFilter.CONTOUR).save(f'./{data}/{file_name}')
                    elif index == 4:
                        image.thumbnail(tuple([int(data.split("x")[0]),int(data.split("x")[0])]))
                        image.save(f'./{data}/{file_name.split(".")[0]}-{data.split("x")[0]}.{file_name.split(".")[1]}')
            index += 1
    global treeview_data
    treeview_data = []
    update_treeview()

def open_file(selection_id): #Gives the selection ID for the treeview item selected
    #treeview.item(selection_id)
    for file in selection_id:
        file_name = treeview.item(file, "text")
        if os.path.isdir(file_name):
            os.startfile(f"{file_name}")
        else:
            try:
                Image.open(f'./{treeview.item(treeview.parent(file))["text"]}/{file_name}').show()
            except:
                Image.open(f'./images/{file_name}').show()

def update_selection(selection):
    for file in treeview.selection():
        if os.path.isdir(treeview.item(file, 'text')):
            save_button.config(state="disabled")
            
    if len(selection) > 1:
        select_label.config(text="Selected multiple files")
        button.config(text="Open Files")
        save_button.config(text="Save Files")
        if [True for i in [treeview.item(x, 'text') for x in treeview.selection()] if os.path.isdir(f"./{i}")]:
            save_button.config(state="disabled")
        else:
            save_button.config(state="enabled")
    elif os.path.isdir(treeview.item(treeview.selection(), 'text')):
        select_label.config(text=f"Selected folder '{treeview.item(treeview.selection(), 'text')}'")
        save_button.config(text="Save File")
        button.config(text="Open Folder")
    elif treeview.item(treeview.selection(), 'text') == "":
        select_label.config(text="No files selected")



    else:
        select_label.config(text=f"Selected file '{treeview.item(treeview.selection(), 'text')}'")
        save_button.config(state="normal")
        button.config(text="Open File")
        save_button.config(text="Save File")
        save_button.config(state="enabled")

# Treeview
treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set,height=8,columns=[1,2])
treeview.pack(expand=True, fill="both")
#treeview.bind('<Double-1>',lambda event: open_file(treeview.selection()))
treeview.bind('<ButtonRelease-1>', lambda event: update_selection(treeview.selection()))
treeScroll.config(command=treeview.yview)

select_label = ttk.Label(widgets_frame, text="No File Selected")
select_label.grid(row=3, column=0)

# Treeview columns

# Treeview headings
treeview.heading("#0", text="Name", anchor="center")
treeview.heading("#1", text="Date", anchor="center")
treeview.heading("#2", text="Size", anchor="center")

treeview_data = []

def get_date(file):
    t = datetime.datetime.fromtimestamp(os.path.getmtime(file),tz=datetime.timezone(datetime.timedelta(hours=-7), 'PST'))
    return f"{t.day}/{t.month}/{t.year} {t.hour % 12:.0f}:{t.minute:.0f}:{('0' + str(t.second)) if t.second < 10 else t.second} {'PM' if t.hour > 12 else 'AM'}"
def update_treeview():
    global treeview
    global treeview_data
    for i in treeview.get_children():
        treeview.delete(i)
    treeview_data = []
    
    id = 1
    for folder in os.listdir('.'):
        if folder in image_folder_paths:
            folder_id = id
            treeview_data.append(("", "end", id, folder, (get_date(folder), f"{os.stat(folder).st_size / 1024 ** 2 : .2f} MB" if (os.stat(folder).st_size / 1024 ** 2) > 1 else f"{os.stat(folder).st_size / 1024 : .2f} KB")))
            id += 1
            for f in os.listdir(f'./{folder}'):
                treeview_data.append((folder_id,"end",id,str(f),(get_date(f'./{folder}/{f}'),f"{os.stat(f'./{folder}/{f}').st_size / 1024 ** 2 : .2f} MB")))
                id += 1
    
    for item in treeview_data:
        try: treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
        except: treeview.item(item[2],text=item[3],values=item[4])
        if item[3] in image_folder_paths:
            pass
        else:
            pass
        if item[0] == "":
            treeview.item(item[2], open=True)

# Button
button = ttk.Button(widgets_frame, text="Open File",command=lambda: open_file(treeview.selection()))
button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

# Accentbutton
save_button = ttk.Button(widgets_frame, text="Save File", style="Accent.TButton",command=lambda: save_file(treeview.selection()))
save_button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

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

update_treeview() #Update the treeview
root.mainloop() #Start the main loop