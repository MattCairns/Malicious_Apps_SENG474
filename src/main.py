import time
from read_matrix import *
from algorithms.gradient_descent import *
from permissions import *
import dataset


def main():
    
    t1 = time.time()
    
    #permission order is always same, given same set of apks
    X, y, permission_order, apk_filename_ordinals = read_csv("../data/dataset.csv")

    # Formats data for gradient descent
    X = np.c_[np.ones((X.shape[0], 1)), X]
    #print(X)

    # weights
    w = stochastic_gradient_descent(10000, 0.00001, X, y)
    print(w)
    print(len(w))
    print('Loss: ' + str(loss(w, X, y)))

    

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
    apkFilename = "6c6aa1f94254e2fa7ad6e223df9ca45d870f7e7b321abec621b0fb1d05c97ae7.apk" #undetected
    features = X[apk_filename_ordinals[apkFilename]]
    np.insert(features,0, 1) #add bias feature of 1 to start of features
    predict = np.dot(np.array(features), w)
    print("Predict (known undetected apk):", predict)
    
    #predict with apk already in dataset
    apkFilename = "2493996b105b30e0a803fd7ebb871813e80f89d98568a9c2b5da7de89c01d275.apk" #detected
    features = X[apk_filename_ordinals[apkFilename]]
    np.insert(features,0, 1) #add bias feature of 1 to start of features
    predict = np.dot(np.array(features), w)
    print("Predict (known detected apk):", predict)
    
    
    
    

    t2 = time.time()
    print("Time: ", round(t2-t1,3))
    

if __name__ == '__main__':
    main()