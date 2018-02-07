## train mlp on data

import sys
from sklearn.neural_network import MLPClassifier
import pickle
import numpy as np

CHANNELS = ['X', 'Y']
WINDOW_SIZE = 20
SHIFT = 10 ## number of datapoints between signal presentation and 

HIDDEN_LAYER_SIZES = (5, 2)

BOUNDS = pickle.load(open('CALIBRATION_BOUNDS.pkl','rb'))

def fit():
    if len(sys.argv) == 1:
        print('No data file given') 
        exit()

    if len(sys.argv) == 2:
        print('No model output filename given.')
        exit()

    file_data = sys.argv[1]
    file_model = sys.argv[2]

    data = pickle.load(open(file_data, 'rb'))
    N = len(data[CHANNELS[0]])
    X = np.zeros((len(CHANNELS),N))
    for i, ch in enumerate(CHANNELS):
        X[i,:] = data[ch]
    Y = data['input']

    i_sample = np.random.choice(np.where(Y[:-WINDOW_SIZE] == 0)[0], size = 30, replace = False)
    i_sample = np.append(i_sample, np.where(Y[:-WINDOW_SIZE] == 1)[0])

    X_sample = []
    Y_sample = []
    for i in i_sample:
        X_sample.append(np.hstack(X[:,(i+SHIFT):(i+SHIFT+WINDOW_SIZE)]))
        Y_sample.append(Y[i])

    print('Y_sample: ', Y_sample)

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=HIDDEN_LAYER_SIZES, random_state=1)
    clf.fit(X_sample, Y_sample)

    pickle.dump(clf, open(file_model, 'wb'))

if __name__ == '__main__':
    fit()

