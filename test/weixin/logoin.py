#coding=utf8
import thread
import time

import itchat
from itchat.content import *

class wxbasic():
    def __init__(self):
        """
        初始化
        """
        pass

    def wxLogon(self):
        '''
        登录到微信
        :return:
        '''
        itchat.auto_login(hotReload=True)

    def wxRun(self):
        '''
        微信运行时状态
        :return:
        '''
        #itchat.run()
        itchat.dump_login_status()

    def GetUserName(self, Comment):
        '''
        通过备注获取到用户的UserName
        :return:
        '''
        userDict =  itchat.search_friends(name=Comment)
        if(userDict):
            return userDict[0]['UserName']
        else:
            my = userDict['UserName']
            itchat.send(u"向用户[%s]发送失败,请检查是否存在该好友！"%(Comment), my)
            return None


    def SendMsg(self,Msg,UserName):
        '''
        向指定用户发送指定数据
        :param Msg:
        :param UserName:
        :return:
        '''
        username = self.GetUserName(UserName)
        if(username):
            itchat.send(Msg, username)
        else:
            print(u"指定用户[%s]不在你的好友列表"%(username))







