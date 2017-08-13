# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:11:33 2017

@author: XINYU HONG

GOAL: Use WeChat to control net-connected electronics

REF: http://python.jobbole.com/84918/
REF: https://github.com/littlecodersh/EasierLife/blob/master/Scripts/SendToMyself.py
"""

import itchat, time
import win32api
from itchat.content import *
import thread

STATUS = 0


def wechat_print():
    @itchat.msg_register([TEXT, ATTACHMENT])
    def print_helper(msg):
        global STATUS
        if msg['ToUserName'] != 'filehelper':
            return
        if msg['Content'] in [u"退出打印", ch2en.get(u"退出打印", None)]:
            STATUS = 0
            itchat.send_msg(u"离开打印模式，进入主菜单。\nLeaving PRINT mode, entering MAIN mode.", 'filehelper')
        else:
            tempfile = r'C:\\Users\\pagpi_000\\Documents\\research\\wechat_print_temp.txt'
            with open(tempfile, 'w') as f:
                f.write(msg['Content'].encode('utf-8'))
            # SETUP YOUR PRINTER
            printerName = ''
            win32api.ShellExecute(
                0,
                "printto",
                tempfile,
                '"{}"'.format(printerName),
                ".",
                0
            )

fun_dict = {
    u'PRINT': wechat_print
}

fun_dict_ch = {
    u'打印': 'PRINT',
    u'播放音乐': 'MUSIC',
}

ch2en = {
    u'打印': 'PRINT',
    u'播放音乐': 'MUSIC',
    u'退出打印': 'quit PRINT'
}

def main_list():    
    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
    def options(msg):
        global STATUS
        if msg['ToUserName'] != 'filehelper':
            return
        if msg['Content'] == 'H':
            welcome_message = u"可进入模式:"+u','.join(map(lambda (x,y): u"{}({})".format(x,y), fun_dict_ch.items()))
            itchat.send_msg(welcome_message, 'filehelper')
        else:
            fun = fun_dict.get(msg['Content'], None)
            if fun:
                STATUS = msg['Content']
                itchat.send_msg(u"进入打印模式。请输入打印内容。\nEntering {} mode, pls send the content you want to print.".format(msg['Content']), 'filehelper')
                fun()
            else:
                itchat.send_msg(u"您现在在主菜单模式。请输入'H'获得帮助。\nYou are at MAIN mode. Pls type 'H' for options.", 'filehelper')

itchat.auto_login(True)
#itchat.run()
thread.start_new_thread(itchat.run, ())

while 1:
    reg_fun = fun_dict.get(STATUS, main_list)
    reg_fun()
    time.sleep(.1)