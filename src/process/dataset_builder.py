"""
Author:		Matthew Cairns - V00709952 & Tim Salomonsson - V00807959
Created:	12-Mar-2019 09:40:11
Filename:	dataset_builder.py
Description:  Builds and cleans our dataset stored on my local computer.  This dataset
                could not be submitted as it is 1.5TB in size.
"""


import csv, os, pickle, sys, re

from zipfile import BadZipFile, ZipFile
from androguard.core.bytecodes import apk

import multiprocessing as mp
import numpy as np
import tqdm as tqdm

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import process.downloader as downloader
from utils.permissions import MANIFEST, extractAndCleanPermissions, isEnglish


LOCAL_PATH = 'Z:/'  # update this when necessary
PICKLE_UNDETECTED = LOCAL_PATH + 'undetected_pickle.p'
PICKLE_DETECTED = LOCAL_PATH + 'detected_pickle.p'

"""
Open a csv dataset and store labels and features
in sparse numpy matrices.

In:
    file_name:     File to read in

Out:
    X:             The array of features [n_samples, n features]
    y:             the array of labels [n_samples]
    headings:      feature names (permissions)
    apk_to_index:  dictionary links apk filename with position in feature matrix X
"""

def load_dataset_csv(file_name):
    pickle_name = re.search('(.*)\.csv', file_name).group(1) + '.p'
    try:
        X, y, headings, apk_to_index = pickle.load(open(pickle_name, 'rb'))
        print('Loaded pickle: {}'.format(pickle_name))
        return X, y, headings, apk_to_index
    except:
        print('No pickle to load from {}'.format(file_name))

    f = open(file_name, encoding='utf-8')
    info = [next(f) for i in range(3)]
    rows = int(info[0])
    columns = int(info[1])
    headings = info[2].rstrip().split(',')[2:]  #remove file and type headings

    print("Loading dataset from", file_name)
    print("Rows:", rows)
    print("Columns:", columns, "\n")

    reader = csv.reader(f, delimiter=',')
    X = np.zeros((rows, columns-2), dtype=np.int8)
    y = np.zeros(rows)

    apk_to_index = {}

    i=0
    for row in reader:
        print("build sparse X, y: sample %d of %d, %.2f percent done." % (i+1, rows, 100 * ((i+1)/rows)))
        sys.stdout.write("\033[F")

        apk_to_index[row[0]] = i
        X[i] = np.asarray(row[2:])
        y[i] = np.asarray(row[1])
        i += 1

    print("")

    pickle.dump((X, y, headings, apk_to_index), open(pickle_name, 'wb'))
    return X,y,headings,apk_to_index


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


def pickler(path, pickle_name, batch_size = 1000):
    """
    Pickles the apk permissions in a specified path.

    Parameters
    ----------
    path : string
        Path to the folder of APKs
    pickle_name : string
        Name of the Pickle file
    batch_size : int
        How often should the pickle be saved?
    """

    print('Loading directories in path: {}'.format(path))
    directories = os.listdir(path)

    perm_set = set()
    permissions = []
    files = []

    try:
        perm_set, permission, files = pickle.load(open(pickle_name, 'rb'))
        directories = list(set(directories) - set(files))
        print('Loaded Pickle with {} files.'.format(str(len(files))))

    except(OSError, IOError) as e:
        print('There was an error loading pickle {}'.format(pickle_name))


    for i in range(0, len(directories), batch_size):
        x, y, z = permissionSet(path, directories[i:i+batch_size])
        perm_set = perm_set.union(x)
        permissions += y
        files += z
        pickle.dump((perm_set, permissions, files), open(pickle_name, 'wb'))

        print("Processed " + str(len(files)) + ' apks')
        sys.stdout.write("\033[F")


def getPermissionSets():
    """
    Pickles both the undetected and detected apks.
    """
    undetected_path = LOCAL_PATH + downloader.LOCAL_UNDETECTED
    detected_path = LOCAL_PATH + downloader.LOCAL_DETECTED

    pickler(undetected_path, PICKLE_UNDETECTED)
    pickler(detected_path, PICKLE_DETECTED)


def permissionSet(path, dirs):
    pool = mp.Pool(mp.cpu_count()) # How many cores are we using?
    unique_set = set()
    perm_list = []
    files = []

    # Process the permissions from the apk files in parallel
    permissions_list = pool.map(extractAndCleanPermissions, [(path, file) for file in dirs])

    pool.close()
    pool.join()


    # Add the processed permissions to lists and return to pickler.
    for permissions, file in permissions_list:
        if len(permissions) > 0:
            files.append(file)
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



def buildDatasetPickle(num=100):
    set1, undetected, undetected_files = pickle.load(open(PICKLE_UNDETECTED, 'rb'))
    set2, detected, detected_files = pickle.load(open(PICKLE_DETECTED, 'rb'))
    unique_set = set1.union(set2)

    data = {}  # filename: [list of perms
    batch_set = set()

    #undetected
    file_index = 0
    for file in undetected_files:
        print("undetected: %d of %d" % (file_index, len(undetected_files)))
        data[file] = {}
        data[file]["!type"] = 0

        for perm in undetected[file_index]:
            data[file][perm] = 1

            batch_set.add(perm)

        file_index +=1

        if file_index == num:
            break

    #detected
    file_index = 0
    for file in detected_files:
        print("detected: %d of %d" % (file_index, len(detected_files)))

        data[file] = {}
        data[file]["!type"] = 1

        for perm in detected[file_index]:
            data[file][perm] = 1
            batch_set.add(perm)


        file_index +=1
        if file_index == num:
            break

    print("Dataset (num = %d) built." % (num))

    batch_set.add("!type")

    return data, unique_set, batch_set

def output_csv(dataset, filename, unique_set, sort=True):

    f = open(filename, "w", newline='')

    # sort rows by type (malicious/benign), then by filename (alphabetical)
    if sort:
        s = sorted(list(dataset.keys()), key=lambda x: (dataset[x]['!type'],x))
    else:
        s = list(dataset.keys())

    # get all permissions
    #s1 = s[0].keys()

    # Writes number of ROWs then number of COLUMNS
    f.write(str(len(dataset.keys())))
    f.write('\n')
    f.write(str(len(unique_set)+1)) #add 1 for filename header
    f.write('\n')

    if sort:
        headings = sorted(list(unique_set))
    else:
        headings = list(unique_set)

    print(headings)

    #writer = csv.DictWriter(f,headings, extrasaction='ignore')

    f.write("!file_name,")
    i = 0
    for heading in headings:


        heading = str(heading)
        if i != 0:
            f.write(",")

        try:

            f.write(heading)
        except:
            pass

        i += 1
    f.write("\n")


    #writer.writeheader()

    fi = 0
    for file in s:

        print("Writing row %d of %d, %.2f percent done." % (fi+1, len(s), round((100 * (fi+1)/len(s)), 2)))

        f.write(file)
        f.write(',')

        i = 0
        for perm in unique_set:

            if str(perm) != "!type":
                if i == 0:
                    f.write(str(dataset[file]["!type"]))

                f.write(",")

                try:
                    d = dataset[file][perm]
                    f.write(str(1))

                except KeyError:
                    f.write(str(0))

                i += 1
        f.write("\n")
        fi += 1

        #writer.writerow(dataset[file])
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

    #getPermissionSets()

    fn = "../../data/dataset.csv"
    data, unique_set, batch_set = buildDatasetPickle(3000)
    output_csv(data, fn, batch_set)

if __name__ == '__main__':
    main()
