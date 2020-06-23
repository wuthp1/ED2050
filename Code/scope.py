#--- MODULES -----------------------------------------------------------

import scope_driver

#--- DEFINES -----------------------------------------------------------

CH_BANDW_TWENTY = 'TWE'
CH_BANDW_FULL =   'FUL'

CH_COUPLING_AC =  'AC'
CH_COUPLING_DC =  'DC'
CH_COUPLING_GND = 'GND'

MEAS_SLOT_PHASE = 1
MEAS_SLOT_FREQ =  2
MEAS_SLOT_VAMP =  3
MEAS_SLOT_D =     4

MEAS_TYPE_PHASE = 'PHA'
MEAS_TYPE_FREQ =  'FREQ'
MEAS_TYPE_VRMS =  'RMS'
MEAS_TYPE_AMPL =  'AMP'

MEAS_STATE_ON =   'ON'
MEAS_STATE_OFF =  'OFF'

#--- SETTINGS ----------------------------------------------------------

#Probe attenuations
PROBE_ATT_GEN =   200
PROBE_ATT_NET =   200
PROBE_GAIN_GEN =  str(1.0/PROBE_ATT_GEN)
PROBE_GAIN_NET =  str(1.0/PROBE_ATT_NET)

#Scope channels for generator and net measurement
INT_CH_GEN = 	  1
INT_CH_NET = 	  2
STR_CH_GEN = 	  'CH%d' %INT_CH_GEN
STR_CH_NET =      'CH%d' %INT_CH_NET

#scale settings
CH_GEN_VER_SCA = '100'		#V/div, must be a string
CH_NET_VER_SCA = '100'		#V/div, must be a string
HOR_SCALE      = '4E-3' 	#s/div, must be a string

#waveform vertical position settings
CH_GEN_VER_POS = 0		#divisions, must be a number (not a string)
CH_NET_VER_POS = 0		#divisions, must be a number (not a string)


#--- FUNCTIONS ---------------------------------------------------------

def setup():
	if (scope_driver.init() == False):
		return False
	#scope_driver.lockFrontPanel()
	scope_driver.setChannelBandwidth(INT_CH_GEN, CH_BANDW_FULL)
	scope_driver.setChannelBandwidth(INT_CH_NET, CH_BANDW_FULL)
	scope_driver.setChannelCoupling(INT_CH_GEN, CH_COUPLING_DC)
	scope_driver.setChannelCoupling(INT_CH_NET, CH_COUPLING_DC)
	scope_driver.setChannelVertPos(INT_CH_GEN, CH_GEN_VER_POS)
	scope_driver.setChannelVertPos(INT_CH_NET, CH_NET_VER_POS)
	scope_driver.setProbeGain(INT_CH_GEN, PROBE_GAIN_GEN)
	scope_driver.setProbeGain(INT_CH_NET, PROBE_GAIN_NET)
	scope_driver.setChannelVertScale(INT_CH_GEN, CH_GEN_VER_SCA)
	scope_driver.setChannelVertScale(INT_CH_NET, CH_NET_VER_SCA)
	scope_driver.setHorScale(HOR_SCALE)
	scope_driver.turnOnChDisp(INT_CH_GEN)
	scope_driver.turnOnChDisp(INT_CH_NET)
	return True
	
def setPhaseMeas():
	scope_driver.setMeasSrc1(STR_CH_GEN, MEAS_SLOT_PHASE)
	scope_driver.setMeasSrc2(STR_CH_NET, MEAS_SLOT_PHASE)
	scope_driver.setMeasType(MEAS_TYPE_PHASE, MEAS_SLOT_PHASE)
	scope_driver.setMeasState(MEAS_STATE_ON, MEAS_SLOT_PHASE)
	
def stopPhaseMeas():
	scope_driver.setMeasState(MEAS_STATE_OFF, MEAS_SLOT_PHASE)

def setFreqMeas():
	scope_driver.setMeasSrc1(STR_CH_GEN, MEAS_SLOT_FREQ)
	scope_driver.setMeasType(MEAS_TYPE_FREQ, MEAS_SLOT_FREQ)
	scope_driver.setMeasState(MEAS_STATE_ON, MEAS_SLOT_FREQ)

def setImmMeas():
	scope_driver.setImmMeasSrc1(STR_CH_GEN)
	scope_driver.setImmMeasType(MEAS_TYPE_FREQ)

def getImmMeasVal():
	return scope_driver.getImmMeasVal()

def stopFreqMeas():
	scope_driver.setMeasState(MEAS_STATE_OFF, MEAS_SLOT_FREQ)

def setVoltMeas():
	scope_driver.setMeasSrc1(STR_CH_GEN, MEAS_SLOT_VAMP)
	scope_driver.setMeasType(MEAS_TYPE_VRMS, MEAS_SLOT_VAMP)
	scope_driver.setMeasState(MEAS_STATE_ON, MEAS_SLOT_VAMP)

def stopVoltMeas():
	scope_driver.setMeasState(MEAS_STATE_OFF, MEAS_SLOT_VAMP)

def getPhase():
	return scope_driver.getMeasVal(MEAS_SLOT_PHASE)
	
def getFreq():
	return scope_driver.getMeasVal(MEAS_SLOT_FREQ)

def getVampl():
	return float(scope_driver.getMeasVal(MEAS_SLOT_VAMP))
