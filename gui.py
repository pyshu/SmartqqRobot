# _*_ coding : utf-8 _*_
__author__ = 'lius'

from tkinter import *
import tkinter.scrolledtext
import datetime
import time

class Window():
    def __init__(self):
        self.root = Tk()
        self.root.title("QQ机器人")
        # root.geometry('200x150')  # 设置窗口大小
        self.root.resizable(width=False, height=False)  # 窗口大小不可变
        # 创建几个frame作为容器
        self.frame_left_top = LabelFrame(self.root, width=380, height=270, bg='white', text=" 消息显示 ")
        self.frame_left_center = LabelFrame(self.root, width=380, height=100, bg='white', text=" 编辑消息 ")
        self.frame_left_bottom = Frame(width=380, height=30)
        self.frame_right_1 = LabelFrame(self.root, width=170, height=400, bg='white', text=" ROBOT配置 ")
        self.frame_right_2 = LabelFrame(self.root, width=170, height=400, bg='white', text=" QQ信息 ")
        # 创建需要的几个元素
        self.text_msglist = Text(self.frame_left_top)
        self.text_msg = Text(self.frame_left_center)
        self.button_sendmsg = Button(self.frame_left_bottom, text='发送', command=self.show_message)

        # self.img_label = Label(self.frame_right_2, text="Enter a name:").grid(column=0, row=0)
        # 创建一个绿色的tag    http://www.jianshu.com/p/b2dc1aa68ce9
        self.text_msglist.tag_config('green', foreground='#008B00')
        # 使用grid设置各个容器位置
        self.frame_left_top.grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        self.frame_left_center.grid(row=1, column=0, rowspan=1, padx=2, pady=5)
        self.frame_left_bottom.grid(row=2, column=0)
        self.frame_right_1.grid(row=0, column=1, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
        self.frame_right_2.grid(row=0, column=2, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
        Label(self.frame_right_2, text="Chooes a number").grid(column=0, row=2)
        self.frame_left_top.grid_propagate(0)
        self.frame_left_center.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)
        # 把元素填充进frame
        # self.text_msglist.grid()
        # self.text_msg.grid()
        self.button_sendmsg.grid(row=0, sticky=W)
        # self.img_label.grid(row=0, column=2)
        # 主事件循环
        self.root.mainloop()

    # 显示消息事件
    def show_message(self,data=None):
        # 在聊天内容上方加一行 显示发送人及发送时间
        msgcontent = 'robot:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        self.text_msglist.insert(END, msgcontent, 'green')
        self.text_msglist.insert(END, self.text_msg.get('0.0', END))
        self.text_msg.delete('0.0', END)

    # 显示个人信息
    def show_self_info(self, context=None, data=None):
        pass

    # 显示个人信息
    def show_cfg_info(self):
        pass

if __name__=="__main__":
    w = Window()
