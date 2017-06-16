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
auto_send_name = {"friend":None, "group":None, "gchat":None}
group_information = {}

class Window():
    def __init__(self,qq=None):
        self.smartqq = qq
        self.root = Tk()
        self.root.title("QQ机器人")
        self.root.resizable(width=False, height=False)  # 窗口大小不可变
        self.center_window(796, 480) # 窗口居中显示

        # 左侧消息栏
        self.frame_left_top = LabelFrame(self.root, width=422, height=320, text=" 消息显示 ")
        # self.frame_left_center_top = Frame(width=422, height=30)
        self.frame_left_center_bottom = LabelFrame(self.root, width=422, height=100, text=" 编辑消息 ")
        self.frame_left_bottom = Frame(width=422, height=30)

        self.frame_left_top.grid_propagate(0)
        # self.frame_left_center_top.grid_propagate(0)
        self.frame_left_center_bottom.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)

        self.frame_left_top.grid(row=0, column=0, rowspan=1, padx=5, pady=0)
        # self.frame_left_center_top.grid(row=1, column=0, pady=0, padx=0,)
        self.frame_left_center_bottom.grid(row=2, column=0, rowspan=1, padx=2, pady=0)
        self.frame_left_bottom.grid(row=3, column=0, pady=1)

        self.text_msglist = ScrolledText(self.frame_left_top, width=57, height=23, borderwidth = 0, state = 'normal',wrap=WORD)
        self.text_msgsend = ScrolledText(self.frame_left_center_bottom, width=57,height=6,borderwidth = 0)
        # 创建绿色的tag
        self.text_msglist.tag_config('green', foreground='#008B00')

        # Label(self.frame_left_center_top, text="").grid(row=0, column=0, ipadx=157, pady=0)
        # self.button_clear_message = Button(self.frame_left_center_top, text='清屏', command=lambda : self.text_msglist.delete(0.0, END), width=5, height=1)#, state='disabled')
        # self.button_save_message = Button(self.frame_left_center_top, text='保存', command=lambda: 1, width=5, height=1, state='disabled')
        # self.button_clear_message.grid(column=1, row=0, padx=3, ipadx=0)
        # self.button_save_message.grid(column=2, row=0, padx=3)

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

        self.button_sendmsg = Button(self.frame_left_bottom, text='发送', command=self.btn_send_message, width=5, state='disabled')
        self.button_send_mode = Button(self.frame_left_bottom, text='多窗口', command=lambda :  1, width=5, state='disabled')

        # 把元素填充进去
        self.text_msglist.grid()
        self.text_msgsend.grid()
        self.text_msglist.grid()
        self.button_sendmsg.grid(column=5, row=0, padx=1, sticky=W)
        self.button_send_mode.grid(column=6, row=0, padx=1, sticky=W)

        # 中间配置栏
        self.frame_right_1 = LabelFrame(self.root, width=170, height=460, text=" ROBOT配置 ")
        self.frame_right_1.grid(row=0, column=1, rowspan=4, padx=4, pady=5, ipadx=2, ipady=5)
        self.frame_right_1.grid_propagate(0)

        self.recv_cho = LabelFrame(self.frame_right_1, width=160, height=45,text=" 接收 ")
        self.recv_cho.grid(row=0, column=0,padx=4, pady=1, ipadx=2, ipady=3)
        self.recv_cho.grid_propagate(0)

        self.ref_cho = LabelFrame(self.frame_right_1, width=160, height=85, text=" 刷新 ")
        self.ref_cho.grid(row=1, column=0, padx=4, pady=1, ipadx=2, ipady=3)
        self.ref_cho.grid_propagate(0)

        self.robot_cho = LabelFrame(self.frame_right_1, width=160, height=110, text=" 监控(需刷新列表) ")
        self.robot_cho.grid(row=2, column=0, padx=4, pady=1, ipadx=2, ipady=3)
        self.robot_cho.grid_propagate(0)

        self.com_cho = LabelFrame(self.frame_right_1, width=160, height=115, text=" 自定义消息导入 ")
        self.com_cho.grid(row=3, column=0, padx=4, pady=1, ipadx=2, ipady=3)
        self.com_cho.grid_propagate(0)

        self.more_cho = LabelFrame(self.frame_right_1, width=160, height=50, text=" 其他 ")
        self.more_cho.grid(row=4, column=0, padx=4, pady=1, ipadx=2, ipady=3)
        self.more_cho.grid_propagate(0)

        # 复选框
        self.rg_chVar = IntVar()  # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,其状态值为int类型 勾选为1  未勾选为0
        rg_check = Checkbutton(self.recv_cho, text="群", variable=self.rg_chVar)#, state='disabled')  # text为该复选框后面显示的名称, variable将该复选框的状态赋值给一个变量，当state='disabled'时，该复选框为灰色，不能点的状态
        rg_check.select()  # 该复选框是否勾选,select为勾选, deselect为不勾选
        rg_check.grid(column=1, row=0, padx=3, sticky=W)

        self.rf_chVar = IntVar()
        rf_check = Checkbutton(self.recv_cho, text="好友", variable=self.rf_chVar)  # , state='disabled')
        rf_check.select()  # 该复选框是否勾选,select为勾选, deselect为不勾选
        rf_check.grid(column=0, row=0, padx=3, sticky=W)

        self.rc_chVar = IntVar()
        rc_check = Checkbutton(self.recv_cho, text="群聊", variable=self.rc_chVar, state='disabled')
        rc_check.deselect()  # 该复选框是否勾选,select为勾选, deselect为不勾选
        rc_check.grid(column=2, row=0, padx=3, sticky=W)

        # 刷新按键
        Button(self.ref_cho, text="好友列表", bd=2, command=self.refresh_friends_list, width=8).grid( row=0, column=0, pady=2, padx=9)
        Button(self.ref_cho, text="群列表", bd=2, command=self.refresh_groups_list, width=8).grid( row=0, column=1, pady=2, padx=1)
        Button(self.ref_cho, text="群聊列表", bd=2, command=self.refresh_group_chat_list, width=8, state='disabled').grid( row=1, column=0, pady=2, padx=9)
        Button(self.ref_cho, text="个人信息", bd=2, command=self.refresh_self_info_list, width=8).grid( row=1, column=1, pady=2, padx=1)

        # robot 监控设置
        Label(self.robot_cho, text="好友:").grid(row=0, column=0, pady=2)
        # 下拉列表
        self.rbt_pull_down_number_friend = StringVar()
        self.rbt_pull_down_combobox_friend = ttk.Combobox(self.robot_cho, width=10, height=3, textvariable=self.rbt_pull_down_number_friend, state='disabled')
        self.rbt_pull_down_combobox_friend['values'] = tuple(["*请选择*","*回复所有*"] + list(friends.keys())) # 设置下拉列表的值
        self.rbt_pull_down_combobox_friend.grid(column=1, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.rbt_pull_down_combobox_friend.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        self.rbt_btn_friend = Button(self.robot_cho, text='OK', command=self.rbt_friend_call, width=3, state='disabled')
        self.rbt_btn_friend.grid(column=2, row=0, padx=1, sticky=W)

        Label(self.robot_cho, text=" 群: ").grid(row=1, column=0, pady=2)
        # 下拉列表
        self.rbt_pull_down_number_group = StringVar()
        self.rbt_pull_down_combobox_group = ttk.Combobox(self.robot_cho, width=10, height=3,textvariable=self.rbt_pull_down_number_group, state='disabled')
        self.rbt_pull_down_combobox_group['values'] = tuple(["*请选择*","*回复所有*"] + list(groups.keys()))   # 设置下拉列表的值
        self.rbt_pull_down_combobox_group.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.rbt_pull_down_combobox_group.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        self.rbt_btn_group = Button(self.robot_cho, text='OK', command=self.rbt_group_call, width=3 , state='disabled')
        self.rbt_btn_group.grid(column=2, row=1, padx=1, sticky=W)

        Label(self.robot_cho, text="群聊:").grid(row=2, column=0, pady=2)
        # 下拉列表
        self.rbt_pull_down_number_gchat = StringVar()
        self.rbt_pull_down_combobox_gchat = ttk.Combobox(self.robot_cho, width=10, height=3, textvariable=self.rbt_pull_down_number_gchat, state='disabled')#, state='readonly')
        self.rbt_pull_down_combobox_gchat['values'] = ("*请选择*","*回复所有*")  # 设置下拉列表的值
        self.rbt_pull_down_combobox_gchat.grid(column=1, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.rbt_pull_down_combobox_gchat.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        self.rbt_btn_gchat = Button(self.robot_cho, text='OK', command=lambda : 1, width=3, state='disabled')
        self.rbt_btn_gchat.grid(column=2, row=2, padx=1, sticky=W)

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

        self.button_clear_message = Button(self.more_cho, text='清屏', command=lambda: self.text_msglist.delete(0.0, END), width=8, height=1)#, state='disabled')
        self.button_save_message = Button(self.more_cho, text='保存', command=self.save_file, width=8, height=1)
        self.button_clear_message.grid(column=0, row=0, padx=6)
        self.button_save_message.grid(column=1, row=0, padx=6)

        # 右边个人信息栏
        self.frame_right_2 = LabelFrame(self.root, width=170, height=460,text=" QQ信息 ")
        self.frame_right_2.grid(row=0, column=2, rowspan=4, padx=4, pady=5, ipadx=2, ipady=5)
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
        self.img_label.grid(row=0, column=0, columnspan=2, rowspan=2, ipadx=2, pady=30)
        Label(self.frame_right_2, textvariable=self.name_label_text, relief="solid", borderwidth=1, width=16, height=1, justify='left').grid(row=2, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.qq_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=3, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.sex_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=4, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.bir_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=6, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.addr_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=7, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.emil_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=8, column=1, pady=2)
        Label(self.frame_right_2, textvariable=self.face_label_text, relief="solid", borderwidth=1, width=16, height=1).grid(row=9, column=1, pady=2)
        self.frame_right_2.grid_propagate(0)

    # 聊天消息保存
    def save_file(self):
        if self.text_msglist.get(0.0, 'end') != '\n':
            with open('./temp/all-' + time.strftime("%Y%m%d%H%M%S", time.localtime()) +'.txt', 'w+') as fd:
                fd.write(self.text_msglist.get(0.0, 'end'))
                print("保存文件成功.")

    # 回复好友按键回调
    def rbt_friend_call(self):
        if self.rbt_btn_friend["text"] == "OK":
            auto_send_name["friend"] = self.rbt_pull_down_combobox_friend.get()
            self.rbt_pull_down_combobox_friend["state"] = "disabled"
            self.rbt_btn_friend["text"] = "取消"
        else:
            auto_send_name["friend"] = None
            self.rbt_pull_down_combobox_friend["state"] = "normal"
            self.rbt_btn_friend["text"] = "OK"

    # 回复群按键回调
    def rbt_group_call(self):
        if self.rbt_btn_group["text"] == "OK":
            auto_send_name["group"] = self.rbt_pull_down_combobox_group.get()
            self.rbt_pull_down_combobox_group["state"] = "disabled"
            self.rbt_btn_group["text"] = "取消"
        else:
            auto_send_name["group"] = None
            self.rbt_pull_down_combobox_group["state"] = "normal"
            self.rbt_btn_group["text"] = "OK"

    # 刷新好友列表
    def refresh_friends_list(self):
        global friends
        self.rbt_pull_down_combobox_friend["state"] = "normal"
        self.rbt_btn_friend['state'] = 'normal'
        friends = self.smartqq.get_friends_info()
        self.rbt_pull_down_combobox_friend['values'] = tuple(["*请选择*","*回复所有*"] + list(friends.keys()))
        self.flb_radCall()
        print("刷新好友列表成功.")
    # 刷新群列表
    def refresh_groups_list(self):
        global groups
        self.rbt_pull_down_combobox_group["state"] = "normal"
        self.rbt_btn_group['state'] = 'normal'
        groups = self.smartqq.get_group_list()
        self.rbt_pull_down_combobox_group['values'] = tuple(["*请选择*","*回复所有*"] + list(groups.keys()))
        self.flb_radCall()
        print("刷新群列表成功.")
    # 刷新群聊列表
    def refresh_group_chat_list(self):
        pass

    # 刷新个人资料
    def refresh_self_info_list(self):
        info = self.smartqq.get_self_info()
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

    # 群资料获取和信息匹配
    def group_information_handle(self, from_group_uin, group_sender_uin):
        print("group_information : %s" % group_information)
        if from_group_uin in group_information.keys():
            for v in group_information[from_group_uin]["s_name"]:
                if v['uin'] == group_sender_uin:
                    return {"g_name": group_information[from_group_uin]["g_name"], "s_name": v["nick"]}
        group_code = 0
        for v in groups.values():
            if v["gid"] == from_group_uin:
                group_code = v["code"]
        group_info = self.smartqq.get_group_info(group_code)
        if group_info != None:
            group_information[from_group_uin] = {"g_name": group_info["ginfo"]["name"], "s_name": group_info["minfo"]}
            for info in group_info['minfo']:
                if info['uin'] == group_sender_uin:
                    return {"g_name":group_info["ginfo"]["name"], "s_name":info["nick"]}
            return {"g_name":group_info["ginfo"]["name"]}
        else:
            return None


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
        self.flb_pull_down_combobox.set('*请选择*')

    # 显示消息
    def show_message(self, strdt, msg):
        # 在聊天内容上方加一行 显示发送人及发送时间
        date = ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
        self.text_msglist.insert(END, strdt + date, 'green')
        self.text_msglist.insert(END, msg + '\n')
        self.text_msglist.see(END)

    # 图形界面输入发送消息处理
    def btn_send_message(self):
        msg = self.text_msgsend.get('0.0', END)
        usr = self.flb_pull_down_combobox.get()
        status = self.flb_radVar.get()
        if msg != '\n' and usr != '*请选择*':
            if status == 0:
                msgcontent = '发送 到 ' + str(usr) + '(好友)'
                self.smartqq.send_buddy_msg(friends[usr]['uin'], msg[:-1])
                self.show_message(msgcontent,msg)
            if status == 1:
                self.smartqq.send_qun_msg(groups[usr]['gid'], msg[:-1])
            self.text_msgsend.delete('0.0', END)

    # 群消息处理
    def group_msg_handle(self, from_uin, send_uin, message):
        if self.rg_chVar.get() == 1:
            info = self.group_information_handle(from_uin, send_uin)
            if info == None:
                return
            if "s_name" in info.keys():
                msgcontent = '来自 ' + info['s_name'] + ' ( ' + info['g_name'] + ' (群))'
            else:
                msgcontent = '发送 到 ' + info['g_name'] + '(群)'
            self.show_message(msgcontent, message + '\n')

    # 好友消息处理
    def friend_msg_handle(self, from_uin, message, flag = None):
        if  self.rf_chVar.get() == 1:
            # 查找dict中好友昵称
            for v in friends.values():
                if v['uin'] == from_uin:
                    if flag == None:
                        msgcontent = '来自 于 ' + v['nick'] + '(好友)'
                    else:
                        msgcontent = '发送 到 ' + v['nick'] + '(好友)'
                    self.show_message(msgcontent, message + '\n')
                    break

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