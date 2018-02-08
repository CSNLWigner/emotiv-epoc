### Emotiv signal based decoder

import numpy as np
import pickle

# CONSTANTS -- these are used to tell the EmokitController 
# how to feed data into the decoder function
WINDOW_SIZE = 20 # number of measure points fed into the decoder
WINDOW_SHIFT = 0.001 # sec (amount of shift between two windows)
CHANNELS = ['X', 'Y']

def bow_decoder(channel_data):
    if (np.mean(channel_data)>0.28):
        return(1)

def trigger (lista,kuszob):
    x=[]
    for elem in lista:
        x.append(int(elem<kuszob))
    return x

def fog(channel_data):
    osztas = int(np.size(channel_data)/2)
    i = np.mean(channel_data[:osztas])
    j = np.mean(channel_data[osztas:-1])
    if ((i < 600) and (j > 600)) or ((i > -600) and (j < -600)):
        return(1)

def fog2(channel_data):
    threshold = 0.25
    if (np.mean(channel_data[0,0:5] < 0.1)) and (np.mean(channel_data[0,5:] > 0.3)):
        return(1)
    return(0)

def szemoldok(channel_data):
    if ((np.mean(channel_data[0,:2])<-0.2) 
        and (np.mean(channel_data[0,2:] > 0.3))):
        return(1)
    else:
        return(0)

def return_mean(channel_data):
    return(int(np.mean(channel_data)>1))

def mlp_decoder(channel_data):
    return(clf.predict([np.hstack(channel_data)])[0])

def all_ones(channel_data):
    return(1)

decode = szemoldok

MLP_MODEL_FILE = 'mlp_model.pkl'
try:
    clf = pickle.load(open(MLP_MODEL_FILE,'rb'))
    decode = mlp_decoder
except:
    print('No mlp model file found.')
    print('Using alternative decoder.')

