"""
Created:	26-Feb-2019 10:49:47
Filename:	downloader.py 
Description:  
"""

from sftp import *





def main():
    download_amount = 0
    apk_amount = 0

    sftp = connect_koodous()
    sftp.chdir(APKS_PATH)
    print(sftp.listdir())
    sftp.chdir(DETECTED_PATH)
    print(sftp.listdir())







if __name__ == '__main__':
    main()
