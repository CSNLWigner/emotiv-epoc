### Emotiv signal based decoder

import numpy as np

# CONSTANTS -- these are used to tell the EmokitController 
# how to feed data into the decoder function
WINDOW_SIZE = 5 # number of measure points fed into the decoder
WINDOW_SHIFT = 0.0010 # sec (amount of shift between two windows)
CHANNELS = ['Y']

def bow_decoder(channel_data):
    if (np.mean(channel_data)>28):
        return(1)

decode = bow_decoder