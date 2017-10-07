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


def get_host():
    return str(socket.getfqdn())


def log_event(text):
    f = open('log.txt', 'a')
    event = '%s >> %s' % (time.ctime(), text)
    print event + '\n'
    f.write(event+'\n')
    f.close()
    return


class Message:
    def __init__(self, text='', user=''):
        self.text = text
        self.user = user
        self.str = '{0}: {1}'.format(self.user, self.text)

    def __str__(self):
        return self.str

    def __len__(self):
        return len(self.str)


class Config:
    def __init__(self):
        tree = ET.parse('private_config.xml')
        root = tree.getroot()
        self.VkToken = root.findall('vk_token')[0].text
        self.TelegramToken = root.findall('telegram_token')[0].text
        proxy = root.findall('proxy')[0].text
        self.proxies = {
            "http": proxy,
            "https": proxy,
        }
        try:
            requests.get('https://www.ya.ru')
            self.proxyMode = False
        except:
            proxies = self.proxies
            requests.get('https://www.ya.ru', proxies=proxies)
            self.proxyMode = True
        self.TELEGRAM_ADMIN = root.findall('telegram_id')[0].text
        self.Telegram_URL = 'https://api.telegram.org/bot'  # HTTP Bot API URL
        self.VK_URL = 'https://api.vk.com/method/'
        tree = ET.parse('config.xml')
        root = tree.getroot()
        self.count = int(root.findall('count')[0].text)
        self.interval = int(root.findall('interval')[0].text)
