from telegram_proto import Telebot
from vk_proto import VkBot
from sqlite_proto import Cash
from common_proto import VkMessage, log_event
import time

def get_attachment(vk_message):
    if 'attachment' in vk_message:
        if 'sticker' in vk_message['attachment']:
            if 'photo_512' in vk_message['attachment']['sticker']:
                return vk_message['attachment']['sticker']['photo_512']

        elif 'photo' in vk_message['attachment']:
            if 'src_big' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src_big']

    log_event("MESSAGE WITHOUT ATTACHMENT: " + str(vk_message))
    return ""



def get_unread_messages(vk_response):  # check vk, and return unread messages
    unread_mes = []
    for vk_message in vk_response['response'][1:]:

        mes_text = vk_message['body'].encode('utf-8')
        mes_id = vk_message['mid']
        user_id = vk_message['uid']
        if vk_message['read_state'] == 0 and 'chat_id' not in vk_message:  # if message is unread, and not in chat
            print vk_message
            if cashDB.check_message(mes_id):
                continue
            else:
                cashDB.add_message(mes_id, mes_text)
                username = cashDB.check_user(user_id)
                if not username:
                    username = vk_bot.get_user(user_id)
                    cashDB.add_user(user_id, username)
                if mes_text == '':
                    mes_text = get_attachment(vk_message)
                try:
                    unread_mes.append(VkMessage(mes_text, username.encode('utf-8')))
                except:  # dirty hack for russian letters
                    unread_mes.append(VkMessage(mes_text, username))
    if not unread_mes:
        log_event('no new mes')
    return unread_mes


def exit_check(update_list): # if you wanna terminate, just text exit to bot
    if update_list:
        for telegram_message in update_list:
            if telegram_message['text'] =='exit':
                return True
    return False


def mes_check(update_list):
    if not update_list:
        return False
    for telegram_message in update_list:
        if 'reply_mes' in telegram_message:
            recipient_name = telegram_message['reply_mes'].split(':')[0].encode('utf-8')
            mes_text = telegram_message['text'].encode('utf-8')
            return {'recipient_name': recipient_name, 'text': mes_text}
    return False


if __name__ == "__main__":
    vk_bot = VkBot()
    cashDB = Cash()
    telegram_bot = Telebot()
    while True:
        try:
            update_list = []
            while True:
                new_update = telegram_bot.get_updates()
                if new_update:
                    update_list += new_update
                else:
                    break  # this means, what no have new updates

            if exit_check(update_list):
                    telegram_bot.send_text(telegram_bot.chat_id, "EXIT COMMAND")
                    log_event("EXIT COMMAND")
                    break

            check_result = mes_check(update_list)
            if check_result:
                    recipient_id = cashDB.get_user_id(check_result['recipient_name'])
                    text = check_result['text']
                    vk_bot.send_text(recipient_id, text)

            for mes in get_unread_messages(vk_bot.get_mes()):
                    telegram_bot.send_text(telegram_bot.chat_id, str(mes))
            time.sleep(vk_bot.interval)
        except KeyboardInterrupt:
            print 'Interrupt by user..'
            break
        except Exception, e:
            log_event(str(e))
            

