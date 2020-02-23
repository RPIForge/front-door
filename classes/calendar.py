from utilities.google_calendar import google_calendar
import time

class calendar():
    variable_object = None
    google_calendar = None

    def __init__(self, variable):
        #init variable object
        self.variable_object = variable
        self.variable_object.logger_class.logger.info("Initialized Calendar class")


    def start(self):
        self.google_calendar = google_calendar()


    def thread(self):
        #Always running
        while(True):
            if(self.variable_object.rpi_handler.mode =='calendar'):
                try:
                    current_events = self.loop_calendar.get_current_events()
                    if(len(current_events)!=0):
                        self.variable_object.led_strip.set_color('GREEN')
                    else:
                        self.variable_object.led_strips.set_color('RED')
                except:
                    self.variable_object.logger_class.logger.serror("Unable to read calendar")

            time.sleep(5)
