"""
Author:		Matthew Cairns & Tim Salomonsson
Created:	12-Mar-2019 09:40:11
Filename:	gd_test.py 
Description:    Testing for the gradient descent algo
"""
from os.path import dirname, join, abspath
import time, pickle, os, sys

from algorithms.gradient_descent import randomize, linear_regression, \
    test_threshold, logistic_regression, loss
from process.dataset_builder import *
from utils.permissions import *
from process.kaggle import normalize_kaggle


sys.path.insert(0, abspath(join(dirname(__file__), '..')))


LOGISTIC_PICKLE = '../../data/logistic_regression_weights.p'
LINEAR_PICKLE = '../../data/linear_regression_weights.p'

def main():

    t1 = time.time()

    #permission order is always same, given same set of apks
    X, y, permission_order, apk_filename_ordinals = load_dataset_csv("../../data/dataset.csv")


    Xkaggle, ykaggle = normalize_kaggle(permission_order)
    Xkaggle = np.c_[np.ones((Xkaggle.shape[0], 1)), Xkaggle]


    # Formats data for gradient descent
    X = np.c_[np.ones((X.shape[0], 1)), X]

    X, y = randomize(X, y)

    Xtest = X[:int(len(X)/2)]
    X = X[int(len(X)/2):]
    ytest = y[:int(len(y)/2)]
    y = y[int(len(y)/2):]


    # run gradient descent
    w = None
    print("\n\nGradient descent for linear regression:")
    try:
        w = pickle.load(open(LINEAR_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LINEAR_PICKLE))
    except:
        w = linear_regression(10, 0.001, X, y, adapt = True)
        pickle.dump(w, open(LINEAR_PICKLE, 'wb'))


    #get random test sample
    threshold = 0.5
    numCorrect, accuracy, precision, recall, f_score = test_threshold(Xtest, ytest, w, threshold)

    print('Accuracy: {:3f}, Precision: {:3f}, Recall: {:3f}'.format(accuracy, precision, recall))

    # run gradient descent
    w = None
    print("\n\nGradient descent for linear regression (kaggle dataset):")
    try:
        w = pickle.load(open(LINEAR_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LINEAR_PICKLE))
    except:
        w = linear_regression(10, 0.001, Xkaggle, ykaggle, adapt = True)
        pickle.dump(w, open(LINEAR_PICKLE, 'wb'))


    #get random test sample
    threshold = 0.5
    numCorrect, accuracy, precision, recall, f_score = test_threshold(Xkaggle, ykaggle, w, threshold)

    print('Accuracy: {:3f}, Precision: {:3f}, Recall: {:3f}'.format(accuracy, precision, recall))



    # run gradient descent
    print("\n\nGradient descent for logistic regression:")
    try:
        w = pickle.load(open(LOGISTIC_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LOGISTIC_PICKLE))
    except:
        w = logistic_regression(25, 0.05, X, y, adapt = True)
        pickle.dump(w, open(LOGISTIC_PICKLE, 'wb'))

    print('Loss: ' + str(loss(w, X, y)))

    #get random test sample
    numCorrect, accuracy, precision, recall, f_score = test_threshold(Xtest, ytest, w, threshold, sig = True)
    print('Accuracy: {:3f}, Precision: {:3f}, Recall: {:3f}, F Score: {:3f}'.format(accuracy, precision, recall, f_score))


    
    # run gradient descent
    print("\n\nGradient descent for logistic regression (kaggle dataset):")
    try:
        w = pickle.load(open(LOGISTIC_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LOGISTIC_PICKLE))
    except:
        w = logistic_regression(25, 0.05, Xkaggle, ykaggle, adapt = True)
        pickle.dump(w, open(LOGISTIC_PICKLE, 'wb'))

    print('Loss: ' + str(loss(w, Xkaggle, ykaggle)))

    #get random test sample
    numCorrect, accuracy, precision, recall, f_score = test_threshold(Xkaggle, ykaggle, w, threshold, sig = True)
    print('Accuracy: {:3f}, Precision: {:3f}, Recall: {:3f}, F Score: {:3f}'.format(accuracy, precision, recall, f_score))



    t2 = time.time()
    print("Time: ", round(t2-t1,3))


if __name__ == '__main__':
    main()
