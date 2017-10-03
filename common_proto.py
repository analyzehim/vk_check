# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import socket
import requests
import time
import datetime


def human_time(date):
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')


def unix_time(day, month, year, hour=0, minute=0, second=0):
    return time.mktime(datetime.datetime(year, month, day, hour, minute, second).timetuple())


def get_time(operation_date, date):
    hour = date.split(':')[0]
    minute = date.split(':')[1]
    current_date = datetime.datetime.fromtimestamp(operation_date)
    return unix_time(int(current_date.day), int(current_date.month), int(current_date.year), int(hour), int(minute))


def log_event(text):
    f = open('log.txt', 'a')
    event = '%s >> %s' % (time.ctime(), text)
    print event + '\n'
    f.write(event+'\n')
    f.close()
    return


class Message:
    def __init__(self, text='', user=''):
        self.text = text.encode('utf-8')
        self.user = user

    def __str__(self):
        return '{0}: {1}'.format(self.user, self.text)


class Config:
    def __init__(self):
        tree = ET.parse('private_config.xml')
        root = tree.getroot()
        self.VkToken = root.findall('vk_token')[0].text
        self.TelegramToken = root.findall('telegram_token')[0].text
        self.TelegramTestToken = root.findall('telegram_test_token')[0].text
        proxy_url = root.findall('proxy')[0].text
        password = root.findall('proxy_password')[0].text
        proxy_url = proxy_url.replace("PASSWORD", password)
        self.proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        self.host = socket.getfqdn()
        try:
            requests.get('https://www.ya.ru')
            self.Mode = False
        except:
            proxies = self.proxies
            requests.get('https://www.ya.ru', proxies=proxies)
            self.Mode = True
        self.TELEGRAM_EUGENE_ID = 74102915  # My ID
        self.VK_EUGENE_ID = 9041600
        self.Telegram_URL = 'https://api.telegram.org/bot'  # HTTP Bot API URL
        self.VK_URL = 'https://api.vk.com/method/'
        tree = ET.parse('config.xml')
        root = tree.getroot()
        test = int(root.findall('test')[0].text)
        if test == 1:
            self.Test = True
        else:
            self.Test = False
