#encoding=utf-8
'''
对应菜单：文件
            ->PLC配置界面
            ->远程服务配置界面
            ->用户配置界面
'''
import wx
import libconf
import os
import io
import re
import string

class PlcConfigFrame(wx.Frame):
    '''
    PLC配置界面
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s" % (os.path.curdir, os.sep, self.configFileName)

        self.SetMinSize(wx.Size(475, 400))
        self.SetMaxSize(wx.Size(475, 400))
        self.SetTitle(u"PLC配置")
        self.Center()
        self.SetBackgroundColour('#4f5049')
        self._init_param()
        self._init_from_confile()
        self._init_window()
        self._init_Sizer()
        self._init_the_Text()
        self._init_bind()

    def _init_param(self):
        '''
        初始化配置代码{以字典形式}
        :return:
        '''
        self.plcConfigDict = {"PLCAddr": "192.168.30.1",
                              "PLCPort": 102,
                              "PLCSlot": 0,
                              "PLCRack": 2,
                              "PLCLocalTSAP": 512,
                              "PLCRemoteTSAP": 512,
                              "ConnectionType": 1}

    def _init_from_confile(self):
        """
        从配置文件中初始化配置
        :return:
        """
        with io.open(self.currentPath, 'r', encoding='utf-8') as f:
            config = libconf.load(f)
        if(config.has_key("PLCconfig")):
            self.plcConfigDict = config["PLCconfig"]

    def _init_the_Text(self):
        '''
        填充内容
        :return:
        '''
        self.IpCtrl.SetValue(self.plcConfigDict["PLCAddr"])
        self.PortCtrl.SetValue(str(self.plcConfigDict["PLCPort"]))
        self.SlotCtrl.SetValue(str(self.plcConfigDict["PLCSlot"]))
        self.RackCtrl.SetValue(str(self.plcConfigDict["PLCRack"]))
        self.STSAPCtrl.SetValue(str(self.plcConfigDict["PLCLocalTSAP"]))
        self.RTSAPCtrl.SetValue(str(self.plcConfigDict["PLCRemoteTSAP"]))
        if(self.plcConfigDict["ConnectionType"] == 1):
            comtxt = "PG"
        elif(self.plcConfigDict["ConnectionType"] == 1):
            comtxt = "OP"
        else:
            comtxt = "BASIC"
        self.ConTypeCtrl.SetValue(comtxt)

    def _get_from_the_frame(self):
        '''
        从输入获取配置
        :return:
        '''
        IP = self.IpCtrl.GetValue()
        if(IP):
            self.plcConfigDict["PLCAddr"] = IP
        PORT = self.PortCtrl.GetValue()
        if(PORT):
            self.plcConfigDict["PLCPort"] = string.atoi(PORT)
        SLOT = self.SlotCtrl.GetValue()
        if (SLOT):
            self.plcConfigDict["PLCSlot"] = string.atoi(SLOT)
        RACK = self.RackCtrl.GetValue()
        if (RACK):
            self.plcConfigDict["PLCRack"] = string.atoi(RACK)
        STSAP = self.STSAPCtrl.GetValue()
        if (STSAP):
            self.plcConfigDict["PLCLocalTSAP"] = string.atoi(STSAP)
        RTSAP = self.RTSAPCtrl.GetValue()
        if (RTSAP):
            self.plcConfigDict["PLCRemoteTSAP"] = string.atoi(RTSAP)
        CONTYPE = self.ConTypeCtrl.GetValue()
        if (CONTYPE == "PG"):
            self.plcConfigDict["ConnectionType"] = 1
        elif (CONTYPE == "OP"):
            self.plcConfigDict["ConnectionType"] = 2
        elif (CONTYPE == "BASIC"):
            self.plcConfigDict["ConnectionType"] = 3

    def _Dict_toFile(self, config):
        '''
        将字典解析后写入配置文件{只考虑两层的字典}
        :return:
        '''
        configTxt = ""
        for ConfigIndex in config:
            configTxt = "%s%s :\n{\n"%(configTxt,ConfigIndex)
            for RealConf in config[ConfigIndex]:
                if(type(config[ConfigIndex][RealConf]) is unicode):
                    configTxt = "%s    %s  =  \"%s\";\n" % (configTxt, RealConf, config[ConfigIndex][RealConf])
                else:
                    configTxt = "%s    %s  =  %s;\n"%(configTxt,RealConf,config[ConfigIndex][RealConf])
            configTxt = "%s};\n"%(configTxt)
        filehandle = open(self.currentPath,"w")
        filehandle.write(configTxt)
        filehandle.close()

    def _checkip(self, ip):
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(ip):
            return True
        else:
            return False

    def _init_window(self):
        '''
        初始化界面
        :return:
        '''
        self.IpCtrl    = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.IpText    = wx.StaticText(self,-1,"PLC IP",size=(100,-1))
        self.PortCtrl  = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.PortText = wx.StaticText(self, -1, "PLC Port", size=(100, -1))
        self.SlotCtrl  = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.SlotText = wx.StaticText(self, -1, "PLC Slot", size=(100, -1))
        self.RackCtrl  = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.RackText = wx.StaticText(self, -1, "PLC Rack", size=(100, -1))
        self.STSAPCtrl = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.STSAPText = wx.StaticText(self, -1, "PLC SRTSP", size=(100, -1))
        self.RTSAPCtrl = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.RTSAPText = wx.StaticText(self, -1, "PLC RTSAP", size=(100, -1))
        self.ConTypeCtrl = wx.ComboBox(self, -1)
        self.ConTypeCtrl.Append("PG")
        self.ConTypeCtrl.Append("OP")
        self.ConTypeCtrl.Append("BASIC")

        self.ConTypeText = wx.StaticText(self, -1, "Connection Type", size=(100, -1))
        self.NoneText_1 = wx.StaticText(self, -1, "", size=(100, -1))
        self.NoneText_2 = wx.StaticText(self, -1, "", size=(100, -1))

        self.OkButton  = wx.Button(self, -1, u"确定")
        self.ExitButton = wx.Button(self, -1, u"取消")

    def _init_Sizer(self):
        '''
        布局
        :return:
        '''
        self.PlcFlexSizer = wx.FlexGridSizer(rows=8, cols=2, vgap=10, hgap=20)
        self.PlcFlexSizer.AddMany([(self.IpText, -1, wx.ALL | wx.EXPAND), (self.PortText, -1, wx.ALL | wx.EXPAND),
                                   (self.IpCtrl, -1, wx.ALL | wx.EXPAND), (self.PortCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.SlotText, -1, wx.ALL | wx.EXPAND), (self.RackText, -1, wx.ALL | wx.EXPAND),
                                   (self.SlotCtrl, -1, wx.ALL | wx.EXPAND), (self.RackCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.STSAPText, -1, wx.ALL | wx.EXPAND), (self.RTSAPText, -1, wx.ALL | wx.EXPAND),
                                   (self.STSAPCtrl, -1, wx.ALL | wx.EXPAND), (self.RTSAPCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.ConTypeText, -1, wx.ALL | wx.EXPAND),(self.NoneText_1, -1, wx.ALL | wx.EXPAND),
                                   (self.ConTypeCtrl, -1, wx.ALL | wx.EXPAND)
                                   ])
        self.buttonSizer = wx.FlexGridSizer(rows=1, cols=4)
        self.buttonSizer.Add(self.OkButton,flag = wx.LEFT | wx.EXPAND, border =1)
        self.buttonSizer.Add(self.NoneText_1, flag=wx.ALL | wx.EXPAND, border=1)
        self.buttonSizer.Add(self.NoneText_2, flag=wx.ALL | wx.EXPAND, border=1)
        self.buttonSizer.Add(self.ExitButton,flag = wx.RIGHT | wx.EXPAND, border =1)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.AddSizer(self.PlcFlexSizer,flag = wx.ALL | wx.EXPAND, border =20)
        self.mainSizer.AddSizer(self.buttonSizer,flag = wx.ALL | wx.EXPAND, border =20)

        self.SetSizer(self.mainSizer)

    def _init_bind(self):
        '''
        绑定事件
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.OkHandle, self.OkButton)
        self.Bind(wx.EVT_BUTTON, self.ExitHandle, self.ExitButton)
        self.Bind(wx.EVT_TEXT, self.IpHandle, self.IpCtrl)

    def ExitHandle(self, e):
        '''
        退出按钮句柄
        :return:
        '''
        self.Close()

    def OkHandle(self, e):
        '''
        确定按钮句柄
        :return:
        '''
        with io.open(self.currentPath, 'r', encoding='utf-8') as f:
            config = libconf.load(f)
        if (config.has_key("PLCconfig")):
            plc_config = config.pop("PLCconfig")
        self._get_from_the_frame()
        tempConfig = {"PLCconfig" : self.plcConfigDict}
        config.update(tempConfig)
        self._Dict_toFile(config)
        self.Close()

    def IpHandle(self,e):
        '''
        处理输入IP的检测
        :param e:
        :return:
        '''
        IP = self.IpCtrl.GetValue()
        if(not self._checkip(IP)):
            self.IpCtrl.SetBackgroundColour("red")
        else:
            self.IpCtrl.SetBackgroundColour("green")


