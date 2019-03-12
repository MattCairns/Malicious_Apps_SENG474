import time

from algorithms.gradient_descent import *
from process.dataset_builder import *
from utils.permissions import *
from algorithms import gradient_descent


def main():
    
    t1 = time.time()
    
    #permission order is always same, given same set of apks
    X, y, permission_order, apk_filename_ordinals = load_dataset_csv("../../data/dataset.csv")

    # Formats data for gradient descent
    X = np.c_[np.ones((X.shape[0], 1)), X]

    # run gradient descent
    print("Gradient descent:")
    w = stochastic_gradient_descent(5, 0.00001, X, y)
    print('Loss: ' + str(loss(w, X, y)))
        
    #get random test sample
    Xtest, ytest = gradient_descent.randomize(X, y)
    
    print("\nModel test:")
    i = 0
    for row in Xtest[:5]:
        predict = np.dot(np.array(row), w)
        print("Prediction: ", predict, " Actual: ", ytest[i])
        
        i += 1

    
    print("")
    #predict with new apk
    apkFilename = "../../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
    features = extractPermissionSample(apkFilename, permission_order)
    features.insert(0, 1) #add bias feature of 1 to start of features
    predict = np.dot(np.array(features), w)
    print("Predict (unknown detected apk):", predict)
    
    #predict with new apk
    apkFilename = "../../apks/9daf1f5501260735223390a81079ce17f4023fb020e4918f4d6e2b397a69c660.apk"
    features1 = extractPermissionSample(apkFilename, permission_order)
    features1.insert(0, 1) #add bias feature of 1 to start of features
    predict1 = np.dot(np.array(features1), w)
    print("Predict (unknown undetected apk):", predict1)
    print("")
    
    t2 = time.time()
    print("Time: ", round(t2-t1,3))
    

if __name__ == '__main__':
    main()
