import os
import re
import shutil
import itchat
import time
from itchat.content import *
from threading import Timer


# 定义一个dict，保存消息体
msg_dict = {}
# 定义一个list，保存要撤回的消息类型
msg_type_listen = ['Text','Picture']


# 收集群文本消息
@itchat.msg_register([TEXT], isGroupChat=True)
def _(msg):
    #存到字典
    msg_dict[msg.MsgId] = msg
    # print(msg_dict)


# 收集群图片消息
@itchat.msg_register([PICTURE], isGroupChat=True)
def download_files(msg):

    #过滤掉官方表情，只存图片和自定义表情
    if msg['Content'] != '':
        # 存到字典
        msg_dict[msg.MsgId] = msg
        # 下载图片到本地
        msg.download(msg.fileName)


# 捕获撤回消息的提醒，查找旧消息并回复
@itchat.msg_register(NOTE, isGroupChat=True)
def _(msg):
    match = re.search('撤回了一条消息', msg['Content'])

    if match:

        #从撤回消息里提取被撤回的消息的msg_id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)

        #判断被撤回消息的msg_id在不在已收取的消息里
        if old_msg_id in msg_dict.keys():
            old_msg = msg_dict[old_msg_id]

            # 原消息是文本消息
            if old_msg['Type'] == 'Text':
                old_msg_text = msg_dict[old_msg_id]['Text']
                itchat.send(msg=msg['ActualNickName']+' 刚才发过这条消息：'+old_msg_text, toUserName=msg['FromUserName'])

            # 原消息是图片消息
            elif old_msg['Type'] == 'Picture':

                # 发送文本消息
                itchat.send_msg(msg=msg['ActualNickName']+' 刚才发过这张图片👇', toUserName=msg['FromUserName'])

                # 发送图片消息
                old_msg_img_file_dir = msg_dict[old_msg_id]['FileName']
                itchat.send('@img@%s' % old_msg_img_file_dir, toUserName=msg['FromUserName'])


# 定时干掉字典里和文件夹里的超时消息备份
out_date_msg_dict = []

def delete_out_date_msg():

    # 遍历存储消息的dict里，哪些消息过期，把消息的key放到list里
    for m in msg_dict:

        current_time = time.time()
        current_time_int = int(current_time)

        if (current_time_int - msg_dict[m]['CreateTime']) > 8:

            out_date_msg_dict.append(m)

    # 用已存储在list里的过期消息的key，去删掉dict里的消息本身和对应文件
    for n in out_date_msg_dict:

        #文本消息只要删掉dict里的消息
        if msg_dict[n]['Type'] == 'Text':
            msg_dict.pop(n)

        #图片消息要额外删掉文件
        elif msg_dict[n]['Type'] == 'Picture':
            os.remove(msg_dict[n]['FileName'])
            msg_dict.pop(n)

        # 清空存储过期消息key的list，为下一次遍历做准备
        out_date_msg_dict.clear()


    t = Timer(2, delete_out_date_msg)
    t.start()

delete_out_date_msg()

itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run()

