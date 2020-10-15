import time
from grove.i2c import Bus
 
ADC_DEFAULT_IIC_ADDR = 0X04
 
ADC_CHAN_NUM = 8
 
REG_RAW_DATA_START = 0X10
REG_VOL_START = 0X20
REG_RTO_START = 0X30
 
REG_SET_ADDR = 0XC0
 
 
class Pi_hat_adc():
    def __init__(self,bus_num=1,addr=ADC_DEFAULT_IIC_ADDR):
        self.bus=Bus(bus_num)
        self.addr=addr
 
 
    #get all raw adc data,THe max value is 4095,cause it is 12 Bit ADC
    def get_all_adc_raw_data(self):
        array = []
        for i in range(ADC_CHAN_NUM):  
            data=self.bus.read_i2c_block_data(self.addr,REG_RAW_DATA_START+i,2)
            val=data[1]<<8|data[0]
            array.append(val)
        return array
 
    def get_nchan_adc_raw_data(self,n):
        data=self.bus.read_i2c_block_data(self.addr,REG_RAW_DATA_START+n,2)
        val =data[1]<<8|data[0]
        return val
 
 
 
ADC = Pi_hat_adc()


def main():
    adcValues = ADC.get_all_adc_raw_data()
    
    print("adc values:")
    print(adcValues)
 
 
if __name__ == '__main__':
    
    while True:
        main()
