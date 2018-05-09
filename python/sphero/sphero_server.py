#!/usr/bin/env python
from sphero_sprk import Sphero
import time
import socket


def successful_connection_led():
    robot.set_rgb_led(200, 0, 0)
    for i in range(3):
        time.sleep(0.3)
        robot.set_rgb_led(0,255-100*i,0)
    print("If connection was successful, sphero should now be green")


print('Waiting for connection to Sphero...')
robot = Sphero("F3:8D:AC:BE:FB:83")
robot.connect()
successful_connection_led()


class Server():
    def __init__(self,Adress=('',5000),MaxClient=1):
        self.s = socket.socket()
        self.s.bind(Adress)
        self.s.listen(MaxClient)
    def WaitForConnection(self):
        print('Waiting for connection from client...')
        self.Client, self.Adr=(self.s.accept())
        print('Got a connection from: '+str(self.Client)+'.')


s = Server()
s.WaitForConnection()
print('Waiting for command... ')

while 1==1:
    time.sleep(1)
    exec(s.Client.recv(1024).decode())

#s.Client.Close()