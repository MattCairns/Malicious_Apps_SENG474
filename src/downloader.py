"""
Created:	26-Feb-2019 10:49:47
Filename:	downloader.py 
Description:  
"""

import random, os, sys
from sftp import *
from parsefilenames import *


LOCAL_PATH = '/tmp/'
LOCAL_UNDETECTED = 'undetected/'
LOCAL_DETECTED = 'detected/'

def choose_n_items(items, n):
    # If we have less then n items left return them
    if len(items) <= n:
        return items

    # Choose n unique items
    choices = []
    while n > 0:
        c = random.choice(items)
        if c not in choices:
            n -= 1
            choices.append(c)

    return choices
        

def diff(A, B):
    B = set(B)
    return [item for item in A if item not in B]


def download_list(sftp, items, bandwidth_limit, server_path, local_path):
    sftp.chdir(server_path)
    downloaded = []
    size = 0
    for i in items:
        print('downloading ' + i)
        size += sftp.stat(i).st_size
        sftp.get(i, local_path + i)
        downloaded.append(i)
        if size >= bandwidth_limit and bandwidth_limit != -1:
            break

    sftp.chdir('..')
    
    return size, downloaded


def get_apks(sftp, apk_amount, bandwidth_limit):
    amount_downloaded = 0

    undetected = get_undetected_filenames()
    detected = get_detected_filenames()

    already_downloaded = get_downloaded()

    undetected = choose_n_items(diff(undetected, already_downloaded), apk_amount)
    detected = choose_n_items(diff(detected, already_downloaded), apk_amount)

    size, downloaded = download_list(sftp, undetected, bandwidth_limit, UNDETECTED_PATH, LOCAL_PATH + LOCAL_UNDETECTED)
    amount_downloaded += size

    size, downloaded = download_list(sftp, detected, bandwidth_limit, DETECTED_PATH, LOCAL_PATH + LOCAL_UNDETECTED) 
    amount_downloaded += size
    


def get_downloaded():
    dirs = os.listdir(LOCAL_PATH + LOCAL_UNDETECTED)
    dirs += os.listdir(LOCAL_PATH + LOCAL_DETECTED)
    return dirs 


def main():
    download_amount = -1
    apk_amount = 2

    sftp = connect_koodous()
    sftp.chdir(APKS_PATH)
    
    parse_filenames()
    
    get_apks(sftp, apk_amount, download_amount)


if __name__ == '__main__':
    main()
