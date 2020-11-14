import requests
import os 
from dotenv import load_dotenv
load_dotenv()
import json


token = os.getenv('TOKEN')
url = "https://api.telegram.org/bot{}/".format(token)

def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def decryption_update_data(data): 
    result = data['result'].pop()
    msg = result['message']
    # username 
    # id 
    u = {}
    u['name'] = msg['from']['username']
    u['id'] = msg['from']['id'] 
    #text = result['message']['text']
    if 'text' in msg:
        u['data'] = msg['text']

    if 'sticker' in msg:
        u['data'] = msg['sticker']

    return u



update = get_updates_json(url)
print(decryption_update_data(update))


#data1 = data['result'].pop()
#print("{}\n".format(data['result'])) 
#print("{}\n".format(data1)) 