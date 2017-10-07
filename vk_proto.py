# -*- coding: cp1251 -*-

from common_proto import *
import requests


class VKbot:
    def __init__(self):
        config = Config()
        self.proxy = config.Mode
        if self.proxy:
            self.proxies = config.proxies
        self.vk_token = config.VkToken
        self.host = config.host
        self.URL = config.VK_URL
        self.count = config.count
        self.chat_id = config.VK_EUGENE_ID
        self.interval = config.interval
        if not self.proxy:
            log_event("VKbot Init completed, host: " + str(self.host))
        if self.proxy:
            log_event("VKbot Init completed with proxy, host: " + str(self.host))

    def send_text(self, chat_id, text):
        log_event('VK sending to %s: %s' % (chat_id, text))  # Logging
        if not self.proxy:
            request = requests.get(self.URL +
                                   'messages.send?access_token={0}&user_id={1}&message={2}'.format(self.vk_token, chat_id, text)) # HTTP request
        else:
            request = requests.get(self.URL +
                                   'messages.send?access_token={0}&user_id={1}&message={2}'.format(self.vk_token, chat_id, text),
                                    proxies=self.proxies)  # HTTP request with proxy
        if not request.status_code == 200:
            log_event('ERROR:' + request.text)
            return False
        return True

    def get_user(self, user_id):
        log_event('get user {0}'.format(user_id))  # Logging
        if not self.proxy:
            request = requests.get(self.URL +
                                   'users.get?access_token={0}&user_ids={1}'.format(self.vk_token, user_id)
                                   ) # HTTP request
        else:
            request = requests.get(self.URL +
                                   'users.get?access_token={0}&user_ids={1}'.format(self.vk_token, user_id),
                                    proxies=self.proxies)  # HTTP request with proxy
        if not request.status_code == 200:
            log_event(request.text)
            return []

        print request.json()
        first_name = request.json()['response'][0]['first_name'].encode('utf-8')
        last_name = request.json()['response'][0]['last_name'].encode('utf-8')
        name = '{0} {1}'.format(first_name, last_name )
        return name

    def get_mes(self):
        log_event('VK get messages')  # Logging
        if not self.proxy:
            request = requests.get(self.URL +
                                   'messages.get?access_token={0}&count={1}'.format(self.vk_token, self.count)) # HTTP request

        else:
            request = requests.get(self.URL +
                                   'messages.get?access_token={0}&count={1}'.format(self.vk_token, self.count),
                                    proxies=self.proxies)  # HTTP request with proxy
        if not request.status_code == 200:
            log_event(request.text)
            return []
        return request.json()