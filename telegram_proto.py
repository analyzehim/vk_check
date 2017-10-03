# -*- coding: utf-8 -*-
import requests

from common_proto import *


class Telebot:
    def __init__(self):
        config = Config()
        self.proxy = config.Mode
        self.test = config.Test
        if not self.test:
            self.TOKEN = config.TelegramToken
        else:
            self.TOKEN = config.TelegramTestToken
        self.URL = config.Telegram_URL
        if self.proxy:
            self.proxies = config.proxies
        self.chat_id = config.TELEGRAM_EUGENE_ID
        self.offset = 0
        self.host = config.host
        if not self.proxy:
            log_event("Telebot init completed, host: " + str(self.host))
        if self.proxy:
            log_event("Telebot init completed with proxy, host: " + str(self.host))

    def get_updates(self):
        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        if not self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data)
        if self.proxy:
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

            from_id = update['message']['chat']['id']  # Chat ID
            author_id = update['message']['from']['id']  # Creator ID
            message = update['message']['text']
            date = update['message']['date']
            try:
                name = update['message']['chat']['first_name']
            except:
                name = update['message']['from']['first_name']
            parameters = (name, from_id, message, author_id, date)
            parametersList.append(parameters)
            try:
                log_event('from %s (id%s): "%s" with author: %s; time:%s' % parameters)
            except:
                pass
        return parametersList

    def send_text_with_keyboard(self, chat_id, text, keyboard):
        try:
            log_event('Sending to %s: %s; keyboard: %s' % (chat_id, text, keyboard))  # Logging
        except:
            log_event('Error with LOGGING')
        json_data = {"chat_id": chat_id, "text": text,
                     "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True}}
        if not self.proxy:  # no proxy
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request

        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def send_text(self, chat_id, text):
        try:
            log_event('Telegram sending to %s: %s' % (chat_id, text))  # Logging
        except:
            log_event('Error with LOGGING')
        data = {'chat_id': chat_id, 'text': text}  # Request create
        if not self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            return False
        return request.json()['ok']  # Check API

    def ping(self):
        log_event('Sending to %s: %s' % (self.chat_id, 'ping'))
        data = {'chat_id': self.chat_id, 'text': 'ping'}
        if not self.proxy:
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        if self.proxy:
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy
