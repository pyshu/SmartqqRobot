# -*- coding: utf-8 -*-
__author__ = 'lius'

import tkinter
import requests
import random
import time
# import re
from multiprocessing import Process
import json

class SmartQQRobot():
    def __init__(self,qq_number):
        self._qq_number = qq_number
        # self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
        self._headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER",
                         'Referer' : 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'}

        self._session = requests.session()
        self._session.headers.update(self._headers)
        self._cookies_qrsig = ""
        self._ptwebqq = ""
        self._vfwebqq = ""
        self._psessionid = ""
        self._uin = ""
        self._clientid = 53999199

        self._login_status = False

    def _show_QRC(self,content):
        # 通过 tkinter 显示二维码.
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
            # self._login_error = True
            print("二维码获取失败.")

    def _get_ptqrtoken(self):
        # ptqrtoken 计算
        token = 0
        for i in range(len(self._cookies_qrsig)):
            token += (token << 5) + ord(self._cookies_qrsig[i])
        print(2147483647 & token)
        return 2147483647 & token

    def _check_login_status(self,p):
        # 登录状态检测
        url = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" + str(self._get_ptqrtoken()) +\
              "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106" \
              "&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10" \
              "&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert" \
              "&action=0-0-" + str(random.randint(1000, 30000)) +\
              "&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10216&login_sig=&pt_randsalt=2"
        print(url)
        # 死循环检测扫码登陆状态
        while 1:
            content = self._session.get(url=url).content.decode("utf-8")
            # 登陆成功跳出循环
            if "二维码" not in content:
                data = content.split(',')
                print("二维码认证成功.登录用户：%s" % data[5])
                # 结束进程 p
                if p.is_alive():
                    p.terminate()
                self._login_status = True
                return data[2].replace("'","")
            print("二维码认证中...")
            # print(content)
            time.sleep(3)

    def _login(self):
        # 下面 url 中 t = ？，？为获取二维码请求随机数。
        url = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&amp;e=0&amp;l=M&amp;s=5&amp;d=72&amp;v=4&amp;t=0.5621849584499783"
        content = self._session.get(url=url).content  #获取二维码数据（二进制）
        self._cookies_qrsig = (requests.utils.dict_from_cookiejar(self._session.cookies))["qrsig"]
        #使用进程显示二维码，等待扫描。
        p = Process(target=self._show_QRC,args=(content,))
        #启动进程 p
        p.start()
        time.sleep(1)
        #获取验证成功后返回的请求地址
        url = self._check_login_status(p)
        self._headers.pop("Referer")
        self._headers['Upgrade-Insecure-Requests'] = "1"
        self._session.headers.update(self._headers)
        # 请求获取 cookies 中 ptwebqq
        self._session.get(url=url)
        self._ptwebqq = (requests.utils.dict_from_cookiejar(self._session.cookies))["ptwebqq"]
        print("ptwebqq : %s" % self._ptwebqq)

        # 请求获取 json 中 vfwebqq
        url = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq=" + str(self._ptwebqq) +\
              "&clientid=53999199&psessionid=&t=1493177741164"
        j_data = json.loads(self._session.get(url=url).content.decode("utf-8"))
        self._vfwebqq = j_data["result"]["vfwebqq"]
        print("vfwebqq : %s" % self._vfwebqq)

        # 请求获取  psessionid  uin
        self._headers.pop("Upgrade-Insecure-Requests")
        self._headers["Referer"] = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"
        self._headers["Origin"] = "http://d1.web2.qq.com"
        self._session.headers.update(self._headers)
        url = "http://d1.web2.qq.com/channel/login2"
        p_data = {"ptwebqq": str(self._ptwebqq),
                    "clientid":53999199,
                    "psessionid":"",
                    "status":"online"}
        r_data = {"r":json.dumps(p_data)}

        j_data = json.loads(self._session.post(url=url,data=r_data).content.decode("utf-8"))
        self._psessionid = j_data["result"]["psessionid"]
        self._uin = j_data["result"]["uin"]
        print("psessionid : %s" % self._psessionid)
        print("uin : %s" % self._uin)
        print("恭喜，SmartQQ登录成功。")

    def msg_robot(self):
        get_msg_url = "http://d1.web2.qq.com/channel/poll2"
        # self._headers.pop("Origin")
        self._session.headers.update(self._headers)
        p_data = {"ptwebqq": str(self._ptwebqq),
                 "clientid": 53999199,
                 "psessionid": str(self._psessionid),
                 "key": ""
                 }
        r_data = {"r": json.dumps(p_data)}
        while 1:
            j_data = json.loads(self._session.post(url=get_msg_url,data=r_data).content.decode("utf-8"))
            print(j_data)
            time.sleep(3)
            # print(self._session.cookies)

    def run(self):
        self._login()
        self.msg_robot()

if __name__=="__main__":
    qq = SmartQQRobot(1)
    qq.run()