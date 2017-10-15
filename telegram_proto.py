# -*- coding: utf-8 -*-
from common_proto import *
import requests


class Telebot:
    def __init__(self):
        config = Config()
        self.proxy = config.proxyMode
        self.offset = 0
        self.TOKEN = config.TelegramToken
        self.URL = config.Telegram_URL
        if self.proxy:
            self.proxies = config.proxies
        self.chat_id = config.TELEGRAM_ADMIN
        if not self.proxy:
            log_event("Telebot init completed, host: " + get_host())
        else:
            log_event("Telebot init completed with proxy, host: " + get_host())

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
        parametersList = []
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
            parametersList.append(telegram_mes)
            '''
            What a heck below?
            try:
                log_event('from %s (id%s): "%s" with author: %s; time:%s' % telegram_mes)
            except:
                pass
            '''
        return parametersList