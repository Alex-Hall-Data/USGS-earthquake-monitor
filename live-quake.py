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
        else:
            hi_quake = None
        
        i=i+1
        
    #print results
    if (hi_mag_quake):
        print ("SEVERE QUAKE IN LAST 24 HOURS")
        time.sleep(2.0)
        print(hi_quake)
        time.sleep(5.0)
        
    print('last quake:')
    print(title)
    time.sleep(10.0)
        
        
    
    
