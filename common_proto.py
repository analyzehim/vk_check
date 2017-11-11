# -*- coding: utf-8 -*-

import socket
import time
import linecache
import sys
import traceback


def get_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return ''.join('!! ' + line for line in lines)


def get_host():
    return str(socket.getfqdn())


def log_event(text):
    f = open('log.txt', 'a')
    event = '%s >> %s' % (time.ctime(), text)
    print event + '\n'
    f.write(event+'\n')
    f.close()
    return True
