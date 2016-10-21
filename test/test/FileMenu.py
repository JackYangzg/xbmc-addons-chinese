#encoding=utf-8
'''
对应菜单：文件
            ->打开配置文件
            ->备份配置文件
            ->清空配置文件
'''
import os
import wx

class OpenConfifure(wx.Frame):
    '''
    操作打开配置文件的类，调用系统文本编辑工具打开配置文件
    '''

    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1)
        self.SetMinSize(wx.Size( 600, 500 ))
        self.SetMaxSize(wx.Size(600, 500))
        self.SetTitle(u"配置文件")
        self.Center()
        self._init_textCtrl()
        self._init_Sizer()
        self._init_bind()
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s"%(os.path.curdir,os.sep,self.configFileName)
        self.read_config()


    def _init_textCtrl(self):
        '''
        初始化界面
        :return:
        '''
        self.text = wx.TextCtrl(self, -1,u"请更改完后，将配置信息写入配置文件",size=(600, 420), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)

        self.writeToFileButton = wx.Button(self, -1, u"写入&&退出")
        self.DefaultButton = wx.Button(self, -1, u"还原")
        self.NoneText_1 = wx.StaticText(self, -1, "", size=(200, -1))
        self.NoneText_2 = wx.StaticText(self, -1, "", size=(200, -1))


    def _init_bind(self):
        '''
        事件的绑定操作
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.WriteToFile, self.writeToFileButton)
        self.Bind(wx.EVT_BUTTON, self.GetDefaultTxt, self.DefaultButton)

    def _init_Sizer(self):
        '''
        界面布局处理
        :return:
        '''
        self.mainSizer   = wx.BoxSizer(wx.VERTICAL)
        self.ButtonSizer = wx.FlexGridSizer(cols = 4)

        self.ButtonSizer.Add(self.writeToFileButton,flag=wx.ALL|wx.BOTTOM | wx.EXPAND)
        self.ButtonSizer.Add(self.NoneText_1, flag=wx.ALL | wx.BOTTOM)
        self.ButtonSizer.Add(self.NoneText_2, flag=wx.ALL | wx.BOTTOM)
        self.ButtonSizer.Add(self.DefaultButton, flag=wx.LEFT | wx.BOTTOM | wx.EXPAND)

        self.mainSizer.Add(self.text, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=2)
        self.mainSizer.AddSizer(self.ButtonSizer,flag=wx.ALL|wx.EXPAND, border=5)

        self.SetSizer(self.mainSizer)

    def read_config(self):
        '''
        从文件中读取配置条目显示在文本框中
        :return:
        '''
        self.configFile = open(self.currentPath,"r")
        self.defaultTxt = self.configFile.read()
        self.configFile.close()
        self.text.SetValue(self.defaultTxt)
        self.text.SetHelpText(u"请直接在该文本框中更改配置信息，更改完成后，点击写入配置文件")

    def WriteToFile(self,event):
        '''
        将数据写入文件
        :param event:
        :return:
        '''
        self.configFile = open(self.currentPath, "w")
        txt = self.text.GetValue()
        self.configFile.write(txt)
        self.configFile.close()
        self.Close()

    def GetDefaultTxt(self,event):
        '''
        退出当前界面
        :param event:
        :return:
        '''
        self.text.SetValue(self.defaultTxt)


class BackUpConfig(wx.Frame):
    '''
    备份配置文件
    '''
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1)
        self.SetMinSize(wx.Size(250, 90))
        self.SetMaxSize(wx.Size(250, 90))
        self.SetTitle(u"配置备份")
        self.Center()
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s" % (os.path.curdir, os.sep, self.configFileName)
        self._init_window()
        self._init_sizer()
        self._init_bind()

    def _init_window(self):
        '''
        初始化界面
        :return:
        '''
        message = u"=====备份 | 还原====="
        self.messageCtrl = wx.StaticText(self, -1, message, size=(120, -1), style=wx.ALIGN_CENTER)
        self.BackupButton = wx.Button(self, -1, u"备份&&退出")
        self.RecoveryButton = wx.Button(self, -1, u"从备份文件还原")
        self.NullText = wx.StaticText(self, -1, "", size=(50, -1))

    def _init_sizer(self):
        '''
        布局
        :return:
        '''
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.FlexGridSizer(cols=3)
        ButtonSizer.Add(self.BackupButton,flag= wx.ALL|wx.EXPAND, border=1)
        ButtonSizer.Add(self.NullText, flag=wx.ALL | wx.EXPAND, border=1)
        ButtonSizer.Add(self.RecoveryButton,flag=wx.ALL|wx.EXPAND, border=1)
        mainSizer.Add(self.messageCtrl,flag=wx.ALL|wx.EXPAND)
        mainSizer.AddSizer(ButtonSizer,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(mainSizer)

    def _init_bind(self):
        '''
        绑定事件
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.BackUpHandle, self.BackupButton)
        self.Bind(wx.EVT_BUTTON, self.RecoveryHandle, self.RecoveryButton)

    def GetThePath(self):
        self.OperatePath = None
        dlg = wx.FileDialog(
            self, message=u"打开文件...", defaultDir=os.getcwd(),
            defaultFile="config.bak",style=wx.SAVE
        )
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            self.OperatePath = dlg.GetPath()
        dlg.Destroy()

    def BackUpHandle(self,event):
        '''
        备份配置文件句柄
        :param event:
        :return:
        '''
        self.GetThePath()
        if (None == self.OperatePath or None == self.currentPath):
            return
        configFile = open(self.currentPath, "r")
        Txt = configFile.read()
        configFile.close()

        backupFile = open(self.OperatePath, "w")
        backupFile.write(Txt)
        backupFile.close()
        self.Close()

    def RecoveryHandle(self, event):
        '''
        备份配置文件句柄
        :param event:
        :return:
        '''
        self.GetThePath()
        if(None == self.OperatePath or None == self.currentPath):
            return
        backupFile = open(self.OperatePath, "r")
        Txt = backupFile.read()
        backupFile.close()

        configFile = open(self.currentPath, "w")
        configFile.write(Txt)
        configFile.close()
        self.Close()

