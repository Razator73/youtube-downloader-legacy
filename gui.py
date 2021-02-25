import os
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox as mbox
from tkinter import ttk

import youtube_dl


def _download():
    os.chdir(file_box.get())
    ydl_opts = {
        'ignoreerrors': True,
        'outtmpl': '%(title)s.%(ext)s',
    }

    vid = vid_audio.get()
    if vid == 1:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio',
                                       'preferredcodec': 'mp3',
                                       'preferredquality': '192'}]
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio'
        ydl_opts['postprocessors'] = [{'key': 'FFmpegVideoConvertor',
                                       'preferedformat': 'mkv'}]

    url = url_box.get()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def _quit():
    win.quit()
    win.destroy()
    exit()


def _msgbox():
    mbox.showinfo('Python Message Info Box', 'A Python GUI created using tkinter:\nYouTube Video Download')


def _folder_select():
    cur_folder = file_box.get()
    dl_folder = filedialog.askdirectory(initialdir=cur_folder)
    os.chdir(dl_folder)
    file_box.set(os.getcwd())


win = tk.Tk()
win.title('Youtube Downloader')

ttk.Label(win, text='Enter the url:').grid(column=0, row=0, sticky='W', padx=10)

url_box = tk.StringVar()
enter_url = ttk.Entry(win, width=100, textvariable=url_box)
enter_url.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
enter_url.focus()

dl_button = ttk.Button(win, text='Download', command=_download)
dl_button.grid(column=1, row=2, padx=10)

vid_audio = tk.IntVar()
vid_audio.set(0)
options = ['Video', 'Audio Only']
for opt in range(len(options)):
    tk.Radiobutton(win, text=options[opt], variable=vid_audio, value=opt).grid(column=opt, row=3)

ttk.Label(win, text='Save to:').grid(column=0, row=4, sticky=tk.W, padx=10)

file_box = tk.StringVar()
file_box.set(os.path.expanduser('~'))
enter_file = ttk.Entry(win, textvariable=file_box, width=100)
enter_file.grid(column=0, row=5, columnspan=2, padx=10, pady=5)

file_btn = ttk.Button(win, text='Pick Folder', command=_folder_select)
file_btn.grid(column=1, row=6, padx=10, pady=5)

# menu bar items
menu_bar = Menu(win)
# file menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Exit', command=_quit)
# help menu
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label='About', command=_msgbox)
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Help', menu=help_menu)
win.config(menu=menu_bar)

win.mainloop()
