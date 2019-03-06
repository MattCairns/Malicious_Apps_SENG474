'''
Created on Feb 22, 2019

@author: Timothy
'''
from zipfile import ZipFile
from androguard.core.bytecodes.axml import AXMLPrinter

MANIFEST = 'AndroidManifest.xml'
PERM_NAME_ATTRIB_KEY= '{http://schemas.android.com/apk/res/android}name'

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
        if permission in perms: #could be slow
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

##############################################################

def main():
    apkFilename = "../seng474data/detected/2493996b105b30e0a803fd7ebb871813e80f89d98568a9c2b5da7de89c01d275.apk"
    printPermissions(apkFilename)

if __name__ == '__main__':
    main()
