from emokit.emotiv import Emotiv
from emokit.packet import EmotivPacket

import sys
import time
import pygame

from pygame.locals import K_UP

class EmokitController:

    def __init__(self, connect_new_device = True, **kwargs):
        self.current_y = 22
        self.previous_y = 22
        self.speed_y = 22
        if connect_new_device:
            self.emotiv = Emotiv(display_output = False, is_research = True)
        if not connect_new_device:
            self.emotiv = kwargs['emotiv']

    def establish_connection(self):
        while True:
            key = self.listen()
            if key != 'UP':
                time.sleep(0.01)
            else:
                break
        print('Connection established.')

    def listen(self):
        sensor_data = self.stream_data()
        key = None
        if(sensor_data['Y'] != []):
            self.current_y = sensor_data['Y']['value']
            if ((self.current_y > 30) and (self.speed_y < self.current_y-self.previous_y)):
                key = 'UP'
            self.speed_y = self.current_y-self.previous_y
            self.previous_y = self.current_y
        return key

    def post_pygame_event(self):
        key = self.listen()
        if (key == 'UP'):
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                 {'key': K_UP, 'unicode': None}))

    def stream_data(self):
        record_sensors = dict()
        channels = 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4 X Y'.split(' ')
        for ch in channels:
            record_sensors[ch]=[]
        while (self.emotiv.running):
            try:
                packet = self.emotiv.dequeue()
                if packet is not None:
                    if type(packet) == EmotivPacket:
                        for ch in channels:
                            record_sensors[ch]=packet.sensors[ch].copy()
            except Exception as ex:
                print("EmotivRender DequeuePlotError ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],
                      " : ", ex)
            return(record_sensors)

    def print_stream_data(self):
        for record_sensors in self.stream_data():
            if (record_sensors['X'] != []):
                print(record_sensors['X']['value'])
            time.sleep(0.1)



def test_EmokitController(headset):
    controller = EmokitController(headset)
    while True:
        key = controller.listen()
        if (key == 'UP'):
            print('UP')
        time.sleep(0.01)


def main(headset):
    test_EmokitController(headset)

if __name__ == "__main__":
    with Emotiv(display_output=False, is_research=True) as headset:
        main(headset)