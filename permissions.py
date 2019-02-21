from zipfile import ZipFile
import re

# extract binary android manifest file from apk (zip)
testapk = "fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
zip = ZipFile(testapk, 'r')
zip.extract('AndroidManifest.xml')

# read binary manifest file as python str
with open('AndroidManifest.xml', 'r') as myfile:
    data = myfile.read()

# create list of acceptable chars (a-z,A-Z,., ,_)
achars = list(map(chr, range(65, 123)))
achars.append(".")
achars.append(" ")
achars.append("_")

# remove all unacceptable chars from manifest file
cleaned = ""
for char in data:
    if char in achars:
        cleaned += char

# find location of permissions data in manfiest file
ind = cleaned.index("usespermission")   
len = len("usespermission")

# remove beginning of file up to permissions data
cleaned = cleaned[ind+len:]

# find ONLY base android permissions using regex
perms = re.findall("android[.]permission[.][_A-Z|A-Z]+", cleaned)

# print permissions      
for perm in perms:
    print(perm)

