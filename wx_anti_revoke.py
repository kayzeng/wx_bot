import os
import re
import shutil
import itchat
import time
from itchat.content import *
from threading import Timer


# 定义一个字典，保存消息体
msg_dict = {}


# 收集群文本消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def _(msg):
    #存到字典
    msg_dict[msg.MsgId] = msg
    # print(msg_dict)


# 收集群图片消息
@itchat.msg_register([PICTURE], isGroupChat=True)
def download_files(msg):

    # 下载图片到本地
    msg.download(msg.fileName)

    # 存到字典
    msg_dict[msg.MsgId] = msg
    # print(msg_dict)



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
            itchat.send(msg=msg['ActualNickName']+' 刚才发过这条消息：'+old_msg_text, toUserName=msg['FromUserName'])

        # 原消息是图片消息
        elif old_msg['Type'] == 'Picture':

            # 发送文本消息
            itchat.send_msg(msg=msg['ActualNickName']+' 刚才发过这张图片', toUserName=msg['FromUserName'])

            # 发送图片消息
            old_msg_img_file_dir = msg_dict[old_msg_id]['FileName']
            itchat.send('@img@%s' % old_msg_img_file_dir, toUserName=msg['FromUserName'])



# 定时干掉字典里和文件夹里的超时消息备份
out_date_msg_dict = []

def delete_out_date_msg():
    for m in msg_dict:

        current_time = time.time()
        current_time_int = int(current_time)

        if (current_time_int - msg_dict[m]['CreateTime']) > 130:

            out_date_msg_dict.append(m)

    for n in out_date_msg_dict:

        if msg_dict[n]['Type'] == 'Text':
            msg_dict.pop(n)

        elif msg_dict[n]['Type'] == 'Picture':
            os.remove(msg_dict[n]['FileName'])
            msg_dict.pop(n)

        # print(msg_dict)
        out_date_msg_dict.clear()


    t = Timer(10, delete_out_date_msg)
    t.start()

delete_out_date_msg()

itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run()

