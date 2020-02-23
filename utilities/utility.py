import sys

#funtion to handle input arguments
def handle_arguments():
    log_level = "ERROR"
    led_level = "LIVE"
    try:
        for arg_number in len(sys.argv):
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
            else:
                raise Exception('Invlaid Option')
    except:
        print("{} is not a valid arguments. Please check README for valid options".format(sys.argv[arg_number]))
    argument_dictionary = {
        'log_level':log_level,
        'led_level':led_level
    }

    return argument_dictionary
