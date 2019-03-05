import csv
import numpy as np

# array shapes in common libraries (sci-kit learn, etc, ...) 
#    features (X):     is a matrix of shape (n_samples, n_features)
#      labels (Y):     is a matrix of shape (n_samples, 1)


def read_csv(file_name):
    """
    Read in a csv and store labels and features

    Args:
        file_name: File to read in

    Returns:
        X: The array of features
        y: the array of labels
    """
    
    f = open(file_name, encoding='utf-8')
    info = [next(f) for i in range(3)]
    rows = int(info[0])
    columns = int(info[1])
    headings = info[2].split(',')[2:]  #remove file and type headings
    #print("R:", rows)
    #print("C:", columns)
    print(headings)
    #print(len(headings))

    reader = csv.reader(f, delimiter=',')
    
    X = np.zeros((rows, columns-2))
    y = np.zeros(rows)
    
    apk_filename_ordinals = {}

    i=0
    for row in reader:
        #print("dataset: ", row)
        apk_filename_ordinals[row[0]] = i
        X[i] = np.asarray(row[2:]).astype(np.int)
        y[i] = np.asarray(row[1]).astype(np.int)
        i += 1

    return X,y,headings,apk_filename_ordinals
