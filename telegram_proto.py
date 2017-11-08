# -*- coding: utf-8 -*-
from common_proto import log_event, get_host
import xml.etree.ElementTree as ET
import requests


class Telebot:
    def __init__(self):
        tree = ET.parse('private_config.xml')
        root = tree.getroot()
        self.offset = 0
        self.TOKEN = root.findall('telegram_token')[0].text
        self.URL = 'https://api.telegram.org/bot'
        self.chat_id = root.findall('telegram_id')[0].text
        proxy_url = root.findall('proxy')[0].text
        self.proxies = {"http": proxy_url,"https": proxy_url}
        self.host = get_host()
        try:
            requests.get('https://www.ya.ru')
            self.proxy = False
        except:
            proxies = self.proxies
            requests.get('https://www.ya.ru', proxies=self.proxies)
            self.proxy = True

        if not self.proxy:
            log_event("Telebot init completed, host: " + self.host)
        else:
            log_event("Telebot init completed with proxy, host: " + self.host)

    def send_text(self, chat_id, text):
        try:
            log_event('Telegram sending to %s: %s' % (chat_id, text))  # Logging
        except Exception as e:
            log_event('Error with LOGGING: {0}'.format(e))
        data = {'chat_id': chat_id, 'text': text}  # Request create
        if not self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def get_updates(self):
        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        if not self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data)
        else:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data, proxies=self.proxies)
        if (not request.status_code == 200) or (not request.json()['ok']):
            return False
        if not request.json()['result']:
            return
        update_list = []
        for update in request.json()['result']:
            self.offset = update['update_id']

            if 'message' not in update or 'text' not in update['message']:
                continue
            print "___"
            message = update['message']
            print message
            print "___"

            telegram_mes = {'author_name': message['from']['first_name'],
                            'chat_id': message['chat']['id'],
                            'text': message['text'],
                            'author_id': message['from']['id'],
                            'date': message['date'],
                            'update_id': self.offset}
            if 'reply_to_message' in message:
                telegram_mes['reply_mes'] = message['reply_to_message']['text']
                update_list.append(telegram_mes)
        return update_list
