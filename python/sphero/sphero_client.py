#!/usr/bin/env python
import socket
import code
import sys


class Client():
    def __init__(self, Adress=(sys.argv[1], 5000)):
        self.s = socket.socket()
        self.s.connect(Adress)


def sendcmd(command):
    c.s.send(command.encode())


c = Client()
code.interact(local=locals())

# c.s.send("print('hi')".encode())
# c.s.send("hello".encode())
# sendcmd("robot.roll(20,20)")
