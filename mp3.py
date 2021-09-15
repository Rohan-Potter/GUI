##### Python Modules
import tkinter as tk
from tkinter import *
from pygame import mixer
from tkinter import filedialog
from PIL import ImageTk,Image
import time
from mutagen.mp3 import MP3
import eyed3
## Initiazing Mixer
mixer.init()

## Main Application
app=tk.Tk()
app.title('mp3 player')
app.geometry('450x600')

## app icon
icon=ImageTk.PhotoImage(file="icon\music.png")
app.iconphoto(False,icon)

## Back-ground Image
img=Image.open('bgimg1.png').resize((450,450))
pic=ImageTk.PhotoImage(img)
img_label=tk.Label(app,image=pic)
img_label.grid(row=0,column=0,columnspan=20)
img_label.configure(bd=0)

##variables
open_file=False
music_pause=False

## label frame

# Player btn
btn_frame=tk.Frame(app,relief='solid',width=450)
btn_frame.grid(row=2,column=0,columnspan=20,pady=10)
btn_frame.configure(background='lightblue2',bd=0)

# List btn
Listbox_frame=tk.Frame(app,relief='solid',width=450)
Listbox_frame.grid(row=2,column=20,columnspan=20,pady=10)
Listbox_frame.configure(background='lightblue2',bd=0)

## Song_list box
Song_list=tk.Listbox(app,bg='black',fg='white',width=200,height=28,bd=0)
Song_list.grid(row=0,rowspan=50,column=21,sticky=tk.N)

## Player btn functions

## Song details Label
def details():
    audio_details=eyed3.load(Song_list.get(Song_list.curselection()))
    song_details=tk.LabelFrame(app,text='',width=1000)
    song_details.grid(row=3,column=0,columnspan=50,sticky=tk.S,ipadx=500,padx=50)
    song_details.configure(bd=0)

    # To display song details
    title_name=tk.Label(song_details,text=f"Title:     {audio_details.tag.title}",font=("Courier",10,'bold')).grid(row=0,column=0,padx=15)
    artist_name=tk.Label(song_details,text=f"Artist:   {audio_details.tag.artist}",font=("Courier",10,'bold')).grid(row=1,column=0,padx=15)
    album_name=tk.Label(song_details,text=f"Album:     {audio_details.tag.album}",font=("Courier",10,'bold')).grid(row=2,column=0,padx=15)

## Get Play Time
def play_time():
    global current_song_pos
    current_time=mixer.music.get_pos()/1000

    ## To time format
    converted_time=time.strftime("%M:%S",time.gmtime(current_time))

    # Get Current Song
    current_song_pos=Song_list.curselection()
    current_song=Song_list.get(current_song_pos)
    mut_song=MP3(current_song)

    # Get length of current song
    song_length=mut_song.info.length
    converted_length=time.strftime("%M:%S",time.gmtime(song_length))

    #To display the time
    song_slider.configure(label=f"{converted_time}:{converted_length}")

    # To update song slider
    song_slider.configure(to=song_length)
    song_slider.set(int(current_time))

    ## Update Play Time
    song_slider.after(1000,play_time)

    # Refresh song details
    details()

### Volumne slider hover 
def set_volume(e):
    volume_slider.configure(label='   Volume',font=("Courier",9,'bold'))

def get_volume(e):
    volume_slider.configure(label='',font=("Courier",9,'bold'))
    mixer.music.set_volume((vol.get())/10)

##

def play_func():
    global music_pause

    if music_pause==True:
        mixer.music.unpause()
        music_pause=False
    else:
        mixer.music.load(Song_list.get(ACTIVE))
        mixer.music.play()
    play_time()    
    
def pause_func():
    global music_pause
    music_pause=True
    mixer.music.pause()

def stop_func():
    mixer.music.fadeout(500)

    #To clear selection and update label to 0
    song_slider.configure(label='')
    Song_list.selection_clear(current_song_pos,None)

def forward():
    current_song=Song_list.curselection()
    next_song=current_song[0]+1
    Song_list.selection_clear(current_song,None)
    Song_list.selection_set(next_song)

    # Refresh song details
    details()

    # Play next song
    mixer.music.load(Song_list.get(next_song))
    mixer.music.play()

def backward():
    current_song=Song_list.curselection()
    previous_song=current_song[0]-1
    Song_list.selection_clear(current_song,None)
    Song_list.selection_set(previous_song)

    # Refresh song details
    details()

    # Play previous song
    mixer.music.load(Song_list.get(previous_song))
    mixer.music.play()

### Slider Hover
def set_position(e):
    song_slider.configure(sliderlength=5)

def get_position(e):
    song_slider.configure(sliderlength=30)

###
def del_one():
    Song_list.delete(ACTIVE,None)

def del_all():
    Song_list.delete(0,END)
####################################################### Main Menubar
main_menu=tk.Menu(app)
main_menu.configure(background='gray23')
################################### Add song menu

file_menu=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label="Add Songs",menu=file_menu)

