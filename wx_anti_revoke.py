import os
import re
import shutil
import itchat
import time
from itchat.content import *


# 定义一个字典，保存消息的信息
msg_dict = {}


# 新建一个文件夹，保存消息的图片
msg_file_tmp_dir = "/Users/kayzeng/Downloads/itchat/msg_file_tmp/"
if not os.path.exists(msg_file_tmp_dir):
    os.mkdir(msg_file_tmp_dir)


# 收集群文本消息到字典里
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def _(msg):
    msg_dict[msg.MsgId] = msg


# 收集群图片消息到字典里
@itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)
def _(msg):
    msg_dict[msg.MsgId] = msg


# 捕获撤回消息的提醒，查找旧消息并回复
@itchat.msg_register(NOTE, isGroupChat=True)
def _(msg):
    match = re.search('撤回了一条消息', msg['Content'])
    if match:

        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_dict[old_msg_id]

        # 原消息是文本消息
        if old_msg['Type'] == 'Text':
            old_msg_text = msg_dict[old_msg_id]['Text']
            itchat.send(msg=msg['ActualNickName']+'：'+old_msg_text, toUserName=msg['FromUserName'])

        # 原消息是图片消息
        elif old_msg['Type'] == 'Picture':


# 定时干掉字典里和文件夹里的超时消息备份



itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run()