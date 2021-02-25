from __future__ import unicode_literals

import csv
import datetime
import os
import re
import shutil
from pathlib import Path

import youtube_dl
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3


# TODO: rewrite this to be run on my pi once a week
class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        errors.append(msg)
        print(msg)


def write_tracks(track_dict):
    with open('..\\..\\google_drive\\Youtube Download\\track_numbers.csv', 'w', newline='') as track_file:
        write_track = csv.writer(track_file)
        for series, track in track_dict.items():
            write_track.writerow([series, track])


def edit_mp3(file, artist, album, genre, track, title, cover_art):

    audio = EasyID3(file)
    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio['genre'] = genre
    audio['tracknumber'] = str(track)
    audio.save()
    audio = MP3(file, ID3=ID3)
    audio.tags.add(APIC(
        encoding=3,
        mime='image/png',
        type=3,
        desc=u'Cover',
        data=open(cover_art, 'rb').read()
    ))
    audio.save()


if __name__ == '__main__':
    tracks = {}
    with open('track_numbers.csv') as track_file:
        track_data = list(csv.reader(track_file))
    for series in track_data:
        tracks[series[0]] = int(series[1])
    download_path = Path.home() / 'Music' / 'youtube-downloads'

    errors = []

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'download_archive': os.path.join('..', '..', 'google_drive',
                                         'YouTube Download', 'cos_downloaded.txt'),
        'logger': MyLogger(),
        'ignoreerrors': True,
        'outtmpl': '%(title)s.%(ext)s',
    }

    # ---------------------Court of Swords------------------------------------
    folder = 'Rollplay Court of Swords'
    series = 'Court of Swords'

    ydl_opts['playliststart'] = tracks[series]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=VqqmQwq3qKw&index=1&list=PL-oTJHKXHicQpK4d231BKSC9UJQr3HQny'])

    title_regex = re.compile(r'Week (\d+)[\s-]+(.*)\s*\(Part (\d+)\)\.mp3')
    os.makedirs(folder, exist_ok=True)
    for file in [x for x in os.listdir('.') if x.endswith('.mp3')]:
        if title_regex.search(file) is not None:
            week, title, part = title_regex.search(file).groups()
            if len(week) < 2:
                week = '0' * (2 - len(week)) + week
            file_title = 'Week {} Part {} - {}'.format(week, part, title) if title else 'Week {} Part {}'.format(week, part)
            tracks.setdefault(series, 1)
            edit_mp3(file, 'JP', folder, 'Books & Spoken', tracks[series], file_title,
                     os.path.join(folder, 'AlbumArt.png'))
            tracks[series] += 1
            write_tracks(tracks)
            shutil.move(file, os.path.join(folder, '{}.mp3'.format(file_title)))

    # ---------------------Far Verona----------------------------------------
    folder = 'Rollplay Far Verona'
    series = 'Far Verona'
    ydl_opts['download_archive'] = os.path.join('..', '..', 'google_drive',
                                                'YouTube Download', 'fv_downloaded.txt')
    ydl_opts['playliststart'] = tracks[series]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/playlist?list=PL-oTJHKXHicRE1O4DJVOkFTcqA0VNVU9J'])

    os.makedirs(folder, exist_ok=True)
    title_regex = re.compile(r'RollPlay - Far Verona - Week (\d+)(.*Part (\d+))?\.mp3')
    for file in [x for x in os.listdir('.') if x.endswith('.mp3')]:
        if title_regex.search(file) is not None:
            week, full_part, part = title_regex.search(file).groups()
            if len(week) < 2:
                week = '0' * (2 - len(week)) + week
            file_title = 'Week {} Part {}'.format(week, part) if part else 'Week {}'.format(week)
            tracks.setdefault(series, 1)
            edit_mp3(file, 'JP', folder, 'Books & Spoken', tracks[series], file_title,
                     os.path.join(folder, 'album_art_far_verona.png'))
            tracks[series] += 1
            write_tracks(tracks)
            shutil.move(file, os.path.join(folder, '{}.mp3'.format(file_title)))

    # ---------------------High Rollers Aerois----------------------------------------
    folder = 'High Rollers'
    ydl_opts['download_archive'] = os.path.join('..', '..', 'google_drive',
                                                'YouTube Download', 'hr_downloaded.txt')
    del ydl_opts['playliststart']
    hr_regex = re.compile(r'High Rollers - Aerois[\s_]+#(\d+)[\s_-]+([^-|]*)\.mp3')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/playlist?list=PLHv5CBoZYv4X5NpzLQKKC6loNz2ZZYyyz'])

    os.makedirs(folder, exist_ok=True)
    for file in [x for x in os.listdir('.') if x.endswith('.mp3')]:
        if hr_regex.search(file) is not None:
            episode, title = hr_regex.search(file).groups()
            episode = ('00' + episode)[-2:]
            file_title = '{} - {}'.format(episode, title)
            edit_mp3(file, 'High Rollers', 'Aerois Campaign', 'Books & Spoken', episode, file_title,
                     os.path.join(folder, 'album_art.jpg'))
            shutil.move(file, os.path.join(folder, '{}.mp3'.format(file_title)))

    # ---------------------Critical Role----------------------------------------
    # ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio',
    #                                'preferredcodec': 'mp3',
    #                                'preferredquality': '128'}]
    # ydl_opts['download_archive'] = os.path.join('..', '..', 'google_drive',
    #                                             'YouTube Download', 'cr_downloaded.txt')
    # cr_regex = re.compile(r'(.*) _ Critical Role _ Campaign 2, Episode (\d+)')
    #
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download(['https://www.youtube.com/watch?v=1cjdslm6xMk&list=PL7atuZxmT955Cw-fFS-_3IQvaCpQgDzWA'])
    #
    # folder = 'Critical Role Campaign 2'
    # os.makedirs(folder, exist_ok=True)
    # for file in [x for x in os.listdir('.') if x.endswith('.mp3')]:
    #     if cr_regex.search(file) is not None:
    #         title, episode = cr_regex.search(file).groups()
    #         episode = ('00' + episode)[-2:]
    #         file_title = '{} - {}'.format(episode, title)
    #         edit_mp3(file, 'Geek and Sundry', folder, 'Books & Spoken', episode, file_title,
    #                  os.path.join(folder, 'critical role album art.png'))
    #         write_tracks(tracks)
    #         shutil.move(file, os.path.join(folder, '{}.mp3'.format(file_title)))

    if errors:
        print('\n\nRecording errors. Check the file to see which videos failed.')
        dt = datetime.datetime.now()
        errorFile = open(os.path.join('..', '..', 'google_drive',
                                      'YouTube Download', 'errorsmp3.txt'), 'a')
        errorFile.write(dt.strftime('%m/%d/%Y %H:%M:%S'))
        errorFile.write('\n')
        errorFile.write('\n'.join(errors))
        errorFile.write('\n\n')
        errorFile.close()

    print('Done')

    # Quick Fix for all windows users:

    # Download the ffmpeg package from http://ffmpeg.zeranoe.com/builds/, unzip it, copy ALL the contents of the Bin
    # directory to the directory where youtube-dl.exe is located.

    # Using DOS navigate to the directory where youtube-dl is located and run using the command:
    # youtube-dl --extract-audio --audio-format mp3

    # And voila.... works like a charm.

    # ---------------------BLADES---------------------------------------------
    # ydl_opts['playliststart'] = 65
    #
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download(['https://www.youtube.com/watch?v=QNzpg-qdZ0g&list=PL-oTJHKXHicTtCC4rgmFSfZSSQsZmENAz&t=33s&index=1'])
    #
    # os.makedirs('Rollplay Blades', exist_ok=True)
    # for file in os.listdir('.'):
    #     if file.endswith('.mp3'):
    #         if title_regex2.search(file) is not None:
    #             # add code to update the metadata automatically
    #             week, part = title_regex2.search(file).groups()
    #             if len(week) < 2:
    #                 week = '0' * (2 - len(week)) + week
    #             shutil.move(file, os.path.join('Rollplay Blades',
    #                                            'Week {} Part {}.mp3'.format(week, part)))


    # ---------------------NEBULA JAZZ----------------------------------------
    # del ydl_opts['playliststart']
    #
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download(['https://www.youtube.com/watch?v=m6Q05wpCk7Q&list=PL-oTJHKXHicQ1mCYbJXMTdXKHnDM_FL8G&index=1'])
    #
    # os.makedirs('Rollplay Nebula Jazz', exist_ok=True)
    # for file in os.listdir('.'):
    #     if file.endswith('.mp3'):
    #         if title_regex2.search(file) is not None:
    #             # add code to update the metadata automatically
    #             week, part = title_regex2.search(file).groups()
    #             if len(week) < 2:
    #                 week = '0' * (2 - len(week)) + week
    #             shutil.move(file, os.path.join('Rollplay Nebula Jazz',
    #                                            'Week {} Part {}.mp3'.format(week, part)))
