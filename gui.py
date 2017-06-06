# _*_ coding : utf-8 _*_
__author__ = 'lius'

from tkinter import *
import tkinter.scrolledtext
import datetime
import time

from tkinter.scrolledtext import ScrolledText

class Window():
    def __init__(self):
        self.root = Tk()
        self.root.title("QQ机器人")
        # root.geometry('200x150')  # 设置窗口大小
        self.num = StringVar()
        self.root.resizable(width=False, height=False)  # 窗口大小不可变
        # 创建几个frame作为容器
        self.frame_left_top = LabelFrame(self.root, width=380, height=270, bg='white', text=" 消息显示 ")
        self.frame_left_center = LabelFrame(self.root, width=380, height=100, bg='white', text=" 编辑消息 ")
        self.frame_left_bottom = Frame(width=380, height=30)
        self.frame_right_1 = LabelFrame(self.root, width=170, height=400, bg='white', text=" ROBOT配置 ")

        # 创建需要的几个元素
        self.text_msglist = ScrolledText(self.frame_left_top, width=51, height=19, borderwidth = 0, state = 'normal',wrap=WORD)
        self.text_msg = ScrolledText(self.frame_left_center, width=51,height=6,borderwidth = 0)
        self.button_sendmsg = Button(self.frame_left_bottom, text='发送', command=self.show_message)

        self.name_label_text = StringVar()
        self.qq_label_text = StringVar()
        self.sex_label_text = StringVar()
        self.age_label_text = StringVar()
        self.bir_label_text = StringVar()
        self.addr_label_text = StringVar()
        self.emil_label_text = StringVar()
        self.face_label_text = StringVar()

        self.frame_right_2 = LabelFrame(self.root, width=170, height=400, bg='white', text=" QQ信息 ")
        Label(self.frame_right_2, text="昵称：", width=6, height=1).grid(row=2, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="qq号：", width=6, height=1).grid(row=3, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="性别：", width=6, height=1).grid(row=4, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="生日：", width=6, height=1).grid(row=6, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="位置：", width=6, height=1).grid(row=7, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="邮箱：", width=6, height=1).grid(row=8, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="face：", width=6, height=1).grid(row=9, column=0, sticky='W', pady=2)

        self.img_label = Label(self.frame_right_2, image = None, width=20, height=6,bg="#FFF")
        self.img_label.grid(row=0, column=0, columnspan=2, rowspan=2, ipadx=2, pady=2)
        Label(self.frame_right_2, textvariable=self.name_label_text, width=16, height=1, justify='left').grid(row=2, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.qq_label_text, width=16, height=1).grid(row=3, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.sex_label_text, width=16, height=1).grid(row=4, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.bir_label_text, width=16, height=1).grid(row=6, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.addr_label_text, width=16, height=1).grid(row=7, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.emil_label_text, width=16, height=1).grid(row=8, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.face_label_text, width=16, height=1).grid(row=9, column=1, pady=2)

        # 创建一个绿色的tag    http://www.jianshu.com/p/b2dc1aa68ce9
        self.text_msglist.tag_config('green', foreground='#008B00')
        # 使用grid设置各个容器位置
        self.frame_left_top.grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        self.frame_left_center.grid(row=1, column=0, rowspan=1, padx=2, pady=5)
        self.frame_left_bottom.grid(row=2, column=0)
        self.frame_right_1.grid(row=0, column=1, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
        self.frame_right_2.grid(row=0, column=2, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)

        # self.text_msglist.grid()
        self.frame_left_top.grid_propagate(0)
        self.frame_left_center.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)
        self.frame_right_2.grid_propagate(0)
        # 把元素填充进frame
        self.text_msglist.grid()
        self.text_msg.grid()
        self.button_sendmsg.grid(row=0, sticky=W)
        # self.img_label.grid(row=0, column=2)


    # 显示消息事件
    def show_message(self,data=None):
        # 在聊天内容上方加一行 显示发送人及发送时间
        msgcontent = 'robot:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        self.text_msglist.insert(END, msgcontent, 'green')
        self.text_msglist.insert(END, self.text_msg.get('0.0', END))
        self.text_msg.delete('0.0', END)
        self.text_msglist.see(END)

    # 显示个人信息
    def show_self_info(self, img=None, data=None):
        # self.img_label.configure(image=img)
        if data != None:
            self.name_label_text.set(data['nick'])
            self.qq_label_text.set(str(data['account']))
            self.sex_label_text.set((lambda :'男' if data['gender'] == 'male' else '女')())
            self.bir_label_text.set(str(data['birthday']['year'])+'年'+str(data['birthday']['month'])+'月'+str(data['birthday']['day'])+'日')
            self.addr_label_text.set(data['country']+'·'+data['province']+'·'+data['city'])
            self.emil_label_text.set(data['email'])
            self.face_label_text.set(str(data['face']))

    # 显示配置信息
    def show_cfg_info(self):
        pass

    def run(self):
        # 主事件循环
        self.root.mainloop()

if __name__=="__main__":
    w = Window()
    w.run()
