"""
Author:		Matthew Cairns & Tim Salomonsson
Created:	12-Mar-2019 09:40:11
Filename:	gd_test.py 
Description:    Testing for the gradient descent algo
"""
import time, pickle, os, sys

from gradient_descent import *
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from process.dataset_builder import *
from utils.permissions import *


LOGISTIC_PICKLE = '../../data/logistic_regression_weights.p'
LINEAR_PICKLE = '../../data/linear_regression_weights.p'

def test_threshold(Xtest, ytest, w, threshold, sig = False):
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

    t1 = time.time()

    #permission order is always same, given same set of apks
    X, y, permission_order, apk_filename_ordinals = load_dataset_csv("../../data/dataset.csv")

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
    result_list = []
    for threshold in np.arange(-10, 10, 0.1):
        accuracy, precision, recall = test_threshold(Xtest, ytest, w, threshold)
        result_list.append((threshold, accuracy, precision, recall))

    threshold, accuracy, precision, recall = max(result_list, key=lambda item:item[1])
    print('With theshold: {}'.format(threshold))
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
    accuracy, precision, recall = test_threshold(Xtest, ytest, w, 0.5, sig = True)
    print('Accuracy: {:3f}, Precision: {:3f}, Recall: {:3f}'.format(accuracy, precision, recall))



    t2 = time.time()
    print("Time: ", round(t2-t1,3))


if __name__ == '__main__':
    main()
