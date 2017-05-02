__author__ = 'lius'

from smartqq import SmartQQ
import os
import time
import messge_text
import random

def robot():
    qq = SmartQQ()
    qq._login() # 登录验证
    qq._get_self_info() # 获取个人信息，主要是获取gid,发送信息会用到。
    # qq._get_friends_info() # 获取好友列表
    groups = qq._get_group_info() # 获取群列表
    robot_group_uin = 0 # 监控的群名称。
    # 设置想监控的群列表
    for g in groups:
        if g['name'] == "有你有我":
            robot_group_uin = g['gid']
    if robot_group_uin == 0:
        print("没有监控的群列表,程序退出.")
        os._exit(0)
    # 循环主题
    while 1:
        get_msg = qq._get_chat_msg()
        if get_msg != None and get_msg["poll_type"] == "group_message" and get_msg["from_uin"] == robot_group_uin:
            print(get_msg)
            if get_msg["content"].find("@时光1号") >= 0:
                if get_msg["content"].find("自动回复") >= 0:
                    msg = messge_text.messge_re[random.randint(0,53)]
                else:
                    msg = "我不明白你的意思."
                qq._send_qun_msg(robot_group_uin, msg)
                print("机器人回复 : %s" %msg)
        time.sleep(2)

if __name__=="__main__":
    robot()