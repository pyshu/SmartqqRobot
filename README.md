#  SmartQQRobot    
基于python实现的QQ机器人
    
功能：   
1、登录验证过程   
2、个人信息获取   
3、好友列表获取   
4、群列表获取    
5、发送消息     
6、接收消息    
7、简单的消息回复    
8、获取在线好友列表     
9、获取最近列表

界面:    
![image](https://github.com/pyshu/SmartQQRobot/raw/master/temp/window.png)

以上功能测试通过（date:2017-06-09）。     
   
-------------------------------    
    	
例子：(详细参见 main.py )    
from smartqq import SmartQQ     
      
qq = SmartQQ()    
       
qq._login() # 登录验证     
      
qq._get_self_info() # 获取个人信息，主要是获取gid,发送信息会用到     
      
qq._get_group_info() # 获取群列表       
      
qq._send_qun_msg(group_uin, msg)  # 发送群消息   
    
qq._get_chat_msg() # 接收消息     
      
--------------------------------     
qq._get_friends_info() # 获取好友列表    
    
qq._get_online_buddies2() # 获取在线好友列表     
     
qq._get_recent_list2() # 获取最近列表	 
      
注意:    
1、如能让SmartQQ收到消息，经实测必须退出PC上QQ客户端。      
2、为了尽量模拟webqq登录，登录成功之后，所有获取列表方法都加上(即时获取的数据不用)。    

