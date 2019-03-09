'''
Created on Feb 26, 2019

@author: Timothy
'''
import csv
import downloader, os, pickle, sys
from permissions import *
from zipfile import BadZipFile
from androguard.core.bytecodes import apk
import multiprocessing as mp
import tqdm as tqdm
import re

LOCAL_PATH = 'Z:/'  # update this when necessary
PICKLE_UNDETECTED = LOCAL_PATH + 'undetected_pickle.p'
PICKLE_DETECTED = LOCAL_PATH + 'detected_pickle.p'

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

        print("Processed " + str(len(undetected_files)) + ' apks')
        sys.stdout.write("\033[F")


def getPermissionSets():
    """
    Pickles both the undetected and detected apks.
    """
    undetected_path = LOCAL_PATH + downloader.LOCAL_UNDETECTED
    detected_path = LOCAL_PATH + downloader.LOCAL_DETECTED

    pickler(undetected_path, PICKLE_UNDETECTED)
    pickler(detected_path, PICKLE_DETECTED)


# must contain at least 1 period
# period separated by other characters
def isValidPermission(perm):
    if not re.match('([^.]+(.)+)', perm) or not re.search('[.]+', perm):
        return False
    else:
        return True

# Clean permission name
def cleanPermissions(permission_list):

    #remove null
    if None in permission_list:
        permission_list.remove(None)
    if '' in permission_list:
        permission_list.remove('')

    #remove non-english permissions
    permission_list = filter(lambda p: isEnglish(p), permission_list)

    #strip leading/trailing whitespace
    permission_list = [str(p).lstrip().rstrip() for p in permission_list]

    # remove invalid permissions
    permission_list = filter(lambda p: isValidPermission(p), permission_list)

    #convert to lowercase
    permission_list = [str(p).lower() for p in permission_list]

    return permission_list


def permissionSet(path, dirs):
    unique_set = set()
    perm_list = []     # TODO: convert to dict of dicts
    files = []

    for file in dirs:
        permissions = extractPermissions(path + file)
        permissions = cleanPermissions(permissions)
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

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def buildDatasetPickle(num=100):
    set1, undetected, undetected_files = pickle.load(open(PICKLE_UNDETECTED, 'rb'))
    set2, detected, detected_files = pickle.load(open(PICKLE_DETECTED, 'rb'))

    unique_set = set1.union(set2)
    unique_set.remove(None)
    unique_set.remove('')

    #lower = [str(u).lower() for u in unique_set]
    #unique_set = set(lower)

    rstriped = [str(u).lstrip() for u in unique_set]
    unique_set = set(rstriped)


    nonEnglish = []
    for perm in unique_set:
        if not isEnglish(perm):
            nonEnglish.append(perm)
    for n in nonEnglish:
        unique_set.remove(n)

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

    if None in batch_set:
        batch_set.remove(None)
    if '' in batch_set:
        batch_set.remove('')

    #nonEnglish = []
    #for perm in batch_set:
    #    if not isEnglish(perm):
    #        nonEnglish.append(perm)
    #for n in nonEnglish:
    #    batch_set.remove(n)

    import re
    print(len(batch_set))

    remove = []
    for perm in batch_set:
        if not re.match('([^.]+(.)+)', perm) or not re.search('[.]+', perm):
            remove.append(perm)


    print(remove)
    for r in remove:
        batch_set.remove(r)

    #lower = [str(u).lower() for u in  batch_set]
    #batch_set = set(lower)
    batch_set.add("!type")

    rstriped = [str(u).lstrip() for u in batch_set]
    batch_set = set(rstriped)

    print(len(batch_set))



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

        print("Writing row %d of %d, %.2f percent done." % (fi, len(s), round((100 * fi/len(s)), 2)))

        f.write(file)
        f.write(',')

        i = 0
        for perm in unique_set:

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

    getPermissionSets()

    fn = "../data/dataset.csv"
    data, unique_set, batch_set = buildDatasetPickle(10000)
    output_csv(data, fn, batch_set)


    #set1, set2, undetected, undetected_files, detected, detected_files = pickle.load(open(PICKLE_FILE, 'rb'))
    #unique_set = set1.union(set2)
    #print("Num unique permissions:", len(unique_set))
    #print("Num undetected files:", len(undetected_files))
    #print("Num detected files:",len(detected_files))


if __name__ == '__main__':
    main()
