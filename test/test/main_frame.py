#encoding=utf-8
#@author:yzg
#@create:2016-10-10

import  time
import  wx
from FileMenu import *
from SystemConfig import *
from DataCof_frame import *


class MyMenuFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'江冶机电', size=(500, 250))
        self.CenterOnScreen()
        self.CreateStatusBar()
        self.SetStatusText(u"江冶机电 @CopyRight 2016")
        # 生成菜单menu
        menuBar = wx.MenuBar()

        # 为菜单栏生成菜单
        menu1 = wx.Menu()
        menu1.Append(101, u"打开配置文件", u"打开配置文件")
        menu1.Append(102, u"备份配置文件", u"备份配置文件")
        menu1.Append(103, u"清空配置文件", u"清空操作很危险，请谨慎操作")
        menu1.Append(104, u"退出", u"退出程序")
        # Append 2nd menu
        menuBar.Append(menu1, u"&文件")

        # 2nd menu from left
        menu2 = wx.Menu()
        # a submenu in the 2nd menu
        submenu = wx.Menu()
        submenu.Append(2011,u"PLC配置", u"PLC配置")
        submenu.Append(2012,u"远程服务器配置", u"远程服务器配置")
        submenu.Append(2013,u"用户配置", u"用户配置")
        menu2.AppendMenu(201, u"系统配置", submenu)
        menu2.Append(202, u"数据配置", u"数据配置")
        # Append 2nd menu
        menuBar.Append(menu2, u"&配置")

        menu3 = wx.Menu()
        menu3.Append(301, u"关于", u"关于")
        menu3.Append(302, u"帮助", u"帮助")
        # Append 2nd menu
        menuBar.Append(menu3, u"&信息")
        self.SetMenuBar(menuBar)

        # Menu events
        self.Bind(wx.EVT_MENU_HIGHLIGHT_ALL, self.OnMenuHighlight)

        self.Bind(wx.EVT_MENU, self.OpenConfig, id=101)
        self.Bind(wx.EVT_MENU, self.BackupConfig, id=102)
        self.Bind(wx.EVT_MENU, self.ClearConfig, id=103)
        self.Bind(wx.EVT_MENU, self.CloseProgram, id=104)

        self.Bind(wx.EVT_MENU, self.DataConfig, id=202)
        self.Bind(wx.EVT_MENU, self.PLCConfig, id=2011)
        self.Bind(wx.EVT_MENU, self.RemoteConfig, id=2012)
        self.Bind(wx.EVT_MENU, self.UserConfig, id=2013)

        self.Bind(wx.EVT_MENU, self.AboutSoft, id=301)
        self.Bind(wx.EVT_MENU, self.HelpSoft, id=302)


    def OnMenuHighlight(self, event):
        '''
        高亮所选择的菜单项
        :param event:
        :return:
        '''
        id = event.GetMenuId()
        item = self.GetMenuBar().FindItemById(id)
        if item:
            text = item.GetText()
            help = item.GetHelp()
        event.Skip()

    def CloseProgram(self,event):
        self.Close()

    def OpenConfig(self, event):
        frame = OpenConfifure(None)
        frame.Show()

    def BackupConfig(self, event):
        frame = BackUpConfig(None)
        frame.Show()

    def ClearConfig(self, event):
        frame = ClearConfig(None)
        frame.Show()

    def PLCConfig(self, event):
        frame = PlcConfigFrame(None)
        frame.Show()

    def RemoteConfig(self, event):
        frame = RemoteConfigFrame(None)
        frame.Show()

    def UserConfig(self, event):
        frame = UserConfigFrame(None)
        frame.Show()

    def DataConfig(self, e):
        frame = DataConfigFrame(None)
        frame.Show()

    def AboutSoft(self,e):
        pass

    def HelpSoft(self,e):
        pass



if __name__ == '__main__':
    app = wx.App()
    frame = MyMenuFrame(None, -1)
    frame.Show()
    app.MainLoop()

