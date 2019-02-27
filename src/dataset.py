'''
Created on Feb 26, 2019

@author: Timothy
'''

import downloader, os
from permissions import extractPermissions

LOCAL_PATH = "/seng474data"  # update this when necessary

def getPermissionSets():
    
    unique_set = set()
    undetected = []     # TODO: convert to dict of dicts
    detected = []       # TODO: convert to dict of dicts
    
    #undetected
    for file in os.listdir(LOCAL_PATH + downloader.LOCAL_UNDETECTED):
        permissions = extractPermissions(file)
        undetected.append(permissions)

        for perm in permissions:
            unique_set.add(perm)

    #undetected
    for file in os.listdir(LOCAL_PATH + downloader.LOCAL_DETECTED):
        permissions = extractPermissions(file)
        detected.append(permissions)

        for perm in permissions:
            unique_set.add(perm)
    
    return (unique_set, undetected, detected)
    