class ClearConfig(wx.Frame):
    '''
    清空配置文件
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.SetMinSize(wx.Size(500, 125))
        self.SetMaxSize(wx.Size(500, 125))
        self.SetTitle(u"清空配置")
        self.Center()
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s" % (os.path.curdir, os.sep, self.configFileName)
        self._init_window()
        self._init_sizer()
        self._init_bind()

    def _init_window(self):
        '''
        创建组件
        :return:
        '''
        message = u"你确定要清空配置文件么!\nAre You Sure To Clear The Config!"
        self.messageCtrl = wx.StaticText(self, -1, message, size = (120, -1), style = wx.ALIGN_CENTER)
        self.messageCtrl.SetBackgroundColour('Yellow')
        self.messageCtrl.SetForegroundColour('Red')
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.messageCtrl.SetFont(font)

        self.ClearButton = wx.Button(self, -1, u"清空")
        self.ExitButton  = wx.Button(self, -1, u"退出")
        self.NullText = wx.StaticText(self, -1, "", size=(300, -1))

    def _init_sizer(self):
        '''
        布局
        :return:
        '''
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.ButtonSizer = wx.FlexGridSizer(cols=3)

        self.ButtonSizer.Add(self.ClearButton, flag=wx.ALL | wx.EXPAND)
        self.ButtonSizer.Add(self.NullText, flag=wx.ALL | wx.EXPAND)
        self.ButtonSizer.Add(self.ExitButton, flag=wx.ALL | wx.EXPAND)

        self.mainSizer.Add(self.messageCtrl, flag=wx.ALL | wx.EXPAND, border=2)
        self.mainSizer.AddSizer(self.ButtonSizer, flag=wx.ALL | wx.EXPAND, border=1)

        self.SetSizer(self.mainSizer)

    def _init_bind(self):
        '''
        事件的绑定操作
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.ClearHandle, self.ClearButton)
        self.Bind(wx.EVT_BUTTON, self.ExitHandle, self.ExitButton)

    def ClearHandle(self,e):
        '''
        清空配置文件
        :return:
        '''
        configFile = open(self.currentPath, "w")
        configFile.write("")
        configFile.close()
        self.Close()

    def ExitHandle(self,e):
        '''
        退出
        :return:
        '''
        self.Close()



if __name__ == "__main__":
    switch_test = 3
    app = wx.App()

    if switch_test == 1:
        frame = OpenConfifure(None)
    elif switch_test == 2:
        frame = BackUpConfig(None)
    elif switch_test == 3:
        frame = ClearConfig(None)

    frame.Show()
    app.MainLoop()







