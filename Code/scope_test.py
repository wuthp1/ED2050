import scope
import time

scope.setup()
scope.setImmMeas()

for i in range(1,100):
	print(scope.getImmMeasVal())
	time.sleep(0.2)
