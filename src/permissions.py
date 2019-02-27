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
    a = AXMLPrinter(readManifest(apkFilename))
    xml = a.get_xml_obj()
    permElements = xml.findall("uses-permission")
    
    perms = []
    for perm in permElements:
        permstr = perm.get(PERM_NAME_ATTRIB_KEY) 
        perms.append(permstr)
        
    return perms
    
def printPermissions(apkFilename):
    print("apk:\t\t", apkFilename, "\npermissions:")
    perms = extractPermissions(apkFilename)
    for perm in perms:
        print("\t\t", perm)

##############################################################

def main():
    apkFilename = "../apks/00006ae4233968830098f7db6b745b106373d6d91e0021a0b660631bf4660d32.apk"
    printPermissions(apkFilename)

if __name__ == '__main__':
    main()
