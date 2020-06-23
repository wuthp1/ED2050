import RPi.GPIO as GPIO

#--- DEFINES -----------------------------------------------------------
RELAY_DE_ENERGIZED = GPIO.HIGH
RELAY_ENERGIZED = GPIO.LOW

#input of rotary switch for automatic/manual excitation control mode choice
GPIO_EXC_CTRL = 4	
#input to read generator contactor state
GPIO_GEN_CONNECTED = 0
#input to read synchronisation contactor state
GPIO_SYNCED = 1

GPIO_RELAY_8 = 26
GPIO_RELAY_7 = 21
GPIO_RELAY_6 = 20
GPIO_RELAY_5 = 19
GPIO_RELAY_4 = 16
GPIO_RELAY_3 = 13
GPIO_RELAY_2 = 6
GPIO_RELAY_1 = 5


RELAY_SYNC = GPIO_RELAY_8
RELAY_PUMP = GPIO_RELAY_7
RELAY_LAMP = GPIO_RELAY_6


#-----------------------------------------------------------------------

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Sync normally disabled
GPIO.setup(RELAY_SYNC,GPIO.OUT, initial=RELAY_DE_ENERGIZED)

#Pump always enabled, will turn off at Reset
GPIO.setup(RELAY_PUMP,GPIO.OUT, initial=RELAY_ENERGIZED)

GPIO.setup(RELAY_LAMP,GPIO.OUT, initial=RELAY_DE_ENERGIZED)


GPIO.setup(GPIO_EXC_CTRL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_GEN_CONNECTED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_SYNCED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def enableSync():
	GPIO.output(RELAY_SYNC,RELAY_ENERGIZED)

def disableSync():
	GPIO.output(RELAY_SYNC,RELAY_DE_ENERGIZED)

def getGenState():
	return GPIO.input(GPIO_GEN_CONNECTED)

def getSyncState():
	return GPIO.input(GPIO_SYNCED)

def getExcState():
	return GPIO.input(GPIO_EXC_CTRL)

def lampOn():
	GPIO.output(RELAY_LAMP,RELAY_ENERGIZED)

def lampOff():
	GPIO.output(RELAY_LAMP,RELAY_DE_ENERGIZED)
	
def pumpOn():
	GPIO.output(RELAY_PUMP,RELAY_ENERGIZED)

def pumpOff():
	GPIO.output(RELAY_PUMP,RELAY_DE_ENERGIZED)
