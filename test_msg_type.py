import os
import re
import shutil
import itchat
import time
from itchat.content import *


# 定义一个字典，保存消息的信息
msg_dict = {}


# 收集群文本消息到字典里
@itchat.msg_register([PICTURE], isGroupChat=True)
def _(msg):
    msg_dict[msg.MsgId] = msg
    print(msg_dict)



itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run()