import requests
import os 
from dotenv import load_dotenv
load_dotenv()
import json

t = 0
last_update_id = 0
token = os.getenv('TOKEN')
my_chat_id = str(os.getenv('MY_CHAT_ID'))
url = "https://api.telegram.org/bot{}/".format(token)
states = { my_chat_id : 0}

def send_message(id, text, reply_markup = ""):
    r = requests.get(url + 'sendMessage?chat_id={}&text={}&reply_markup={}'.format(id, text,reply_markup))
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
        update_id = data['update_id']
        u = {}
        if 'message' in data:
            msg = data['message']
            msg_id = msg['message_id']
            u['name'] = msg['from']['username']
            u['id'] = msg['from']['id'] 
            if 'text' in msg:
                u['data'] = msg['text']

            if 'sticker' in msg:
                u['data'] = msg['sticker']

        if 'callback_query' in data:
            call_back = data['callback_query']
            u['data'] = call_back['data']
            u['name'] = call_back['from']['username']
            u['id'] = call_back['from']['id'] 

        
        return u, update_id 
    else: 
        return 0, 0

def check_state(id): #database for states
    return states[str(id)] 

def change_state(id, st): 
    states[str(id)] = st

def send_menu(id):
    send_message(id, "Menu", '{%22keyboard%22:[[{%22text%22:%22read%22}],[{%22text%22:%22my+score%22}]]}')

def descypt_message(u):
    state = check_state(u['id'])
    print(state, u['data'])
    if state == 0 :
        if u['data'] == 'read' : 
            reply_markup = '{%22inline_keyboard%22%20:%20%0A%20%20%20%20[%0A%20%20%20%20%20%20%20%20[%0A%20%20%20%20%20%20%20%20%20%20%20%20{%22text%22:%20%2210%22,%22callback_data%22:%20%2210%22},%20%0A%20%20%20%20%20%20%20%20%20%20%20%20{%22text%22:%20%2220%22,%22callback_data%22:%20%2220%22}%0A%20%20%20%20%20%20%20%20],%0A%20%20%20%20%20%20%20%20[%0A%20%20%20%20%20%20%20%20%20%20%20%20{%22text%22:%20%2230%22,%22callback_data%22:%20%2230%22},%20%0A%20%20%20%20%20%20%20%20%20%20%20%20{%22text%22:%20%2240%22,%22callback_data%22:%20%2240%22}%0A%20%20%20%20%20%20%20%20]%0A%20%20%20%20]%0A}'
            send_message(u['id'], "how much time", reply_markup)
            change_state(u['id'], 10)

    if state == 10 : 
        if u['data'] != 'read' : # check it is time 
            print(u['data'])
            send_message(u['id'], "save your time {} min".format(u['data']))
            change_state(u['id'], 0)
            send_menu(u['id'])

        else:  
            send_message(u['id'], "something go wrong send another time") 
    

while 1 :
    update = get_last_update(url)
    u, update_id = decryption_update_data(update)
    if update_id != last_update_id:
        last_update_id = update_id
        descypt_message(u)
        




#data1 = data['result'].pop()
#print("{}\n".format(data['result'])) 
#print("{}\n".format(data1)) 