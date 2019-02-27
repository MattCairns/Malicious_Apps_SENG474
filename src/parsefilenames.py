import csv

DET = "../data/detected.labels.csv"
UNDET = "../data/undetected.csv"
D_FILES = []
UND_FILES = []

def parse_filenames():
    with open(DET) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            D_FILES.append(row[0] + ".apk")
    
    with open(UNDET) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            UND_FILES.append(row[0] + ".apk")
            
    csvfile.close()
    
def get_undetected_filenames():
    return UND_FILES

def get_detected_filenames():
    return D_FILES
    
def main():
    parse_filenames()
    print("  # detected files: ", len(D_FILES))
    print("           example: ", D_FILES[0])
    print("# undetected files: ", len(UND_FILES))
    print("           example: ", UND_FILES[0])
    
if __name__ == "__main__": main()
