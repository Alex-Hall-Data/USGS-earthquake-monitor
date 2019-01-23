# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:15:55 2018

@author: ahall
"""

from quakefeeds import QuakeFeed
import time
import math
import Adafruit_CharLCD as LCD
import aurorawatchuk
import RPi.GPIO as GPIO

#setup pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)



#setup lcd

# Raspberry Pi pin configuration:
lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

#initialise the lcd
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                           lcd_columns, lcd_rows, lcd_backlight)

while(True):

    lcd.clear()
    GPIO.output(12,GPIO.LOW)
    
    #query api and retrieve data for last 24 hours
    feed = QuakeFeed("4.5", "day")
    last_quake = feed[0]
    
    title = last_quake.get('properties').get('title')
    magnitude = last_quake.get('properties').get('mag')
    q_time = last_quake.get('properties').get('time')
    q_time=time.strftime("%D %H:%M", time.gmtime(int(str(q_time)[0:10])))
    
    #look for mag 7+ earthquakes in last day
    i=0
    #marker to indicate whether 7+ quake occured today
    hi_mag_quake=False
    hi_quake=str()
    for quake in feed:
        mag = quake.get('properties').get('mag')
        
        if(mag >= 7):
            hi_mag_quake=True
            hi_quake = feed[i].get('properties').get('title')
            hq_time = feed[i].get('properties').get('time')
            hq_time = time.strftime("%D %H:%M", time.gmtime(int(str(hq_time)[0:9])))
        else:
            hi_quake = None
        
        i=i+1
        
    #print results to lcd

    #print details of hi mag quake
    if(hi_mag_quake):
        GPIO.output(12,GPIO.HIGH)
        for i in range(len(hi_quake)+len(hq_time)):
            lcd.clear()
            lcd.message('MAG 7+ QUAKE' + '\n')
            lcd.message(('  ' + hi_quake + '  ' + hq_time)[i:i+lcd_columns])
            time.sleep(0.3)
        
               
   

    for i in range(len(title) + len(q_time)):
        lcd.clear()
        lcd.message('last quake' + '\n')
        lcd.message(('  ' + title+ '  ' +q_time)[i:i+lcd_columns])
        time.sleep(0.3)   
        

    #print last quake    
    lcd.message('last quake: '+q_time+title)
    for i in range(lcd_columns+len(title)+len(q_time)):
        time.sleep(0.3)
        lcd.move_left()
        
        
    #AURORA DATA
    aurorawatchuk.user_agent = 'test'
    awuk = aurorawatchuk.AuroraWatchUK(raise_=False)
    stat = awuk.status
    
    lcd.message("Aurora Status:\n"+ awuk.status.level)
    time.sleep(5)
    
    lcd.message("Disturbance:\n"+ awuk.activity.latest.value + "nT")
    time.sleep(5)
    
    alert_msg = 'AT THIS TIME OF THE YEAR...IN THIS PART OF THE COUNTRY'
    if(awuk.status == "red"):
        for i in range(lcd_columns+len(alert_msg)):
            lcd.clear()
            lcd.message("AURORA BOREALIS" + "\n")
            lcd.message(alert_msg)
            time.sleep(0.3)
            lcd.move_left()

         
 

        
        
    
    
