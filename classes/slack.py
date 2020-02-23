#import for slack
import slack
import threading
import os


class slack_bot:
    #variable object
    variable_object = None

    #slack object
    slack_object = None

    #logger
    logger = None

    ###### INIT FUNCTIONS ######
    def __init__(self, variable ,user_file="static/user_file.txt"):
        #init variable object
        global variable_object_global
        variable_object_global = variable
        self.variable_object = variable

        slack_token = os.environ["SLACK_API_TOKEN"]
        self.slack_object = slack.RTMClient(token=slack_token)

        self.logger = self.variable_object.logger_class.logger
        self.logger.info("Initialized Slack class")


    def start(self):
        self.slack_object.start()

    














    @slack.RTMClient.run_on(event='message')
    def handle_slack_payload(**payload):
        data = payload['data']
        web_client = payload['web_client']
        rtm_client = payload['rtm_client']
        variable_object_global.slack_class.handle_message(data,web_client,rtm_client)
