from telegram_proto import Telebot
from vk_proto import VKbot
from sqlite_proto import Cash

def parse_mes(vk_response, cash):
    not_read_mes = []
    for mes in vk_response['response'][1:]:
        use_id.append(mes['id'])
        if mes['read_state'] == 1:
            if not cash.check_message(mes['id']):
                cash.add_message(mes['id'], mes['body'])
                if 'chat_id' in mes:
                    if 'push_settings' in mes:
                        if mes['push_settings']['disabled_until'] == -1:
                            continue
                            not_read_mes.append(Message(mes['body'], mes['uid']))
    return not_read_mes

if __name__ == "__main__":
    vkbot = VKbot()
    cash = Cash()
    telebot = Telebot()
    vkbot.send_text(vkbot.chat_id, "Run on {0}".format(vkbot.host))
    telebot.send_text(telebot.chat_id, "Run on {0}".format(telebot.host))
    print vkbot.get_mes()
