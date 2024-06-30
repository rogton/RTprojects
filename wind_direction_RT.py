
# created a dictionary with cardinal point using try and except. Updated May 12,2023 by Roger Tonneman

from gpiozero import MCP3008
import time
import math
adc=MCP3008(channel=0)
count = 0
volts =dict()
volts={2.9:"N",1.9:"ENE",2.1:"NE",0.5:"ENE",0.6:"E",0.4:"ESE",1.1:"SE",0.8:"SSE",1.5:"S",1.3:"SSW",1.4:"SEBW",2.6:"SW",2.5:"WSW",3.2:"W",3.0:"WNW",2.7:"NW",3.1:"NNW"}
values =[]
global actual
actual = 0

def wind_direction():
    try:
        actual = adc.value*3.3
        wind= round(actual,1)
        time.sleep(3)
        return volts[wind]
        
    
    except KeyError:
        wind = 2.9
        time.sleep(3)
        print("KeyError exception triggered")
        return volts[wind]
    
#while True:
#  time.sleep(1)
#print("\n wind out of ", wind_direction())
