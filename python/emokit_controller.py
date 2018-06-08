from emokit.emotiv import Emotiv
from emokit.packet import EmotivPacket

import sys
import time
import pygame
import pickle
import emotiv_decoder
import numpy as np
from pygame.locals import K_UP, K_LEFT, K_DOWN, K_RIGHT

CHANNELS = 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4 X Y'.split(' ')

class EmokitController:

    def __init__(self, connect_new_device = True, cache=True, cache_length=200, is_research = True, **kwargs):
        self.current_y = 22
        self.previous_y = 22
        self.speed_y = 22
        self.cache = cache
        self.t_last_window=time.time()
        self.t = []
        if self.cache:
            self.cache_data = dict()
            self.cache_decoder = []
            for ch in CHANNELS:
                self.cache_data[ch]=[0]
            self.cache_length = cache_length
        if connect_new_device:
            self.emotiv = Emotiv(display_output = False, is_research = is_research)
        else:
            self.emotiv = kwargs['emotiv']
        self.load_calibration()

    def load_calibration(self):
        self.calibrated = False
        try: 
            self.bounds = pickle.load(open('CALIBRATION_BOUNDS.pkl','rb'))
            self.calibrated = True
        except:
            print('No calibration profile found (CALIBRATION_BOUNDS.pkl)')

    def establish_connection(self):
        while True:
            self.stream_data()
            key = self.decode()
            if key != 1:
                time.sleep(0.01)
            else:
                break
        print('Connection established.')

    def decode(self):
        data = np.array([self.cache_data[ch][-emotiv_decoder.WINDOW_SIZE:] for ch in emotiv_decoder.CHANNELS], dtype = 'float')
        if (np.size(data,1) == emotiv_decoder.WINDOW_SIZE):
            if self.calibrated:
                for i, ch in enumerate(emotiv_decoder.CHANNELS):
                    data[i,:] = (data[i,:]-(self.bounds['max'][ch]+self.bounds['min'][ch])/2) / (self.bounds['max'][ch]-self.bounds['min'][ch])
            key = emotiv_decoder.decode(data)
            #print(self.cache_data)
            if(len(self.cache_decoder)>=self.cache_length):
                self.cache_decoder.pop(0)
            self.cache_decoder.append(key)
            return(key)
        else:
            return(0)

    def post_pygame_event(self):
        self.stream_data()
        if (time.time()-self.t_last_window)>=emotiv_decoder.WINDOW_SHIFT:
            key = self.decode()
            self.t_last_window = time.time()
            if (key == 1):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                     {'key': K_UP, 'unicode': None}))
            elif (key == 2):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                     {'key': K_DOWN, 'unicode': None}))
            elif (key == 3):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                     {'key': K_LEFT, 'unicode': None}))
            elif (key == 4):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                     {'key': K_RIGHT, 'unicode': None}))
            else:
                self.cache_decoder.append(0)
        else:
            self.cache_decoder.append(0)

    def get_cache_data(self):
        return(self.cache_data)

    def get_cache_decoder(self):
        return(self.cache_decoder)

    def get_cache_decoder_last(self):
        return(self.cache_decoder[-1])

    def stream_data(self):
        record_sensors = dict()
        
        for ch in CHANNELS:
            record_sensors[ch]=[]
        while (self.emotiv.running):
            try:
                packet = self.emotiv.dequeue()
                if packet is not None:
                    if type(packet) == EmotivPacket:
                        for ch in CHANNELS:
                            record_sensors[ch]=packet.sensors[ch].copy()
            except Exception as ex:
                print("EmotivRender DequeuePlotError ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],
                      " : ", ex)
            if self.cache:
                for ch in CHANNELS:
                    if (len(self.cache_data[ch])>=self.cache_length):
                        self.cache_data[ch].pop(0)
                    if (record_sensors[ch] != []):
                        self.cache_data[ch].append(record_sensors[ch]['value'])
                    else: 
                        # Not correctly controlling for shifting series for lost packet
                        self.cache_data[ch].append(self.cache_data[ch][-1])
                if(len(self.t)>self.cache_length):
                    self.t.pop(0)
                self.t.append(time.time())

            return(record_sensors)

    def record_session(self, t, name=None):
        self.establish_connection()
        data = dict()
        for ch in CHANNELS:
            data[ch]=[]
        for i in range(t):
            data_point = self.stream_data().copy()
            for ch in CHANNELS:
                if(data_point[ch] != []):
                    data[ch].append(data_point[ch]['value'])
            time.sleep(0.01)

        if (name is not None):
            import pickle
            pickle.dump(data,open(name,'wb'))
        else:
            return(data)



def test_EmokitController(headset):
    controller = EmokitController(headset)
    while True:
        key = controller.decode()
        if (key == 'UP'):
            print('UP')
        time.sleep(0.01)

def main(headset):
    test_EmokitController(headset)

if __name__ == "__main__":
    with Emotiv(display_output=False, is_research=True) as headset:
        main(headset)