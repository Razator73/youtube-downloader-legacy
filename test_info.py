from __future__ import unicode_literals
import youtube_dl
import os
import datetime
import re
import shutil


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        errors.append(msg)
        print(msg)


os.makedirs('..\\..\\Videos\\YouTube Downloads', exist_ok=True)
os.chdir('..\\..\\Videos\\YouTube Downloads')
errors = []

ydl_opts = {
    # 'format': 'bestvideo[height<=720]+bestaudio',
    'format': 'bestvideo+bestaudio',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mkv'
    }],

    'logger': MyLogger(),
    'ignoreerrors': True,
    'outtmpl': '%(title)s.%(ext)s',
    'list_thumbnails': True
}

# ydl_opts = {
#     'format': 'bestaudio/best', # choice of quality
#     'extractaudio' : True,      # only keep the audio
#     'audioformat' : "mp3",      # convert to mp3
#     'outtmpl': '%(title)s',        # name the file the ID of the video
# }

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=B7bqAsxee4I'])
