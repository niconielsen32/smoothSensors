#pip install grove.py
from grove.i2c import Bus
 
 
class Pi_hat_adc():
    def __init__(self,bus_num=1,addr=0X04):
        self.bus=Bus(bus_num)
        self.addr=addr
 
    #get all raw adc data,THe max value is 4095,cause it is 12 Bit ADC
    def get_all_adc_raw_data(self):
        array = []
        for i in range(8):  
            data=self.bus.read_i2c_block_data(self.addr,0X10+i,2)
            val=data[1]<<8|data[0]
            array.append(val)
        return array
 
    def get_nchan_adc_raw_data(self,n):
        data=self.bus.read_i2c_block_data(self.addr,0X10+n,2)
        val =data[1]<<8|data[0]
        return val



class irSensor():
    
    def __init__(self, adc, numberOfSensors, sensorThreshold):
        self.adc = adc
        self.numberOfSensors=numberOfSensors
        self.sensorThreshold = sensorThreshold
        self.values = [0] * self.numberOfSensors
        self.cups = [0] * self.numberOfSensors
        self.adcStandardValue = [0] * self.numberOfSensors
        self.adcThreshold = [0] * self.numberOfSensors
        self.cupRemoved = [0] * self.numberOfSensors
        self.cupPutback = [0] * self.numberOfSensors
        self.cupNotRemoved = [0] * self.numberOfSensors
        self.numberOfCupsTaken = 0
        
 
    def initSensors(self):

        # Load all the first values into a list to have a default ir value for each sensor
        adcValue = self.adc.get_all_adc_raw_data()
        
        for i in range(self.numberOfSensors):
            # Set the threshold for each individual sensor
            self.adcThreshold[i] = adcValue[i] * self.sensorThreshold
            
            if adcValue[i] == 0:
                print("Cup Sensor " + str(i) + " does not work! - Check connections")
        
        print("ADC first value: ", adcValue[:self.numberOfSensors])
        print("ADC threshold: ", self.adcThreshold)
        
        return self.adcThreshold
        
    
    def detectCups(self):

        values = self.adc.get_all_adc_raw_data()
        
        for i in range(self.numberOfSensors):
            
            # check if sensor value goes over threshold - cup removed/placed back
            if values[i] >= self.adcThreshold[i]:
                self.cupNotRemoved[i] = True
            elif self.cupNotRemoved[i] and values[i] < self.adcThreshold[i]:
                self.cupRemoved[i] = True
                self.cupNotRemoved[i] = False
                print("Cup " + str(i) + " Removed")
                self.numberOfCupsTaken += 1
                print("Number of cups taken: ", self.numberOfCupsTaken)
            if self.cupRemoved[i] and values[i] >= self.adcThreshold[i]:
                self.cupPutback[i] = True
                self.cupRemoved[i] = False
                print("Cup " + str(i) + " Putback")
                    
                
            #print(values)
            # Print the ADC values.
            #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |'.format(*values))
            # Pause for half a second.
            
            return self.cupRemoved, self.numberOfCupsTaken
