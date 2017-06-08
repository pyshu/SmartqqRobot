# _*_ coding : utf-8 _*_
__author__ = 'lius'

from tkinter import *
from tkinter import ttk
import time
import os
from tkinter.scrolledtext import ScrolledText

groups = {}
friends = {}

class Window():
    def __init__(self,qq):
        self.smartqq = qq
        self.root = Tk()
        self.root.title("QQ机器人")
        self.root.resizable(width=False, height=False)  # 窗口大小不可变

        # 创建三个frame作为容器
        self.frame_left_top = LabelFrame(self.root, width=380, height=270, bg='white', text=" 消息显示 ")
        self.frame_left_center = LabelFrame(self.root, width=380, height=100, bg='white', text=" 编辑消息 ")
        self.frame_left_bottom = Frame(width=380, height=30)
        self.frame_left_top.grid_propagate(0)
        self.frame_left_center.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)

        # 左侧消息栏
        self.text_msglist = ScrolledText(self.frame_left_top, width=51, height=19, borderwidth = 0, state = 'normal',wrap=WORD)
        self.text_msgsend = ScrolledText(self.frame_left_center, width=51,height=6,borderwidth = 0)
        self.button_sendmsg = Button(self.frame_left_bottom, text='发送', command=self.show_message, width=8)
        # 创建绿色的tag    http://www.jianshu.com/p/b2dc1aa68ce9
        self.text_msglist.tag_config('green', foreground='#008B00')

        self.frame_left_top.grid(row=0, column=0, rowspan=1, padx=5, pady=7)
        self.frame_left_center.grid(row=1, column=0, rowspan=1, padx=2, pady=2)
        self.frame_left_bottom.grid(row=2, column=0, pady=5)

        # 单选框实现
        Label(self.frame_left_bottom, text="发送选择：", width=6, height=1).grid(row=0, column=0, ipadx=15, pady=2)

        self.flb_radVar = IntVar()  # 通过tk.IntVar() 获取单选按钮value参数对应的值
        self.flb_radVar.set(99)
        self.flb_fir_curRad = Radiobutton(self.frame_left_bottom, width=2, height=1,  text='好友', variable=self.flb_radVar, value=0,command=self.flb_radCall)  # 当该单选按钮被点击时，会触发参数command对应的函数
        self.flb_grp_curRad = Radiobutton(self.frame_left_bottom, width=4, height=1, text='群', variable=self.flb_radVar, value=1,command=self.flb_radCall)
        self.flb_fir_curRad.grid(column=1, row=0,)  # 参数sticky对应的值参考复选框的解释
        self.flb_grp_curRad.grid(column=2, row=0,)

        # 一个下拉列表
        self.flb_pull_down_number = StringVar()
        self.flb_pull_down_combobox = ttk.Combobox(self.frame_left_bottom, width=16, height=3, textvariable=self.flb_pull_down_number, state='readonly')
        self.flb_pull_down_combobox['values'] = ("请选择")  # 设置下拉列表的值
        self.flb_pull_down_combobox.grid(column=3, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.flb_pull_down_combobox.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        # 把元素填充进去
        self.text_msglist.grid()
        self.text_msgsend.grid()
        self.button_sendmsg.grid(column=4, row=0, padx=2, sticky=W)
        self.text_msglist.grid()

        # 中间配置栏
        self.frame_right_1 = LabelFrame(self.root, width=170, height=400, bg='white', text=" ROBOT配置 ")
        self.frame_right_1.grid(row=0, column=1, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)

        # 右边个人信息栏
        self.frame_right_2 = LabelFrame(self.root, width=170, height=400, bg='white', text=" QQ信息 ")
        self.frame_right_2.grid(row=0, column=2, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
        self.name_label_text = StringVar()
        self.qq_label_text = StringVar()
        self.sex_label_text = StringVar()
        self.age_label_text = StringVar()
        self.bir_label_text = StringVar()
        self.addr_label_text = StringVar()
        self.emil_label_text = StringVar()
        self.face_label_text = StringVar()

        Label(self.frame_right_2, text="昵称：", width=6, height=1).grid(row=2, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="QQ ：", width=6, height=1).grid(row=3, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="性别：", width=6, height=1).grid(row=4, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="生日：", width=6, height=1).grid(row=6, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="位置：", width=6, height=1).grid(row=7, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="邮箱：", width=6, height=1).grid(row=8, column=0, sticky='W', pady=2)
        Label(self.frame_right_2, text="face：", width=6, height=1).grid(row=9, column=0, sticky='W', pady=2)

        bm = PhotoImage(file="./temp/QQ.png")
        self.img_label = Label(self.frame_right_2, image=bm, width=160, height=160, bg="#FFF")
        self.img_label.bm = bm
        self.img_label.grid(row=0, column=0, columnspan=2, rowspan=2, ipadx=2, pady=2)
        Label(self.frame_right_2, textvariable=self.name_label_text, width=16, height=1, justify='left').grid(row=2, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.qq_label_text, width=16, height=1).grid(row=3, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.sex_label_text, width=16, height=1).grid(row=4, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.bir_label_text, width=16, height=1).grid(row=6, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.addr_label_text, width=16, height=1).grid(row=7, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.emil_label_text, width=16, height=1).grid(row=8, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.face_label_text, width=16, height=1).grid(row=9, column=1, pady=2)

        self.frame_right_2.grid_propagate(0)

    # 单选按钮回调函数,就是当单选按钮被点击会执行该函数
    def flb_radCall(self):
        radSel = self.flb_radVar.get()
        if radSel == 0:
            self.flb_pull_down_combobox['values'] = tuple(friends.keys())  # 设置下拉列表的值
            print(self.flb_radVar.get())
        elif radSel == 1:
            self.flb_pull_down_combobox['values'] = tuple(groups.keys())  # 设置下拉列表的值
            print(self.flb_radVar.get())
        self.flb_pull_down_combobox.set('请选择')

    # 发送消息
    def send_message(self, usr, data=None):
        status = self.flb_radVar.get()
        if status == 0:
            self.smartqq._send_buddy_msg(friends[usr]['uin'], data)
        if status == 1:
            self.smartqq._send_qun_msg(groups[usr]['gid'], data)

    # 显示消息事件
    def show_message(self,data=None):
        if self.text_msgsend.get('0.0', END) != '\n' or data != None:
            # 在聊天内容上方加一行 显示发送人及发送时间
            msgcontent = '发来的信息 : ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
            if data != None:
                self.text_msglist.insert(END, msgcontent, 'green')
                self.text_msglist.insert(END, data + '\n')
            else:
                usr = self.flb_pull_down_combobox.get()
                msgcontent = str(self.smartqq._qqname) + ' to '+ str(usr) + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
                self.text_msglist.insert(END, msgcontent, 'green')
                msg = self.text_msgsend.get('0.0', END)
                self.text_msglist.insert(END, msg)
                msg = msg[:-1]
                self.send_message(usr, msg)
            self.text_msgsend.delete('0.0', END)
            self.text_msglist.see(END)

    # 显示个人信息
    def show_self_info(self, img=None, data=None):
        if not os.path.isdir('temp'):
            os.mkdir('temp')
        with open('./temp/my.png', "w+b") as code:
            code.write(img)
        try:
            bm = PhotoImage(file="./temp/my.png")
            self.img_label.configure(image=bm)
            self.img_label.bm = bm
        except:
            pass
        if os.path.isfile('./temp/my.png'):
            os.remove("./temp/my.png")

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


