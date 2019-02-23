import pysftp
import permissions

SFTP_HOST = 'academic.koodous.com'
SFTP_PORT = 4445
SFTP_USER = "mrcairns"
SFTP_PASS = "geeNuph7uh2aMei"

APKS_PATH = "APKs"
DETECTED_PATH = "Detected"
UNDETECTED_PATH = "Undetected"

NUM_FILES_PARSE = 2

####################################

def getSftpFile(sftp,folder,filename):
    
    #print(sftp.pwd)
    sftp.chdir(APKS_PATH)
    sftp.chdir(folder)
    print(sftp.pwd)
    file = sftp.get(filename)

    return file

####################################

cnopts = pysftp.CnOpts()
cnopts.hostkeys=None
sftp = pysftp.Connection(SFTP_HOST, port = SFTP_PORT, username = SFTP_USER, password = SFTP_PASS,cnopts=cnopts)

filename = "00006ae4233968830098f7db6b745b106373d6d91e0021a0b660631bf4660d32.apk"
file = getSftpFile(sftp,DETECTED_PATH,filename)
perms = permissions.extractPermissions(filename)

print("apk:\t\t", filename, "\npermissions:")
for perm in perms:
    print("\t\t", perm)

