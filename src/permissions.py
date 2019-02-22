from zipfile import ZipFile
import re

MANIFEST = 'AndroidManifest.xml'
MF_PERMISSIONS_TAG = "usespermission"
MF_ENCODING = 'cp1252'
ACCEPTCHARS = list(map(chr, range(65, 123))) + [".", " ", "_"]
MF_PERM_PATTERN = "android[.]permission[.][_A-Z|A-Z]+"


# Input:     filename of apk
# Output:    decoded manifest
def extractManifest(apkFilename):
    with ZipFile(apkFilename, 'r') as apk:
        mf = apk.read(MANIFEST)
        return mf.decode(MF_ENCODING)


# Input:     decode binary manifest
# Output:    cleaned manifest
def cleanManifest(manifest):
    clean = filter(lambda char: (char in ACCEPTCHARS), manifest)
    charlst = list(clean)
    cleanMf = "".join(charlst)
    return cleanMf


def extractPermissions(apkFilename):
    manifest = extractManifest(apkFilename)
    cleanMf = cleanManifest(manifest)
    permStartIndex = cleanMf.index(MF_PERMISSIONS_TAG)
    manifest = manifest[permStartIndex + len(MF_PERMISSIONS_TAG):]
    perms = re.findall(MF_PERM_PATTERN, cleanMf)
    return perms
    

#############################################################


apkFilename = "../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
perms = extractPermissions(apkFilename)

print("apk:\t\t", apkFilename, "\npermissions:")
for perm in perms:
    print("\t\t", perm)

