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
        try:
            log_event('VK sending to %s: %s' % (chat_id, text))  # Logging
        except:
            log_event('Error with LOGGING')

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
        try:
            log_event('get user {0}'.format(user_id))  # Logging
        except:
            log_event('Error with LOGGING')
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
        try:
            log_event('VK get messages')  # Logging
        except:
            log_event('Error with LOGGING')

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

'''




f = open("cash2", "wb")
pickle.dump(r.json(), f)
f.close()

access_token = getVkToken()
proxies = getProxies()
r = requests.get('https://api.vk.com/method/messages.get?count={0}&access_token={1}'.format(10, access_token),proxies=proxies)
print r.text


f = open("cash2", "rb")
ans_dict = pickle.load(f)
f.close()


for mes in ans_dict['response'][1]['fwd_messages']:
    download_jpg(get_photo(mes['attachment']))
    for attach in mes['attachments']:
        download_jpg(get_photo(attach))

'''



#https://oauth.vk.com/authorize?client_id=4904805&scope=friends,offline,photos,audio,video,docs,notes,pages,wall,groups,messages&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token

