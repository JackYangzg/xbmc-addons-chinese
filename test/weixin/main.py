#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from logoin import *
from ParseRecodes import *
from time import sleep
import wx
import os
import six
import threading

class main_frame(wx.Frame):
    '''
    主界面
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.SetMinSize(wx.Size(400, 230))
        self.SetMaxSize(wx.Size(400, 230))
        self.SetTitle(u"向家长发送成绩....")
        self.icon = wx.Icon('main.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.wxFile = None
        self.recodeFile = None
        self.Over = False
        self.Center()
        self._init_window()
        self._init_sizer()
        self._init_bind()

    def _init_window(self):
        '''
        初始化界面
        :return:
        '''
        self.wxFileButton = wx.Button(self, -1, u"打开花名册")
        self.RecodeButton = wx.Button(self, -1, u"打开成绩")
        self.OkButton = wx.Button(self, -1, u"确认发送成绩")
        self.NullText = wx.StaticText(self, -1, "", size=(205, -1))
        self.NullText1 = wx.StaticText(self, -1, "", size=(230, 100))
        self.CtrlText1 = wx.TextCtrl(self, -1, "", size=(300, -1))
        self.t1 = wx.Timer(self)

        self.CtrlText1.SetToolTipString("请输入此次考试的名称！\n"
                                        "譬如：第12周语文考试")

        self.OkButton.SetToolTipString("单击该按钮向家长发送学生的成绩\n"
                                       "当发送完毕之后，该按钮将变绿")

    def _init_sizer(self):
        '''
        布局
        :return:
        '''
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.FlexGridSizer(cols=3)
        ButtonSizer.Add(self.wxFileButton, flag=wx.ALL | wx.EXPAND, border=1)
        ButtonSizer.Add(self.NullText, flag=wx.ALL | wx.EXPAND, border=1)
        ButtonSizer.Add(self.RecodeButton, flag=wx.ALL | wx.EXPAND, border=1)
        mainSizer.Add(self.CtrlText1, flag=wx.ALL | wx.EXPAND)
        mainSizer.AddSizer(ButtonSizer, flag=wx.ALL | wx.EXPAND)
        mainSizer.Add(self.NullText1, flag=wx.ALL | wx.EXPAND)
        mainSizer.Add(self.OkButton, flag=wx.ALL | wx.EXPAND, border=1)
        self.SetSizer(mainSizer)

    def _init_bind(self):
        '''
        绑定事件
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.OpenwxFileButton, self.wxFileButton)
        self.Bind(wx.EVT_BUTTON, self.OpenRecodeFileButton, self.RecodeButton)
        self.Bind(wx.EVT_BUTTON, self.SendRecodeButton, self.OkButton)
        self.Bind(wx.EVT_TIMER, self.CheckIsSendOver, self.t1)

    def GetThePath(self):
        OperatePath = None
        dlg = wx.FileDialog(
            self, message=u"打开文件...", defaultDir=os.getcwd(),
            defaultFile="4班花名册.xls", style=wx.SAVE
        )
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            OperatePath = dlg.GetPath()
        dlg.Destroy()
        return OperatePath

    def OpenwxFileButton(self, event):
        '''
        备份配置文件句柄
        :param event:
        :return:
        '''
        self.wxFile = self.GetThePath()


    def OpenRecodeFileButton(self, event):
        '''
        备份配置文件句柄
        :param event:
        :return:
        '''
        self.recodeFile = self.GetThePath()

    def SendRecodeButton(self, event):
        '''
        發送學生成績
        :param event:
        :return:
        '''
        if(self.recodeFile == None or self.wxFile == None):
            print(u"請設定每一個文件。再點擊該按鈕！")
            return
        self.t1.Start(1000)
        t = threading.Thread(target=self.sendRecode)
        t.start()

    def sendRecode(self):

        self.Over = False
        self.IndexData = self.CtrlText1.GetValue()
        wxb = wxbasic()
        wxfile = GetUserWxName()
        recodefile = ReadRecodeOperation()
        wxb.wxLogon()
        wxfile.OpenExl(self.wxFile)
        recodefile.OpenExl(self.recodeFile)
        rows = wxfile.GetNrowsOfTable()
        for i in range(1, rows):
            try:
                user = wxfile.GetIndexUser(i)
                username = wxfile.GetWxName(user)
                print ("begin to send the data of :" + str(user))
                recode = recodefile.GetUserData(user)
                wxb.SendMsg(self.IndexData + ":\n\n" + recode + "\n", username)
            except Exception as e:
                print("Have errors Occur in the times [%d]"%(i))
            sleep(5)
        wxb.wxRun()
        print("\n\nSend OverO(∩_∩)O\n\n")
        self.Over = True

    def CheckIsSendOver(self, evt):
        if(self.Over == True):
            self.OkButton.SetBackgroundColour("green")
        else:
            self.OkButton.SetBackgroundColour("yellow")



if __name__ == "__main__":
    app = wx.App()
    frame = main_frame(None)
    frame.Show()
    app.MainLoop()

