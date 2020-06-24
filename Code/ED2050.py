#/usr/bin/env python
# -*- coding: utf-8 -*-

"""ED2050 main script.

Program terminates by pressing the ESCAPE-Key.
"""

#--- external modules

#the next line is only needed for python2.x and not necessary for python3.x --> Würkli? Chame doch lösche?! --> TODO
# from __future__ import print_function, division
from math import sqrt,pow
from simple_pid import PID
import pygame
import time

#--- own modules

import PM
import draw
import scope
import gpio
import dc_src_driver
#import adc_driver --> ADC hat sich in Rauch aufgelöst


#--- defines
SYNC_MAX_PHASE_DEV = 20
SYNC_MAX_VOLT_DEV = 15
SYNC_MAX_FREQ_DEV = 2

NOM_VOLT = 230
NOM_FREQ = 50

WHITE = (255, 255, 255)

NOMINAL_POWER = 2000
MAX_FREQ = 2700/30
MAX_VOLTAGE = 300

MIN_PUMP_OFF_TIME = 1

PID_KP = 0.1
PID_KI = 0.001
PID_KD = 0


scopeConnected = False
dcSrcConnected = False
ratingsExceeded = False
pumpOffTime = 0
Vexc = 10
volt = 0
excSwitchState = False

"""ED2050 main function.

Handles all the processes and connections of the ED2050 power plant model
"""
def main():
    
    PM.init()                   #initialize MODBUS connection with PowerMeter
    initDcSrc()                 #initialize USB connection with DC Source
    initScope()                 #initialize USB connection with scope and scope settings
    initExcCtrl()
    screen = initScreen()       #initialize display

    global ratingsExceeded, dcSrcConnected, scopeConnected
    
    syncOK = False              #do not allow do connect to the grid, yet
    genState = False
    
    mainloop = True
    while mainloop:
        mainloop = checkEvents()
        
        if (dcSrcConnected == False):
            initDcSrc()
        
        if (scopeConnected == False):
            initScope()
            
        if (ratingsExceeded and (time.time() - pumpOffTime) > MIN_PUMP_OFF_TIME):
            gpio.pumpOn()
            ratingsExceeded = False
        
        if(gpio.getGenState() == True) and (genState == False):
            dc_src_driver.OutputOn()
            genState = True
        elif(gpio.getGenState() == False) and (genState == True):
            dc_src_driver.OutputOff()
            genState = False
        
        checkSync()
        getData()
        checkSync()             #read data from powermeter
        drawData(screen)        #draw data on screen (chart and text)
        checkSync()
        pygame.display.flip()   #Update display.
        
        checkSync()             #check if sync possible, enable, if yes
        
    
    # exit when mainloop has been left
    gpio.lampOff()
    pygame.quit()

"""Reads Data from Powermeter.

Reads the relevant power, voltage and current data from the powermeter
via MODBUS.
"""
def getData():
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

        
    U3=PM.readReg('U3N')
    UAVG = PM.readReg('ULN_AVG')
    
    I1=PM.readReg('I1')
    I2=PM.readReg('I2')
    I3=PM.readReg('I3')
    IAVG = PM.readReg('I_AVG')
    
    checkMaximumRatings(U2,S,f)

"""Visalizes measured data an screen.

Args:
        screen (pygame.Surface): 

"""
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
    
    screen.blit(draw.write('frequency:      ' + '%7.2f' %f + ' Hz'),(10,410))
    screen.blit(draw.write('rotor speed:    ' + '%7.2f' %(f*30) + ' rpm'),(10,460))
    
    if(scopeConnected == False):
        screen.blit(draw.write('CONNECT SCOPE!!!', "FreeMonoBold",100),(10,600))
    
    if(dcSrcConnected == False):
        screen.blit(draw.write('CONNECT DC SOURCE!!!', "FreeMonoBold",100),(10,700))
    

def checkSync():
    global scopeConnected, volt
    if (scopeConnected == False):
        return False
        
    try:
        phase = float(scope.getPhase())
        freq = float(scope.getFreq())
        volt = float(scope.getVampl())
    except:
        scopeConnected = False
        return False
    
    if checkExcSwitch():
        updateExcCtrl()
    
    
    if (phase < SYNC_MAX_PHASE_DEV) and (phase > (-SYNC_MAX_PHASE_DEV)) and (volt > NOM_VOLT - SYNC_MAX_VOLT_DEV) and (volt < NOM_VOLT + SYNC_MAX_VOLT_DEV) and (freq > NOM_FREQ - SYNC_MAX_FREQ_DEV) and (freq < NOM_FREQ + SYNC_MAX_FREQ_DEV):
        gpio.enableSync()
        time.sleep(0.2)
    else:
        gpio.disableSync()
    return True


def checkEvents():
    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            return  False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def initScreen():
    global background, screensize
    screen = draw.init()
    screensize = screen.get_size()
    background = pygame.Surface(screen.get_size())
    # Fill the background white color.
    background.fill(WHITE)
    # Convert Surface object to make blitting faster.
    background = background.convert()
    return screen


def initScope():
    global scopeConnected
    if (scope.setup() == False):
        return
    scopeConnected = True
    scope.setPhaseMeas()
    scope.setFreqMeas()
    scope.setVoltMeas()


def initDcSrc():
    global dcSrcConnected
    if (dc_src_driver.init() == False):
        return
    dcSrcConnected = True


def checkMaximumRatings(U2, S, f):
    #strobo lamp must not be turned on at small voltages 
    if (U2 > 100):
        gpio.lampOn()
    else:
        gpio.lampOff()
    
    global ratingsExceeded, pumpOffTime
    if (S > NOMINAL_POWER) or (f > MAX_FREQ) or (U2 > MAX_VOLTAGE):
        gpio.pumpOff()
        ratingsExceeded = True
        pumpOffTime = time.time()


def initExcCtrl():
    global pid
    pid = PID(PID_KP, PID_KI, PID_KD, setpoint=NOM_VOLT)


def updateExcCtrl():
    global Vexc
    if dcSrcConnected == False:
        return
    Vrms = volt
    Vexc += pid(Vrms)
    if Vexc > 34:
        Vexc = 34
    
    dc_src_driver.setVoltage(Vexc)
    
def checkExcSwitch():
    if gpio.getExcState():
        return True
    else:
        return False

#main func MUST be called AFTER all function definitions
#this is a workaround, so the main code is at the beginning of the file
main()
