#import system and set default values/take input from args
from utilities.utility import handle_arguments
arguments = handle_arguments()


# import variable object
from classes.variable import variable
variable_object = variable()

#initalize logger
from utilities.logger import logger
variable_object.logger_class = logger(variable_object)
variable_object.logger_class.start(arguments['log_level'])

#inistalize led led_strip
from utilities.led_strip import led
variable_object.led_strip = led(variable_object, arguments['led_level'])
