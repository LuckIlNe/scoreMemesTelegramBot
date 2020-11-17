import requests
import os 
from dotenv import load_dotenv
load_dotenv()
import json


jo = `{"inline_keyboard" : 
    [
        [
            {"text": "10","callback_data": "10"}, 
            {"text": "20","callback_data": "20"}
        ],
        [
            {"text": "30","callback_data": "30"}, 
            {"text": "40","callback_data": "40"}
        ]
    ]
}`

t = 0
last_message_id = 0
token = os.getenv('TOKEN')
my_chat_id = str(os.getenv('MY_CHAT_ID'))
url = "https://api.telegram.org/bot{}/".format(token)
states = { my_chat_id : 0}

def send_message(u, text):
    j = ""
    r = requests.get(url + 'sendMessage?chat_id={}&text={}&reply_markup={}'.format(u['id'], text, j))
    print(r.status_code)
    return 1

def get_last_update(request):
    response = requests.get(request + 'getUpdates?' + "offset={}&limit={}".format(-1, 1))
    data = response.json()
    #result = data['result']
    return data

def decryption_update_data(res): 
    if res['result']: 
        data = res['result'].pop()
        msg = data['message']
        msg_id = msg['message_id']
        u = {}
        u['name'] = msg['from']['username']
        u['id'] = msg['from']['id'] 
        if 'text' in msg:
            u['data'] = msg['text']

        if 'sticker' in msg:
            u['data'] = msg['sticker']

        return u, msg_id
    else: 
        return 0, 0

def check_state(id): #database for states
    return states[str(id)] 

def change_state(id, st): 
    states[str(id)] = st

def descypt_message(u):
    state = check_state(u['id'])
    print(state, u['data'])
    if state == 0 :
        if u['data'] == 'read' : 
            send_message(u, "how much time")
            change_state(u['id'], 10)

    if state == 10 : 
        if u['data'] != 'read' : # check it is time 
            print(u['data'])
            send_message(u, "save your time {} min".format(u['data']))
            change_state(u['id'], 0)

        else:  
            send_message(u, "something go wrong send another time") 
    

while 1 :
    update = get_last_update(url)
    print(update)
    u, msg_id = decryption_update_data(update)
    if msg_id != last_message_id:
        last_message_id = msg_id
        descypt_message(u)
        




#data1 = data['result'].pop()
#print("{}\n".format(data['result'])) 
#print("{}\n".format(data1)) 