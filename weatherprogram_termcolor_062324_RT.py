## latest program for temperature, windspeed and direction using cardinal points.
## Includes CPU temperature monitoring. Includes pressure altitude
## This version is the latest and usable version created July 5, 2023 by Roger Tonneman
## Updated in june 2023 to eliminate heat index calculation.
## HI formula only works above 80 F and 40% RH which rarely happens at home.
## put in if statement for CPU temperature to warm if CPU gets above 65 C 
## 071423- Updated in July to incorporate color in output using termcolor commands.
## 071723- pdated to include cumulative rainfall amount
##062324- addeded dewppoint calculation and display. Dewpt=Temp-((100-RH)/5) where Temp is in C


import math
import time
import sys
import statistics
from gpiozero import Button
from time import strftime
from time import localtime
from termcolor import colored, cprint
import bme280_021624_RT
import os
import wind_direction_RT



adjustment=1.18
# adjustment to match physical rain guage
rain_adjustment= 3
wind_count = 0
wind_speed = 0
wind_gust =0
cpu_threshold=65
Bucket_size=.011
count=0
rainfall=0
store_rain=[]
rain_amt=0
store_speeds=[]
old_speeds=[]
radius_cm = 9.2
wind_interval = 30
speed_rounded = 0
ts=bme280_021624_RT
wd=wind_direction_RT
rain_sensor=Button(13)

#a functioj to get cpu temperature
def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return(temp.replace("temp=",""))
#a function to reset wind_counts if needed


def speed_calc(wind_interval):
        """ refresh the content of the label every second """
        # increment the time
def spin():
        global wind_count
        wind_count=wind_count+1
        return wind_count
    

# calculate wind speed and display in MPH to 1 digit
def calculate_speed(time_sec):
        global wind_count
        circumference_cm=(2*math.pi)* radius_cm
        rotations=wind_count/2.0
        dist_cm=circumference_cm * rotations
        speed = adjustment *((dist_cm/10000) / (time_sec/3600))*.6213 # converted to miles per hour
        speed_rounded= round(speed,1)
        return speed_rounded
    
#a function to reset wind_counts if needed

def reset_wind():
        global wind_count
        wind_count=0
        return wind_count
        
def reset_speed():
        global store_speeds
        store_speeds=[]
        return store_speeds
    
def bucket_tipped():
    global count,rainfall,rain_amt
    rainfall=count*Bucket_size*rain_adjustment
    store_rain.append(rainfall)
    
    count +=1
    rain_amt=max(store_rain)
    #print("amt of rain", rain_amt)
    
def rain_calc():
        global count
        global rainfall
        global rain_amt
        latertime=time.localtime(time.time())
        count=count+1
        rainfall= count*Bucket_size*rain_adjustment    
        store_rain.append(rainfall)
        rain_amt=max(store_rain)
        
        return rain_amt
        

def reset_rainfall():
    global count
    count=0        


time_string_inital=time.strftime('%l:%M %p %Z on %b %d, %Y')

nowtime=time.localtime(time.time())
wind_speed_sensor=Button(5)
wind_speed_sensor.when_pressed=spin

print('Start time of the program', time_string_inital)
print("")
while True:
# get functions from bme280_62923_RT
        ts.calcTPCoeff()
        ts.calcHumCoeff()
        ts.convertAll()
        ts.offsetTemp()
        ts.offsetPress()
        ts.offsetHumdity()
        pressalt=152000*(1.0-(ts.pressure/1015.25)**(1/5.255))
        dewpointC=ts.cTemp-((100-ts.humidity)/5)
        dewpointF=dewpointC*(9/5) +32
        #start rain sensor
        rain_sensor.when_pressed=bucket_tipped
#calculate wind speed and gusts over an interval       
        start_time = time.time()
        while time.time() - start_time <= wind_interval:
                reset_wind()
                time.sleep(wind_interval)
                final_speed = calculate_speed(wind_interval)
                store_speeds.append(final_speed)
                gust=round(max(store_speeds))
                wind_speed = round(statistics.mean(store_speeds))
                if len(store_speeds)>12:
                    store_speeds=[round(statistics.mean(store_speeds),1)]
                else:
                    store_speeds= store_speeds
  # print day and time

        time_string=time.strftime('%l:%M %p %Z on %b %d, %Y')
        cprint ("CURRENT WEATHER", "blue", attrs=["underline", "bold"])
        print(time_string)      
        # calculate roger's heat index and/or windchill. Please only heat index or windchill
        if ts.fTemp>90:
                
                cprint("feels like its really HOT ! STAY INSIDE!!","red", attrs=["reverse", "blink"])
                print("temperature is", round(ts.fTemp,1), "in degrees F")
                print("dewpoint is", round(dewpointF), "in degrees F")
    
                
        elif ts.fTemp<50:
                wind_chill= ts.fTemp-.7*wind_speed
                cprint ("BRRR!!! with windchill feels like", "blue","on_white", attrs=["bold"])
                print("With wind chill temperature is", round(wind_chill,1)," degrees F")
                print("dewpoint is", round(dewpointF), "in degrees F")
        else:
                cprint("Feels good", "green", attrs=["bold"])
                print ("Temperature in F",round(ts.fTemp,1))
                print("Humidity ", round(ts.humidity,0),"%" )
                print("dewpoint is", round(dewpointF), "in degrees F")
                
# calculate pressure altitude in feet.Formula found at bosch-sensortec.com. 1015 is the sea level pressure in hPA.
#152000 is a constant to convert from meters to feet and match estimate alttude from iPhone


        print("")
        print("Wind out of the", wd.wind_direction())
        print("Wind speed is",wind_speed, "gusting to", gust,"in mph")
        print("")
        print("CPU temperature is",measure_temp())
        print("")
        print("Pressure",round(ts.pressure,2),"hPA")
        print("Pressure altitude is ", round(pressalt),"feet")
        print("")
        print("cumulative rainfall amount is",round(rainfall,3), "inches")
        
        print("")
       
        time.sleep(300)
        


