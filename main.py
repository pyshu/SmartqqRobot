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
    # 简单回复机器人实现
    '''
    qq = SmartQQ()
    w = Window(qq)
    qq._login() # 登录验证
    dat = qq._get_self_info() # 获取个人信息，主要是获取gid,发送信息会用到。
    friends = qq._get_friends_info() # 获取好友列表
    onli = qq._get_online_buddies2() # 获取在线好友
    rev = qq._get_recent_list2() # 获取最近列表
    groups = qq._get_group_info() # 获取群列表
    img = qq._get_self_img()  # 获取个人头像
    robot_group_uin = 0 # 监控的群名称。

    w.show_self_info(img=img, data=dat) # 显示个人信息

    gui.groups = groups
    gui.friends = friends

    # 设置想监控的群列表
    if '有你有我' in groups.keys():
            robot_group_uin = groups['有你有我']['gid']
    if robot_group_uin == 0:
        print("没有监控的群列表,程序退出.")
        os._exit(0)

    # 循环主题
    def recv_func():
        while 1:
            get_msg = qq._get_chat_msg()
            if get_msg != None:
                print(get_msg)
                w.show_message(get_msg)
            if get_msg != None and get_msg["poll_type"] == "group_message" and get_msg["from_uin"] == robot_group_uin:
                if get_msg["content"].find("@时光1号") >= 0:
                    if get_msg["content"].find("自动回复") >= 0:
                        msg = messge_text.messge_re[random.randint(0, 53)]
                    else:
                        msg = "我不明白你的意思."
                    qq._send_qun_msg(robot_group_uin, msg)
                    print("机器人回复 : %s" % msg)
            time.sleep(1)

    t = threading.Thread(target=recv_func)#, args=({'friends':friends, 'groups':groups}),)
    t.start()

    w.run()

if __name__=="__main__":
    robot()