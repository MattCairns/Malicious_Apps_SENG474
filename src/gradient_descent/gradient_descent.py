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
    start = time.time()
    X = read_csv_as_matrix("../../data/dataset.csv")

    print(time.time() - start)
if __name__ == '__main__':
    main()
