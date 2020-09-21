#import for slack
import slack
import os
import string
from utilities.general_helpers.luis import luis_send

class slack_bot:
    #variable object
    variable_object = None

    #slack object
    slack_object = None

    #logger
    logger = None

    #message translator
    string_translator = str.maketrans('', '', string.punctuation)

    ###### INIT FUNCTIONS ######
    def __init__(self, variable ,user_file="static/user_file.txt"):
        #init variable object and set to global to allow handle_slack_payload to access it
        global variable_object_global
        variable_object_global = variable
        self.variable_object = variable

        #get token from
        try:
            slack_token = os.environ["SLACK_API_TOKEN"]
            self.slack_object = slack.RTMClient(token=slack_token)
        except:
            print("Invalid Slack Token SLACK_API_TOKEN must be set")
            exit()

        self.logger = self.variable_object.logger_class.logger
        self.logger.info("Initialized Slack class")


    def start(self):
        self.slack_object.start()


    def handle_message(self,data,web_client,rtm_client):
        try:
            if(not "<@UPENFEMDM>" in  data['text']):
                return
            #if("GP6M8KPAM"!=data['channel'] and "G7X672W82"!=data['channel']):
            #    return
        except:
            self.logger.error('Invalid message type [name/location check]')
            return


        channel_id = data['channel']
        incoming_user = data['user']

        incoming_message = str(data['text']).replace("<@UPENFEMDM>","")
        incoming_message = incoming_message.translate(self.string_translator)
        self.logger.info("Message Received:"+incoming_message)

        luis_output = luis_send(incoming_message)

        response = self.variable_object.message_handler.parse_command(luis_output,data)
        formated_response = "TEST <@{}> {}".format(incoming_user,response)

        web_client.chat_postMessage(
            channel=channel_id,
            text=formated_response,
        )

        self.logger.info("Message Sent: "+formated_response)








    @slack.RTMClient.run_on(event='message')
    def handle_slack_payload(**payload):
        data = payload['data']
        web_client = payload['web_client']
        rtm_client = payload['rtm_client']
        variable_object_global.slack_class.handle_message(data,web_client,rtm_client)
