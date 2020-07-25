#import google calendar class
from utilities.class_helpers.google_calendar import google_calendar

#import helper modules
from time import sleep
import threading

class calendar():
    variable_object = None
    google_calendar = None

    calendar_thread = None

    def __init__(self, variable):
        #init variable object
        self.variable_object = variable
        self.google_calendar = google_calendar()
        self.variable_object.logger_class.logger.info("Initialized Calendar class")


    def start(self):
        self.calendar_thread = threading.Thread(target=self.thread)
        self.calendar_thread.start()


    def thread(self):
        #Thread to check the current events
        while(True):
            if(self.variable_object.calendar_mode =='calendar'):
                try:
                    current_events = self.google_calendar.get_current_events()
                    if(len(current_events)!=0):
                        self.variable_object.led_strip.set_color('GREEN')
                    else:
                        self.variable_object.led_strip.set_color('RED')
                except:
                   self.variable_object.logger_class.logger.error("Unable to read calendar")

            sleep(5)
