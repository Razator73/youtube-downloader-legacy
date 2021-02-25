from __future__ import unicode_literals
import youtube_dl
import os
import datetime
import re
import shutil


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
    'download_archive': os.path.join('..', '..', 'Google Drive',
                                     'YouTube Download', 'viddownloaded.txt'),
    'ignoreerrors': True,
    'playliststart': 13,
    'outtmpl': '%(title)s.%(ext)s',
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # Road to Ranked
    # ydl.download(['https://www.youtube.com/watch?v=VJEGXrsCgu4&t=2s&index=1&list=PLq4FWz75gv-Z2neTWEfs-qKRGzSkrxmov'])
    # SAO-A
    # ydl.download(['https://www.youtube.com/watch?v=V6kJKxvbgZ0&index=1&list=PLuAOJfsMefuej06Q3n4QrSSC7qYjQ-FlU'])
    # ydl.download(['https://www.youtube.com/watch?v=E5YUAuFPLis'])
    ydl.download(['https://www.youtube.com/playlist?list=PL9EBq1DyhMVBB0AIiJBDdXzF4hSGE6CL3',
                  'https://www.youtube.com/playlist?list=PLd4du1T3t3aWSLU98JEjmuejciFZjH02B'])
    # ydl.download(['https://www.youtube.com/playlist?list=PLrHO_aFPAv9TRhEZYUlnl7iMU5PkW1pI6'])
    # ydl.download(['https://www.youtube.com/playlist?list=PLd4du1T3t3aWSLU98JEjmuejciFZjH02B'])
    # ydl.download(['https://www.youtube.com/watch?v=0dCTtEuWsC4'])

# title_regex = re.compile(r'\[(201\d) GSL Season (\d)\]Code S Ro.(\d*) Group (\w) (Match\d)')
# gsl_vs_world = re.compile(r'(Ro\.\d) (Match\d)')
# os.makedirs('GSL vs World', exist_ok=True)
# for file in os.listdir('.'):
#     if title_regex.search(file) is not None:
#         year, season, ro, group, match = title_regex.search(file).groups()
#         os.makedirs('{} GSL S{}'.format(year, season), exist_ok=True)
#         print('Moving {}'.format(match))
#         shutil.move(file, os.path.join('{} GSL S{}'.format(year, season),
#                     'Ro.{} Group {} {}.mkv'.format(ro, group, match)))
#     if gsl_vs_world.search(file) is not None:
#         ro, match = gsl_vs_world.search(file).groups()
#         print('Moving {} {}'.format(ro, match))
#         shutil.move(file, os.path.join('GSL vs World', '{} {}.mkv'.format(ro, match)))

ser_str = r'([a-zA-Z \'-]+!+) - My Time at Portia \(Full Release\) – Part (\d+)\.mkv'
for file in [x for x in os.listdir() if re.search(ser_str, x)]:
    print(file)
    title, part = re.search(ser_str, file).groups()
    part = '00{}'.format(part)[-2:]
    print('{} - {}.mkv'.format(part, title))
    shutil.move(file, '{} - {}.mkv'.format(part, title))

print('Done')

# ydl_opts documentation
# https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279

# http://manpages.ubuntu.com/manpages/xenial/man1/youtube-dl.1.html
