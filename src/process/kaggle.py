import csv
import numpy as np
from utils.permissions import cleanPermissions


def load_kaggle():
    f = open("../../data/kaggle.csv", 'r')
    
    print("Load kaggle dataset.")
    
    perms = next(f).rstrip().split(",") #remove type header
    clean_perms = cleanPermissions(perms)

    
    #for perm in perms:
        #print(perm)
    
    reader = csv.reader(f, delimiter=',')
    
    matrix = [[int(perm) for perm in row] for row in reader]
    
    #print(matrix)
    
    clean = []
    for name in perms:
        if cleanPermissions([name]) != []:
            clean.append(1)
        else:
            clean.append(0)


    #print("len clean: ", len(clean))
    #print("len perms: ", len(perms))

    
    clean_matrix = [[row[x] for x in range(len(row)) if clean[x] == 1 or perms[x] == 'type'] for row in matrix]
    
    
    
    return clean_perms, clean_matrix


def normalize_kaggle(permissions):

    clean_perms, clean_matrix = load_kaggle()
    
    #print(len(clean_perms))
    #print(len(clean_matrix[0]))
    
    ordinal = {}
    i =0
    for perm in clean_perms:
        ordinal[perm] = i
        i += 1
    
    rows = len(clean_matrix)
    columns = len(permissions)
    
    X = np.zeros((rows, columns), dtype=np.int8)
    y = np.zeros(rows)

    for i in range(rows):
        y[i] = clean_matrix[i][-1]
        j =0
        
        for perm in permissions:
            
            if perm in clean_perms:
                X[i][j] = clean_matrix[i][ordinal[perm]]
            else:
                X[i][j] = 0
            j += 1
    
    return X, y
