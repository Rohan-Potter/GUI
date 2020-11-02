## Importing Python Modules
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mbox
from PIL import ImageTk,Image,ImageEnhance
import os

## Aplication window
app=tk.Tk()
app.attributes("-fullscreen", True)
app.title('Image Editor')
app.configure(background='grey')
## App Frames
# Menu frame
menu_frame=tk.LabelFrame(app,text='Menu',relief='solid')
menu_frame.grid(row=0,column=0,sticky=tk.W)
menu_frame.configure(background='grey')
# Image frame
image_frame=tk.LabelFrame(app,text='',relief='solid')
image_frame.grid(row=1,column=0)
image_frame.configure(background='grey')
# Action frame
action_frame=tk.LabelFrame(app,text='Action Buttons',relief='solid')
action_frame.grid(row=1,column=1,sticky=tk.N,padx=50)
action_frame.configure(background='grey')

## Variables

# color variable
v1 = tk.IntVar()
v1.set(1)

# sharpness variable
v2 = tk.IntVar()
v2.set(1)

# brightness variable
v3=tk.IntVar()
v3.set(1)

# contarst variable
v4=tk.IntVar()
v4.set(1)

file_open= False
file_saved=False



################################## Menu Frame ###################################


## open btn and function
def open_image():
    global pic
    global img
    global img_label
    global file_open
    tk.filename=filedialog.askopenfilename(title="Choose File",initialdir='C://',filetypes=(('.png','*.png'),('.jpg','*.jpg')))
    file_open=True
    ## Image Label
    img = Image.open(tk.filename).resize((900,450))
    pic=ImageTk.PhotoImage(img)
    img_label=tk.Label(image_frame,image=pic)
    img_label.grid(row=0,column=0,columnspan=3)

# Button
img_label=ttk.Label(image_frame,text="Please! Insert A Image",font=("Courier",20,'italic','bold'))
img_label.grid(row=0,column=0,padx=10,pady=10)
open_btn=tk.Button(menu_frame,text='Open Image',command=open_image)
open_btn.grid(row=0,column=0,sticky=tk.W)

## Save and save as btn
def save():
    global file_open
    global file_saved
    if file_open:
        img2.save(tk.filename)
        mbox.showinfo('Save',"You'r Image is successfully saved")
        file_open=False
        file_saved=True
        os.remove('temp_pic.jpg')

# Button
Save_btn=tk.Button(menu_frame,text="Save",command=save)
Save_btn.grid(row=0,column=1,padx=50)

## Save as btn and function
def save_as():
    global file_saved
    savefile=filedialog.asksaveasfile(title='Save as',initialdir=tk.filename,defaultextension=".jpg",filetypes=(('.png','*.png'),('.jpg','*.jpg')))
    os.remove('temp_pic.jpg')
    file_saved=True
save_as_btn=tk.Button(menu_frame,text='Save as',command=save_as)
save_as_btn.grid(row=0,column=2)

## Quit btn and fuction
def exit():
    global file_saved
    global file_open
    if file_saved==True:
        msg=mbox.askquestion("Are you sure",'Do you want to quit the application',icon='question')
        if msg=='yes':
            app.quit()
    elif file_open==False:
        msg=mbox.askquestion("Are you sure",'Do you want to quit the application',icon='question')
        if msg=='yes':
            app.quit()
    else:
        msg=mbox.askquestion("Editor",'Do you want to save changes')
        if msg=='yes':
            save()
            app.quit()
        else:
            app.quit()
exit_btn=tk.Button(menu_frame,text='Quit',command=exit)
exit_btn.grid(row=0,column=3,padx=50)
exit_btn.grid_anchor('e')
################################# End Menu Frame #######################################


############################### Action Frame ######################################
def apply_color():
    global pic2
    global img2
    enhancer=ImageEnhance.Color(img)
    enhancer.enhance(v1.get()).save('temp_pic.jpg')
    
    # saving color
    img2 = Image.open('temp_pic.jpg').resize((900,450))
    pic2=ImageTk.PhotoImage(img2)
    img_label=tk.Label(image_frame,image=pic2)
    img_label.grid(row=0,column=0,columnspan=3)
    
## Sliders

# color slider and label
s1 = Scale( action_frame, variable = v1, from_ = 0, to = 5, orient = HORIZONTAL)
s1.grid(row=0,column=0,columnspan=3,padx=5)
s1.configure(background='grey')
l1=tk.Label(action_frame,text="Slide for color",font=("Courier",10)).grid(row=1,column=0)

color_btn=tk.Button(action_frame,text='Apply',command=apply_color)
color_btn.grid(row=2,column=0)
color_btn.grid_anchor(CENTER)

# Sharpness slider and label

def apply_sharpness():
    global pic2
    global img2 
    # For sharpness
    enhancer=ImageEnhance.Sharpness(img)
    enhancer.enhance(v2.get()).save('temp_pic.jpg') 

    # saving sharpness
    img2 = Image.open('temp_pic.jpg').resize((900,450))
    pic2=ImageTk.PhotoImage(img2)
    img_label=tk.Label(image_frame,image=pic2)
    img_label.grid(row=0,column=0,columnspan=3)  

s2 = Scale( action_frame, variable = v2, from_ = 0, to = 5, orient = HORIZONTAL)
s2.grid(row=3,column=0,columnspan=3,padx=5)
s2.configure(background='grey')
l2=tk.Label(action_frame,text="Slide for Sharpness",font=("Courier",10)).grid(row=4,column=0)

sharpness_btn=tk.Button(action_frame,text='Apply',command=apply_sharpness)
sharpness_btn.grid(row=5,column=0)
sharpness_btn.grid_anchor(CENTER)

# For Brightness

def apply_brightness():
    global pic2
    global img2 
    # For contrast
    enhancer=ImageEnhance.Brightness(img)
    enhancer.enhance(v3.get()).save('temp_pic.jpg') 

    # saving brightness
    img2 = Image.open('temp_pic.jpg').resize((900,450))
    pic2=ImageTk.PhotoImage(img2)
    img_label=tk.Label(image_frame,image=pic2)
    img_label.grid(row=0,column=0,columnspan=3)  

s3 = Scale( action_frame, variable = v3, from_ = 0, to = 5, orient = HORIZONTAL)
s3.grid(row=6,column=0,columnspan=3,padx=5)
s3.configure(background='grey')
l3=tk.Label(action_frame,text="Slide for Brightness",font=("Courier",10)).grid(row=7,column=0)

brightness_btn=tk.Button(action_frame,text='Apply',command=apply_brightness)
brightness_btn.grid(row=8,column=0)
brightness_btn.grid_anchor(CENTER)

# For contrast

def apply_contrast():
    global pic2
    global img2 
    # For contrast
    enhancer=ImageEnhance.Contrast(img)
    enhancer.enhance(v4.get()).save('temp_pic.jpg') 

    # saving contrast
    img2 = Image.open('temp_pic.jpg').resize((900,450))
    pic2=ImageTk.PhotoImage(img2)
    img_label=tk.Label(image_frame,image=pic2)
    img_label.grid(row=0,column=0,columnspan=3)  

s4 = Scale( action_frame, variable = v4, from_ = 0, to = 5, orient = HORIZONTAL)
s4.grid(row=9,column=0,columnspan=3,padx=5)
s4.configure(background='grey')
l4=tk.Label(action_frame,text="Slide for Contrast",font=("Courier",10)).grid(row=10,column=0)

contrast_btn=tk.Button(action_frame,text='Apply',command=apply_contrast)
contrast_btn.grid(row=11,column=0)
contrast_btn.grid_anchor(CENTER)


app.mainloop()