import json
import re
from pathlib import Path

import youtube_dl as yt

from rollplay2 import edit_mp3

folder = Path('/home/ryan/Music/cadence-of-hyrule')
# os.chdir(folder)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ignoreerrors': True,
    'outtmpl': str(folder / '%(title)s.%(ext)s'),
    # 'playlistend': 2,
    'writeinfojson': True
}

playlist_url = 'https://www.youtube.com/playlist?list=PLxZPEb_jVjLC_1MNYsdqOHSMcCmR4HH5V'
with yt.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])

file_pattern = rf'{folder}/((.*) - Cadence of Hyrule Soundtrack)\.mp3'
for file in folder.glob('*.mp3'):
    file_search = re.search(file_pattern, str(file))
    if file_search:
        file_name, title = file_search.groups()
        with open(folder / f'{file_name}.info.json') as f:
            file_info = json.load(f)
        edit_mp3(file, 'Cadence of Hyrule', 'Cadence of Hyrule OST', 'Soundtrack',
                 file_info['playlist_index'], title, folder / 'album-art.png')
        file.rename(folder / f'{title}.mp3')
        (folder / f'{file_name}.info.json').unlink()
