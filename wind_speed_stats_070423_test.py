# a program to calculate wind speed (average and gusts) using an anemometer
import math
from gpiozero import Button
import math
import time
import statistics

global wind_count, gust, wind_speed, store_speeds
adjustment=1.18
wind_count = 0
wind_speed = 0
wind_gust =0

store_speeds=[]
radius_cm = 9.2
wind_interval = 30
speed_rounded = 0

#spin = wind_speed_sensor.when_pressed
# every half rotation add 1 to count
def spin():
    global wind_count
    wind_count=wind_count+1
    

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
    wind_count =0
   
    
    

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin


# loop to measure wind speed and report every wind_interval seconds

def wind_stats():
    global gust, wind_speed, store_speeds
    store_speeds=[]
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
    return gust, wind_speed
    

while True:
    wind_stats()
    print("wind is gusting to %.2f"% gust , "average speed is %.2f in mph"%wind_speed )
    print(store_speeds)



    
    


