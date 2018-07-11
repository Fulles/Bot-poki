import sys
sys.path.insert(0, '../')

import data
import time
import vk_api
from datetime import datetime
import att
from lxml import html
import random
import requests
login, password, my_id = data.data()
vk_ses = vk_api.VkApi(login, password)
vk_ses.auth()
del login, password
global vk
vk = vk_ses.get_api()
tm = datetime.now()

def anekdot_sender(item):

    response = requests.get('http://olikart.blogspot.com/2011/09/blog-post_23.html')
    tree = html.fromstring(response.content)
    text = tree.xpath('//*[@id="post-body-2655186918807662008"]/div[1]/text()')
    count = 0
    anekdots = []
    anekdot = ''

    while count < len(text):

        try:
            if len(text[count]) > 1:
                while len(text[count]) > 1:
                    anekdot = anekdot + text[count]
                    count += 1
                anekdots.append(anekdot)
                anekdot = ''

            if len(text[count]) >= 1:
                count += 1

        except:
            pass

    num = random.randint(0, len(anekdots))
    anekdot_ready = anekdots[num]
    vk_ses.method('messages.send', {'user_id': item['user_id'], 'message': anekdot_ready})


def choice_group_and_send(mas,response,item,vk_ses,id_group):
    mas.index(response)
    print(item)
    attachment = att.get_photos(vk_ses, id_group, vk)
    write_msg(item['user_id'], 'Ну только если для тебя=)', attachment)

def write_msg(user_id, s, att):
    vk_ses.method('messages.send', {'user_id':user_id, 'message':s, 'attachment':att})

def picture_bot():
    values = {'out': 0, 'count': 10, 'time_offset': 15}
    dog = ['пёсель', 'собака', 'пёс', 'doge', 'песель', 'псина', 'пёсели', 'песели', 'псины', 'пёсики', 'песики', 'пес']
    loli = ['лоли', 'лольки', 'loli', 'лолька', 'лоля', 'лоликон', 'lolikon']
    anek = ['анекдот', 'шутейка', 'анек']
    id_group_dog = -152487270
    id_group_loli = -127518015

    try:
        response = vk_ses.method('messages.get', values)

        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            response = response['items'][0]['body'].lower()
            if response == 'writeron' and item['user_id'] == my_id:
                vk_ses.method('messages.send', {'user_id': my_id, 'message': 'bot is on'})
            if anek.index(response) >= 0:
                anekdot_sender(item)
            try:
                choice_group_and_send(dog, response, item, vk_ses, id_group_dog)
                ids = open('ids.txt', 'a')
                ids.write('Peseli were used ' + str(tm) + '  by ' + str(item['user_id']) + '\n')
                ids.close()
            except:
                try:
                    choice_group_and_send(loli, response, item, vk_ses, id_group_loli)
                    ids = open('ids.txt', 'a')
                    ids.write('Loli were used ' + str(tm) + '  by ' + str(item['user_id']) + '\n')
                    ids.close()
                except:
                    pass

        time.sleep(2)

    except:
        pass

def process():
    longPoll = vk_ses.method('messages.getLongPollServer')
    server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
    print(server, key, ts)
    while True:
        response = requests.get(
            'https://' + str(server) + '?act=a_check&key=' + str(key) + '&ts=' + str(ts) + '&wait=25&mode=2&version=2 ')
        json = response.json()
        ts = json['ts']
        event = json['updates']
        if len(event) >= 1:
            try:
                if event[0][0] == 4:

                    picture_bot()
            except:
                pass

process()

