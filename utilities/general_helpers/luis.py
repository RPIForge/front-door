import requests
from utilities.utility import get

def luis_send(message):
    #luis endpoints
    luis_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b04ac42f-76da-4a12-b5fa-45de1a95401c"
    luis_key = "ee22c360b86d4589a80b09507d0946db"


    #send request
    luis_params = {
        "verbose":"false",
        "timezoneOffset":0,
        "subscription-key":luis_key,
        "log":True,
        "q":message
    }
    luis_response = get(URL = luis_url, PARAMS = luis_params)

    try:
        #format output
        output = {}
        output['intent'] = luis_response['topScoringIntent']['intent']
        output['entities'] = {}
        for entities in luis_response["entities"]:

            try:
                output['entities'][entities['type']] = entities['resolution']['values'][0]
            except:
                output['entities'][entities['type']] = entities['entity']


        return output
    except:
        return {}
