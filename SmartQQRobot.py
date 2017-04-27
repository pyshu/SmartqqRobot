# -*- coding: utf-8 -*-
__author__ = 'lius'

import tkinter
import requests
import random
import time
import json
from multiprocessing import Process

class SmartQQRobot():
    def __init__(self):
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
        self._face = 0

        # self._login_status = False

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
        return 2147483647 & token

    def _check_login_status(self,p):
        # 登录状态检测
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
        # self._ptwebqq = json.loads(self._session.get(url=url).content.decode("utf-8"))["result"]["vfwebqq"]
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
        uin = int(self._uin)
        ptwebqq = self._ptwebqq
        # hah = "0A4C0362501C02FE"
        ptb = [0,0,0,0]
        for i in range(len(ptwebqq)):
            ptb[i % 4] ^= ord(ptwebqq[i])
        # salt = ["EC", "OK"]
        uin = int(uin)
        uinByte = [0,0,0,0]
        uinByte[0] = uin >> 24 & 255 ^ 69
        uinByte[1] = uin >> 16 & 255 ^ 67
        uinByte[2] = uin >> 8 & 255 ^ 79
        uinByte[3] = uin & 255 ^ 75
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

    def _get_group_info(self):
        url = "http://s.web2.qq.com/api/get_group_name_list_mask2"
        p_data = {"vfwebqq": str(self._vfwebqq), "hash": self._get_hash()}
        r_data = {"r": json.dumps(p_data)}
        j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
        print("QQ群：")
        # for group in j_data["result"]["gnamelist"]:
        #     print(group["name"])
        print(j_data["result"]["gnamelist"])
        return j_data["result"]["gnamelist"]

    def _get_friends_info(self):
        url = "http://s.web2.qq.com/api/get_user_friends2"
        p_data = {"vfwebqq": str(self._vfwebqq),"hash": self._get_hash()}
        r_data = {"r": json.dumps(p_data)}
        j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
        print("QQ好友信息：")
        print(j_data)
        return j_data

    def _get_chat_msg(self):
        get_msg_url = "https://d1.web2.qq.com/channel/poll2"
        # self._headers["Origin"] = "http://d1.web2.qq.com"
        # self._headers["Referer"] = "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"
        # self._session.headers.update(self._headers)
        p_data = {"ptwebqq": str(self._ptwebqq),
                  "clientid": 53999199,
                  "psessionid": str(self._psessionid),
                  "key": ""}
        r_data = {"r": json.dumps(p_data)}
        j_data = json.loads(self._session.post(url=get_msg_url, data=r_data).content.decode("utf-8"))
        print(j_data)
        if j_data.keys("errmsg"):
            return "None"
        if j_data.keys("result"):# and  j_data["result"]["poll_type"] == "group_message":
            return {"poll_type":j_data["result"]["poll_type"],
                     "from_uin":j_data["result"]["value"]["from_uin"],
                     "content":j_data["result"]["value"]["content"][1:]
                    }
        return j_data
        '''{"errmsg":"error!!!","retcode":0}'''
        '''{"result":[{"poll_type":"group_message",
                      "value":{"content":[["font",{"color":"000000","name":"微软雅黑","size":10,"style":[0,0,0]}],"4"],
                               "from_uin":1031415212,
                                "group_code":1031415212,"msg_id":56791,"msg_type":0,"send_uin":2327452558,"time":1493302500,"to_uin":979885605}}],"retcode":0}
        '''
        '''{"result":[{"poll_type":"message",
                      "value":{"content":[["font",{"color":"000000","name":"微软雅黑","size":10,"style":[0,0,0]}],"哈哈"],
                      "from_uin":2327452558,
                      "msg_id":56807,"msg_type":0,"time":1493304815,"to_uin":979885605}}],"retcode":0}'''
        '''{"result":[{"poll_type":"group_message",
                        "value":{"content":[["font",{"color":"000000","name":"微软雅黑","size":10,"style":[0,0,0]}],"哼哼","@时光1号",""," "],
                        "from_uin":1031415212,
                        "group_code":1031415212,"msg_id":56815,"msg_type":0,"send_uin":2327452558,"time":1493305091,"to_uin":979885605}}],"retcode":0}'''

    def _get_self_info(self):
        url = "http://s.web2.qq.com/api/get_self_info2?t=1493263376886"
        j_data = json.loads(self._session.get(url=url).content.decode("utf-8"))
        self._face = j_data["result"]["face"]
        print("我的QQ资料：")
        print(j_data)
        return j_data

    def _send_qun_msg(self,group_uin,msg):
        url = "https://d1.web2.qq.com/channel/send_qun_msg2"
        p_data = {"group_uin":group_uin,
                "content":'[\"' + str(msg) + '\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]',
                "face":self._face,
                "clientid":53999199,
                "msg_id":1530000 + random.randint(1000,10000),
                "psessionid":str(self._psessionid)}
        r_data = {"r": json.dumps(p_data)}
        j_data = json.loads(self._session.post(url=url, data=r_data).content.decode("utf-8"))
        print("群消息发送状态：%s" % j_data)

    def msg_robot(self):
        self._get_self_info()
        self._get_friends_info()

        for group in self._get_group_info():
            if group['name'] == "时光 年华":
                group_uin = group['gid']
                msg = "你们好啊，我是机器人！"
                self._send_qun_msg(group_uin,msg)
                time.sleep(10)
        # while 1:
            # self._get_chat_msg()
            # self._send_qun_msg(group_uin)
            # time.sleep(3)

    def run(self):
        self._login()
        self.msg_robot()

if __name__=="__main__":
    qq = SmartQQRobot()
    qq.run()