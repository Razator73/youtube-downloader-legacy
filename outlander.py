import json
import re
from pathlib import Path

import youtube_dl as yt

from rollplay2 import edit_mp3


def get_playlist(album, artist, url, title_regex, folder, opts, album_art):
    folder.mkdir(exist_ok=True)
    opts['outtmpl'] = str(folder / '%(title)s.%(ext)s')
    with yt.YoutubeDL(opts) as ydl:
        ydl.download([url])

    file_pattern = rf'{folder}/{title_regex}'
    for file in folder.glob('*.mp3'):
        file_search = re.search(file_pattern, str(file))
        if file_search:
            file_name, title = file_search.groups()
            with open(folder / f'{file_name}.info.json') as f:
                file_info = json.load(f)
            edit_mp3(file, artist, album, 'Soundtrack',
                     file_info['playlist_index'], title, album_art)
            file.rename(folder / f'{title}.mp3')
            (folder / f'{file_name}.info.json').unlink()


if __name__ == '__main__':
    parent_folder = Path('/home/ryan/Music/outlander-ost')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'writeinfojson': True
    }

    album_artist = 'Bear McCreary'
    seasons = [
               {'name': 'Outlander: Season 1, Vol. 1',
                'url': 'https://www.youtube.com/playlist?list=OLAK5uy_nExzJ649LnBLz3-xDo8_EZpJDJfVxMS88',
                'title_regex': r'((.*))\.mp3',
                'art': parent_folder / 's1v1_album_art.png',
                'folder': parent_folder / 'outlander-season-1-vol-1'},
               {'name': 'Outlander: Season 1, Vol. 2',
                'url': 'https://www.youtube.com/playlist?list=PLeigbpMXUkYkvpT37e-364djnRATSd5qx',
                'title_regex': r'(Outlander, \d{2}, (.*), Vol 2 Soundtrack, Bear McCreary)\.mp3',
                'art': parent_folder / 's1v2_album_art.png',
                'folder': parent_folder / 'outlander-season-1-vol-2'},
               {'name': 'Outlander: Season 2',
                'url': 'https://www.youtube.com/playlist?list=OLAK5uy_kHPOY9kLUQiCsriM2bEmsropaTypl-F58',
                'title_regex': r'((.*))\.mp3',
                'art': parent_folder / 's2_album_art.png',
                'folder': parent_folder / 'outlander-season-2'},
               {'name': 'Outlander: Season 3',
                'url': 'https://www.youtube.com/playlist?list=PLeigbpMXUkYnRXw6d0Mo1bUfy8Ttxynqr',
                'title_regex': r'(Outlander, \d{2}, (.*), Season 3.*)\.mp3',
                'art': parent_folder / 's3_album_art.png',
                'folder': parent_folder / 'outlander-season-3'},
               {'name': 'Outlander: Season 4',
                'url': 'https://www.youtube.com/playlist?list=PLDisKgcnAC4Smi3YhuznqE24NFYtM5Yx8',
                'title_regex': r'((.*) _ Outlander - Season 4 OST)\.mp3',
                'art': parent_folder / 's4_album_art.png',
                'folder': parent_folder / 'outlander-season-4'}
    ]
    for season in seasons:
        get_playlist(album=season['name'],
                     artist=album_artist,
                     url=season['url'],
                     title_regex=season['title_regex'],
                     opts=ydl_opts,
                     album_art=season['art'],
                     folder=season['folder'])
