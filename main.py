__author__ = 'lius'

from smartqq import SmartQQ
import os
import time
import messge_text
import random

def robot():
    '''
    # 简单回复机器人实现
    '''
    qq = SmartQQ()
    qq._login() # 登录验证
    qq._get_self_info() # 获取个人信息，主要是获取gid,发送信息会用到。
    qq._get_friends_info() # 获取好友列表
    qq._get_online_buddies2() # 获取在线好友
    qq._get_recent_list2() # 获取最近列表
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

from tkinter import *
import datetime
import time

def window():
    root = Tk()
    root.title("QQ机器人")
    # root.geometry('200x150')  # 设置窗口大小
    root.resizable(width=False, height=False)  # 窗口大小不可变

    # 发送按钮事件
    def show_message():
        # 在聊天内容上方加一行 显示发送人及发送时间
        msgcontent = 'robot:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, text_msg.get('0.0', END))
        text_msg.delete('0.0', END)

    # 创建几个frame作为容器
    frame_left_top = Frame(width=380, height=270, bg='white')
    frame_left_center = Frame(width=380, height=100, bg='white')
    frame_left_bottom = Frame(width=380, height=30)
    frame_right_1 = Frame(width=170, height=400, bg='white')
    frame_right_2 = Frame(width=170, height=400, bg='white')
    # 创建需要的几个元素
    text_msglist = Text(frame_left_top)
    text_msg = Text(frame_left_center)
    button_sendmsg = Button(frame_left_bottom, text='发送', command=show_message)
    # 创建一个绿色的tag
    text_msglist.tag_config('green', foreground='#008B00')
    # 使用grid设置各个容器位置
    frame_left_top.grid(row=0, column=0, rowspan=1, padx=2, pady=5)
    frame_left_center.grid(row=1, column=0, rowspan=1, padx=2, pady=5)
    frame_left_bottom.grid(row=2,  column=0 )
    frame_right_1.grid(row=0, column=1, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
    frame_right_2.grid(row=0, column=2, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
    frame_left_top.grid_propagate(0)
    frame_left_center.grid_propagate(0)
    frame_left_bottom.grid_propagate(0)
    # 把元素填充进frame
    text_msglist.grid()
    text_msg.grid()
    button_sendmsg.grid(row=0, sticky=W)
    # 主事件循环
    root.mainloop()

if __name__=="__main__":
    # robot()
    window()