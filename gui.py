# _*_ coding : utf-8 _*_
__author__ = 'lius'

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import time
import os


groups = {}
friends = {}

class Window():
    def __init__(self,qq=None):
        self.smartqq = qq
        self.root = Tk()
        self.root.title("QQ机器人")
        self.root.resizable(width=False, height=False)  # 窗口大小不可变
        self.center_window(755, 425) # 窗口居中显示

        # 左侧消息栏
        self.frame_left_top = LabelFrame(self.root, width=380, height=270, text=" 消息显示 ")
        self.frame_left_center = LabelFrame(self.root, width=380, height=100, text=" 编辑消息 ")
        self.frame_left_bottom = Frame(width=380, height=30)
        self.frame_left_top.grid_propagate(0)
        self.frame_left_center.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)

        self.text_msglist = ScrolledText(self.frame_left_top, width=51, height=19, borderwidth = 0, state = 'normal',wrap=WORD)
        self.text_msgsend = ScrolledText(self.frame_left_center, width=51,height=6,borderwidth = 0)
        self.button_sendmsg = Button(self.frame_left_bottom, text='发送', command=self.show_message, width=6, state='disabled')
        # 创建绿色的tag
        self.text_msglist.tag_config('green', foreground='#008B00')

        self.frame_left_top.grid(row=0, column=0, rowspan=1, padx=5, pady=7)
        self.frame_left_center.grid(row=1, column=0, rowspan=1, padx=2, pady=2)
        self.frame_left_bottom.grid(row=2, column=0, pady=5)

        # 单选框实现
        Label(self.frame_left_bottom, text="发送选择：", width=5, height=1).grid(row=0, column=0, ipadx=12, pady=2)

        self.flb_radVar = IntVar()  # 通过tk.IntVar() 获取单选按钮value参数对应的值
        self.flb_radVar.set(99)
        self.flb_fir_curRad = Radiobutton(self.frame_left_bottom, width=2, height=1,  text='好友', variable=self.flb_radVar, value=0,command=self.flb_radCall)  # 当该单选按钮被点击时，会触发参数command对应的函数
        self.flb_grp_curRad = Radiobutton(self.frame_left_bottom, width=2, height=1, text='群', variable=self.flb_radVar, value=1,command=self.flb_radCall)
        self.flb_gch_curRad = Radiobutton(self.frame_left_bottom, width=3, height=1, text='群聊', variable=self.flb_radVar, value=2,command=self.flb_radCall, state='disabled')
        self.flb_fir_curRad.grid(column=1, row=0,)  # 参数sticky对应的值参考复选框的解释
        self.flb_grp_curRad.grid(column=2, row=0,)
        self.flb_gch_curRad.grid(column=3, row=0,)

        # 一个下拉列表
        self.flb_pull_down_number = StringVar()
        self.flb_pull_down_combobox = ttk.Combobox(self.frame_left_bottom, width=15, height=3, textvariable=self.flb_pull_down_number, state='readonly')
        self.flb_pull_down_combobox['values'] = ("请选择")  # 设置下拉列表的值
        self.flb_pull_down_combobox.grid(column=4, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.flb_pull_down_combobox.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        # 把元素填充进去
        self.text_msglist.grid()
        self.text_msgsend.grid()
        self.button_sendmsg.grid(column=5, row=0, padx=2, sticky=W)
        self.text_msglist.grid()

        # 中间配置栏
        self.frame_right_1 = LabelFrame(self.root, width=170, height=400, text=" ROBOT配置 ")
        self.frame_right_1.grid(row=0, column=1, rowspan=3, padx=4, pady=5, ipadx=2, ipady=5)
        self.frame_right_1.grid_propagate(0)

        self.recv_cho = LabelFrame(self.frame_right_1, width=160, height=70,text=" 接收 ")
        self.recv_cho.grid(row=0, column=0,padx=4, pady=5, ipadx=2, ipady=5)
        self.recv_cho.grid_propagate(0)

        self.ref_cho = LabelFrame(self.frame_right_1, width=160, height=85, text=" 刷新 ")
        self.ref_cho.grid(row=1, column=0, padx=4, pady=5, ipadx=2, ipady=5)
        self.ref_cho.grid_propagate(0)

        self.com_cho = LabelFrame(self.frame_right_1, width=160, height=175, text=" 综合 ")
        self.com_cho.grid(row=2, column=0, padx=4, pady=5, ipadx=2, ipady=5)
        self.com_cho.grid_propagate(0)

        # 复选框
        self.rg_chVar = IntVar()  # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,其状态值为int类型 勾选为1  未勾选为0
        rg_check = Checkbutton(self.recv_cho, text="群消息", variable=self.rg_chVar)#, state='disabled')  # text为该复选框后面显示的名称, variable将该复选框的状态赋值给一个变量，当state='disabled'时，该复选框为灰色，不能点的状态
        rg_check.select()  # 该复选框是否勾选,select为勾选, deselect为不勾选
        rg_check.grid(column=1, row=0, sticky=W)

        self.rf_chVar = IntVar()
        rf_check = Checkbutton(self.recv_cho, text="好友消息", variable=self.rf_chVar)  # , state='disabled')
        rf_check.select()  # 该复选框是否勾选,select为勾选, deselect为不勾选
        rf_check.grid(column=0, row=0, sticky=W)

        self.rc_chVar = IntVar()
        rc_check = Checkbutton(self.recv_cho, text="群聊消息", variable=self.rc_chVar, state='disabled')
        rc_check.deselect()  # 该复选框是否勾选,select为勾选, deselect为不勾选
        rc_check.grid(column=0, row=1, sticky=W)

        # 刷新按键
        Button(self.ref_cho, text="好友列表", bd=2, command=self.refresh_friends_list, width=8).grid( row=0, column=0, pady=2, padx=9)
        Button(self.ref_cho, text="群列表", bd=2, command=self.refresh_groups_list, width=8).grid( row=0, column=1, pady=2, padx=1)
        Button(self.ref_cho, text="群聊列表", bd=2, command=self.refresh_group_chat_list, width=8, state='disabled').grid( row=1, column=0, pady=2, padx=9)
        Button(self.ref_cho, text="个人信息", bd=2, command=self.refresh_self_info_list, width=8).grid( row=1, column=1, pady=2, padx=1)

        # 读取文件选项
        self.path_file_1 = StringVar()
        Label(self.com_cho, text="文件1:").grid(row=0, column=0, pady=2)
        Entry(self.com_cho, borderwidth = 4, relief='groove',textvariable=self.path_file_1,width=7).grid(row=0, column=1, pady=3)
        Button(self.com_cho, text="选择", bd=1, command=lambda : self.select_path_file(self.path_file_1), width=3).grid(row=0, column=2, padx=1, pady=2)
        Button(self.com_cho, text="读取", bd=1, command=lambda: self.select_path_file(self.path_file_1), width=3).grid(row=0,column=3, pady=2)

        self.path_file_2 = StringVar()
        Label(self.com_cho, text="文件2:").grid(row=1, column=0, pady=2)
        Entry(self.com_cho, borderwidth=4, relief='groove', textvariable=self.path_file_2, width=7).grid(row=1, column=1, pady=3 )
        Button(self.com_cho, text="选择", bd=1, command=lambda: self.select_path_file(self.path_file_1), width=3).grid(row=1, column=2, padx=1, pady=2)
        Button(self.com_cho, text="读取", bd=1, command=lambda: self.select_path_file(self.path_file_1), width=3).grid(row=1, column=3, pady=2)

        self.path_file_3 = StringVar()
        Label(self.com_cho, text="文件3:").grid(row=2, column=0, pady=2)
        Entry(self.com_cho, borderwidth=4, relief='groove', textvariable=self.path_file_3, width=7).grid(row=2, column=1, pady=3 )
        Button(self.com_cho, text="选择", bd=1, command=lambda: self.select_path_file(self.path_file_1), width=3).grid(row=2, column=2, padx=1, pady=2 )
        Button(self.com_cho, text="读取", bd=1, command=lambda: self.select_path_file(self.path_file_1), width=3).grid(row=2, column=3, pady=2 )

        # 右边个人信息栏
        self.frame_right_2 = LabelFrame(self.root, width=170, height=400,text=" QQ信息 ")
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
        self.img_label = Label(self.frame_right_2, image=bm, width=160, height=160)
        self.img_label.bm = bm
        self.img_label.grid(row=0, column=0, columnspan=2, rowspan=2, ipadx=2, pady=2)
        Label(self.frame_right_2, textvariable=self.name_label_text, relief="solid", borderwidth=1, width=16, height=1, justify='left').grid(row=2, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.qq_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=3, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.sex_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=4, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.bir_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=6, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.addr_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=7, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.emil_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=8, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.face_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=9, column=1, pady=2)
        self.frame_right_2.grid_propagate(0)

    # 刷新好友列表
    def refresh_friends_list(self):
        global friends
        friends = self.smartqq._get_friends_info()
        self.flb_radCall()
        print("刷新好友列表成功.")
    # 刷新群列表
    def refresh_groups_list(self):
        global groups
        groups = self.smartqq._get_group_info()
        self.flb_radCall()
        print("刷新群列表成功.")
    # 刷新群聊列表
    def refresh_group_chat_list(self):
        pass
    # 刷新个人资料
    def refresh_self_info_list(self):
        info = self.smartqq._get_self_info()
        print("刷新个人资料成功.")
        self.show_self_info(data=info)

    # 选择加载文件
    def select_path_file(self, pf):
        # path_ = askdirectory()
        path_ = filedialog.askopenfilename(title='打开文件', filetypes=[('All Files', '*')])
        pf.set(path_)

    # 设置界面屏幕居中显示
    def center_window(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size)

    def group_information_handle(self, from_group_uin, group_sender_uin):
        group_info = self.smartqq.get_group_info(from_group_uin)
        if group_info != None:
            for info in group_info['minfo']:
                if info['uin'] == group_sender_uin:
                    return {"g_name":group_info["ginfo"]["name"],"s_name":info["nick"]}
            return {"g_name":group_info["ginfo"]["name"]}


    # 单选按钮回调函数,就是当单选按钮被点击会执行该函数
    def flb_radCall(self):
        self.button_sendmsg['state'] = 'normal'  # 将发送按钮设置为 活动状态
        radSel = self.flb_radVar.get()
        if radSel == 0:
            self.flb_pull_down_combobox['values'] = tuple(friends.keys())  # 设置下拉列表的值
            print("切换为好友列表.")
        elif radSel == 1:
            self.flb_pull_down_combobox['values'] = tuple(groups.keys())  # 设置下拉列表的值
            print("切换为群列表.")
        self.flb_pull_down_combobox.set('请选择')

    # 显示消息事件
    def show_message(self, data=None):
        # 在聊天内容上方加一行 显示发送人及发送时间
        date = ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
        msgcontent = '消息出错 '
        if data != None:  # 接收消息显示处理
            # 群消息处理 if
            if data['poll_type'] == "group_message" and self.rg_chVar.get() == 1:
                info = self.group_information_handle(data['from_uin'], data['send_uin'])
                if "s_name" in info.keys():
                    msgcontent = '来自 ' + info['s_name'] + ' ( ' + info['g_name'] + ' (群))' + date
                else:
                    msgcontent = '发送 到 ' + info['g_name'] + '(群)' + date
            # 好友消息处理 if
            if data['poll_type'] == "message" and self.rf_chVar.get() == 1:
                # 查找dict中好友昵称
                for v in friends.values():
                    if v['uin'] == data['from_uin']:
                        msgcontent = '来自 ' + v['nick'] + '(好友)' + date
                        break
            self.text_msglist.insert(END, msgcontent, 'green')
            self.text_msglist.insert(END, data['content'] + '\n')
        else:  # 发送消息显示处理
            msg = self.text_msgsend.get('0.0', END)
            usr = self.flb_pull_down_combobox.get()
            if msg != '\n' and usr != '请选择':
                status = self.flb_radVar.get()
                if status == 0:
                    msgcontent = '发送 到 ' + str(usr) + '(好友)' + date
                    self.smartqq._send_buddy_msg(friends[usr]['uin'], msg[:-1])
                if status == 1:
                    # msgcontent = '发送 到 '+ str(usr) + '(群)' + date
                    self.smartqq._send_qun_msg(groups[usr]['gid'], msg[:-1])
                    return
                self.text_msglist.insert(END, msgcontent, 'green')
                self.text_msglist.insert(END, msg)
                self.text_msgsend.delete('0.0', END)
        self.text_msglist.see(END)

    # 显示个人信息
    def show_self_info(self, img=None, data=None):
        # 文件夹检测
        if img != None:
            if not os.path.isdir('temp'):
                os.mkdir('temp')
            # 保存图片
            with open('./temp/my.png', "w+b") as code:
                code.write(img)
            # 读取图片
            try:
                bm = PhotoImage(file="./temp/my.png")
                self.img_label.configure(image=bm)
                self.img_label.bm = bm
            except:
                pass
            # 删除图片
            if os.path.isfile('./temp/my.png'):
                os.remove("./temp/my.png")
            # 将显示信息填入label
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


