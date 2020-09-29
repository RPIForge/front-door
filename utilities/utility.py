#argument import
import sys
import os

#network import
import socket
import requests
import json


#funtion to handle input arguments
def handle_arguments():
    log_level = "ERROR"
    led_level = "LIVE"
    log_time = 7

    try:
        #handle arguments
        skip_next = False
        for arg_number in range(1,len(sys.argv)):
            if(skip_next):
                skip_next = False
                continue

            if(sys.argv[arg_number] == '-d'):
                log_level = "DEBUG"
            elif(sys.argv[arg_number] == '-i'):
                log_level = "INFO"
            elif(sys.argv[arg_number] == '-e'):
                log_level = "ERROR"
            elif(sys.argv[arg_number] == '-live'):
                led_level = "LIVE"
            elif(sys.argv[arg_number] == '-debug'):
                led_level = "DEBUG"
            elif(sys.argv[arg_number] == '-t'):
                skip_next=True
                log_time = int(sys.argv[arg_number+1])
                
                
            else:
                raise Exception('Invlaid arugments')
    except:
        if(skip_next):
            print("{} is an incomplete argument. Please check README for valid options".format(sys.argv[arg_number]))
            raise Exception("Invalid arugments")
        else:  
            print("{} is not a valid arguments. Please check README for valid options".format(sys.argv[arg_number]))
            raise Exception("Invalid arugments")


    argument_dictionary = {
        'log_level':log_level,
        'led_level':led_level,
        'log_time':log_time
    }

    return argument_dictionary



#NETWORK COMMANDS
def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        sock.connect(('10.255.255.255', 1))
        IP = sock.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        sock.close()
    return IP

def post(URL=None, PARAMS=None, HEADERS=None,DATA=None):
    r = requests.post(URL, params=PARAMS, data=json.dumps(DATA), headers=HEADERS)
    return r.json()

def get(URL=None, PARAMS=None, HEADERS=None):
    r = requests.get(url=URL, params=PARAMS, headers=HEADERS)

    return r.json()

#FILE COMMANDS
def read_data(file):
    user_information = {}
    with open(file) as input_file:
        for line in input_file:
            input_array = line.split(',')
            user_information[input_array[0].rstrip()]=input_array[1].rstrip()

    return user_information


def get_user(self, username,user_information):
    try:
        output = user_information[username]
    except:
        output = ''

    return output
