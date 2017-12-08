## plotter

from emokit_controller import EmokitController, CHANNELS
import pygame

import numpy as np
import time
import pickle

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
    for name, channel in sorted(data.items()):
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
    recording = False
    data = dict()
    for ch in CHANNELS:
        data[ch]=[]
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    emokit_controller = EmokitController(cache=True, cache_length=400)
    #emokit_controller.establish_connection()
    decoder_cache=[0 for i in range(400)]
    t = 0
    data_t = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (recording):
                    filename=input('Filename: ')
                    pickle.dump(data,open(filename,'wb'))
                    for ch in CHANNELS:
                        data[ch]=[]
                if not recording:
                    data_t = 0
                recording = not recording

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        new_data = emokit_controller.post_pygame_event()
        plot_data = emokit_controller.get_cache_data()
        #plot_data['decoder'] = emokit_controller.get_cache_decoder()
        screen.fill((0,0,0))
        if recording:
            data_t += 1
            screen.blit(FONT.render(str(data_t), True, (230,230,230)), (SCREEN_WIDTH*(1-MARGIN_X*0.9), 50))
            for ch in CHANNELS:
            	data[ch].append(plot_data[ch][-1])
            pygame.draw.rect(screen,(250,0,0),(SCREEN_WIDTH*(1-MARGIN_X/4*3),5,20,20))

        t += 1
        if (len(plot_data['AF4'])>100) and (t % 15==0):
            plot_channels(screen, plot_data)
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
