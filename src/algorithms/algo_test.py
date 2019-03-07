'''
Created on Mar 1, 2019

@author: Timothy
'''
from sklearn import linear_model
from read_matrix import *
from algorithms import gradient_descent
from permissions import *


def main():
    
    X, y, permission_order, apk_filename_ordinals = read_csv("../../data/dataset.csv")

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
    print("True sum: ", true_sum)
        
    print("CV Score:", LR.score(X1,y1))
    
    numCorrect = 0
    i = 0
    for x in X1:
        result = LR.predict([x])
        if y1[i] == result:
            numCorrect += 1
        
        i += 1
    print("numCorrect: ", numCorrect)

if __name__ == '__main__':
    main()