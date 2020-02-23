class message_handler:
    variable_object = None

    def __init__(self, variable):
        #init variable object
        self.variable_object = variable
        self.variable_object.logger_class.logger.info("Initialized message handler")


    def color_command(self, luis_input,slack_data):
        try:
            self.variable_object.calendar_mode = 'override'
            self.variable_object.led_strip.set_color(luis_input['entities']['color_type'])
            return "the door is now "+str(luis_input['entities']['color_type'])
        except KeyError:
            self.variable_object.logger_class.logger.debug("Invalid luis message")
            return "That is not a valid color"
        except ValueError:
            self.variable_object.logger_class.logger.debug("Invalid color supplied")
            return "{} is not a valid color".format(luis_input['entities']['color_type'])

    def color_question_command(self, luis_input,slack_data):
        return "The Door is currently {}".format(self.variable_object.led_strip.current_color)

    def reset_command(self, luis_input,slack_data):
        self.variable_object.color_mode = "calendar"
        return "The Door is now based off the calendar"


    def parse_command(self, luis_input,slack_data):
        intent = luis_input['intent']
        try:
            if(intent=="Color"):
                return self.color_command(luis_input,slack_data)
            elif(intent=='Color_Question'):
                return self.color_question_command(luis_input,slack_data)
            #elif(intent=='Hour_Question'):
            #    self.hour_question_command(input['slack_data'],input['data']['entities'])
            elif(intent=='Reset'):
                return self.reset_command(luis_input,slack_data)
            elif(intent=='Ip_Question'):
                return self.ip_command(luis_input,slack_data)
            #elif(intent=='Calendar_Question'):
            #    self.calendar_question_command(input['slack_data'],input['data']['entities'])
            #elif(intent=='Introduction'):
            #    self.introduction_command(input['slack_data'],input['data']['entities'])
            #elif(intent=='Hour'):
            #    self.hour_command(input['slack_data'],input['data']['entities'])
            else:
                return "I'm sorry. I don't know what you mean by that"

        except Exception as exc:
            self.variable_object.logger_class.logger.error(exc, exc_info=True)
            self.variable_object.logger_class.logger.error('Command error. Luis data:'+str(luis_input))
            return("I got your message but couldn't quite reply, sorry")
