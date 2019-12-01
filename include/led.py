import os
if(not ("DOOR_DEV" in os.environ and os.environ['DOOR_DEV']=='True')):
    import RPi.GPIO as GPIO

import threading
import time
import logging

class led:
    #pin variables
    red_pin = None
    green_pin = None
    blue_pin = None

    #color variables
    current_color = 'OFF'
    color_list = ['RED','GREEN','BLUE','CYAN','YELLOW','PURPLE','WHITE', 'OFF']

    #effect variables
    continue_bump = None
    bump_thread = None
    #logger
    logger = None
    
    ########################### HARDWARE METHODS ###########################
    #constuctor
    def __init__(self, red, green, blue):
        #initalize logging
        self.logger = logging.getLogger('rpi_logger')
        
        self.red_pin=red
        self.green_pin=green
        self.blue_pin=blue
        
        if(not ("DOOR_DEV" in os.environ and os.environ['DOOR_DEV']=='True')):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.red_pin, GPIO.OUT)
            GPIO.setup(self.green_pin, GPIO.OUT)
            GPIO.setup(self.blue_pin, GPIO.OUT)
            
        self.bump_thread = threading.Thread(target=self.infinite_color_bump)

    #pin setup 
    def set_pin(self,pin,state):
        state = state.upper()
        if((pin != self.red_pin) and (pin != self.green_pin) and (pin != self.blue_pin)):
            return
        
        if(not ("DOOR_DEV" in os.environ and os.environ['DOOR_DEV']=='True')):
            if(state=='HIGH'):
                GPIO.output(pin, GPIO.HIGH)
            elif(state=='LOW'):
                GPIO.output(pin, GPIO.LOW)
            else:
                return


    ############################## COLOR METHODS ##############################        
    def set_color(self, color, bump=False):
        if(not bump and self.continue_bump==True):
            self.logger.info("Stopping Bump")
            self.continue_bump=False
            
        if(color==self.current_color):
            return self.current_color
        
        self.logger.info('Setting LED to: '+str(color))
        color = color.upper()
        if(color == 'RED'):
            self.set_pin(self.red_pin,'HIGH')
            self.set_pin(self.green_pin,'LOW')
            self.set_pin(self.blue_pin,'LOW')
        elif(color == 'GREEN'):
            self.set_pin(self.red_pin,'LOW')
            self.set_pin(self.green_pin,'HIGH')
            self.set_pin(self.blue_pin,'LOW')
        elif(color == 'BLUE'):
            self.set_pin(self.red_pin,'LOW')
            self.set_pin(self.green_pin,'LOW')
            self.set_pin(self.blue_pin,'HIGH')
        elif(color == 'CYAN'):
            self.set_pin(self.red_pin,'LOW')
            self.set_pin(self.green_pin,'HIGH')
            self.set_pin(self.blue_pin,'HIGH')
        elif(color == 'YELLOW'):
            self.set_pin(self.red_pin,'HIGH')
            self.set_pin(self.green_pin,'HIGH')
            self.set_pin(self.blue_pin,'LOW')
        elif(color == 'PURPLE'):
            self.set_pin(self.red_pin,'HIGH')
            self.set_pin(self.green_pin,'LOW')
            self.set_pin(self.blue_pin,'HIGH')
        elif(color == 'WHITE'):
            self.set_pin(self.red_pin,'HIGH')
            self.set_pin(self.green_pin,'HIGH')
            self.set_pin(self.blue_pin,'HIGH')
        elif(color == 'BUMP'):
            self.continue_bump=True
            self.bump_thread.start()
        elif(color =='OFF'):
            self.set_pin(self.red_pin,'LOW')
            self.set_pin(self.green_pin,'LOW')
            self.set_pin(self.blue_pin,'LOW')
        else:
            raise Exception("Not a color") 
            
        self.current_color=color
        return self.current_color

    ####################### COLOR EFFECTS #####################################
    def color_bump(self):
        for colors in color_list:
            self.set_color(color)
            time.sleep(0.5)
    
    def infinite_color_bump(self):
        
        while(True): 
            for colors in self.color_list:
                if(colors == 'OFF'):
                    continue
                
                self.set_color(colors, True)
                
                print(self.continue_bump)
                if(not self.continue_bump):
                    self.set_color("OFF")
                    return
                
                time.sleep(0.5)
                
    def quick_bump(self):
        self.set_color('RED')
        time.sleep(0.5)
        self.set_color('GREEN')
        time.sleep(0.5)
        self.set_color('BLUE')
        time.sleep(0.5)
        self.set_color('OFF')
    
    def next_color(self):
        index = self.color_list.index(self.current_color)
       
            
        #if off then go to calendar
        if(index == (len(self.color_list)-1)):
            self.set_color("RED")
            
        #loop through list
        else:
            self.set_color(self.color_list[index+1])
            
        return self.current_color    

        
