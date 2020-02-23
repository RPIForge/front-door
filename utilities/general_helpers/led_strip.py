import os
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

    #variable object and logger
    variable_object = None
    logger = None

    #mode
    mode = None

    ########################### HARDWARE METHODS ###########################
    #constuctor
    def __init__(self,variable, mode_input="LIVE", red=13, green=15, blue=29):
        #set variable object
        self.variable_object = variable

        #set pins
        self.red_pin=red
        self.green_pin=green
        self.blue_pin=blue

        # set mode and logger
        self.mode = mode_input
        self.logger = self.variable_object.logger_class.logger

        if(self.mode == "LIVE"):
            import RPi.GPIO as GPIO

            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.red_pin, GPIO.OUT)
            GPIO.setup(self.green_pin, GPIO.OUT)
            GPIO.setup(self.blue_pin, GPIO.OUT)
        self.logger.info("Initialized LED strip in {} mode".format(self.mode))
    #pin setup
    def set_pin(self,pin,state):
        state = state.upper()
        if((pin != self.red_pin) and (pin != self.green_pin) and (pin != self.blue_pin)):
            return False

        if(self.mode != "DEBUG"):
            if(state=='HIGH'):
                GPIO.output(pin, GPIO.HIGH)
            elif(state=='LOW'):
                GPIO.output(pin, GPIO.LOW)
            else:
                return False

        return True

    ############################## COLOR METHODS ##############################
    def set_color(self, color, bump=False):
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
            raise ValueError("Not a color")

        self.current_color=color
        return self.current_color

    ####################### COLOR EFFECTS #####################################
    def color_bump(self):
        for colors in color_list:
            self.set_color(color)
            time.sleep(0.5)

    def quick_bump(self):
        self.set_color('RED')
        time.sleep(0.5)
        self.set_color('GREEN')
        time.sleep(0.5)
        self.set_color('BLUE')
        time.sleep(0.5)
        self.set_color('OFF')
