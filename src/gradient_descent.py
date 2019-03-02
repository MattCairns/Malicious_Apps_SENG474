"""
Author:		Matthew Cairns
ID:			V00709952
Created:	01-Mar-2019 10:11:14
Filename:	gradient_descent.py 
Description:  

"""
import sys, time, re
from read_matrix import *

def main():
    
    t1 = time.time()
    X, y = read_csv("../data/dataset.csv")
    print("X: ", X)
    print("y: ", y)
    t2 = time.time()
    print("Time: ", round(t2-t1,3))
    

if __name__ == '__main__':
    main()
