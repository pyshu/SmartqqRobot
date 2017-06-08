# -*- coding: utf-8 -*-
__author__ = 'lius'

import tkinter
import requests
import random
import time
import json
from multiprocessing import Process

class SmartQQ():
    def __init__(self):
        self._headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER",
                         'Referer' : 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'}

        self._session = requests.session()
        self._session.headers.update(self._headers)
        self._cookies_qrsig = ""
        self._ptwebqq = ""
        self._vfwebqq = ""
        self._psessionid = ""
        self._uin = ""
        self._face = 0
        self._qqnum = 0
        self._qqname = ''

    def _show_QRC(self,content):
        '''
        通过 tkinter 显示二维码.
        '''
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
            print("二维码获取失败.")

    def _get_ptqrtoken(self):
        '''
        # ptqrtoken 计算
        '''
        token = 0
        for i in range(len(self._cookies_qrsig)):
            token += (token << 5) + ord(self._cookies_qrsig[i])
        return 2147483647 & token

    def _check_login_status(self,p):
        '''
        # 登录状态检测
        '''
        url = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" + str(self._get_ptqrtoken()) +\
              "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106" \
              "&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10" \
              "&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert" \
              "&action=0-0-" + str(random.randint(1000, 30000)) +\
              "&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10216&login_sig=&pt_randsalt=2"
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
            print("二维码认证中.....（请用手机QQ扫描二维码并确认登陆.）")
            time.sleep(3)

    def _login(self):
        '''
        # qq登陆过程
        '''
        # 下面 url 中 t = ？，？为获取二维码请求随机数。
        url = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&amp;e=0&amp;l=M&amp;s=5&amp;d=72&amp;v=4&amp;t=0.562284958449" + str(random.randint(10000,100000))
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
        p_data = {"ptwebqq": str(self._ptwebqq),"clientid":53999199,"psessionid":"","status":"online"}
        r_data = {"r":json.dumps(p_data)}

        j_data = json.loads(self._session.post(url=url,data=r_data).content.decode("utf-8"))
        self._psessionid = j_data["result"]["psessionid"]
        self._uin = j_data["result"]["uin"]
        print("psessionid : %s" % self._psessionid)
        print("uin : %s" % self._uin)
        print("恭喜，SmartQQ登录成功。")

    def _get_hash(self):
        '''
        # hash 值计算
        '''
        uin = int(self._uin)
        ptwebqq = self._ptwebqq
        ptb = [0,0,0,0]
        for i in range(len(ptwebqq)):
            ptb[i % 4] ^= ord(ptwebqq[i])
        uin = int(uin)
        uinByte = [0,0,0,0]
        uinByte[0] = uin >> 24 & 255 ^ 69   # E
        uinByte[1] = uin >> 16 & 255 ^ 67   # C
        uinByte[2] = uin >> 8 & 255 ^ 79    # O
        uinByte[3] = uin & 255 ^ 75         # K
        result = [0 for x in range(8)]
        for i in range(0,8):
            if(i % 2 == 0):
                result[i] = ptb[i >> 1]
            else:
                result[i] = uinByte[i >> 1]
        hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        buf = ""
        for i in result:
            buf += hex[i >> 4 & 15]
            buf += hex[i & 15]
        return buf

    def _recur_list(self,lst):
        '''
        递归将list的元素处理成字符串，函数主要针对list内有list。
        '''
        con = ""
        for ele in lst:
            if isinstance(ele, list):
                con += self._recur_list(ele)
            else:
                con += str(ele)
        return con

    def _get_self_info(self):
        '''
        # 获取个人信息
        '''
        url = "http://s.web2.qq.com/api/get_self_info2?t=1493263376886"
        try:
            j_data = json.loads(self._session.get(url=url).content.decode("utf-8"))
            self._face = j_data["result"]["face"]
            self._qqname = j_data["result"]["nick"]
            # self._qqnum = j_data["result"]["account"]
            print("我的QQ资料：%s" % j_data["result"])
            return j_data["result"]
        except:
            return None

    def _get_group_info(self):
        '''
        # 获取QQ群信息
        '''
        url = "http://s.web2.qq.com/api/get_group_name_list_mask2"
        p_data = {"vfwebqq": str(self._vfwebqq), "hash": self._get_hash()}
        r_data = {"r": json.dumps(p_data)}
        try:
            j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
            groups_data = { k['name']: k for k in j_data["result"]["gnamelist"] }
            print("QQ群：%s" % groups_data)
            return groups_data
        except:
            return None

    def _get_friends_info(self):
        '''
        # 获取QQ好友信息
        '''
        url = "http://s.web2.qq.com/api/get_user_friends2"
        p_data = {"vfwebqq": str(self._vfwebqq),"hash": self._get_hash()}
        r_data = {"r": json.dumps(p_data)}
        try:
            j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
            friends_data = { k['nick']: k for k in j_data["result"]["info"] }
            print("QQ好友信息：%s" % friends_data)
            return friends_data
        except:
            return None

    def _get_chat_msg(self):
        '''
        # 接收消息
        '''
        get_msg_url = "https://d1.web2.qq.com/channel/poll2"
        self._headers["Origin"] = "https://d1.web2.qq.com"
        self._headers["Referer"] = "https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1"
        self._session.headers.update(self._headers)
        p_data = {"ptwebqq": str(self._ptwebqq),
                  "clientid": 53999199,
                  "psessionid": str(self._psessionid),
                  "key": ""}
        r_data = {"r": json.dumps(p_data)}
        try:
            j_data = json.loads(self._session.post(url=get_msg_url, data=r_data).content.decode("utf-8"))
            if "errmsg" in j_data.keys():
                print(j_data)
                return None
            if "result" in j_data.keys():
                content = self._recur_list(j_data["result"][0]["value"]["content"][1:])
                return {"poll_type": j_data["result"][0]["poll_type"],
                        "from_uin": j_data["result"][0]["value"]["from_uin"],
                        "content": content
                        }
            return j_data
        except:
            print('Fetch message exception!')
            return None

    def _get_online_buddies2(self):
        '''
        # 获取QQ在线好友
        '''
        url = "http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq=" + str(self._vfwebqq) +\
              "&clientid=53999199&psessionid="+ str(self._psessionid) +\
              "&t=149429685" + str(random.randint(1000,10000))
        # self._headers["Host"] = "d1.web2.qq.com"
        # self._headers["Referer"] = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"
        # self._session.headers.update(self._headers)
        try:
            j_data = json.loads(self._session.get(url=url).content.decode("utf-8"))
            print("QQ在线好友：%s" % j_data["result"])
            return j_data["result"]
        except:
            return None

    def _get_recent_list2(self):
        '''
        # 获取最近列表
        '''
        url = "http://d1.web2.qq.com/channel/get_recent_list2"
        # self._headers["Host"] = "d1.web2.qq.com"
        # self._headers["Origin"] = "http://d1.web2.qq.com"
        # self._headers["Referer"] = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"
        # self._session.headers.update(self._headers)
        p_data = {"vfwebqq":str(self._vfwebqq),"clientid":53999199,"psessionid": str(self._psessionid)}
        r_data = {"r": json.dumps(p_data)}
        try:
            j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
            if "errmsg" in j_data.keys():
                print(j_data)
                return None
            print("QQ附近列表：%s" % j_data["result"])
            return j_data["result"]
        except:
            return None

    def _send_qun_msg(self,group_uin,msg):
        '''
        # 发送QQ群信息
        '''
        url = "https://d1.web2.qq.com/channel/send_qun_msg2"
        p_data = {"group_uin":group_uin,
                "content":'[\"' + str(msg) + '\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]',
                "face":self._face,
                "clientid":53999199,
                "msg_id":1530000 + random.randint(1000,10000),
                "psessionid":str(self._psessionid)}
        r_data = {"r": json.dumps(p_data)}
        j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
        if "errCode" in j_data.keys() and j_data["msg"] == "send ok":
            print("群消息发成功.")
            return True
        else:
            print("群消息发失败.")
            return False

    def _send_buddy_msg(self,uin,msg):
        '''
        # 发送QQ好友消息
        '''
        url = "https://d1.web2.qq.com/channel/send_buddy_msg2"
        p_data = {"to": uin,
                  "content": "[\""+ str(msg) +"\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]",
                  "face": self._face,
                  "clientid": 53999199,
                  "msg_id": 1530000 + random.randint(1000,10000),
                  "psessionid": str(self._psessionid)}
        r_data = {"r": json.dumps(p_data)}
        j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
        if "errCode" in j_data.keys() and j_data["msg"] == "send ok":
            print("好友消息发成功.")
            return True
        else:
            print("好友消息发失败.")
            return False

    def _get_self_img(self):
        '''
        # 获取自己的头像
        '''
        # self._headers["Accept"] = "image/webp,image/*,*/*;q=0.8"
        # self._headers["Host"] = "q.qlogo.cn"
        # self._headers["Referer"] = "http://w.qq.com/"
        self._session.headers.update(self._headers)
        url = 'http://q.qlogo.cn/g?b=qq&nk='+ str(self._uin) +'&s=100&t=149673935' + str(random.randint(1000, 10000))
        content = self._session.get(url=url).content
        print(content)
        return content

