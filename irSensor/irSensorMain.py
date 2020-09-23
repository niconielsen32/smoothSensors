#pip install grove.py
from irSensorClass import irSensor, Pi_hat_adc



numSensors = 4
sensorThreshold = 0.4

ADC = Pi_hat_adc()

irSensors = irSensor(ADC, numSensors, sensorThreshold)

thresholdValue = irSensors.initSensors()

while True:
    
    cupsList, numberOfCupsTaken = irSensors.detectCups()
    
    """print("cups: ", cupsList)
    print("number: ", numberOfCupsTaken)
    time.sleep(0.5)"""