# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:15:55 2018

@author: ahall
"""

from quakefeeds import QuakeFeed
import time
import math
import Adafruit_CharLCD as LCD

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
    
    #query api and retrieve data for last 24 hours
    feed = QuakeFeed("4.5", "day")
    last_quake = feed[0]
    
    title = last_quake.get('properties').get('title')
    magnitude = last_quake.get('properties').get('mag')
    q_time = last_quake.get('properties').get('time')
    q_time=time.strftime("%D %H:%M", time.gmtime(int(str(q_time)[0:9])))
    
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
    if (hi_mag_quake):
        lcd.message("SEVERE QUAKE\nIN LAST 24 HOURS")
        time.sleep(5.0)
        
	#print details of hi mag quake
        lcd.message(hq_time + hi_quake)

        for i in range(lcd_columns + len(hi_quake)+len(hq_time)):
                time.sleep(0.3)
                lcd.move_left()
        
    #print last quake    
    lcd.message('last quake: '+q_time+title)
    for i in range(lcd_columns+len(title)+len(q_time)):
        time.sleep(0.3)
        lcd.move_left()
    
        
        
    
    
