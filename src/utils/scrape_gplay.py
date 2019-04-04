"""
Author:		Matthew Cairns - V00709952 & Tim Salomonsson - V00807959
Created:	26-Mar-2019 18:11:29
Filename:	scrape_gplay.py
Description:    Quick script to scrape gplay store and use
                gplaycli to download top free apps.
"""
from lxml import html
import requests
import re
import os


folder = '\"Documents/SENG474Project/apks/top_free\"'
page = requests.get('https://play.google.com/store/apps/collection/topselling_free')

# Extract apk app ID
ids = re.findall(r'data-docid=\"(([^\"])*)\"', str(page))

# Make a nice list
apps = []
for i in ids:
    if i[0] not in apps:
        apps.append(i[0])


# Make sure we have not already downloaded the app
files = os.listdir('.')
apps = list(set(apps) - set(files))

# Download the apps
cmd = 'gplaycli -d '
for i in apps:
    print('downloading {}'.format(i)
    os.system(cmd + i)
