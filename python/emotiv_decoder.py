### Emotiv signal based decoder

import numpy as np

# CONSTANTS -- these are used to tell the EmokitController 
# how to feed data into the decoder function
WINDOW_SIZE = 5 # number of measure points fed into the decoder
WINDOW_SHIFT = 0.0010 # sec (amount of shift between two windows)
CHANNELS = ['F8', 'F7']

CHANNELS = ['Y']

def blink_decoder(channel_data):
    # channel_data: numpy.ndarray: 
    #   - columns (len(CHANNELS)): CHANNELS (in order)
    #   - rows (WINDOW_SIZE): channel values
    
    # Left blink: F8 above threshold for x amount of time and F7 not
    # Right blink: vice versa
    # Double blink: both

    # Parameters - to be learned later
    # (Can be better: first need to be below threshold, later over threshold)
    f8_threshold = 400
    f7_threshold = 300

    f8_signal_time = 0.3
    f7_signal_time = 0.3

    # Signal processing
    f8_over_threshold = np.mean(channel_data[:,1]>f8_threshold)
    f7_over_threshold = np.mean(channel_data[:,2]>f7_threshold)

    if (f8_over_threshold > f8_signal_time) and (f7_over_threshold < f7_signal_time):
        return('LEFT')
    if (f8_over_threshold < f8_signal_time) and (f7_over_threshold > f7_signal_time):
        return('RIGHT')
    if (f8_over_threshold > f8_signal_time) and (f7_over_threshold > f7_signal_time):
        return('UP')

    return(None)

def bow_decoder(channel_data):
    if (np.mean(channel_data)>28):
        return('UP')

decode = bow_decoder