'''
Created on Mar 1, 2019

@author: Timothy
'''
from sklearn import linear_model
from read_matrix import *
from algorithms import gradient_descent


def main():
    
    X, y, permission_order, apk_filename_ordinals = read_csv("../../data/dataset.csv")

    X = np.array(X)
    y = np.array(y)
    
    X,y = gradient_descent.randomize(X, y)
    
    LR = linear_model.LogisticRegression()
    LR.fit(X[10:], y[10:])
    
    coeff = LR.coef_
    print(coeff)
    
    results = LR.predict(X[:10])
    numCorrect = 0
    
    i = 0
    for result in results:
        if result == y[i]:
            numCorrect +=1
        i += 1
    
    print("Accuracy: ", numCorrect/len(results))
    #print(LR.get_params())


if __name__ == '__main__':
    main()