'''
Created on Feb 26, 2019

@author: Timothy
'''
import csv
import downloader, os
from permissions import *

LOCAL_PATH = "/seng474data/"  # update this when necessary

def isBadZip(file):
    
    try:
        with ZipFile(file, 'r') as apk:
            apk.read(MANIFEST)
            return False
    except ZipFile.BadZipFile:
        return True


def removeBadZips(path):
    count = 0
    for file in os.listdir(path):
        if isBadZip(path+file):
            os.remove(path + file)
            count_undetected += 1

    return count 


def getPermissionSets():
    set1, undetected, undetected_files = permissionSet(LOCAL_PATH + downloader.LOCAL_UNDETECTED) 
    set2, detected, detected_files = permissionSet(LOCAL_PATH + downloader.LOCAL_DETECTED)
    unique_set = set1.union(set2)
    
    return (unique_set, undetected, undetected_files, detected, detected_files)


def permissionSet(path):
    unique_set = set()
    perm_list = []     # TODO: convert to dict of dicts
    files = []
    
    for file in os.listdir(path):
        files.append(file)
        permissions = extractPermissions(path + file)
        perm_list.append(permissions)

        for perm in permissions:
            unique_set.add(perm)

    return unique_set, perm_list, files
    

def buildDataset():
    unique_set, undetected, undetected_files, detected, detected_files = getPermissionSets()
    data = {}  # filename: [list of perms]
    
   
    #undetected
    file_index = 0
    for file in undetected_files:
        data[file] = {}
        data[file]["!type"] = 0 
        
        for perm in unique_set:
            if perm in undetected[file_index]:
                data[file][perm] = 1
            else:
                data[file][perm] = 0

        file_index +=1
        
    #detected
    file_index = 0
    for file in detected_files:
        data[file] = {}
        data[file]["!type"] = 1
        
        for perm in unique_set:
            if perm in detected[file_index]:
                data[file][perm] = 1
            else:
                data[file][perm] = 0

        file_index +=1
    print("Dataset built.")

    return data

def output_csv(dataset, filename, sort=True):
    f = open(filename, "w", newline='')
    
    if sort:
        s = sorted(list(dataset.keys()), key=lambda x: (dataset[x]['!type'],x))
    else:
        s = list(dataset.keys())
        

    d = s[0]

    # Writes number of ROWs then number of COLUMNS
    f.write(str(len(dataset.keys())))
    f.write('\n')
    f.write(str(len(dataset[d].keys())))
    f.write('\n')


    # Change NoneType to strings
    dataset[d]['None'] = dataset[d].pop(None)


    headings = sorted(list(dataset[d].keys()))

    # extrasaction ignores fields that are 'extra' such as nonetype
    # I have not verified if the csv output is correct when extras are deleted
    writer = csv.DictWriter(f,headings, extrasaction='ignore')
    

    # TODO: The resulting output is not square and has varying number of columns...
    # TODO: This needs to be fixed to be able to read into a numpy matrix
    
    writer.writeheader()
    for file in s:
        writer.writerow(dataset[file])
    f.close()
    
    print("Dataset saved to", filename)

def input_csv(filename):
    dataset = {}
    return dataset

def main():
    count_undetected = removeBadZips(LOCAL_PATH + downloader.LOCAL_UNDETECTED)
    count_detected = removeBadZips(LOCAL_PATH + downloader.LOCAL_DETECTED)
    print("Removed %d bad undetected zips." % count_undetected)
    print("Removed %d bad detected zips." % count_detected)

    data = buildDataset()
    output_csv(data, "../data/dataset.csv")

    
if __name__ == '__main__':
    main()
