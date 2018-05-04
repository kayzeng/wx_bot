import itchat, time
from itchat.content import *

@itchat.msg_register([TEXT])
def text_reply(msg):
    match = re.search('年', msg['Text']).span()
    if match:
        itchat.send(('那我祝您狗年大吉大利'), msg['FromUserName'])

itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run()