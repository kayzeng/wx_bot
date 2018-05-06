import os
import re
import shutil
import itchat
import time
from itchat.content import *


# 定义一个字典，保存消息的信息
msg_dict = {}


current_time = time.time()
current_time_int = int(current_time)


@itchat.msg_register([TEXT], isGroupChat=True)
def _(msg):
    msg_dict[msg.MsgId] = msg
    # print(msg_dict)
    print(current_time_int)
    print(msg['CreateTime'])
    delta = msg['CreateTime'] - current_time_int
    print(delta)
    print(type(delta))



# msg_dict@itchat.msg_register([PICTURE], isGroupChat=True)
# def download_files(msg):
#
#     # 下载图片到本地
#     msg.download(msg.fileName)
#
#     # 图片消息存到字典
#     msg_dict[msg.MsgId] = msg
#     print(msg_dict)




# 发送文本消息
# itchat.send_msg(msg='Text Message', toUserName=None)

# 发送图片消息
# send_img(fileDir, toUserName=None)


itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run()