"""
Author:     Matthew Cairns
ID:         V00709952
Created:    01-Mar-2019 10:11:14
Filename:   gradient_descent.py 
Description:  

"""
import sys, time, re
from random import randint
import numpy as np

#constants
batch_size = 1

def compute_grads(lr, w, X, y):
    m = len(y)
    n = len(w)
    w_T = w.T

    for i in range(m):
        h = (w_T.dot(X[i]) - y[i])
        for j in range(n):
            w[j] =  w[j] - float(lr/batch_size) * h * X[i][j]

    return w

def stochastic_gradient_descent(T, lr, X, y):
    #generate intial set of random weights
    w = np.random.random_sample((len(X[0]),))
    X_sz = X.shape[0]

    # Randomize the our dataset
    X, y = randomize(X, y)
    for i in range(T):
        # Ensures the data is sampled randomly on each epoch
        print("Epoch " + str(i) + ", loss: " + str(loss(w, X, y)))

        for i in range(0, len(y), batch_size):
            X_i = X[i : i + batch_size]
            y_i = y[i : i + batch_size]
            w = compute_grads(lr, w, X_i, y_i)

    return w


def randomize(X, y):
    # Randomly sorts X, y the same way.
    perm = np.random.permutation(X.shape[0])
    return X[perm], y[perm]



def loss(w, X, y):
    """
    Calculates the loss 
    Args:
        w: NP Array of coefficients
        X: NP Array of data points
        y: NP Array of labels
    Returns:
        The loss of the linear regression
    """
    n = X.shape[0]
    l = 0
    for i in range(0, n):
        l += np.power(y[i] - w.T.dot(X[i]), 2)
    return (1/(2 * n)) * l


def main():
    return None


if __name__ == '__main__':
    main()
