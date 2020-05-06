#/usr/bin/env python
# -*- coding: utf-8 -*-

"""
002_display_fps.py

Open a Pygame window and display framerate.
Program terminates by pressing the ESCAPE-Key.
 
works with python2.7 and python3.4 

URL    : http://thepythongamebook.com/en:part2:pygame:step002
Author : horst.jens@spielend-programmieren.at
License: GPL, see http://www.gnu.org/licenses/gpl.html
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import PM
import DC_Src
import draw
from math import sqrt,pow


clock = pygame.time.Clock()
#calculate nominal values
UN = 400
SN = 1500
PN = 1050
QN = sqrt(pow(SN,2)-pow(PN,2))
IN = SN/(UN*sqrt(3))

screen = draw.init()
screensize = screen.get_size()
PM.init()




mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30
# How many seconds the "game" is played.
playtime = 0.0

while mainloop:
    # Do not go faster than this framerate.
    clock.tick(1)  
    
    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    
    #get data from PM
    S=PM.readReg('Stot')*1000
    P=PM.readReg('Ptot')*1000
    Q=PM.readReg('Qtot')*1000
    
    f=PM.readReg('freq')
    U1=PM.readReg('U1N')
    U2=PM.readReg('U2N')
    U3=PM.readReg('U3N')
    
    I1=PM.readReg('I1')
    I2=PM.readReg('I2')
    I3=PM.readReg('I3')
    
    #draw chart in the right half
    chart = draw.op_chart(screen, P/PN, Q/QN)
    screen.blit(chart,(0,200))
    
    
    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()
