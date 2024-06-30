## latest program for temperature, windspeed and direction using cardinal points.
## Includes CPU temperature moniring. Includes pressure altitude
## This version is the latest and usable version created May 12,2023 by Roger Tonneman
## Updated in june 2023 with corrected coefficients for heat index. Updated ptressuree to hPa. 

import math
import time

import statistics
from gpiozero import Button
from time import strftime
from time import localtime

import bme280_62923_RT

import wind_direction_RT

from gpiozero import CPUTemperature
from gpiozero import OutputDevice
import tkinter as tk
import random

ts=bme280_62923_RT
wd=wind_direction_RT
cpu=CPUTemperature()
adjustment=1.18
wind_count = 0
wind_speed = 0
gust =100
direct= 'NNW'

store_speeds=[]
old_speeds=[]
radius_cm = 9.2
wind_interval = 30
speed_rounded = 0
HI=0


class Display:
    def __init__(self, parent):
        
        
        color_bg="blanched almond"
        time_string_inital=time.strftime('%l:%M %p %Z on %b %d, %Y')
        # label displaying time
        self.label_time=tk.Label(parent, text= time_string_inital, font ="Arial 30", bg=color_bg, fg="blue2", width=80)
        self.label_temp= tk.Label(parent, text=" Temperature is degrees F", font="Arial 30", bg=color_bg,fg="green",width=40)
        self.label_humidity= tk.Label(parent, text=" Humidity is percent RH", font="Arial 30", bg=color_bg,fg="purple3",width=40)      
        self.label_speed= tk.Label(parent, text=" Wind speed is  gusting to", font="Arial 30", bg=color_bg,fg="red2",width=40)
        #self.label_gust= tk.Label(parent, text=" Wind gusts to MPH", font="Arial 30", bg="blanched almond",fg="red2",width=40)
        #self.label_direct=tk.Label(parent, text="Wind out of degees", font="Arial 30", bg="blanched almond", fg="medium blue", width=40)
        self.label_rain= tk.Label(parent, text=" It rained inches", font="Arial 30", bg=color_bg,fg="chocolate3",width=40)
        self.label_cpu=tk.Label(parent, text=" CPU temperature is and fan is ", font="Arial 30", bg=color_bg, fg="DarkOrange3", width=40)
        self.label_time.pack()
        self.label_temp.pack()
        self.label_humidity.pack()
        self.label_speed.pack()
        self.label_cpu.pack()
        #self.label_gust.pack()
        #self.label_direct.pack()
        self.label_rain.pack()
        
        self.label_time.after(500, self.refresh_label_time)
        self.label_temp.after(500, self.refresh_label_temp)
        self.label_humidity.after(500, self.refresh_label_humidity)
        self.label_speed.after(500, self.refresh_label_speed)
        #self.label_gust.after(1000, self.refresh_label_gust)
        #self.label_direct.after(1000, self.refresh_label_direct)
        #self.label_rain.after(500, self.refresh_label_rain)
        self.label_cpu.after(500, self.refresh_label_cpu)
        
    def refresh_label_time(self):
        time_string=time.strftime('%l:%M %p %Z on %b %d, %Y')
        #self.now=time.asctime(time.localtime(time.time()))
        #self.label_time.configure(bg="blanched almond", fg="blue2", text= time_string, self.now)
        self.label_time.configure(bg=color_bg, fg="blue2", text= time_string)
        self.label_time.after(500, self.refresh_label_time)
        
    def refresh_label_temp(self):
        """ refresh the content of the label every time period set in after statement"""
        # update data from bme280
        ts.calcTPCoeff()
        ts.calcHumCoeff()
        ts.convertAll()
        ts.offsetTemp()
        ts.offsetPress()
        ts.offsetHumdity()
        #Temp_c=temperature_BME280_RT.bme280.temperature
        #ambient_temp = round(Temp_c*1.8+32,1)
        ambient_temp=round(ts.fTemp,2)
        #self.seconds = temp_f
        #self.seconds=hazel
        # display the new time
        self.label_temp.configure(bg=color_bg,fg="Green",text="Temperature is %i  degrees F" % ambient_temp)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_temp.after(500, self.refresh_label_temp)
        return ambient_temp

    def refresh_label_humidity(self):
        """ refresh the content of the label every second """
        
        humidity=ts.humidity
        self.label_humidity.configure(bg=color_bg,fg="purple3",text="Humidity is  %i percent RH" % humidity)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_humidity.after(500, self.refresh_label_humidity)

        

    def refresh_label_speed(self):
        """ refresh the content of the label every second """
        # increment the time
        #def spin():
           # global wind_count
            #wind_count=wind_count+1
            #return wind_count
    

