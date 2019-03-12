import time

from algorithms.gradient_descent import *
from process.dataset_builder import *
from utils.permissions import *
from algorithms import gradient_descent



def test_threshold(Xtest, ytest, w, threshold):
    print("\nModel test:")
    i = 0
    predictions = []
    results = []
    for row in Xtest:
        predict = np.dot(np.array(row), w)
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
    
    X, y = gradient_descent.randomize(X, y)

    Xtest = X[:int(len(X)/2)]
    X = X[int(len(X)/2):]
    ytest = y[:int(len(y)/2)]
    y = y[int(len(y)/2):]


    # run gradient descent
    print("Gradient descent:")
    w = stochastic_gradient_descent(4, 0.0001, X, y)
    print('Loss: ' + str(loss(w, X, y)))
        
    #get random test sample
    
    threshold = 0.5
    
    for threshold in np.arange(-10, 10, 0.1):
        test_threshold(Xtest, ytest, w, threshold)
    
    
#     print("")
#     #predict with new apk
#     apkFilename = "../../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
#     features = extractPermissionSample(apkFilename, permission_order)
#     features.insert(0, 1) #add bias feature of 1 to start of features
#     predict = np.dot(np.array(features), w)
#     print("Predict (unknown detected apk):", predict)
#     
#     #predict with new apk
#     apkFilename = "../../apks/9daf1f5501260735223390a81079ce17f4023fb020e4918f4d6e2b397a69c660.apk"
#     features1 = extractPermissionSample(apkFilename, permission_order)
#     features1.insert(0, 1) #add bias feature of 1 to start of features
#     predict1 = np.dot(np.array(features1), w)
#     print("Predict (unknown undetected apk):", predict1)
#     print("")
    
    t2 = time.time()
    print("Time: ", round(t2-t1,3))
    

if __name__ == '__main__':
    main()
