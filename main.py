from telegram_proto import Telebot
from vk_proto import VKbot
from sqlite_proto import Cash
from common_proto import Message, log_event
import time


def parse_mes(vk_response):
    unread_mes = []
    for message in vk_response['response'][1:]:
        mes_text = message['body'].encode('utf-8')
        mes_id = message['mid']
        user_id = message['uid']
        if message['read_state'] == 0 and 'chat_id' not in message:
            if cashDB.check_message(mes_id):
                continue
            else:
                cashDB.add_message(mes_id, mes_text)
                username = cashDB.check_user(user_id)
                if not username:
                    username = vk_bot.get_user(user_id)
                    cashDB.add_user(user_id, username)
                try:
                    unread_mes.append(Message(mes_text, username.encode('utf-8')))
                except:
                    unread_mes.append(Message(mes_text, username))
    if not unread_mes:
        log_event('no new mes')
    return unread_mes

def exit_check(update_list):
    if update_list:
        for message in update_list:
            if message['body'] =='exit':
                return True
    return False

if __name__ == "__main__":
    vk_bot = VKbot()
    cashDB = Cash()
    telegram_bot = Telebot()
    while True:
        try:
            update_list = telegram_bot.get_updates()
            if exit_check(update_list):
                telegram_bot.send_text(telegram_bot.chat_id, "EXIT COMMAND")
                log_event("EXIT COMMAND")
                telegram_bot.get_updates() #dirty hack (without this, foreverexit)
                break
            for mes in parse_mes(vk_bot.get_mes()):
                telegram_bot.send_text(telegram_bot.chat_id, str(mes))
            time.sleep(vk_bot.interval)
        except Exception as e:
            log_event(e)