from lxml import html
import requests
import re
import os 

folder = '\"Documents/SENG474Project/apks/top_free\"'
page = requests.get('https://play.google.com/store/apps/collection/topselling_free')
f = open('apps.html', 'r')

page = f.read()

ids = re.findall(r'data-docid=\"(([^\"])*)\"', str(page))

apps = []

for i in ids:
    if i[0] not in apps:
        apps.append(i[0])


files = os.listdir('.')

apps = list(set(apps) - set(files))

cmd = 'gplaycli -d '
for i in apps:
    print('downloading {}'.format(i)
    os.system(cmd + i)