# a function to reset wind_counts if needed
        def reset_wind():
                global wind_count
                wind_count=0
                return wind_count
        
        def reset_speed():
                global store_speeds
                store_speeds=[]
                return store_speeds

# calculate wind speed and display in MPH to 1 digit
#a function to reset wind_counts if needed

        def speed_calc(wind_interval):
        # refresh the content of the label every second
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
        
        
    

        def calculate_speed(time_sec):
            global wind_count, gust, wind_speed
            circumference_cm=(2*math.pi)* radius_cm
            rotations=wind_count/2.0
            dist_cm=circumference_cm * rotations
            speed = adjustment *((dist_cm/10000) / (time_sec/3600))*.6213 # converted to miles per hour
    
            speed_rounded= round(speed,1)
            return speed_rounded


            store_speeds=list()
            start_time = time.time()
            while time.time() - start_time <= wind_interval:
         
                final_speed = calculate_speed(wind_interval)
                time.sleep(2)
                store_speeds.append(final_speed)
        gust=round(max(store_speeds))
        #gust=random.randint(8,15)
        #wind_speed = round(statistics.mean(store_speeds),1)
        wind_speed=random.randint(1,7)
        direct='SE'
                    
#                return gust ,wind_speed
       
        #print(final_speed, store_speeds, gust)
        #self.seconds = temp_f
        #self.seconds=hazel
        # display the new time
        self.label_speed.configure(bg="blanched almond",fg="red2",text="Wind speed is {0} gusting to {1} from {2} degrees".format(wind_speed, gust, direct))
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_speed.after(1000, self.refresh_label_speed)
        
        
    def refresh_label_cpu(self):
            #global ct
           #ct=CPUTemperature()
            #ct=int(cpu.temperature)
     
            
        self.label_cpu.configure(bg=color_bg,fg="DarkOrange3",text="CPU Temperature is %i" % cpu.temperature)
        
        self.label_cpu.after(1000, self.refresh_label_cpu)      
        
               

   
            
            
# define functions for sensors

#spin = wind_speed_sensor.when_pressed
# every half rotation add 1 to count
#def spin():
#    global wind_count
#    wind_count=wind_count+1
    

# calculate wind speed and display in MPH to 1 digit
#def calculate_speed(time_sec):
#    global wind_count
#    circumference_cm=(2*math.pi)* radius_cm
#    rotations=wind_count/2.0
#    dist_cm=circumference_cm * rotations
#    speed = adjustment *((dist_cm/10000) / (time_sec/3600))*.6213 # converted to miles per hour
    
#    speed_rounded= round(speed,1)
#    return speed_rounded
    
#a function to reset wind_counts if needed
#def reset_wind():
#    global wind_count
#    wind_count =0
   

#def wind_stats(time_sec):
#    while True:
#        global wind_speed
#        global wind_gust
#        global loop
#        global store_speeds
#        global final_speed
        #store_speeds=[]
 #       start_time =time.time()
 #       while time.time() - start_time <= wind_interval:

            # create a loop and print statement to help debug issues
            #print("inner loop number:", loop)
            #time.sleep(wind_interval)
 #           final_speed = calculate_speed(wind_interval)
 #           store_speeds.append(final_speed)
            #print statement to help debug issues
            #print ("list of speeds ", store_speeds)
            #wind_gust = max(store_speeds)
            #wind_speed = round(statistics.mean(store_speeds),1)
            
            #loop +=1
        # print statement to help debug   
        #print("gusting to", wind_gust,"wind speed", wind_speed)
#        store_speeds =[]
        
#        return wind_gust, wind_speed, final_speed

