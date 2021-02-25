from __future__ import unicode_literals
import youtube_dl
import os
import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import shutil


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        errors.append(msg)
        print(msg)


def edit_mp3(file, artist, album, genre, cover_art=None):

    audio = EasyID3(file)
    audio['artist'] = artist
    audio['album'] = album
    audio['genre'] = genre
    audio.save()

    if cover_art:
        audio = MP3(file, ID3=ID3)
        audio.tags.add(APIC(
            encoding=3,
            mime='image/png',
            type=3,
            desc=u'Cover',
            data=open(cover_art, 'rb').read()
        ))
        audio.save()


# os.makedirs('..\\..\\Music\\YouTube Downloads\\KHS', exist_ok=True)
os.chdir('..\\..\\Music\\YouTube Downloads\\Cursed Castle')

errors = []

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'outtmpl': '%(title)s.%(ext)s',
    'ignoreerrors': True,
    # 'writethumbnail': True
}

# ydl_opts['playlistend'] = 25
# ydl_opts['download_archive'] = os.path.join('..', '..', '..', 'Google Drive',
#                                             'YouTube Download', 'khs_download.txt')

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # ydl.download(['https://www.youtube.com/watch?v=Bjwf_xyX2pI&list=UUplkk3J5wrEl0TNrthHjq4Q'])
    ydl.download(['https://www.youtube.com/watch?v=70VlAyEUXYM&index=2&t=0s&list=PLybAUSaWSki9SMCRXct5D0XFeE6Kn2L3m'])

# for file in [mp3 for mp3 in os.listdir('.') if mp3.endswith('.mp3')]:
#     edit_mp3(file, 'Kurt Hugo Schneider', 'YouTube Downloads', 'KHS', file[:-4] + '.jpg')
#     shutil.move(file, os.path.join('Thumbnails', file))
#     os.unlink(file[:-4] + '.jpg')
if errors:
    print('\n\nRecording errors. Check the file to see which videos failed.')
    dt = datetime.datetime.now()
    errorFile = open(os.path.join('.', 'errorsmp3.txt'), 'a')
    errorFile.write(dt.strftime('%m/%d/%Y %H:%M:%S'))
    errorFile.write('\n')
    errorFile.write('\n'.join(errors))
    errorFile.write('\n\n')
    errorFile.close()

print('Done')
