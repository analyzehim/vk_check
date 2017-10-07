# -*- coding: utf-8 -*-
from common_proto import *
import requests


class Telebot:
    def __init__(self):
        config = Config()
        self.proxy = config.proxyMode
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

    def ping(self):
        log_event('Sending to %s: %s' % (self.chat_id, 'ping'))
        data = {'chat_id': self.chat_id, 'text': 'ping'}
        if not self.proxy:
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request

        if self.proxy:
            requests.post(self.URL + self.TOKEN + '/sendMessage', data=data, proxies=self.proxies)  # HTTP with proxy