# a function to calculate rainfall

    
    
# a function to reset rainfall   

    



        
    print("TKINTER_WS_realdata_working-temperature only....")
#measure wind speed   
#wind_speed_sensor = Button(5)
#wind_speed_sensor.when_pressed = spin

# measure rainfall
#rain_sensor= Button(6)
#rain_sensor.when_pressed= rain_calc

loop = 0
loop_big = 0


#loop to turn fan on
#    ct=int(cpu.temperature)
#    if ct>overtempthreshold:
#        print("OVER TEMPERATURE !!!! Computer will start shutdown")
#        print("computer will reboot program will stop")
#        localtime=time.asctime(time.localtime(time.time()))
#        print("time is", localtime)
#        os.system("sudo shutdown -r now")
              
#    elif ct<on_threshold:
#        fan.off()
        #print("It's COOL! CPU is ", ct)
#        localtime=time.asctime(time.localtime(time.time()))
        #print("time is", localtime)
        
        
#   else:
#        if ct>on_threshold:
#            fan.on()
#            print("fan is on because CPU is greater than ", ct)
#            localtime=time.asctime(time.localtime(time.time()))
            #print("time is", localtime)
            
    # time.sleep(2)
#    reset_wind()
 #   wind_stats(wind_interval)
 #   store_speeds.append(final_speed)
 #   wind_gust =max(store_speeds)
 #   wind_speed = round(statistics.mean(store_speeds),1) 
   # humidity = temperature_BME280_RT.bme280.humidity
   # Temp_c=temperature_BME280_RT.bme280.temperature
 #   ambient_temp = round(Temp_c*1.8+32,1)
   # pressure = temperature_BME280_RT.pressure_inmg
   # altitude = round(temperature_BME280_RT.bme280.altitude*3.28,1)
#  wind_direct= wind_direction_RT.wind_direction()
    
    #loop_big +=1
    
    # print statements to help debug
    #print("last print statement", "gusting to", wind_gust, "wind at", wind_speed)
    #print ("list ",store_speeds)
    #print("\nouter loop number", loop_big)
    #print("rain tally is", rain_tally)
    #print("temperature ", ambient_temp)
    #print("altitude in feet ", altitude)

   
# create a string to hold the first part of the URL

    #WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=KCOCOLOR986&PASSWORD=2sfixvbn&dateutc=now"
#    WU_station_pwd = "2sfixvbn" # Replace YYYY with your Password
#WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
#    date_str = "&dateutc=now"
   # action_str = "&action=updateraw"

# turn data fields into strings

 
 
 
   
if __name__ == "__main__":
    color_bg="blanched almond"
    
   
    root = tk.Tk()
    root.title("Backyard Weather")
    root.configure(bg=color_bg)
   
    weather_display = Display(root)
    
    root.mainloop()



    

        

        
        


time_string_inital=time.strftime('%l:%M %p %Z on %b %d, %Y')

  




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
        
# calculate wind speed and gusts      
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
        print(time_string)
        
# calculate roger's heat index and/or windchill. Please only heat index or windchill
        if ts.fTemp>80 and ts.humidity>45:
                
                print("feels like its really HOT ! STAY INSIDE!!")
        else:
                print("Humidity ", round(ts.humidity,0),"%" )
        if ts.fTemp<50:
                wind_chill= ts.fTemp-.7*wind_speed
                print ("with windchill feels like", round(wind_chill,0))
        else:
                print ("Temperature in F",round(ts.fTemp,1))
# calculate pressure altitude in feet.Formula found at bosch-sensortec.com. 1015 is the sea level pressure in hPA.
#152000 is a constant to convert from meters to feet and match estimate alttude from iPhone

        pressalt=152000*(1.0-(ts.pressure/1015.25)**(1/5.255))
                        
# display results to screen
        print("Pressure",round(ts.pressure,2),"hPA")
        print("Wind out of the", wd.wind_direction())
        print("Wind speed is",wind_speed, "gusting to", gust)
        print("CPU temperature in C is", round(cpu.temperature,1))
        print("Pressure altitude is ", round(pressalt),"feet")
        
        print("")
       
        time.sleep(300
                   )
        #print("another loop")

