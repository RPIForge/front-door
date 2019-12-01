import os
if(not os.path.isdir("logs")):
    os.mkdir("logs")


import logging
from logging.handlers import TimedRotatingFileHandler

print('initalizing logging')
logger = logging.getLogger('rpi_logger')
logger.setLevel(logging.DEBUG)

# create file handler which logs all messages
file_handler = TimedRotatingFileHandler('logs/application.log', when="midnight", interval=1)
file_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

#adder handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
print('initialized logging')

##### ASCIOI ART FOR BEGENNING OF FILE #########

logger.info("___________.__             ____________________.___  ___________")                         
logger.info("\__    ___/|  |__   ____   \______   \______   \   | \_   _____/__________  ____   ____")    
logger.info("  |    |   |  |  \_/ __ \   |       _/|     ___/   |  |    __)/  _ \_  __ \/ ___\_/ __ \ ")   
logger.info("  |    |   |   Y  \  ___/   |    |   \|    |   |   |  |     \(  <_> )  | \/ /_/  >  ___/")   
logger.info("  |____|   |___|  /\___  >  |____|_  /|____|   |___|  \___  / \____/|__|  \___  / \___  >")  
logger.info("                \/     \/          \/                     \/             /_____/      \/") 


logger.info('initalizing system')
logger.info('importing other modules')

import os 
import slack
import traceback

#import raspberry pi
from include.bot import door_bot

logger.info('Finished importing other modules')
logger.info('Getting slack token')

#get slack token from enviromental variables
try:
    slack_token = os.environ['DOOR_SLACK_TOKEN']
except:
    raise Exception("Slack token enviromental variable is not found")
    
#set up pinouts
red_pin = 13
green_pin = 15
blue_pin = 29      
input_pin_1 = 7
input_pin_2 = 16
input_pin_3 = 12
input_pin_4 = 11

logger.info('Initializing slack bot')
#initialize slack bot
slack_app = door_bot(slack_token, 'include/user_file.txt',red_pin, green_pin,blue_pin, input_pin_1,input_pin_2, input_pin_3, input_pin_4)   
logger.info('initialized system')

#slack handle rtm message
@slack.RTMClient.run_on(event='message')
def get_message(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    logger.debug(data)
    #have slack bot handle message
    slack_app.handle_message(data)

#start slack rtm client
logger.info("starting rtm service")
rtm_client = slack.RTMClient(token=slack_token,auto_reconnect=True)
rtm_client.start()  
