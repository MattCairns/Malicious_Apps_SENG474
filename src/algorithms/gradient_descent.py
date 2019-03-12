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

    f = float(lr/batch_size)

    for i in range(m):
        h = sigmoid(w_T.dot(X[i])) - y[i]
        for j in range(n):
            w[j] =  w[j] - f * h * X[i][j]

    return w

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def stochastic_gradient_descent(T, lr, X, y):
    #generate intial set of random weights
    w = np.random.random_sample((len(X[0]),))
    X_sz = X.shape[0]

    # Randomize the our dataset
    X, y = randomize(X, y)

    prev_loss = 0

    for epoch in range(T):
        prev_loss = loss(w, X, y)
        # Ensures the data is sampled randomly on each epoch
        for i in range(0, len(y), batch_size):
            X_i = X[i : i + batch_size]
            y_i = y[i : i + batch_size]
            w = compute_grads(lr, w, X_i, y_i)

        new_loss = loss(w, X, y)
        print('Epoch: {}, lr: {:.5f}, loss: {:.5f}'.format(epoch, lr, new_loss))

        lr = adaptLearningRate(lr, prev_loss, new_loss)

    return w

def adaptLearningRate(lr, prev_loss, new_loss):
    if new_loss < prev_loss:
        return lr * 1.05
    else:
        return lr / 2.0


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
