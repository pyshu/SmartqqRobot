#  SmartQQRobot    
基于python实现的QQ自动回复机器人
    
功能：   
1、登录验证过程   
2、个人信息获取   
3、好友列表获取   
4、群列表获取    
5、发送消息     
6、接收消息    
7、自动消息回复    
    	
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
      
注意:    
1、如能让SmartQQ收到消息，经实测必须退出PC上QQ客户端。    
