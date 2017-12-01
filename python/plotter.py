## plotter

from emokit_controller import EmokitController
import pygame

import numpy as np
import time

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 800
#print(pygame.font.get_default_font())
pygame.font.init()
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 25)
SPACING_Y = 0.1 # ratio of spacing to channel display
MARGIN_X  = 0.07

def plot_channel(screen, x, name, pos_y, height):
    x_min = np.min(x)
    x_max = np.max(x)
    points = []
    i = 0
    if (x_min < x_max):
        for xx in x:
            points.append( ((i/len(x)*(1-2*MARGIN_X)+MARGIN_X)*SCREEN_WIDTH, (xx-(x_min+x_max)/2)/(x_max-x_min)*height+pos_y))
            i+=1
    else:
        for xx in x:
            points.append( ((i/len(x)*(1-2*MARGIN_X)+MARGIN_X)*SCREEN_WIDTH, (xx-(x_min+x_max)/2)*height+pos_y))
            i+=1
    lineThickness = 1
    color = (230,230,230)
    screen.blit(FONT.render(name, True, (230,230,230)), (SCREEN_WIDTH*MARGIN_X/4, pos_y-height*0.2))
    pygame.draw.lines(screen, (170,170,170), False, [(SCREEN_WIDTH*MARGIN_X,pos_y),(SCREEN_WIDTH,pos_y)], 1)
    pygame.draw.lines(screen, color, False, points, lineThickness)

def plot_channels(screen, data):
    n_channel = len(data)
    i = 1
    channel_height = SCREEN_HEIGHT / (n_channel*(1+SPACING_Y)+SPACING_Y)
    for name, channel in data.items():
        try: 
            plot_channel(screen, channel, name, (i)*channel_height, channel_height/(1+SPACING_Y))
        except:
            print(name, channel)
        i += 1
    #pygame.display.update()
    pygame.display.flip()

def channel_diff(ch1,ch2):
    return([ch1[i]-ch2[i] for i in range(len(ch1))])

def emotiv_plotter():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    emokit_controller = EmokitController()
    data = dict()
    for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4 X Y'.split(' '):
        data[name] = []
    emokit_controller.establish_connection()
    t = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        new_data = emokit_controller.stream_data()
        for ch in new_data:
            if(len(data[ch])>400):
                data[ch].pop(0)
            if (new_data[ch] != []):
                data[ch].append(new_data[ch]['value'])

        channels = dict(AF3_AF4=channel_diff(data['AF3'],data['AF4']),
                        F3_F4=channel_diff(data['F3'],data['F4']))
        screen.fill((0,0,0))
        t += 1
        if (len(data['AF4'])>100) and (t % 15==0):
            plot_channels(screen, data)
        time.sleep(0.001)

def main():
    #emotiv = Emotiv(display_output=False, is_research=True)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    t=0.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        t+=0.03
        channels = dict(X_gyro = [np.sin(x/100+t) for x in range(800*4)],
                        AF4 = [np.cos(x/50+t) for x in range(400)],
                        AF3 = [np.cos(x/50+t) for x in range(400)],
                        F4 = [np.cos(x/50+t) for x in range(400)],
                        F3 = [np.cos(x/50+t) for x in range(400)])
        screen.fill((0,0,0))
        plot_channels(screen, channels)
        time.sleep(1/48)

if __name__ == '__main__':
    emotiv_plotter()
