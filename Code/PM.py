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
    'freq'    : 3110,
    }

def init():
    global pm
    pm = minimalmodbus.Instrument('/dev/serial0',1)
    pm.serial.baudrate=38400

def readReg(regName):
    return pm.read_float(regs[regName]+OFFSET)

