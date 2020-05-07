"""provides API for USB communication with scope.


"""


import pyvisa

def init():
	"""Establishes USB connection with scope.
	
	Uses PyVisa to establish connection to scope.
	The handle to access the scope is saved in the global variable "scope"
	"""
	rm = pyvisa.ResourceManager()
	instr = rm.list_resources()
	global scope = rm.open_resource(instr[1])
	#TODO: UI to choose USB Instrument instead of just taking instr[1]
	return True

def getID():
	"""Reads id from scope.
	
	Returns:
		str: identification string received from scope"""
	return scope.query('*IDN?')

def getChannelInfo(chNr):
	"""Reads scope channel info.
	
	Args:
		chNr (int): channel number, may be a integer from 1 to 4
		
	Returns:
		str: channel info received from scope"""
	return scope.query('CH%d?' %chNr)

def getBandwidth(chNr):
	"""Reads scope channel bandwidth setting.
	
	Args:
		chNr (int): channel number, may be a integer from 1 to 4
		
	Returns:
		str: bandwith setting received from scope"""
	return scope.query('CH%d:BAN?' %chNr)
	
def setBandwidth(chNr,bandwidth):
	"""Sets scope channel bandwidth.
	
	Args:
		chNr (int): channel number, may be a integer from 1 to 4
		bandwith: channel bandwidth setting
			May be 'TWE' for 20Mhz, 'FUL' for full bandwith or a
			double-precision ASCII string. In this case, the scope
			rounds the value to an available bandwdith
		
	Returns:
		bool: True"""
	scope.write('CH%d:BAN ' %chNr + bandwidth)
	return True
	
def getCoupling(chNr):
	"""Reads scope input attenuator coupling setting
	
	Args:
		chNr (int): channel number, may be a integer from 1 to 4
	
	Returns:
		str: current scope input attenuator coupling setting
	"""
	return scope.query('CH%d:COUP?' %chNr)

def setCoupling(chNr, coupl):
	scope.write('CH%d:COUP ' %chNr + coupl)
	return True

def getVertPos(chNr):
	return scope.query('CH%d:POS?' %chNr)
	
def setVertPos(chNr, div):
	scope.write('CH%d:POS ' + div)
	return True
