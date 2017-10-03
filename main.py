from telegram_proto import Telebot
from vk_proto import VKbot
from sqlite_proto import Cash
from common_proto import Message, log_event

import time

def parse_mes(vk_response):
    not_read_mes = []
    for mes in vk_response['response'][1:]:
        mes_text = mes['body'].encode('utf-8')
        mes_id = mes['mid']
        user_id = mes['uid']
        if mes['read_state'] == 0 and not 'chat_id' in mes:
            if cash.check_message(mes_id):
                continue
            else:
                cash.add_message(mes_id, mes_text)
                username = cash.check_user(user_id)
                if not username:
                    username = vkbot.get_user(user_id)
                    cash.add_user(user_id, username)
                try:
                    not_read_mes.append(Message(mes_text, username.encode('utf-8')))
                except:
                    not_read_mes.append(Message(mes_text, username))
    if not_read_mes == []:
        log_event('no new mes')
    return not_read_mes

if __name__ == "__main__":
    vkbot = VKbot()
    cash = Cash()
    telebot = Telebot()

    #vkbot.send_text(vkbot.chat_id, "Run on {0}".format(vkbot.host))
    #telebot.send_text(telebot.chat_id, "Run on {0}".format(telebot.host))
    while (True):
        try:
            for mes in parse_mes(vkbot.get_mes()):
                telebot.send_text(telebot.chat_id, str(mes))
            time.sleep(vkbot.interval)
        except Exception as e:
            log_event(e)

