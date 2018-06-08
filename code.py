import sys
sys.path.insert(0, '../')

import data
import time
import vk_api
from datetime import datetime
import att

login, password = data.data()
vk_ses = vk_api.VkApi(login, password)
vk_ses.auth()
del login, password
global vk
vk = vk_ses.get_api()
tm = datetime.now()

values = {'out':0, 'count':10, 'time_offset':3}
response = vk_ses.method('messages.get', values)

def choice_group_and_send(mas,response,item,vk_ses,id_group):
    mas.index(response)
    print(item)
    attachment = att.get_photos(vk_ses, id_group, vk)
    write_msg(item['user_id'], 'Ну только если для тебя=)', attachment)

def write_msg(user_id, s, att):
    vk_ses.method('messages.send', {'user_id':user_id, 'message':s, 'attachment':att})

dog = [ 'пёсель','собака','пёс','doge','песель','псина','пёсели','песели','псины','пёсики','песики', 'пес']
loli = ['лоли','лольки','loli','лолька','лоля','лоликон','lolikon']
id_group_dog = -152487270
id_group_loli = -127518015

while True:
    try:

        response = vk_ses.method('messages.get', values)
        if response['items']:

            values['last_message_id'] = response['items'][0]['id']
            print(values['last_message_id'])
            print(response['items'][0])
        for item in response['items']:
            response = response['items'][0]['body'].lower()
            try:
                choice_group_and_send(dog, response, item, vk_ses, id_group_dog)
                ids = open('ids txt', 'a')
                ids.write('Peseli were used ' + str(tm) + '  by ' + str(item['user_id']) + '\n')
                ids.close()
            except:
                try:
                    choice_group_and_send(loli, response, item, vk_ses, id_group_loli)
                    ids = open('ids txt', 'a')
                    ids.write('Loli were used ' + str(tm) + '  by ' + str(item['user_id']) + '\n')
                    ids.close()
                except:
                    pass

        time.sleep(2)

    except:

        pass


