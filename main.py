__author__ = 'lius'

from smartqq import SmartQQ
from gui import Window
import gui
import os
import time
import messge_text
import random
import threading

def robot():
    '''
    # 简单机器人实现
    '''
    qq = SmartQQ()
    w = Window(qq)
    qq.login() # 登录验证
    slf = qq.get_self_info() # 获取个人信息，主要是获取gid,发送信息会用到。
    friends = qq.get_friends_info() # 获取好友列表
    onli = qq.get_online_buddies2() # 获取在线好友
    rev = qq.get_recent_list2() # 获取最近列表
    groups = qq.get_group_list() # 获取群列表
    img = qq.get_self_img()  # 获取个人头像
    robot_group_uin = 0 # 监控的群名称。

    w.show_self_info(img=img, data=slf) # 显示个人信息

    gui.groups = groups
    gui.friends = friends

    # 循环主题
    def recv_func():
        while 1:
            get_msg = qq.get_chat_msg()
            print("get_msg %s" % get_msg)
            if get_msg != None:
                send_msg = "我不明白你的意思."
                if get_msg["poll_type"] == "group_message":
                    w.group_msg_handle(get_msg["from_uin"], get_msg["send_uin"], get_msg["content"])
                    if get_msg["content"].find("@"+qq.qqname) >= 0 and gui.auto_send_name['group'] != None and \
                                    get_msg["from_uin"] == groups[gui.auto_send_name['group']]['gid']:
                        if get_msg["content"].find("自动回复") >= 0:
                            send_msg = messge_text.messge_re[random.randint(0, 53)]
                        qq.send_qun_msg(groups[gui.auto_send_name['group']]['gid'], send_msg)
                        print("机器人回复 : %s" % send_msg)
                if get_msg["poll_type"] == "message" :
                    w.friend_msg_handle(get_msg["from_uin"], get_msg["content"])
                    if gui.auto_send_name['friend'] != None and get_msg["from_uin"] == friends[gui.auto_send_name['friend']]['uin']:
                        if get_msg["content"].find("自动回复") >= 0:
                            send_msg = messge_text.messge_re[random.randint(0, 53)]
                            qq.send_buddy_msg(friends[gui.auto_send_name['friend']]['uin'], send_msg)
                        print("机器人回复 : %s" % send_msg)
                        w.friend_msg_handle(get_msg["from_uin"], send_msg,True)

            time.sleep(1)

    t = threading.Thread(target=recv_func)
    t.start()

    w.run()

if __name__=="__main__":
    robot()