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

def logistic_regression(T, lr, X, y, adapt = False):
    return stochastic_gradient_descent(T, lr, X, y, adapt, logisitic_enable = True)

def linear_regression(T, lr, X, y, adapt = False):
    return stochastic_gradient_descent(T, lr, X, y, adapt, logisitic_enable = False)

def compute_grads(lr, w, X, y, logistic = False):
    '''
    Computes the gradients for regression.
    '''
    m = len(y)
    n = len(w)
    w_T = w.T

    f = float(lr/batch_size)

    for i in range(m):
        # Applies logistic regression if true
        if logistic == True:
            h = sigmoid(w_T.dot(X[i])) - y[i]
        else:
            h = w_T.dot(X[i]) - y[i]

        for j in range(n):
            w[j] =  w[j] - f * h * X[i][j]

    return w

def sigmoid(z):
    '''
    Returns the sigmoid of the weights vector
    '''
    return 1 / (1 + np.exp(-z))

def stochastic_gradient_descent(T, lr, X, y, adapt = False, logisitic_enable = False):
    '''
    Applies stochastic gradient descent

    Args:
        T:      The number of epochs
        lr:     Learning rate
        X:      Data
        y:      Labels for data
        adapt_learning_rate:    True - learning rate will change each epoch for faster training
        logisitic_enable:       Runs logisitic regression if true, otherwise linear regression
    Returns:
        w:  The weights vector for our regression
    '''

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
            w = compute_grads(lr, w, X_i, y_i, logisitic_enable)

        new_loss = loss(w, X, y)
        print('Epoch: {}, lr: {:.5f}, loss: {:.5f}'.format(epoch, lr, new_loss))

        if adapt == True:
            lr = adapt_learning_rate(lr, prev_loss, new_loss)

    return w

def adapt_learning_rate(lr, prev_loss, new_loss):
    '''
    Applies an adaptive learning rate -
    if loss increases from last epoch then halve learning rate
    if loss decreases from last epoch then add 5% to learning rate

    Args:
        lr:         The learning rate
        prev_loss:  The loss from previous epoch
        new_loss:   The loss from the current epoch

    Returns:
        lr: The new learning rate
    '''
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


def test_threshold(Xtest, ytest, w, threshold, sig = False):
    '''
    Returns the accuracy, precision and recall for a test set
    for a given trained dataset.

    Args:
        Xtest:  Data test matrix
        ytest:  Label test matrix
        w:      Trained dataset
        threshold: Treshold to choose predicitions
        sig:    Use sigmoid activiation function

    Returns:
        Accuracy, Precision, Recall for the dataset
    '''
    i = 0
    predictions = []
    results = []

    accuracy = 0
    precision = 0
    recall = 0

    for row in Xtest:
        predict = np.dot(np.array(row), w)
        if sig == True:
            predict = sigmoid(predict)
        if predict < threshold:
            results.append(0.0)
        else:
            results.append(1.0)
        #print("Prediction: ", predict, " Actual: ", ytest[i])
        predictions.append(predict)
        i += 1

    numCorrect = 0
    i = 0

    true_positive = 0
    false_positive = 0

    true_negative = 0
    false_negative = 0

    for res in results:
        if ytest[i] == 1.0:
            if res == 1.0:
                true_positive += 1
            if res == 0.0:
                false_positive += 1
        if ytest[i] == 0.0:
            if res == 1.0:
                true_negative += 1
            if res == 0.0:
                false_negative += 1
        if res == ytest[i]:
            numCorrect += 1
        i += 1

    accuracy = numCorrect / len(ytest)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)

    return accuracy, precision, recall


def main():
    return None


if __name__ == '__main__':
    main()
