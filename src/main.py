import time, pickle, random, sys
from read_matrix import *
from algorithms.gradient_descent import *
from permissions import *
import dataset
GRAD_PICKLE = '../data/gradient_descent_weights.p'

def main():

    t1 = time.time()

    #permission order is always same, given same set of apks
    X, y, permission_order, apk_filename_ordinals = read_csv("../data/dataset.csv")

    X,y = randomize(X, y)
    # Formats data for gradient descent
    X = np.c_[np.ones((X.shape[0], 1)), X]
    #print(X)
    X1 = X[:int(len(X)/2)]
    X = X[int(len(X)/2):]
    y1 = y[:int(len(y)/2)]
    y = y[int(len(y)/2):]

    w = None
    # weights
    try:
        w = pickle.load(open(GRAD_PICKLE, 'rb'))
        print('Loaded gradient descent model from pickle')
    except:
        w = stochastic_gradient_descent(500, 0.05, X, y)
        w = pickle.dump(w, open(GRAD_PICKLE, 'wb'))

    print('Loss: ' + str(loss(w, X, y)))

    theshold = 0.5
    i = 0
    numCorrect=0
    for row in X1:
        predict = sigmoid(np.dot(np.array(row), w))
        if predict >= theshold and y1[i] == 1.0:
            numCorrect += 1
        if predict < theshold and y1[i] == 0.0:
            numCorrect += 1
        i += 1

    print((numCorrect/i)*100)

    # Was going to use this to test making a prediction but we need to make sure the permissions are always in the same order.

    #predict with new apk
    apkFilename = "../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
    features = extractPermissionSample(apkFilename, permission_order)
    features.insert(0, 1) #add bias feature of 1 to start of features
    predict = sigmoid(np.dot(np.array(features), w))
    print("Predict (unknown detected apk):", predict)

    #predict with new apk
    apkFilename = "../apks/9daf1f5501260735223390a81079ce17f4023fb020e4918f4d6e2b397a69c660.apk"
    features = extractPermissionSample(apkFilename, permission_order)
    features.insert(0, 1) #add bias feature of 1 to start of features
    predict = sigmoid(np.dot(np.array(features), w))
    print("Predict (unknown undetected apk):", predict)


    t2 = time.time()
    print("Time: ", round(t2-t1,3))


if __name__ == '__main__':
    main()