class RemoteConfigFrame(wx.Frame):
    '''
    远程服务器配置界面
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s" % (os.path.curdir, os.sep, self.configFileName)

        self.SetMinSize(wx.Size(475, 250))
        self.SetMaxSize(wx.Size(475, 250))
        self.SetTitle(u"远程服务器配置")
        self.Center()
        self.SetBackgroundColour('#4f5049')
        self._init_param()
        self._init_from_confile()
        self._init_window()
        self._init_Sizer()
        self._init_the_Text()
        self._init_bind()

    def _init_param(self):
        '''
        初始化配置代码{以字典形式}
        :return:
        '''
        self.RemoteConfigDict = {"IpAddress": "0.0.0.0",
                              "Port": 0,
                              "AsyncConect": False
                              }

    def _init_from_confile(self):
        """
        从配置文件中初始化配置
        :return:
        """
        with io.open(self.currentPath, 'r', encoding='utf-8') as f:
            config = libconf.load(f)
        if(config.has_key("remotesocket")):
            self.RemoteConfigDict = config["remotesocket"]

    def _init_the_Text(self):
        '''
        填充内容
        :return:
        '''
        self.IpCtrl.SetValue(self.RemoteConfigDict["IpAddress"])
        self.PortCtrl.SetValue(str(self.RemoteConfigDict["Port"]))

        if(self.RemoteConfigDict["AsyncConect"] == False):
            comtxt = "SyncConect"
        else:
            comtxt = "AsyncConect"
        self.ConTypeCtrl.SetValue(comtxt)

    def _get_from_the_frame(self):
        '''
        从输入获取配置
        :return:
        '''
        IP = self.IpCtrl.GetValue()
        if(IP):
            self.RemoteConfigDict["IpAddress"] = IP
        PORT = self.PortCtrl.GetValue()
        if(PORT):
            self.RemoteConfigDict["Port"] = string.atoi(PORT)
        CONTYPE = self.ConTypeCtrl.GetValue()
        if(CONTYPE == "SyncConect"):
            self.RemoteConfigDict["ConnectionType"] = False
        elif (CONTYPE == "AsyncConect"):
            self.RemoteConfigDict["ConnectionType"] = True

    def _Dict_toFile(self, config):
        '''
        将字典解析后写入配置文件{只考虑两层的字典}
        :return:
        '''
        configTxt = ""
        for ConfigIndex in config:
            configTxt = "%s%s :\n{\n"%(configTxt,ConfigIndex)
            for RealConf in config[ConfigIndex]:
                if(type(config[ConfigIndex][RealConf]) is unicode):
                    configTxt = "%s  %s  =  \"%s\";\n" % (configTxt, RealConf, config[ConfigIndex][RealConf])
                else:
                    configTxt = "%s  %s  =  %s;\n"%(configTxt,RealConf,config[ConfigIndex][RealConf])
            configTxt = "%s};\n"%(configTxt)
        filehandle = open(self.currentPath,"w")
        filehandle.write(configTxt)
        filehandle.close()

    def _checkip(self, ip):
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(ip):
            return True
        else:
            return False

    def _init_window(self):
        '''
        初始化界面
        :return:
        '''
        self.IpCtrl    = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.IpText    = wx.StaticText(self,-1,"Remote Server IP",size=(200,-1))
        self.PortCtrl  = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.PortText = wx.StaticText(self, -1, "Remote Server Port", size=(200, -1))

        self.ConTypeCtrl = wx.ComboBox(self, -1)
        self.ConTypeCtrl.Append(u"SyncConect")
        self.ConTypeCtrl.Append(u"AsyncConect")

        self.ConTypeText = wx.StaticText(self, -1, "Connection Type", size=(200, -1))
        self.NoneText_1 = wx.StaticText(self, -1, "", size=(100, -1))
        self.NoneText_2 = wx.StaticText(self, -1, "", size=(100, -1))

        self.OkButton  = wx.Button(self, -1, u"确定")
        self.ExitButton = wx.Button(self, -1, u"取消")

    def _init_Sizer(self):
        '''
        布局
        :return:
        '''
        self.PlcFlexSizer = wx.FlexGridSizer(rows=3, cols=2, vgap=10, hgap=20)
        self.PlcFlexSizer.AddMany([(self.IpText, -1, wx.ALL | wx.EXPAND), (self.IpCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.PortText, -1, wx.ALL | wx.EXPAND), (self.PortCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.ConTypeText, -1, wx.ALL | wx.EXPAND),(self.ConTypeCtrl, -1, wx.ALL | wx.EXPAND),
                                   ])
        self.buttonSizer = wx.FlexGridSizer(rows=1, cols=4)
        self.buttonSizer.Add(self.OkButton,flag = wx.LEFT | wx.EXPAND, border =1)
        self.buttonSizer.Add(self.NoneText_1, flag=wx.ALL | wx.EXPAND, border=1)
        self.buttonSizer.Add(self.NoneText_2, flag=wx.ALL | wx.EXPAND, border=1)
        self.buttonSizer.Add(self.ExitButton,flag = wx.RIGHT | wx.EXPAND, border =1)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.AddSizer(self.PlcFlexSizer,flag = wx.ALL | wx.EXPAND, border =20)
        self.mainSizer.AddSizer(self.buttonSizer,flag = wx.ALL | wx.EXPAND, border =20)

        self.SetSizer(self.mainSizer)

    def _init_bind(self):
        '''
        绑定事件
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.OkHandle, self.OkButton)
        self.Bind(wx.EVT_BUTTON, self.ExitHandle, self.ExitButton)
        self.Bind(wx.EVT_TEXT, self.IpHandle, self.IpCtrl)

    def ExitHandle(self, e):
        '''
        退出按钮句柄
        :return:
        '''
        self.Close()

    def OkHandle(self, e):
        '''
        确定按钮句柄
        :return:
        '''
        with io.open(self.currentPath, 'r', encoding='utf-8') as f:
            config = libconf.load(f)
        if (config.has_key("remotesocket")):
            plc_config = config.pop("remotesocket")
        self._get_from_the_frame()
        tempConfig = {"remotesocket" : self.RemoteConfigDict}
        config.update(tempConfig)
        self._Dict_toFile(config)
        self.Close()

    def IpHandle(self,e):
        '''
        处理输入IP的检测
        :param e:
        :return:
        '''
        IP = self.IpCtrl.GetValue()
        if(not self._checkip(IP)):
            self.IpCtrl.SetBackgroundColour("red")
        else:
            self.IpCtrl.SetBackgroundColour("green")



