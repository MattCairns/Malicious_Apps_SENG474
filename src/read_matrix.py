import csv, sys, pickle, re
import numpy as np

# array shapes in common libraries (sci-kit learn, etc, ...) 
#    features (X):     is a matrix of shape (n_samples, n_features)
#      labels (Y):     is a matrix of shape (n_samples, 1)


def read_csv(file_name):
    """
    Read in a csv and store labels and features

    Args:
        file_name: File to read in

    Returns:
        X: The array of features
        y: the array of labels
    """
    Xy_pickle = re.search('(.*)\.csv', file_name).group(1) + '.p'
    print(Xy_pickle)
    try:
        X, y, headings, apk_filename_ordinals = pickle.load(open(Xy_pickle, 'rb'))
        print('Loaded pickled data: {}'.format(Xy_pickle))
        return X, y, headings, apk_filename_ordinals
    except(OSError, IOError) as e:
        print('Could not load pickle {}, building from {}'.format(Xy_pickle, file_name))

    
    f = open(file_name, encoding='utf-8')
    info = [next(f) for i in range(3)]
    rows = int(info[0])
    columns = int(info[1])
    headings = info[2].split(',')[2:]  #remove file and type headings
    print("R:", rows)
    print("C:", columns)
    #print(headings)
    #print(len(headings))

    reader = csv.reader(f, delimiter=',')
    
    X = np.zeros((rows, columns-2), dtype=np.int8)
    y = np.zeros(rows)
    
    apk_filename_ordinals = {}

    i=0
    for row in reader:
        print("build X,y: %d of %d, %.2f" % (i, rows, 100 * (i/rows)))
        sys.stdout.write('\033[F')
        apk_filename_ordinals[row[0]] = i
        X[i] = np.asarray(row[2:-1])
        #print(X[i])
        y[i] = np.asarray(row[1])
        #print(y[i])
        i += 1

    pickle.dump((X, y, headings, apk_filename_ordinals), open(Xy_pickle, 'wb'))

    return X,y,headings,apk_filename_ordinals
