import scope_driver


INT_CH_GEN = 	  1
INT_CH_NET = 	  2
STR_CH_GEN = 	  'CH%d' %INT_CH_GEN
STR_CH_NET =      'CH%d' %INT_CH_NET

CH_BANDW_TWENTY = 'TWE'
CH_BANDW_FULL =   'FUL'

CH_COUPLING_AC =  'AC'
CH_COUPLING_DC =  'DC'
CH_COUPLING_GND = 'GND'

MEAS_SLOT_PHASE = 1
MEAS_SLOT_FREQ =  2
MEAS_SLOT_VRMS =  3
MEAS_SLOT_D =     4

MEAS_TYPE_PHASE = 'PHA'
MEAS_TYPE_FREQ =  'FREQ'
MEAS_TYPE_VRMS =  'RMS'
MEAS_TYPE_AMPL =  'AMP'



MEAS_STATE_ON =   'ON'
MEAS_STATE_OFF =  'OFF'


def setup():
	scope_driver.init()
	scope_driver.lockFrontPanel()
	scope_driver.setChannelBandwidth(INT_CH_GEN, CH_BANDW_TWENTY)
	scope_driver.setChannelBandwidth(INT_CH_NET, CH_BANDW_TWENTY)
	scope_driver.setChannelCoupling(INT_CH_GEN, CH_COUPLING_DC)
	scope_driver.setChannelCoupling(INT_CH_NET, CH_COUPLING_DC)
	scope_driver.setChannelVertPos(INT_CH_GEN, 1)
	scope_driver.setChannelVertPos(INT_CH_NET, -1)
	# set probe attenuation first
	scope_driver.setChannelVertScale(INT_CH_GEN,'100')
	scope_driver.setChannelVertScale(INT_CH_NET,'100')
	scope_driver.setHorScale('10E-3')
	
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

def stopFreqMeas():
	scope_driver.setMeasState(MEAS_STATE_OFF, MEAS_SLOT_FREQ)

def setVoltMeas():
	scope_driver.setMeasSrc1(STR_CH_GEN, MEAS_SLOT_VRMS)
	scope_driver.setMeasType(MEAS_TYPE_VRMS, MEAS_SLOT_VRMS)
	scope_driver.setMeasState(MEAS_STATE_ON, MEAS_SLOT_VRMS)

def stopVoltMeas():
	scope_driver.setMeasState(MEAS_STATE_OFF, MEAS_SLOT_VRMS)

def getPhase():
	return getMeasVal(MEAS_SLOT_PHASE)
	
def getFreq():
	return getMeasVal(MEAS_SLOT_FREQ)

def getVrms():
	return getMeasVal(MEAS_SLOT_VRMS)