class UserConfigFrame(wx.Frame):
    '''
    远程服务器配置界面
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s" % (os.path.curdir, os.sep, self.configFileName)

        self.SetMinSize(wx.Size(475, 250))
        self.SetMaxSize(wx.Size(475, 250))
        self.SetTitle(u"用户配置")
        self.Center()
        self.SetBackgroundColour('#4f5049')
        self._init_param()
        self._init_from_confile()
        self._init_window()
        self._init_Sizer()
        self._init_the_Text()
        self._init_bind()

    def _init_param(self):
        '''
        初始化配置代码{以字典形式}
        :return:
        '''
        self.UserConfigDict = {"MachineName": "JIANGYE",
                              "PassWord": "NONE",
                              "Frequency": 10
                              }

    def _init_from_confile(self):
        """
        从配置文件中初始化配置
        :return:
        """
        with io.open(self.currentPath, 'r', encoding='utf-8') as f:
            config = libconf.load(f)
        if(config.has_key("SysConfig")):
            self.UserConfigDict = config["SysConfig"]

    def _init_the_Text(self):
        '''
        填充内容
        :return:
        '''
        self.MachineCtrl.SetValue(self.UserConfigDict["MachineName"])
        self.PasswordCtrl.SetValue(self.UserConfigDict["PassWord"])
        self.FreqCtrl.SetValue(str(self.UserConfigDict["Frequency"]))

    def _get_from_the_frame(self):
        '''
        从输入获取配置
        :return:
        '''
        Machine = self.MachineCtrl.GetValue()
        if(Machine):
            self.UserConfigDict["MachineName"] = Machine
        Password = self.PasswordCtrl.GetValue()
        if(Password):
            self.UserConfigDict["PassWord"] = Password
        Freq = self.FreqCtrl.GetValue()
        if(Freq):
            self.UserConfigDict["Frequency"] = string.atoi(Freq)

    def _Dict_toFile(self, config):
        '''
        将字典解析后写入配置文件{只考虑两层的字典}
        :return:
        '''
        configTxt = ""
        for ConfigIndex in config:
            configTxt = "%s%s :\n{\n"%(configTxt,ConfigIndex)
            for RealConf in config[ConfigIndex]:
                if(type(config[ConfigIndex][RealConf]) is unicode):
                    configTxt = "%s  %s  =  \"%s\";\n" % (configTxt, RealConf, config[ConfigIndex][RealConf])
                else:
                    configTxt = "%s  %s  =  %s;\n"%(configTxt,RealConf,config[ConfigIndex][RealConf])
            configTxt = "%s};\n"%(configTxt)
        filehandle = open(self.currentPath,"w")
        filehandle.write(configTxt)
        filehandle.close()


    def _init_window(self):
        '''
        初始化界面
        :return:
        '''
        self.MachineCtrl    = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.MachineText    = wx.StaticText(self,-1,"Machine Name",size=(200,-1))
        self.PasswordCtrl  = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.PasswordText = wx.StaticText(self, -1, "Password", size=(200, -1))

        self.FreqCtrl = wx.ComboBox(self, -1)
        self.FreqCtrl.Append("0")
        self.FreqCtrl.Append("1")
        self.FreqCtrl.Append("2")
        self.FreqCtrl.Append("5")
        self.FreqCtrl.Append("8")
        self.FreqCtrl.Append("10")
        self.FreqCtrl.Append("15")
        self.FreqCtrl.Append("20")
        self.FreqCtrl.Append("30")
        self.FreqCtrl.Append("60")

        self.FreqText = wx.StaticText(self, -1, "Frequency", size=(200, -1))
        self.NoneText_1 = wx.StaticText(self, -1, "", size=(100, -1))
        self.NoneText_2 = wx.StaticText(self, -1, "", size=(100, -1))

        self.OkButton  = wx.Button(self, -1, u"确定")
        self.ExitButton = wx.Button(self, -1, u"取消")

    def _init_Sizer(self):
        '''
        布局
        :return:
        '''
        self.PlcFlexSizer = wx.FlexGridSizer(rows=3, cols=2, vgap=10, hgap=20)
        self.PlcFlexSizer.AddMany([(self.MachineText, -1, wx.ALL | wx.EXPAND), (self.MachineCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.PasswordText, -1, wx.ALL | wx.EXPAND), (self.PasswordCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.FreqText, -1, wx.ALL | wx.EXPAND),(self.FreqCtrl, -1, wx.ALL | wx.EXPAND),
                                   ])
        self.buttonSizer = wx.FlexGridSizer(rows=1, cols=4)
        self.buttonSizer.Add(self.OkButton,flag = wx.LEFT | wx.EXPAND, border =1)
        self.buttonSizer.Add(self.NoneText_1, flag=wx.ALL | wx.EXPAND, border=1)
        self.buttonSizer.Add(self.NoneText_2, flag=wx.ALL | wx.EXPAND, border=1)
        self.buttonSizer.Add(self.ExitButton,flag = wx.RIGHT | wx.EXPAND, border =1)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.AddSizer(self.PlcFlexSizer,flag = wx.ALL | wx.EXPAND, border =20)
        self.mainSizer.AddSizer(self.buttonSizer,flag = wx.ALL | wx.EXPAND, border =20)

        self.SetSizer(self.mainSizer)

    def _init_bind(self):
        '''
        绑定事件
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self.OkHandle, self.OkButton)
        self.Bind(wx.EVT_BUTTON, self.ExitHandle, self.ExitButton)

    def ExitHandle(self, e):
        '''
        退出按钮句柄
        :return:
        '''
        self.Close()

    def OkHandle(self, e):
        '''
        确定按钮句柄
        :return:
        '''
        with io.open(self.currentPath, 'r', encoding='utf-8') as f:
            config = libconf.load(f)
        if (config.has_key("SysConfig")):
            plc_config = config.pop("SysConfig")
        self._get_from_the_frame()
        tempConfig = {"SysConfig" : self.UserConfigDict}
        config.update(tempConfig)
        self._Dict_toFile(config)
        self.Close()




if __name__ == "__main__":
    switch_test = 3
    app = wx.App()

    if switch_test == 1:
        frame = PlcConfigFrame(None)
    elif switch_test == 2:
        frame = RemoteConfigFrame(None)
    elif switch_test == 3:
        frame = UserConfigFrame(None)

    frame.Show()
    app.MainLoop()



