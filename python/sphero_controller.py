import pygame
from pygame.locals import *

from sphero_sprk import Sphero
import time
import os

SPEED = 10
ROTATION = 30

def successful_connection_led():
    robot.set_rgb_led(200,0,0)
    for i in range(3):
        time.sleep(0.3)
        robot.set_rgb_led(0,255-100*i,0)
    print("If connection was successful, sphero should now be green")

def szinallito(robot, irany, megy):
    if (irany<=90) and (irany>=0):
        robot.set_rgb_led(int(255*(1-irany/90)), 
                          int(255*irany/90),
                          0)

    if (irany>=90) and (irany<=180):
        robot.set_rgb_led(0,
                          int(255*(1-(irany-90)/90)), 
                          int(255*(irany-90)/90))
    if (irany>=180) and (irany<=270):
        robot.set_rgb_led(int(255*(irany-180)/90),
                          int(255*(irany-180)/90), 
                          255)
    if (irany>=270) and (irany<=360):
        robot.set_rgb_led(255,
                          int(255*(1-(irany-270)/90)), 
                          int(255*(1-(irany-270)/90)))

def normalize_irany(irany):
    return(irany % 360)

if os.geteuid() == 0: # only works if run as admin
    robot = Sphero()
    robot.connect()
    successful_connection_led()
else:
    robot = Sphero("F3:8D:AC:BE:FB:83")
    robot.connect()
    successful_connection_led()

irany = 0
megy = False
pygame.init()
SCREEN = pygame.display.set_mode((600,400))
while True:
    # emotiv_controller.post_pygame_event()
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            # menjen előre
            robot.roll(SPEED,irany)
            robot.sleep(1)

        if event.type == KEYDOWN and event.key == K_LEFT:
            # forduljon balra
            irany -= ROTATION
            irany = normalize_irany(irany)
            szinallito(robot, irany, megy)
        
        if event.type == KEYDOWN and event.key == K_RIGHT:
            # forduljon jobbra
            irany += ROTATION
            irany = normalize_irany(irany)
            szinallito(robot, irany, megy)
        
