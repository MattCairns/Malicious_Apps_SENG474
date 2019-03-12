
from sklearn import linear_model
import gradient_descent

import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from utils.permissions import *
from process.dataset_builder import *

def main():
    
    X, y, permission_order, apk_filename_ordinals = load_dataset_csv("../../data/dataset.csv")

    X = np.array(X)
    y = np.array(y)
    X = np.c_[np.ones((X.shape[0], 1)), X]

    
    X,y = gradient_descent.randomize(X, y)
    X1 = X[:int(len(X)/2)]
    X = X[int(len(X)/2):]
    y1 = y[:int(len(y)/2)]
    y = y[int(len(y)/2):]
    
    LR = linear_model.LogisticRegression()
    #LR = linear_model.SGDClassifier(loss='log')
    LR.fit(X, y)
    
    coeff = LR.coef_
    #print(coeff)
    w = coeff[0]
    print(len(coeff[0]))
    print(len(permission_order))

    results = LR.predict(X1)
    #print(results)
    import sklearn.metrics
    
    precision, recall, fscore, true_sum = sklearn.metrics.precision_recall_fscore_support(y1,results)
    
    print("Precision:", precision)
    print("Recall:", recall)
    print("F-score:", fscore)
    print("Support: ", true_sum)
        
    print("CV Score:", LR.score(X1,y1))
    
    numCorrect = 0
    i = 0
    for x in X1:
        result = LR.predict([x])
        if y1[i] == result:
            numCorrect += 1
        
        i += 1
    print("numCorrect: ", numCorrect)
    
    print("")
    #predict with new apk
    apkFilename = "../../apks/fffe457162a14a5f6289ee3803129202045314684349df91bc736e19abd5c544.apk"
    features = extractPermissionSample(apkFilename, permission_order)
    features.insert(0, 1) #add bias feature of 1 to start of features
    #print(features)
    result = LR.predict([features])
    print("Predict (unknown detected apk):", result)
    
    #predict with new apk
    apkFilename1 = "../../apks/9daf1f5501260735223390a81079ce17f4023fb020e4918f4d6e2b397a69c660.apk"
    features1 = extractPermissionSample(apkFilename1, permission_order)
    features1.insert(0, 1) #add bias feature of 1 to start of features
    #predict1 = np.dot(np.array(features1), w)
    #print(features1)
    #print(features == features1)
    result1 = LR.predict([features1])

    print("Predict (unknown undetected apk):", result1)
    print("")

if __name__ == '__main__':
    main()
