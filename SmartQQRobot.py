# -*- coding: utf-8 -*-
__author__ = 'lius'

import tkinter
import requests
# import random
import time
# import re
from multiprocessing import Process
# import threading

class SmartQQRobot():
    def __init__(self,qq_number):
        self._qq_number = qq_number
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}

        self._session = requests.session()
        self._session.headers.update(self._headers)

        self._login_error = False

    def _show_QRC(self):
        url = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&amp;e=0&amp;l=M&amp;s=5&amp;d=72&amp;v=4&amp;t=0.6228904674882688"
        content = self._session.get(url=url).content  #获取二维码数据（二进制）
        if(content != None):
            root = tkinter.Tk()  #显示二维码
            root.title("扫描二维码")
            root.geometry('200x150') #设置窗口大小
            root.resizable(width=False, height=False) #窗口大小不可变
            img = tkinter.PhotoImage(data=content)
            label = tkinter.Label(root, image=img)
            label.pack()
            root.mainloop()
        else:
            self._login_error = True
            print("二维码获取失败.")

    def _check_login_status(self):
        pass


    def _login(self):
        #使用进程显示二维码，等待扫描。
        p = Process(target=self._show_QRC)
        #启动进程 p
        p.start()

        time.sleep(10)
        #结束进程 p
        if p.is_alive():
            p.terminate()

    def msg_robot(self):
        pass

    def run(self):
        self._login()

if __name__=="__main__":
    qq = SmartQQRobot(111)
    qq.run()