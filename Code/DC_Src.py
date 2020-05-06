#package imports
import serial

#defines

def init():
    global ser
    PORT = '/dev/ttyUSB0'    
    ser = serial.Serial(PORT)

def deInit():
    global ser
    ser.close()

def setVoltage(volts):
    global ser
    if 1 > volts > 36:
        #TODO ERROR
        return 1
    else:
        #create command string (e.g. "VOLT123" for 12.3V)
        if volts<10:
            add_str = '0'
        else:
            add_str = ''
        str_volts = "VOLT" + add_str + str(int(volts*10)) + "\r"
        #encode to "bytes" format
        ser.write(str.encode(str_volts))
        return 0

def setCurrent(amps):
    global ser
    if amps > 10:
        #TODO ERROR
        return 1
    else:
        if amps<10:
            add_str = '0'
        else:
            add_str = ''
        #create command string (e.g. "CURR025" for 2.5A) 
        str_amps = "CURR" + add_str + str(int(amps*10)) + "\r"
        #encode to "bytes" format
        ser.write(str_amps)
        return 0

def OutputOn():
    global ser
    ser.write('SOUT0\r')

def OutputOff():
    global ser
    ser.write('SOUT1\r')