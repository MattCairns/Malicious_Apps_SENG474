'''
Created on Feb 22, 2019

@author: Timothy
'''
from zipfile import ZipFile
from androguard.core.bytecodes.axml import AXMLPrinter
import re

MANIFEST = 'AndroidManifest.xml'
PERM_NAME_ATTRIB_KEY = '{http://schemas.android.com/apk/res/android}name'

##################################################


def readManifest(apkFilename):
    with ZipFile(apkFilename, 'r') as apk:
        mf = apk.read(MANIFEST)
        return mf


def extractPermissions(apkFilename):

    try:
        a = AXMLPrinter(readManifest(apkFilename))
        xml = a.get_xml_obj()
        permElements = xml.findall("uses-permission")

        perms = []
        for perm in permElements:
            permstr = perm.get(PERM_NAME_ATTRIB_KEY)
            perms.append(permstr)

        return perms
    except:
        return []


def extractPermissionSample(apkFilename, features):
    a = AXMLPrinter(readManifest(apkFilename))
    xml = a.get_xml_obj()
    permElements = xml.findall("uses-permission")

    perms = []
    for perm in permElements:
        permstr = perm.get(PERM_NAME_ATTRIB_KEY)
        perms.append(permstr)

    out_features = []
    index = 0
    for permission in features:
        if permission in perms:  # could be slow
            out_features.append(1)
        else:
            out_features.append(0)
        index += 1

    return out_features


def printPermissions(apkFilename):
    print("apk:\t\t", apkFilename, "\npermissions:")
    perms = extractPermissions(apkFilename)
    for perm in perms:
        print("\t\t", perm)


def extractAndCleanPermissions(args):
    """
    Extract and then cleans the permissions.  Used by imap_unordered call in parallel.

    Parameters
    ----------
    args : tuple
        Contains the path and the file to get permmissions for.

    Returns
    -------
    list, string
        Returns permissions and file.

    """
    path=args[0]
    file=args[1]
    permissions=extractPermissions(path + file)
    permissions=cleanPermissions(permissions)
    return permissions, file


# Clean permission name
def cleanPermissions(permission_list):

    # remove null
    if None in permission_list:
        permission_list.remove(None)
    if '' in permission_list:
        permission_list.remove('')

    # remove non-english permissions
    permission_list=filter(lambda p: isEnglish(p), permission_list)

    # strip leading/trailing whitespace
    permission_list=[str(p).lstrip().rstrip() for p in permission_list]

    # remove invalid permissions
    permission_list=filter(lambda p: isValidPermission(p), permission_list)

    # convert to lowercase
    permission_list=[str(p).lower() for p in permission_list]

    return permission_list


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except (UnicodeDecodeError, AttributeError):
        return False
    else:
        return True


# must contain at least 1 period
# period separated by other characters
def isValidPermission(perm):
    if not re.match('([^.]+(.)+)', perm) or not re.search('[.]+', perm):
        return False
    else:
        return True

##############################################################

def main():
    apkFilename="../seng474data/detected/2493996b105b30e0a803fd7ebb871813e80f89d98568a9c2b5da7de89c01d275.apk"
    printPermissions(apkFilename)

if __name__ == '__main__':
    main()
