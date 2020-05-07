"""Provides API to communicate with powermeter PM3250.

This package is used to set up the connection to Schneider Electric
PM3250 and to read the most important register values
"""
import minimalmodbus

#Depending on MODBUS Master Device, there can be an address offset.
OFFSET = -1

#Dictionnary for register addresses of powermeter PM3250
regs = {
    'I1'      : 3000,
    'I2'      : 3002,
    'I3'      : 3004,
    'IN'      : 3006,
    'I_AVG'   : 3010,
    'U12'     : 3020,
    'U23'     : 3022,
    'U31'     : 3024,
    'ULL_AVG' : 3026,
    'U1N'     : 3028,
    'U2N'     : 3030,
    'U3N'     : 3032,
    'ULN_AVG' : 3036,
    'P1'      : 3054,
    'P2'      : 3056,
    'P3'      : 3058,
    'Ptot'    : 3060,
    'Q1'      : 3062,
    'Q2'      : 3064,
    'Q3'      : 3066,
    'Qtot'    : 3068,
    'S1'      : 3070,
    'S2'      : 3072,
    'S3'      : 3074,
    'Stot'    : 3076,
    'cosphi1' : 3078,
    'cosphi2' : 3080,
    'cosphi3' : 3082,
    'cosphi'  : 3084,
    'freq'    : 3110,
    }

def init(port='/dev/serial0', addr=1, baudrate=38400):
    """opens connection to powermeter.
    
    
    """
    global pm
    pm = minimalmodbus.Instrument(port,addr)
    pm.serial.baudrate=baudrate

def readReg(regName):
    return pm.read_float(regs[regName]+OFFSET)

