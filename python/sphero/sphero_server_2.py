#!/usr/bin/python
from bluepy import btle
import struct
import BB8_driver
import sys
import time
import socket

class Server():
    def __init__(self,Adress=('',5000),MaxClient=1):
        self.s = socket.socket()
        self.s.bind(Adress)
        self.s.listen(MaxClient)
    def WaitForConnection(self):
        print('Waiting for connection from client...')
        self.Client, self.Adr=(self.s.accept())
        print('Got a connection from: '+str(self.Client)+'.')

print('Waiting for connection to Sphero...')
robot = BB8_driver.Sphero()
robot.connect()
robot.start()
time.sleep(2)
robot.set_rgb_led(0,255,0,0,False)
robot.set_back_led(255, False)

s = Server()
s.WaitForConnection()
print('Waiting for command... ')

#time.sleep(5)
#robot.set_back_led(0, False)
#robot.disconnect()

while 1==1:
    time.sleep(0.1)
    exec(s.Client.recv(1024).decode())

#s.Client.Close()


