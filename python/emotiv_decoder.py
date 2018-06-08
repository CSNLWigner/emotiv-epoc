### Emotiv signal based decoder

import numpy as np
import pickle

# CONSTANTS -- these are used to tell the EmokitController 
# how to feed data into the decoder function
window_size = 4
refraction_time = 8
WINDOW_SIZE = window_size #+refraction_time # number of measure points fed into the decoder
WINDOW_SHIFT = 0.001 # sec (amount of shift between two windows)
CHANNELS = ['T7','T8','X']

PARAMETER_NAMES = ['threshold']

szemoldok_kuszob_file = input('Szemöldök küszöb filename: ')
szemoldok_kuszob = pickle.load(open('data'+szemoldok_kuszob_file,'rb'))

try:
    parameters = np.load(open('PARAMETERS.pkl','rb'))
except:
    print('No parameters found by emotiv_decoder.py')
    print('Using default (0) parameters')
    parameters = dict()
    for parameter_name in PARAMETER_NAMES:
        parameters[parameter_name] = 0

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
    if (np.mean(channel_data)>szemoldok_kuszob):
        return(1)
    else:
        return(0)

def mlp_decoder(channel_data):
    return(clf.predict([np.hstack(channel_data)])[0])

def refraction_decoder(channel_data):
    decoded_seq = []
    for i in range(refraction_time):
        window = channel_data[:,i:i+window_size]
        decoded_seq.append(szemoldok(window))
    # Check if only the last window produces 1
    if (decoded_seq[-1] == 1): #and (sum(decoded_seq) == 1):
        return(1)
    else:
        return(0)

def multi_output_decoder(channel_data):
    # returns a refraction decoder and the last item of X channel
    return(refraction_decoder(channel_data[:-1,:]), channel_data[-1,-1])

decode = szemoldok 
decode = refraction_decoder
decode = multi_output_decoder

MLP_MODEL_FILE = 'mlp_model.pkl'
try:
    clf = pickle.load(open(MLP_MODEL_FILE,'rb'))
    decode = mlp_decoder
except:
    print('No mlp model file found.')
    print('Using alternative decoder.')