# Add  Single song and fuctions
def single_song():
    global single_audio
    single_audio=filedialog.askopenfilename(title="Choose File",initialdir=r'C:\Users\rohan\Music\music',defaultextension=".mp3",filetypes=(('.mp3','*.mp3'),))
    open_file=True
    Song_list.insert(END,single_audio)
file_menu.add_command(label="Add Single Song",command=single_song)

# Add many song and fuctions
def many_song():
    global single_audio
    songs=filedialog.askopenfilenames(title="Choose File",initialdir=r'C:\Users\rohan\Music\music',defaultextension=".mp3",filetypes=(('.mp3','*.mp3'),))
    open_file=True
    for song in songs:
        Song_list.insert(END,song)
file_menu.add_command(label="Add Many Songs",command=many_song)
#################################### End Add song menu

################################### Player color menu

player_color=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label="Theme",menu=player_color)


###################################  End Player color menu

######################################################################## End menu bar


################ Player buttons and Sliders

## previous btn
img1=Image.open('icon\previous.png')
previous_img=ImageTk.PhotoImage(img1)
previous_btn=tk.Button(btn_frame,image=previous_img,command=backward)
previous_btn.grid(row=1,column=1)
previous_btn.configure(activebackground='gray63',bd=0)

## next btn
img2=Image.open('icon\enext.png')
next_img=ImageTk.PhotoImage(img2)
next_btn=tk.Button(btn_frame,image=next_img,command=forward)
next_btn.grid(row=1,column=4)
next_btn.configure(activebackground='gray63',bd=0)

## play btn
img3=Image.open('icon\play.png')
play_img=ImageTk.PhotoImage(img3)
play_btn=tk.Button(btn_frame,image=play_img,command=play_func)
play_btn.grid(row=1,column=2)
play_btn.configure(bg='blue',activebackground='white',bd=2,relief='flat')

## pause btn
img4=Image.open('icon\pause.png')
pause_img=ImageTk.PhotoImage(img4)
pause_btn=tk.Button(btn_frame,image=pause_img,command=pause_func)
pause_btn.grid(row=1,column=3)
pause_btn.configure(bg='deep sky blue',activebackground='gray63',bd=2,relief='flat')

## stop btn
img5=Image.open('icon\stop.png')
stop_img=ImageTk.PhotoImage(img5)
stop_btn=tk.Button(btn_frame,image=stop_img,command=stop_func)
stop_btn.grid(row=1,column=0,padx=10,pady=10)
stop_btn.configure(activebackground='gray63',bd=0)

## repeat btn
img6=Image.open('icon\one.png')
repeat_img=ImageTk.PhotoImage(img6)
repeat_btn=tk.Button(btn_frame,image=repeat_img)
repeat_btn.grid(row=1,column=5,padx=10)
repeat_btn.configure(activebackground='gray63',bd=0)

## Volumn Slider
vol=tk.IntVar()
volume_slider=tk.Scale(btn_frame,variable=vol,from_=0,to=10,orient=HORIZONTAL)
volume_slider.grid(row=1,column=7,columnspan=5)
volume_slider.configure(bg='lightblue2',bd=0)
volume_slider.set(4)

volume_slider.bind("<Enter>",set_volume)
volume_slider.bind("<Leave>",get_volume)

## Color radio button and it's functions
def color():
    color_list=['white','black','gray23']
    _color=['lightblue2','khaki2','dark khaki']
    app.configure(background=color_list[color_var.get()])
    btn_frame.configure(background=_color[color_var.get()])
    volume_slider.configure(bg=_color[color_var.get()])
    Listbox_frame.configure(bg=_color[color_var.get()])

color_var=tk.IntVar()
player_color.add_radiobutton(label="White",value=0,variable=color_var,command=color)
player_color.add_radiobutton(label="Black",value=1,variable=color_var,command=color)
player_color.add_radiobutton(label="Gray",value=2,variable=color_var,command=color)

## Song slider
song_pos=tk.IntVar()
song_slider=Scale(app,variable=song_pos,from_=0,to=100,orient=HORIZONTAL)
song_slider.grid(row=1,column=0,columnspan=1000,pady=0,sticky=tk.W,padx=10)
song_slider.configure(bg='lightblue2',bd=0,length=1340,showvalue=0,sliderlength=5)

song_slider.bind("<Enter>",get_position)
song_slider.bind("<Leave>",set_position)

## Delete songs from the list box
delete_one=tk.Button(Listbox_frame,text='Delete One',command=del_one)
delete_one.grid(row=0,column=0,pady=10,padx=10)

delete_all=tk.Button(Listbox_frame,text='Delete All',command=del_all)
delete_all.grid(row=0,column=1,padx=10)

delete_label=tk.Label(Listbox_frame,text="Delete Song(s) from the list",font=("Courier",9,'bold'))
delete_label.grid(row=1,column=0,columnspan=5)

################################ End Player buttons and Sliders

app.config(menu=main_menu)
app.mainloop()