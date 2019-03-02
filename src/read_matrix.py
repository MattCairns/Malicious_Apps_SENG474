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
    reader = csv.reader(f, delimiter=',')
    
    rows = 0
    columns = 0
    
    X = None
    y = []

    init = False
    i = 0
   
    for row in reader:
        print(row)
        if not init:
            if rows == 0:
                rows = int(row[0])
                continue
            if columns == 0:
                columns = int(row[0])
                continue
            X = np.zeros((rows, columns-1))
            y = np.zeros(rows)
            init = True
            continue
        X[i] = np.asarray(row[1:]).astype(np.int)
        y[i] = np.asarray(row[0]).astype(np.int)
        i += 1

    return X,y
