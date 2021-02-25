from __future__ import unicode_literals
import youtube_dl
import os
import re
import shutil
import requests
import bs4


url = 'https://www.sc2links.com/tournament/?match=595&action=Ascending'  # GSL 2019 Season 1
sets_html = requests.get(url)
sets_html.raise_for_status()
sets_parsed = bs4.BeautifulSoup(sets_html.text, "lxml")

video_ids = []
for link in sets_parsed.findAll('a'):
    divs = link.findAll('div', attrs={'class': 'match'})
    if len(divs) > 0:
        match_url = link['href']
        match_html = requests.get(match_url)
        match_html.raise_for_status()
        match_parsed = bs4.BeautifulSoup(match_html.text, 'lxml')
        try:
            vid_id = re.search(r'https://www.youtube.com/embed/([a-zA-Z0-9_-]+)\?',
                      match_parsed.find('iframe')['src']).group(1)
            video_ids.append(vid_id)
        except AttributeError:
            pass

os.makedirs('..\\..\\Videos\\YouTube Downloads\\GSL', exist_ok=True)
os.chdir('..\\..\\Videos\\YouTube Downloads\\GSL')
errors = []


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        errors.append(msg)
        print(msg)


ydl_opts = {
    # 'format': 'bestvideo[height<=720]+bestaudio',
    'format': 'bestvideo+bestaudio',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mkv'
    }],
    'download_archive': os.path.join('..', '..', '..', 'Google Drive',
                                     'YouTube Download', 'gsl_vids.txt'),
    'logger': MyLogger(),
    'ignoreerrors': True,
    'outtmpl': '%(title)s.%(ext)s',
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(video_ids)

for file in os.listdir('.'):
    file_search = re.search(r'\[2019 GSL S(?:eason)?\s*1\] Ro\.(\d+) Group ([A-Z]) Match(\d)', file)
    if file_search:
        gsl_round, group_letter, match_num = file_search.groups()
        file_name = 'Ro.{} Group {} Match {}.mkv'.format(gsl_round, group_letter, match_num)
        shutil.move(file, file_name)
