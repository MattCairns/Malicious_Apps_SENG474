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
    
    LR = linear_model.LogisticRegressionCV()
    LR.fit(X[10:], y[10:])
    
    coeff = LR.coef_
    print(coeff)
    
    results = LR.predict(X[:10])
    
    print("CV Score:", LR.score(X[:10],y[:10]))


if __name__ == '__main__':
    main()