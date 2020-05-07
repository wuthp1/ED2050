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

WHITE = (255, 255, 255)

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

# Create empty pygame surface.
background = pygame.Surface(screen.get_size())
# Fill the background white color.
background.fill(WHITE)
# Convert Surface object to make blitting faster.
background = background.convert()



mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30


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
    PF = PM.readReg('cosphi')
    
    S1=PM.readReg('S1')*1000
    P1=PM.readReg('P1')*1000
    Q1=PM.readReg('Q1')*1000
    PF1 = PM.readReg('cosphi1')
    
    S2=PM.readReg('S2')*1000
    P2=PM.readReg('P2')*1000
    Q2=PM.readReg('Q2')*1000
    PF2 = PM.readReg('cosphi2')
    
    S3=PM.readReg('S3')*1000
    P3=PM.readReg('P3')*1000
    Q3=PM.readReg('Q3')*1000
    PF3 = PM.readReg('cosphi3')
    
    f=PM.readReg('freq')
    U1=PM.readReg('U1N')
    U2=PM.readReg('U2N')
    U3=PM.readReg('U3N')
    UAVG = PM.readReg('ULN_AVG')
    
    I1=PM.readReg('I1')
    I2=PM.readReg('I2')
    I3=PM.readReg('I3')
    IAVG = PM.readReg('I_AVG')
    
    #draw chart in the right half
    chart = draw.op_chart(screen, P/PN, Q/QN)
    
    # Copy background to screen (position (0, 0) is upper left corner).
    screen.blit(background, (0,0))
    screen.blit(chart,(screensize[0]/2,screensize[1]/2))
    x = 10
    screen.blit(draw.write('Total',"FreeMonoBold"),(x,10))
    screen.blit(draw.write('S: ' + '%7.2f' %S + '  VA'),(x,60))
    screen.blit(draw.write('P: ' + '%7.2f' %P + '  W'),(x,110))
    screen.blit(draw.write('Q: ' + '%7.2f' %Q + '  var'),(x,160))
    screen.blit(draw.write('PF: ' + '%6.2f' %PF),(x,310))
    
    x = (screensize[0] - 10)/4
    
    screen.blit(draw.write('L1',"FreeMonoBold"),(x,10))
    screen.blit(draw.write('S1:' + '%7.2f' %S1 + '  VA'),(x,60))
    screen.blit(draw.write('P1:' + '%7.2f' %P1 + '  W'),(x,110))
    screen.blit(draw.write('Q1:' + '%7.2f' %Q1 + '  var'),(x,160))
    screen.blit(draw.write('U1:' + '%7.2f' %U1 + '  V'),(x,210))
    screen.blit(draw.write('I1:' + '%7.2f' %I1 + '  A'),(x,260))
    screen.blit(draw.write('PF1: ' + '%6.2f' %PF1),(x,310))
    
    x = (screensize[0] - 10)/2
    screen.blit(draw.write('L2',"FreeMonoBold"),(x,10))
    screen.blit(draw.write('S2:' + '%7.2f' %S2 + '  VA'),(x,60))
    screen.blit(draw.write('P2:' + '%7.2f' %P2 + '  W'),(x,110))
    screen.blit(draw.write('Q2:' + '%7.2f' %Q2 + '  var'),(x,160))
    screen.blit(draw.write('U2:' + '%7.2f' %U2 + '  V'),(x,210))
    screen.blit(draw.write('I2:' + '%7.2f' %I2 + '  A'),(x,260))
    screen.blit(draw.write('PF2: ' + '%6.2f' %PF2),(x,310))
    
    x = 3*(screensize[0] - 10)/4
    screen.blit(draw.write('L3',"FreeMonoBold"),(x,10))
    screen.blit(draw.write('S3:' + '%7.2f' %S3 + '  VA'),(x,60))
    screen.blit(draw.write('P3:' + '%7.2f' %P3 + '  W'),(x,110))
    screen.blit(draw.write('Q3:' + '%7.2f' %Q3 + '  var'),(x,160))
    screen.blit(draw.write('U3:' + '%7.2f' %U3 + '  V'),(x,210))
    screen.blit(draw.write('I3:' + '%7.2f' %I3 + '  A'),(x,260))
    screen.blit(draw.write('PF3: ' + '%6.2f' %PF3),(x,310))
    
    pygame.draw.line(screen, (0,0,0), (0,385),(screensize[0],385))
    
    screen.blit(draw.write('frequency:   ' + '%7.2f' %f + ' Hz'),(10,410))
    screen.blit(draw.write('rotor speed: ' + '%7.2f' %(f*30) + ' rpm'),(10,460))
    screen.blit(draw.write('pressure:    '),(10,510))
    
    

    
    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()
