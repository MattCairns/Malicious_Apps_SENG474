import time
from read_matrix import *
from algorithms.gradient_descent import *
from permissions import *


def main():
    
    t1 = time.time()
    X, y = read_csv("../data/dataset.csv")
    #print("X: ", X)
    #print("y: ", y)

    # Formats data for gradient descent
    X = np.c_[np.ones((X.shape[0], 1)), X]

    # weights
    w = stochastic_gradient_descent(30, 0.000001, X, y)
    print(w)
    print('Loss: ' + str(loss(w, X, y)))


    # Was going to use this to test making a predicition but we need to make sure the permissions are always in the same order.
    apkFilename = "../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
    printPermissions(apkFilename)


    t2 = time.time()
    print("Time: ", round(t2-t1,3))
    

if __name__ == '__main__':
    main()