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
import draw
import time
import scope
import gpio
from math import sqrt,pow

#defines
SYNC_MAX_PHASE_DEV = 20
SYNC_MAX_AMPL_DEV = 15
SYNC_MAX_FREQ_DEV = 2

SYNC_NOM_AMPL = 325
SYNC_NOM_FREQ = 50

WHITE = (255, 255, 255)

NOMINAL_POWER = 2000



clock = pygame.time.Clock()
scopeConnected = False



def main():
    
    PM.init()                   #initialize MODBUS connection with PowerMeter
    initScope()                 #initialize scope connections and its settings
    screen = initScreen()       #initialize display

    
    syncOK = False              #do not allow do connect to the net, yet
    
    mainloop = True
    while mainloop:
        if (scopeConnected == False):
            initScope()
        mainloop = checkEvents()
        
    
        
        getPmData()             #read data from powermeter
        drawData(screen)        #draw data on screen (chart and text)
        pygame.display.flip()   #Update display.
        checkSync()             #check if sync possible, enable, if yes
    
    # exit when mainloop has been left
    pygame.quit()

def getPmData():
    global S,P,Q,PF
    global S1,P1,Q1,PF1
    global S2,P2,Q2,PF2
    global S3,P3,Q3,PF3
    global f,U1,U2,U3,UAVG
    global I1,I2,I3, IAVG
    
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
    
    if U2 > 100:
        gpio.lampOn
    else:
        gpio.lampOff
        
    U3=PM.readReg('U3N')
    UAVG = PM.readReg('ULN_AVG')
    
    I1=PM.readReg('I1')
    I2=PM.readReg('I2')
    I3=PM.readReg('I3')
    IAVG = PM.readReg('I_AVG')
    
def drawData(screen):
    #draw chart in the right half
    chart = draw.op_chart(screen, P/NOMINAL_POWER, Q/NOMINAL_POWER)
    
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
    
    if(scopeConnected == False):
        screen.blit(draw.write('CONNECT SCOPE!!!', "FreeMonoBold",100),(10,470)

def checkSync():
    if (scopeConnected == False):
        return False
    phase = float(scope.getPhase())
    freq = float(scope.getFreq())
    ampl = float(scope.getVampl())
    if (phase < SYNC_MAX_PHASE_DEV) and (phase > (-SYNC_MAX_PHASE_DEV)) and (ampl > SYNC_NOM_AMPL - SYNC_MAX_AMPL_DEV) and (ampl < SYNC_NOM_AMPL + SYNC_MAX_AMPL_DEV) and (freq > SYNC_NOM_FREQ - SYNC_MAX_FREQ_DEV) and (freq < SYNC_NOM_FREQ + SYNC_MAX_FREQ_DEV):
        gpio.enableSync()
        time.sleep(1)
    else:
        gpio.disableSync()
    return True
    
def checkEvents():
    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False

def initScreen():
    screen = draw.init()
    screensize = screen.get_size()
    background = pygame.Surface(screen.get_size())
    # Fill the background white color.
    background.fill(WHITE)
    # Convert Surface object to make blitting faster.
    background = background.convert()
    return screen

def initScope():
    if (scope.setup() == False):
        return
    scopeConnected = True
    scope.setPhaseMeas()
    scope.setFreqMeas()
    scope.setVoltMeas()

#main func MUST be called AFTER all fuction definitions
#this is a workaround, so the main code is at the beginning of the file
main()
