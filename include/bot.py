import slack
import string
import traceback
import datetime
import logging


from .luis import * 
from .rpi_handler import rpi_handler
from .network import *
from .google_calendar import *



class door_bot:
    #slack information
    slack_client=None
    slack_token=None
    
    #user file
    user_file=None
    user_information={}
    
    #raspberry pi handler
    rpi_handler = None
    
    #logging
    logger = None

    #helper variables
    string_translator = str.maketrans('', '', string.punctuation)
    
    #calendar specifically for slack api/users
    update_calendar = None
    
    def __init__(self, token, user_file, red_pin,green_pin,blue_pin,input_1,input_2, input_3,input_4):
        #initalize logging
        self.logger = logging.getLogger('rpi_logger')


        #Initalize slack client
        self.slack_token=token
        self.slack_client = slack.WebClient(token=token)
        self.logger.info('started slack client')
        
        #read in personal data
        self.user_file = user_file
        self.read_data(user_file)

        #start threas
        self.rpi_handler = rpi_handler(red_pin,green_pin,blue_pin,input_1,input_2,input_3,input_4)
        self.rpi_handler.start()
        
        #init calendar
        self.update_calendar = calendar()
        
        
   
    #################### SLACK SEND METHODS #######################################
    #function to send slack message
    def slack_send_message(self,channel, message):
        self.logger.info('sent message: '+str(message)+' in channel:' + str(channel))
        self.slack_client.chat_postMessage(channel=channel,as_user=False,link_names=1,text=message)

    
    
    
    #################### SLACK ACCESSOR METHODS #######################################   
    def slack_get_user(self,userid):
        #setup slack paramaters
        slack_params = {
            'token':self.slack_token,
            'user':userid
        }
        #get message
        response = get(URL = "https://slack.com/api/users.info", PARAMS = slack_params)
        
        if(response['ok']):  
            return response['user']['name']
        else:
            return "default_name"
            
    ########################## BOT FUNCTIONS ############################################
    def color_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        try:
            self.rpi_handler.color_mode = 'override'
            self.rpi_handler.led_strip.set_color(entities['color_type'])
            self.slack_send_message(channel,"@"+str(user)+" the door is now "+str(entities['color_type']))
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            self.slack_send_message(channel,"@"+str(user)+" "+str(entities['color_type'])+" is not a color I support")
    
    
    def color_question_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        self.slack_send_message(channel,"@"+str(user)+" the door is currently "+str(self.rpi_handler.led_strip.current_color))
    
    def introduction_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        user_info = self.get_user(slack_data['user'])
        if(user_info == ''):
            file = open(self.user_file,"a+")
            file.write(str(user)+","+entities['user_name']+"\n")
            self.user_information[str(user)] = entities['user_name']
            file.close()
            self.slack_send_message(channel,"@"+str(user)+" we have now been introduced!")
        else:
            self.slack_send_message(channel,"@"+str(user)+" we've already been introduced! I think you're "+str(user_info))
            
    def reset_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        self.rpi_handler.color_mode = 'calendar'
        self.rpi_handler.led_strip.set_color(self.rpi_handler.calendar_color)
        self.slack_send_message(channel,"@"+str(user)+" the door is now based on the calendar")
        
    def hour_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        
        #get user information
        user_info = self.get_user(slack_data['user'])
        
        #see if user exitst
        if(user_info == ''):
            self.slack_send_message(channel,"@"+str(user)+" please introduce yourself to me before you try to change your hours!.")
            return
        
        #replace article value with letter
        try:
            if(entities['hour_value']=='a' or entities['hour_value']=='an'):
                entities['hour_value']=1
        except:
            pass
        
        #see if calendar is running
        self.update_calendar.running = True   
        #handle data
        if("hour_value" in entities):
            if(entities['hour_type']=='late'):
                self.update_calendar.change_hours(str(user_info), str(entities['hour_name']), int(entities['hour_value']))
                self.slack_send_message(channel,"@"+str(user)+" the calendar and door is now updated to show that you will be "+str(entities['hour_value'])+" "+str(entities['hour_name'])+" "+str(entities['hour_type'])+" to your hours.")
            if(entities['hour_type']=='early'):
                self.update_calendar.change_hours(str(user_info), str(entities['hour_name']), -int(entities['hour_value']))
                self.slack_send_message(channel,"@"+str(user)+" the calendar and door is now updated to show that you will be "+str(entities['hour_value'])+" "+str(entities['hour_name'])+" "+str(entities['hour_type'])+" to your hours.")
            if(entities['hour_type']=='miss'):
                self.update_calendar.cancel_hours(user_info)
                self.slack_send_message(channel,"@"+str(user)+" the calendar and door is now updated to show that you will miss your hours.")
        else:
            if(entities['hour_type']=='late'):
                self.update_calendar.change_hours(str(user_info), 'minutes', int(15))
                self.slack_send_message(channel,"@"+str(user)+" the calendar and door is now updated to show that you will be 15 minutes late to your hours. This is the default value")
            if(entities['hour_type']=='early'):
                self.update_calendar.change_hours(str(user_info), 'minutes', -15)
                self.slack_send_message(channel,"@"+str(user)+" the calendar and door is now updated to show that you will be 15 minutes early to your hours. This is the default value")
            if(entities['hour_type']=='miss'):
                self.update_calendar.cancel_hours(user_info)
                self.slack_send_message(channel,"@"+str(user)+" the calendar and door is now updated to show that you will miss your hours.")
        self.update_calendar.running = False 
        
    def hour_question_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        
        #get user information
        user_info = self.get_user(slack_data['user'])
        
        #see if user exitst
        if(user_info == ''):
            self.slack_send_message(channel,"@"+str(user)+" please introduce yourself to me before you try to change your hours!.")
            return
        self.update_calendar.running = True
        next_event = self.update_calendar.get_next_user_event(user_info)
        self.update_calendar.running = False
        print(next_event)
        
        start_time = datetime.datetime.strptime(next_event['start']['dateTime'][:16],'%Y-%m-%dT%H:%M')
        end_time = datetime.datetime.strptime(next_event['end']['dateTime'][:16],'%Y-%m-%dT%H:%M')
        
        self.slack_send_message(channel,"@"+str(user)+" your next hours are on "+start_time.strftime("%m-%d-%Y")+" from "+ start_time.strftime("%H:%M")+" to "+end_time.strftime("%H:%M"))
        
    
    def ip_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        self.slack_send_message(channel,"@"+str(user)+" the raspberry pi is located at "+str(get_ip()))
            
    def calendar_question_command(self,slack_data,entities):
        user = slack_data['original_user']
        channel = slack_data['channel']
        

        current_events = self.update_calendar.get_current_events()
        if(current_events!=[]):
            
            if(len(current_events) == 1):
                self.slack_send_message(channel,"@"+str(user)+" "+str(current_events[0]['name'])+" is the current volunteer on duty")
            else:
                output_names = current_events[0]['name']
                for number in range(len(current_events)):
                    if(number == 0):
                        continue
                        
                    if(number == len(current_events)-1):
                        output_names = output_names + ', and ' + str(current_events[number]['name'])
                    else:
                        output_names = output_names + ', ' + str(current_events[number]['name'])
                
                self.slack_send_message(channel,"@"+str(user)+" the current volunteers on duty are: "+output_names)   

        else:
            self.slack_send_message(channel,"@"+str(user)+ "noone is currently on duty :(")

    def process_command(self,input):
        print("processing command")
        try:
            if(input['data']['intent']=="Color"):
                self.color_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Color_Question'):
                self.color_question_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Introduction'):
                self.introduction_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Hour'):
                self.hour_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Hour_Question'):
                self.hour_question_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Reset'):
                self.reset_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Ip_Question'):
                self.ip_command(input['slack_data'],input['data']['entities'])
            elif(input['data']['intent']=='Calendar_Question'):
                self.calendar_question_command(input['slack_data'],input['data']['entities'])
                
                
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            self.logger.error('Command error. Luis data:'+str(input['data']))
            self.slack_send_message(input['slack_data']['channel'],"@"+str(input['slack_data']['original_user'])+" I got your message but couldn't quite reply, sorry")
            
            
    def handle_message(self,incoming_data):
        try:
            print(incoming_data['channel'])
            if(not "<@UPENFEMDM>" in  incoming_data['text']):
                return
            if("GP6M8KPAM"!=incoming_data['channel'] and "G7X672W82"!=incoming_data['channel']):
                return
        except:
            self.logger.error('invalid message')
            return
        
        
        incoming_message = str(incoming_data['text']).replace("<@UPENFEMDM>","")
        incoming_message = incoming_message.translate(self.string_translator)
        
        output = luis_send(incoming_message)
        
        incoming_data['original_user']=self.slack_get_user(incoming_data['user']) 
        self.process_command({'data':output,'slack_data':incoming_data})
        
    ####################################### HELPER FUNCTIONS #################################################
    def read_data(self,file):
        try:
            with open(file) as input_file:
                for line in input_file:  
                    input_array = line.split(',')
                    self.user_information[input_array[0].rstrip()]=input_array[1].rstrip()
        except Exception as exp:
            traceback.print_exc()
            self.logger.error("unable to read in user data")
            
            
    def get_user(self, username):
        try:
            output = self.user_information[username]
        except:
            output = ''
        
        return output
        
        
    
        
        
        
