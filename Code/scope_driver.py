"""provides API for USB communication with scope.
 TODO try catch security shit

"""


import pyvisa

def init():
    """Establishes USB connection with scope.
    
    Uses PyVisa to establish connection to scope.
    The handle to access the scope is saved in the global variable "scope"
    """
    
    global scope
    rm = pyvisa.ResourceManager()
    instr = rm.list_resources()
    scope = rm.open_resource(instr[1])
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

def getChannelBandwidth(chNr):
    """Reads scope channel bandwidth setting.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
        
    Returns:
        str: bandwith setting received from scope"""
    return scope.query('CH%d:BAN?' %chNr)
    
def setChannelBandwidth(chNr,bandwidth):
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
    
def getChannelCoupling(chNr):
    """Reads scope input attenuator coupling.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
    
    Returns:
        str: current scope input attenuator coupling setting
    """
    return scope.query('CH%d:COUP?' %chNr)

def setChannelCoupling(chNr, coupl):
    """Sets scope input attenuator coupling.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
        coupling (str): Input attenuator setting.
            May be:
            'AC' for AC coupling
            'DC' for DC coubling
            'GND'. This sets channel to ground-level. Only a flat
            waveform will be displayed
    
    Returns:
        bool: True
    """
    scope.write('CH%d:COUP ' %chNr + coupl)
    return True

def getChannelVertPos(chNr):
    """Reads vertical position of channel in divisions.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
    
    Returns:
        (str): vertical position of channel in divisions
    """
    return scope.query('CH%d:POS?' %chNr)
    
def setChannelVertPos(chNr, div):
    """Sets vertical position of channel in divisions.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
        div (float): horizontal position in divisions
            May be a value between -4 and 4, where 4 is the upper border
            of the screen and -4 the lower one
    
    Returns:
        (bool): True
        
    Example:
        The following line sets the vertical position of channel 2
        3.2 divisons over the center:
            setChannelVertPos(2, 3.2)
    """
    scope.write('CH%d:POS %.4f' %(chNr,div))
    return True

def getChannelVertScale(chNr):
    """Reads vertical scale of channel in volts/div.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
        
    Returns:
        (str): vertical scale of channel in volts/div.
    """
    return scope.query('CH%d:SCA?' %chNr)
    
def setChannelVertScale(chNr, scale):
    """Set vertical scale of channel in volts/div.
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
        scale (str): vertical scale in volts/div 
            (e.g. '1.2' or '5.5E-3')
        
    Returns:
        (bool): True
    """
    scope.write('CH%d:SCA' %chNr + scale)
    return True

def getHorScale():
    """Reads scope time base horizontal scale.
    
    Returns:
        (str): scope time base horizontal scale in s/div
    """
    return scope.query('HOR:SCA?')

def setHorScale(scale):
    """Sets scope time base horizontal scale.
    
    Args:
        scale (str): time base horizontal scale in s/div
            e.g. '2E-6' for 2us per division
    
    Returns:
        (str): scope time base horizontal scale in s/div
    """
    return scope.write('HOR:SCA ' + scale)

def lockFrontPanel():
    """Locks all buttons and knobs on the front panel of the scope.
    
    Returns:
        (bool): True
    """
    scope.write('LOC ALL')
    return True

def unlockFrontPanel():
    """Unlocks all buttons and knobs on the front panel of the scope.
    
    Returns:
        (bool): True
    """
    scope.write('UNL ALL')
    return True

def setMeasSrc1(src, slot):
    """Sets measurement source 1.
    
    Sets measurement source for all single source measuremets and
    specifies the source to measure "from" for phase and delay
    measurements.
    
    Args:
        src (str): Measurement source
            May be 'CHx', 'REFx' where x is the (reference) channel
            number or 'MATH1' for math waveform.
        
        slot (int): Measurement slot, may be an integer in 1 to 4"""
    
    scope.write('MEASU:MEAS%d:SOURCE1 ' %slot + src)
    return True
    
def setMeasSrc2(src, slot):
    """Sets measurement source 2.
    
    Specifies the source to measure "to" for phase and delay
    measurements.
    
    Args:
        src (str): Measurement source
            May be 'CHx', 'REFx' where x is the (reference) channel
            number or 'MATH1' for math waveform.
        
        slot (int): Measurement slot, may be an integer in 1 to 4"""
    
    scope.write('MEASU:MEAS%d:SOURCE2 ' %slot + src)
    return True

def setMeasType(MeasType, slot):
    """Sets what should be measured.
    
    Args:
        MeasType (str): Specifies what should be measured
        Only the most important types are listed here. For more
        possibilities see Textronix DPO 2000 Programmer Manual
            'AMP':  Amplitude
            'FREQ': Frequency
            'PHA': Phase in degrees
            'RMS': RMS Voltage
        
        slot (int): Measurement slot, may be an integer in 1 to 4
        
    Returns:
        (bool): True
            
    """
    scope.write('MEASU:MEAS%d:TYP ' %slot + MeasType)
    return True

def setMeasState(state, slot):
    """Starts/stops measurements of specified slot.
    
    Starts/stops calculation and display of the specified measurement
    slot. Measurement sourc(es) and type must be defined befor measuring
    can be started.
    
    Args:
        state (str): measurement state; may be 'ON' or 'OFF'.
            Alternatively '0' can be used instead of 'OFF'. Any other
            values will set the state to 'ON'
        
        slot (int): Measurement slot, may be an integer in 1 to 4
    
    Returns:
        (bool): True
    """
    scope.write('MEASU:MEAS%d:STATE ' %slot + state)
    return True

def getMeasVal(slot):
    """Reads measured value of specified slot.
    
    Args:
        slot (int): Measurement slot, may be an integer in 1 to 4
    
    Returns
        (str): Measured value
    """
    return scope.query('MEASU:MEAS%d:VAL?' %slot)
    
def selectChannel(chNr,state):
    """Turns display of specified channel on or off
    
    Args:
        chNr (int): channel number, may be a integer from 1 to 4
        
        state (str): channel state; may be 'ON' or 'OFF'.
            Alternatively '0' can be used instead of 'OFF'. Any other
            values will set the state to 'ON'
    
    Returns:
        (bool): True
    """
    scope.write('SEL:CH%d ' %chNr + state)
    return True

def setEdgeTrigger(source, coupl='HFR', slope='RIS'):
    """sets up edge trigger.
    
    Args:
        source (str): May be 'CH<x>', D'<y>','EXT','LINE' or 'AUX'
            where x and y may be an integer in 1 to 4 or 0 to 15,
            respectively
        
        coupl (str): Edge trigger coupling.
            May be 'DC' for DC coupling,
            'HFR' for HF rejection (attenuates signals with f > 50kHz)
            'LFR' for LF rejection (attenuates signals with f < 50kHz)
            or 'NOISE' for noise rejection, which provides stable
            triggering by increasing trigger hysteresis. This may
            require greater trigger signal amplitude
            
    Returns:
        (bool): True
    """
    scope.write('TRIG:A:TYP EDG')
    scope.write('TRIG:A:EDGE:COUP ' + coupl)
    scope.write('TRIG:A:EDGE:SLO ' + slope)
    scope.write('TRIG:A:EDGE:SOU ' + source) 
    return True











