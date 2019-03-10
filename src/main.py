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
        w = stochastic_gradient_descent(100, 0.00001, X, y)
        w = pickle.dump(w, open(GRAD_PICKLE, 'wb'))
    print(w)
    print(len(w))
    print(len(permission_order))
    print('Loss: ' + str(loss(w, X, y)))

    numCorrect = 0

    i = 0
    total_one = 0
    total_zero = 0
    z = 0
    v = 0
    for row in X:
        predict = np.dot(np.array(row), w)
        if y[i] == 1.0:
            total_one += predict
            z += 1
        else:
            total_zero += predict
            v += 1
        i += 1

    total_one = total_one/z
    total_zero = total_zero/v

    print('AVG1: {}, AVG0: {}'.format(total_one, total_zero))

    theshold = (total_one + total_zero)/2 
    vals = []
    i = 0
    for j in range(1000):
        theshold = random.uniform(-2,2)
        i = 0
        numCorrect=0
        print(j)
        sys.stdout.write('\033[F')
        for row in X1:
            predict = np.dot(np.array(row), w)
            if predict >= theshold and y1[i] == 1.0:
                numCorrect += 1
            if predict < theshold and y1[i] == 0.0:
                numCorrect += 1
        #print("Prediction: ", predict, " Actual: ", y1[i])
            i += 1
        vals.append((theshold, (numCorrect/i)*100))

    print(sorted(vals,key=lambda x: x[1], reverse=True)[0])
    print(numCorrect)
    print(i)
    print('Accuracy: {}'.format((numCorrect/i)*100))



    # Was going to use this to test making a prediction but we need to make sure the permissions are always in the same order.

    #predict with new apk
    apkFilename = "../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
    features = extractPermissionSample(apkFilename, permission_order)
    features.insert(0, 1) #add bias feature of 1 to start of features
    predict = np.dot(np.array(features), w)
    print("Predict (unknown detected apk):", predict)

    #predict with new apk
    apkFilename = "../apks/9daf1f5501260735223390a81079ce17f4023fb020e4918f4d6e2b397a69c660.apk"
    features = extractPermissionSample(apkFilename, permission_order)
    features.insert(0, 1) #add bias feature of 1 to start of features
    predict = np.dot(np.array(features), w)
    print("Predict (unknown undetected apk):", predict)

    #predict with apk already in dataset
    #apkFilename = "6c6aa1f94254e2fa7ad6e223df9ca45d870f7e7b321abec621b0fb1d05c97ae7.apk" #undetected
    #features = X[apk_filename_ordinals[apkFilename]]
    #np.insert(features,0, 1) #add bias feature of 1 to start of features
    #predict = np.dot(np.array(features), w)
    #print("Predict (known undetected apk):", predict)

    #predict with apk already in dataset
    #apkFilename = "2493996b105b30e0a803fd7ebb871813e80f89d98568a9c2b5da7de89c01d275.apk" #detected
    #features = X[apk_filename_ordinals[apkFilename]]
    #np.insert(features,0, 1) #add bias feature of 1 to start of features
    #predict = np.dot(np.array(features), w)
    #print("Predict (known detected apk):", predict)





    t2 = time.time()
    print("Time: ", round(t2-t1,3))


if __name__ == '__main__':
    main()
