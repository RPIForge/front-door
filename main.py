#initialize system and set default values/take input from args
from utilities.utility import handle_arguments
try:
    arguments = handle_arguments()
except:
    print("Invalid arguments. Please read the readme for further instructions")
    exit()

#initialize variable object
from classes.variable import variable
variable_object = variable()

#initialize logger
from utilities.general_helpers.logger import logger
variable_object.logger_class = logger(variable_object)
variable_object.logger_class.start(arguments['log_level'],arguments['log_time'])

#initialize led led_strip
from utilities.general_helpers.led_strip import led
variable_object.led_strip = led(variable_object, arguments['led_level'])

#initalize calendar class
from classes.calendar import calendar
variable_object.calendar_class = calendar(variable_object)
variable_object.calendar_class.start()



#initalize slack bot
from classes.slack import slack_bot
variable_object.slack_class = slack_bot(variable_object)


#initalize message handlers
from utilities.class_helpers.message_handler import message_handler
variable_object.message_handler = message_handler(variable_object)

##MUST BE LAST AS IT WILL NOT RETURN
## SLACK HAS TO BE ON MAIN THREAD UNTIL they fix their stuff
while(True):
    try:
        variable_object.slack_class.start()
    except:
        self.variable_object.logger_class.logger.exception("Unable to read calendar")