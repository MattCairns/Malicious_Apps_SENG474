"""
Author:		Matthew Cairns
ID:			V00709952
Created:	01-Mar-2019 10:06:57
Filename:	helpers.py 
Description:  

"""
import csv
import numpy as np

def read_csv_as_matrix(file_name, as_set = True):
    """
    Read in a csv and stores labels and features

    Args:
        file_name: File to read in

    Returns:
        X: The array of features
    """
    rows = 0
    columns = 0

    X = None # Array of features

    init = False
    i = 0
    with open(file_name, encoding='utf8') as tsvin:
        reader = csv.reader(tsvin, delimiter = ',')
        for row in reader:
            if not init:
                if rows == 0:
                    rows = int(row[0])
                    continue
                if columns == 0:
                    columns = int(row[0])
                    continue
                X = np.zeros((rows, columns))
                init = True
                continue


            X[i] = np.asarray(row[1:]).astype(np.int)
            i += 1

           
    return X
