import os
import youtube_dl


os.chdir('..\\..\\Music\\YouTube Downloads\\Cursed Castle')
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'ignoreerrors': True,
    # 'writethumbnail': True
    'download_archive': os.path.join('..', '..', '..', 'google_drive',
                                     'YouTube Download', 'castle_downloaded.txt'),
}

# vids = ['70VlAyEUXYM',
#         'd6UR0FRL_q4',
#         'hosCuzo6JKo',
#         'Pa8iyHzHUSQ',
#         '2axiYQYJMUU',
#         '7H9A4996g4U',
#         'BKWHkoNBb9g',
#         'rL5_44L0yV4',
#         '6zckQ5kxXkM',
#         'ZW25nrh-mxo',
#         'SNJ--gHasOE',
#         'AMkz9JF7teY',
#         'xmckBT-IUeE',
#         'FSW371FMLns',
#         'Yx39-jnpZH8',
#         'rCXKVwcQVek',
#         '3SpikQ3erXM',
#         'u9Dg-g7t2l4',
#         'Qk1LlQG8tbs',
#         'PcP4-cotaPQ',
#         'mBYUcjGdVUY',
#         '0I647GU3Jsc',
#         'GZrddJPGp1I',
#         '5VInr-cSNNU']

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # ydl.download(['https://www.youtube.com/watch?v={}'.format(vid) for vid in vids])
    ydl.download(['https://www.youtube.com/playlist?list=PLybAUSaWSki9SMCRXct5D0XFeE6Kn2L3m'])

print('Done')
