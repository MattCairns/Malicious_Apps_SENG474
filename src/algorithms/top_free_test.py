"""
Author:		Matthew Cairns - V00709952 & Tim Salomonsson - V00807959
Created:	26-Mar-2019 18:15:47
Filename:	top_free_test.py
Description: This uses the top 400 free apps on Google play and runs it through
            our model to find malicious apps.  We used this as discussion in our
            presentation.

"""
from os.path import dirname, join, abspath
import time, pickle, os, sys

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from algorithms.gradient_descent import randomize, linear_regression, \
    test_threshold, logistic_regression, loss
from process.dataset_builder import *
from utils.permissions import *


LOGISTIC_PICKLE = '../../data/logistic_regression_weights.p'

TOP_FREE_PICKLE = '../../data/top_free.p'
TOP_FREE_FOLDER = '../../apks/top_free/'

def main():
    # run gradient descent
    print("\n\nGradient descent for logistic regression:")
    try:
        w = pickle.load(open(LOGISTIC_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(LOGISTIC_PICKLE))
    except:
        w = logistic_regression(25, 0.05, X, y, adapt = True)
        pickle.dump(w, open(LOGISTIC_PICKLE, 'wb'))

    try:
        apk_dict = pickle.load(open(TOP_FREE_PICKLE, 'rb'))
        print('Loaded pickle: {}'.format(TOP_FREE_PICKLE))
    except:
        X, y, permission_order, apk_filename_ordinals = load_dataset_csv("../../data/dataset.csv")

        apks = os.listdir(TOP_FREE_FOLDER)
        apk_dict = {}
        for apk in apks:
            print(TOP_FREE_FOLDER + apk)
            removeBadZips(TOP_FREE_FOLDER + apk)
            features = extractPermissionSample(TOP_FREE_FOLDER + apk, permission_order)
            features.insert(0, 1) #add bias feature of 1 to start of features
            apk_dict[apk] = features
        pickle.dump(apk_dict, open(TOP_FREE_PICKLE, 'wb'))

    bad_apps = []
    for name, f in apk_dict.items():
        if w.dot(f) > 0.5:
            bad_apps.append(name)


    good_apps = apk_dict.keys()

    good_apps = list(set(good_apps) - set(bad_apps))

    for i in bad_apps:
        print(i)



if __name__ == '__main__':
    main()
