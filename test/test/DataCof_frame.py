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

class DataConfigFrame(wx.Frame):
    '''
    PLC配置界面
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.configFileName = "config.cfg"
        self.currentPath = "%s%s%s" % (os.path.curdir, os.sep, self.configFileName)
        self.CreateStatusBar()
        self.SetMinSize(wx.Size(475, 290))
        self.SetMaxSize(wx.Size(475, 290))
        self.SetTitle(u"PLC配置")
        self.Center()
        self.SetBackgroundColour('#4f5049')
        self._init_param()
        self._init_window()
        self._init_Sizer()
        self._init_the_Text()
        self._init_bind()

    def _init_param(self):
        '''
        初始化配置代码{以字典形式}
        :return:
        '''
        self.dataConfigDict = {"BlockName": "DB",
                              "DBNumber": 0,
                              "Start": 0,
                              "Amount": 0}


    def _init_the_Text(self):
        '''
        填充内容
        :return:
        '''
        self.BlockCtrl.SetValue(self.dataConfigDict["BlockName"])
        self.BlockNumCtrl.SetValue(str(self.dataConfigDict["DBNumber"]))
        self.StartCtrl.SetValue(str(self.dataConfigDict["Start"]))
        self.AmountCtrl.SetValue(str(self.dataConfigDict["Amount"]))

    def _get_from_the_frame(self):
        '''
        从输入获取配置
        :return:
        '''
        BlockType = self.BlockCtrl.GetValue()
        if(BlockType == "DB"):
            BlockNum = self.BlockNumCtrl.GetValue()
            self.dataConfigDict["DBNumber"] = string.atoi(BlockNum)
            self.dataConfigDict["BlockName"] = "%s%s"%(BlockType,BlockNum)
        elif(BlockType):
            self.dataConfigDict["DBNumber"] = "0"
            self.dataConfigDict["BlockName"] = BlockType

        Start = self.StartCtrl.GetValue()
        if (Start):
            self.dataConfigDict["Start"] = string.atoi(Start)
        Amount = self.AmountCtrl.GetValue()
        if (Amount):
            self.dataConfigDict["Amount"] = string.atoi(Amount)
        self.dataConfigDict["WordLength"] = "1"

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

    def _checkCbChange(self):
        Block = self.BlockCtrl.GetValue()
        if(Block != "DB"):
            self.BlockNumText.Hide()
            self.BlockNumCtrl.Hide()
        else:
            self.BlockNumText.Show()
            self.BlockNumCtrl.Show()

    def _init_window(self):
        '''
        初始化界面
        :return:
        '''
        self.BlockCtrl     = wx.ComboBox(self, -1)
        self.BlockCtrl.SetToolTipString(u"请选择块类型----->\nDB :数据块\nPE :输入设备\nPA: 输出设备\nMK :位记忆区\nCT :计数器\nTM :计时器")
        self.BlockText     = wx.StaticText(self,-1,"Block Type",size=(100,-1))
        self.BlockNumCtrl     = wx.ComboBox(self, -1)
        self.BlockNumCtrl.SetToolTipString(u"请选择DB对应的块，可以手动输入")
        self.BlockNumText     = wx.StaticText(self, -1, "Block Number", size=(100, -1))
        self.StartCtrl     = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.StartCtrl.SetToolTipString(u"请选择起始地址，从0开始")
        self.StartText     = wx.StaticText(self, -1, "Start", size=(100, -1))
        self.AmountCtrl    = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.AmountCtrl.SetToolTipString(u"请选择采集的数量总数，单位为字节(BYTE)")
        self.AmountText    = wx.StaticText(self, -1, "Amount", size=(100, -1))
        self.BlockCtrl.Append("DB")
        self.BlockCtrl.Append("PE")
        self.BlockCtrl.Append("PA")
        self.BlockCtrl.Append("MK")
        self.BlockCtrl.Append("CT")
        self.BlockCtrl.Append("TM")
        self.BlockNumCtrl.Append("1")
        self.BlockNumCtrl.Append("2")
        self.BlockNumCtrl.Append("3")
        self.BlockNumCtrl.Append("4")
        self.BlockNumCtrl.Append("5")
        self.BlockNumCtrl.Append("6")
        self.BlockNumCtrl.Append("7")
        self.BlockNumCtrl.Append("8")

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
        self.PlcFlexSizer.AddMany([(self.BlockText, -1, wx.ALL | wx.EXPAND), (self.BlockNumText, -1, wx.ALL | wx.EXPAND),
                                   (self.BlockCtrl, -1, wx.ALL | wx.EXPAND), (self.BlockNumCtrl, -1, wx.ALL | wx.EXPAND),
                                   (self.StartText, -1, wx.ALL | wx.EXPAND), (self.AmountText, -1, wx.ALL | wx.EXPAND),
                                   (self.StartCtrl, -1, wx.ALL | wx.EXPAND), (self.AmountCtrl, -1, wx.ALL | wx.EXPAND),
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
        self.Bind(wx.EVT_COMBOBOX, self.CbHandle, self.BlockCtrl)

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
        ConfigKey = "NONE"
        Block = self.BlockCtrl.GetValue()
        if(Block == "DB"):
            BlockNum = self.BlockNumCtrl.GetValue()
            if(BlockNum != None and BlockNum != "0"):
                ConfigKey = "DB_%s"%(BlockNum)
        elif(Block):
            ConfigKey = Block

        if(ConfigKey == "NONE"):
            self.Close()
            return

        if (config.has_key(ConfigKey)):
            plc_config = config.pop(ConfigKey)
        self._get_from_the_frame()
        tempConfig = {ConfigKey : self.dataConfigDict}
        config.update(tempConfig)
        self._Dict_toFile(config)
        self.Close()

    def CbHandle(self,e):
        '''
        处理输入IP的检测
        :param e:
        :return:
        '''
        self._checkCbChange()

if __name__ == "__main__":
    switch_test = 1
    app = wx.App()

    if switch_test == 1:
        frame = DataConfigFrame(None)
    elif switch_test == 2:
        pass
    elif switch_test == 3:
        pass

    frame.Show()
    app.MainLoop()