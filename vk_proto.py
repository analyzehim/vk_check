# -*- coding: cp1251 -*-

from common_proto import log_event, get_host
import xml.etree.ElementTree as ET
import requests
COUNT = 10
INTERVAL = 10

class VkBot:
    def __init__(self):
        tree = ET.parse('private_config.xml')
        root = tree.getroot()
        self.vk_token = root.findall('vk_token')[0].text
        self.URL = 'https://api.vk.com/method/'
        self.count = COUNT
        self.interval = INTERVAL
        self.chat_id = root.findall('vk_id')[0].text
        self.ignoring_chats = root.findall('ignor_chats')[0].text.split(';')
        self.host = get_host()
        proxy_url = root.findall('proxy')[0].text
        self.proxies = {"http": proxy_url,"https": proxy_url}
        try:
            requests.get('https://www.ya.ru')
            self.proxy = False
        except:
            proxies = self.proxies
            requests.get('https://www.ya.ru', proxies=self.proxies)
            self.proxy = True

        if not self.proxy:
            log_event("VkBot Init completed, host: " + self.host)
        if self.proxy:
            log_event("VkBot Init completed with proxy, host: " + self.host)

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


    def get_chat(self, chat_id):
        log_event('get chat {0}'.format(chat_id))  # Logging
        if not self.proxy:
            request = requests.get(self.URL +
                                   'messages.getChat?access_token={0}&chat_id={1}'.format(self.vk_token, chat_id)
                                   ) # HTTP request
        else:
            request = requests.get(self.URL +
                                   'messages.getChat?access_token={0}&chat_id={1}'.format(self.vk_token, chat_id),
                                    proxies=self.proxies)  # HTTP request with proxy
        if not request.status_code == 200:
            log_event(request.text)
            return []
        print request.json()
        chatname = request.json()['response']['title'].encode('utf-8')
        name = '{0}'.format(chatname)
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


class VkMessage:
    def __init__(self, text='', user='', chat=''):
        self.text = text
        self.user = user
        self.chat = chat
        if self.chat:
            self.str = '{0}:{1}: {2}'.format(self.chat, self.user, self.text)
        else:
            self.str = '{0}: {1}'.format(self.user, self.text)

    def __str__(self):
        return self.str

    def __len__(self):
        return len(self.str)
