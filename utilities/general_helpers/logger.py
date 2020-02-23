#Impport to creater log folder if none exists
import os

#Import logging classes
import logging
from logging.handlers import TimedRotatingFileHandler


class logger():
    variable_object = None
    logger = None

    def __init__(self, variable):
        #init variable object
        self.variable_object = variable

        if(not os.path.isdir("logs")):
            os.mkdir("logs")

        self.logger = logging.getLogger('general_logger')


    def start(self, level):
        if(level=="DEBUG"):
            level = logging.DEBUG
        elif(level=="INFO"):
            level = logging.INFO
        elif(level=="ERROR"):
            level = logging.ERROR

        #Set logger levels
        self.logger.setLevel(level)

        # create file handler which logs all messages
        file_handler = TimedRotatingFileHandler('logs/general_logs.log', when="midnight", interval=1)
        file_handler.setLevel(level)

        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        #adder handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info("___________.__             ____________________.___  ___________")
        self.logger.info("\__    ___/|  |__   ____   \______   \______   \   | \_   _____/__________  ____   ____")
        self.logger.info("  |    |   |  |  \_/ __ \   |       _/|     ___/   |  |    __)/  _ \_  __ \/ ___\_/ __ \ ")
        self.logger.info("  |    |   |   Y  \  ___/   |    |   \|    |   |   |  |     \(  <_> )  | \/ /_/  >  ___/")
        self.logger.info("  |____|   |___|  /\___  >  |____|_  /|____|   |___|  \___  / \____/|__|  \___  / \___  >")
        self.logger.info("                \/     \/          \/                     \/             /_____/      \/")
