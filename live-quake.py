# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:15:55 2018

@author: ahall
"""

from quakefeeds import QuakeFeed
import time


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
        
        
    
    