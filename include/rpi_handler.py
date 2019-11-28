import os

if(not ("DOOR_DEV" in os.environ and os.environ['DOOR_DEV']=='True')):
    import RPi.GPIO as GPIO
else:
    print("Running in DEV")

import datetime
import threading
import logging
import time

#led pin start up 
from .led import led
from .google_calendar import calendar

class rpi_handler:
    #color mode
    color_mode = None
    
    #pins
    red_pin = None
    green_pin = None
    blue_pin = None
    input_pin_1 = None
    input_pin_2 = None
    input_pin_3 = None
    input_pin_4 = None
    
    #led controller
    led_strip=None
    
    #calendar
    loop_calendar = None
    calendar_color = None
    
    #logger
    logger = None
    
    
    
    def change_state(self, channel):
        if(not GPIO.input(channel)):
            return
            
        self.logger.info("button pressed:"+str(channel))
        if(channel==self.input_pin_1):
            self.logger.debug("GREEN SWITCH")
            #set the new values
            self.color_mode = "override"
            self.led_strip.set_color('GREEN')
        elif(channel==self.input_pin_2):
            self.logger.debug("RED SWITCH")
            #set new values
            self.color_mode = "override"
            self.led_strip.set_color('RED')
        elif(channel==self.input_pin_3):
            self.logger.debug("RESET SWITCH")
            #set new values
            self.color_mode = "calendar"
            self.led_strip.set_color(self.calendar_color)
            
        elif(channel==self.input_pin_4):
            self.logger.debug("COLOR BUMP SWITCH")
            #set new values
            self.color_mode = "override"
            self.led_strip.set_color('BUMP')


    def __init__(self, red, green, blue, input1, input2, input3, input4):
        #initalize logging
        self.logger = logging.getLogger('rpi_logger')

        
        self.red_pin=red
        self.green_pin=green
        self.blue_pin=blue
        self.input_pin_1 = input1
        self.input_pin_2 = input2
        self.input_pin_3 = input3
        self.input_pin_4 = input4
        
        
        #start and test led strip
        self.logger.info("starting led strip")
        self.led_strip = led(red,green,blue)
        self.led_strip.quick_bump()
        self.logger.info("Finished led startup")
        
        self.logger.info("configuring input")
            
        if("DOOR_DEV" in os.environ and os.environ['DOOR_DEV']=='True'):
            pass
        else:
            GPIO.setup(input1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(input2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(input3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(input4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            # add handler
            GPIO.add_event_detect(input1, GPIO.RISING, callback=self.change_state, bouncetime=750)        
            GPIO.add_event_detect(input2, GPIO.RISING, callback=self.change_state, bouncetime=750)
            GPIO.add_event_detect(input3, GPIO.RISING, callback=self.change_state, bouncetime=750)        
            GPIO.add_event_detect(input4, GPIO.RISING, callback=self.change_state, bouncetime=750)                
        
        self.logger.info("finished configuration")

        # add handlers
        self.color_mode="calendar"
        self.loop_calendar = calendar()
        
        
    
    ################################### HELPER FUNCTIONS ############################################   
    #search for reoccurring events
    def calendar_thread(self):
        #Always running
        while(True):
            if(self.color_mode=='calendar'):
                try:
                    if(self.loop_calendar.running):
                        time.sleep(5)
                        continue
                    
                    
                    self.loop_calendar.running = True
                    current_events = self.loop_calendar.get_current_events()
                    self.loop_calendar.running = False
                
                    if(self.color_mode=='calendar'):
                        if(len(current_events)!=0): 
                            self.calendar_color= "GREEN"
                            self.led_strip.set_color('GREEN')
                        else:
                            self.calendar_color= "RED"
                            self.led_strip.set_color('RED')
                except:
                    self.logger.error("Unable to read calendar")
                    
            time.sleep(5)

    def start(self):
        calendar_thread = threading.Thread(target=self.calendar_thread)
        calendar_thread.start()

