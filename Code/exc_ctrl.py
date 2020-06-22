import dc_src_driver
import adc_driver
import gpio

from simple_pid import PID

dc_src_driver.init()

Kp = 0.2
Ki = 0
Kd = 0

def startControl():
    pid = PID(Kp,Ki,Kd, setpoint=230)
    Vexc = 10
    while gpio.getExcState:
	# compute new ouput from the PID according to the systems current value
	Vrms = adc_driver.getVoltage()
	Vexc += pid(Vrms)
	if(Vexc>34):
	    Vexc = 34
	dc_src_driver.setVoltage(Vexc)
	
