'''
Created on Feb 26, 2019

@author: Timothy
'''
import csv
import downloader, os
from permissions import *
from zipfile import BadZipFile
from androguard.core.bytecodes import apk
import multiprocessing as mp
import tqdm


LOCAL_PATH = "Z:/"  # update this when necessary
counter = None

def isBadZip(file):
    try:
        with ZipFile(file, 'r') as apk:
            apk.read(MANIFEST)
            return False
    except BadZipFile:
        return True
    except:
        return True


def removeBadZips(file):
    if isBadZip(file):
        print('\nRemoved ' + file)
        os.remove(file)
        return 1
    return 0 

def removeParallel(path):
    pool = mp.Pool(mp.cpu_count())

    print(path)
    args = [path+file for file in os.listdir(path)]
    #results = pool.map_async(removeBadZips, args).get()
    for _ in tqdm.tqdm(pool.imap_unordered(removeBadZips, args), total=len(args)):
        pass

    pool.close()


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
    
    # sort rows by type (malicious/benign), then by filename (alphabetical)
    if sort:
        s = sorted(list(dataset.keys()), key=lambda x: (dataset[x]['!type'],x))
    else:
        s = list(dataset.keys())

    # get all unique permissions
    d = s[0]

    # Writes number of ROWs then number of COLUMNS
    f.write(str(len(dataset.keys())))    
    f.write('\n')
    f.write(str(len(dataset[d].keys())+1)) #add 1 for filename header
    f.write('\n')

    if sort:
        headings = sorted(list(dataset[d].keys()))
    else:
        headings = list(dataset[d].keys())
    
    #print(len(headings))

    writer = csv.DictWriter(f,headings, extrasaction='ignore')
    
    f.write("!file_name,")
    writer.writeheader()
    for file in s:
        f.write(file)
        f.write(',')
        writer.writerow(dataset[file])
        #print("len row: ",len(dataset[file]))
    f.close()
    
    print("Dataset saved to", filename)
    
def getPermissionOrder(file_name):
    
    f = open(file_name, encoding='utf-8')
    lines = [line for line in f]
    rows = lines[0]
    cols = lines[1]
    headings = lines[2].split(',')[1:]
    return headings

def main():
    #removeParallel(LOCAL_PATH + downloader.LOCAL_UNDETECTED)
    #removeParallel(LOCAL_PATH + downloader.LOCAL_DETECTED)

    fn = "../data/dataset.csv"
    data = buildDataset()
    output_csv(data, fn)
    
    #f = open("../data/apk_file_order.txt",'w')
    #for apk in apk_filename_order:
    #    f.write(apk)
    #    f.write("\n")
    #f.close()
    #print("Apk filename order saved to", "../data/apk_file_order.txt")
    
    #print(apk_filename_order)
    #print(getPermissionOrder(fn))
    
if __name__ == '__main__':
    main()
