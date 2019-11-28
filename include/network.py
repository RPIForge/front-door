import socket 
import requests
import json

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
    
