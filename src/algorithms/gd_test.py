import time, pickle, os, sys

from gradient_descent import *
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from process.dataset_builder import *
from utils.permissions import *


LOGISTIC_PICKLE = '../../data/logistic_regression_weights.p'
LINEAR_PICKLE = '../../data/linear_regression_weights.p'

def test_threshold(Xtest, ytest, w, threshold, sig = False):
    print("\nModel test:")
    i = 0
    predictions = []
    results = []
    for row in Xtest:
        predict = np.dot(np.array(row), w)
        if sig == True:
            predict = sigmoid(predict)
        if predict < threshold:
            results.append(0)
        else:
            results.append(1)
        #print("Prediction: ", predict, " Actual: ", ytest[i])
        predictions.append(predict)
        i += 1

    numCorrect = 0
    i = 0
    for res in results:
        if res == ytest[i]:
            numCorrect += 1
        i += 1

    print("Threshold: ", threshold)
    print("Num Correct: ", numCorrect)
    print("Accuracy: ", numCorrect / len(ytest))

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
    print("Gradient descent for linear regression:")
    try:
        w = pickle.load(open(LINEAR_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LINEAR_PICKLE))
    except:
        w = linear_regression(4, 0.05, X, y, adapt = True)
        pickle.dump(w, open(LINEAR_PICKLE, 'wb'))

    #get random test sample
    threshold = 0.5
    for threshold in np.arange(-10, 10, 0.1):
        test_threshold(Xtest, ytest, w, threshold)

    # run gradient descent
    print("Gradient descent for logistic regression:")
    try:
        w = pickle.load(open(LOGISTIC_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LOGISTIC_PICKLE))
    except:
        w = logistic_regression(25, 0.05, X, y, adapt = True)
        pickle.dump(w, open(LOGISTIC_PICKLE, 'wb'))

    print('Loss: ' + str(loss(w, X, y)))

    #get random test sample
    test_threshold(Xtest, ytest, w, 0.5)



    t2 = time.time()
    print("Time: ", round(t2-t1,3))


if __name__ == '__main__':
    main()
