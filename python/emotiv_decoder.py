### Emotiv signal based decoder

import numpy as np

# CONSTANTS -- these are used to tell the EmokitController 
# how to feed data into the decoder function
WINDOW_SIZE = 1 # number of measure points fed into the decoder
WINDOW_SHIFT = 0.0010 # sec (amount of shift between two windows)
CHANNELS = ['T7']

def bow_decoder(channel_data):
    if (np.mean(channel_data)>28):
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

def return_mean(channel_data):
    return(np.mean(channel_data))

decode = return_mean
