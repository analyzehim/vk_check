from telegram_proto import Telebot
from vk_proto import VkBot, VkMessage
from sqlite_proto import Cash
from common_proto import log_event, get_exception
import time
from parsing_proto import *



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
            check_result = check_ans(update_list)
            if check_result:
                for ans in check_result:
                    if ans['type'] == "GROUP_CHAT":
                        chat_id = cashDB.get_chat_id(ans['chatname'])
                        text = ans['text']
                        vk_bot.send_text(chat_id, text)

                    elif ans['type'] == "CHAT":
                        user_id = cashDB.get_user_id(ans['username'])
                        text = ans['text']
                        vk_bot.send_text(user_id, text)
                    else:
                        log_event("STRANGE ANS {0}".format(ans))
            else:
                for mes in get_unread_messages(vk_bot, cashDB):
                        telegram_bot.send_text(telegram_bot.chat_id, str(mes))
            time.sleep(vk_bot.interval)
        except Exception as e:
            log_event(get_exception())

