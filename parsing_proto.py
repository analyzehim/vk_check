from vk_proto import VkMessage, VkBot
from sqlite_proto import Cash
from common_proto import log_event
import time


def get_attachment(vk_message):  # get attachment (photo, sticker, forward messages)
    if 'attachment' in vk_message:
        if 'sticker' in vk_message['attachment']:
            if 'photo_512' in vk_message['attachment']['sticker']:
                return vk_message['attachment']['sticker']['photo_512']

        elif 'photo' in vk_message['attachment']:  # from higher resolution to lower
            if 'src_xxxbig' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src_xxxbig']
            elif 'src_xxbig' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src_xxbig']
            elif 'src_xbig' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src_xbig']
            elif 'src_big' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src_big']
            elif 'src' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src']
            elif 'src_small' in vk_message['attachment']['photo']:
                return vk_message['attachment']['photo']['src_small']
            else:
                log_event("IMAGE WITHOUT CORRECT SIZE: " + str(vk_message))
                return "IMAGE WITHOUT CORRECT SIZE"

        elif 'wall' in vk_message['attachment']:
            if 'text' in vk_message['attachment']['wall']:
                return vk_message['attachment']['wall']['text']
    elif "fwd_messages" in vk_message:
        print vk_message["fwd_messages"][0]
        if "body" in vk_message["fwd_messages"][0]:
            return "[FWD]: " + vk_message["fwd_messages"][0]["body"].encode('utf-8')
    else:
        log_event("MESSAGE WITHOUT ATTACHMENT: " + str(vk_message))
        return "WITHOUT ATTACHMENT"


def get_unread_messages(vk_bot, cashDB):  # check vk, and return unread messages
    vk_response = vk_bot.get_mes()
    unread_mes = []
    for vk_message in vk_response['response'][1:]:

        mes_id = vk_message['mid']

        if cashDB.check_message(mes_id):
            continue
        if vk_message['read_state'] != 0:
            continue
        mes_text = vk_message['body'].encode('utf-8')

        if 'chat_id' in vk_message:
            chat_id = vk_message['chat_id']
            chatname = vk_message['title'].encode('utf-8')
            if str(chat_id) in vk_bot.ignoring_chats:
                continue
            chat_id += 2000000000
            user_id = vk_message['uid']
            username = cashDB.check_user(user_id)
            if not username:
                username = vk_bot.get_user(user_id)
                cashDB.add_user(user_id, username)

            cashDB.add_chat(chat_id, chatname)

            if mes_text == '':
                mes_text = get_attachment(vk_message)
            try:
                unread_mes.append(VkMessage(mes_text, username.encode('utf-8'), chatname.encode('utf-8')))
            except:  # dirty hack for russian letters
                unread_mes.append(VkMessage(mes_text, username, chatname))
            cashDB.add_message(mes_id, mes_text)

        elif 'uid' in vk_message:
            user_id = vk_message['uid']
            if str(user_id) in vk_bot.ignoring_chats:
                continue
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
            cashDB.add_message(mes_id, mes_text)

        else:
            log_event('Strange mes {0}'.format(vk_message))


    if not unread_mes:
        log_event('no new mes')
    return unread_mes


def exit_check(update_list): # if you wanna terminate, just text exit to bot
    if update_list:
        for telegram_message in update_list:
            if telegram_message['text'] == 'exit':
                return True
    return False


def check_ans(update_list):
    if not update_list:
        return False
    ans_list = []
    for telegram_message in update_list:
        if 'reply_mes' in telegram_message:
            chat_info = telegram_message['reply_mes'].split(']')[0][1:]
            if ":" in chat_info:
                chat_type = "GROUP_CHAT"
                chatname = chat_info.split(":")[0].encode('utf-8')
                mes_text = telegram_message['text'].encode('utf-8')
                ans_list.append({'type': chat_type, 'chatname': chatname, 'text': mes_text})

            else:
                chat_type = "CHAT"
                username = chat_info.encode('utf-8')
                mes_text = telegram_message['text'].encode('utf-8')
                ans_list.append({'type': chat_type, 'username': username, 'text': mes_text})
    return ans_list
