#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
'''
解析成绩类
'''
import xlrd

class ReadRecodeOperation():
    '''
    从Excel中读取指定用户的成绩
    学号--------姓名--------成绩1-----成绩2----
    20160302   刘晓晓       A+         A++
    20160302   刘晓晓       B++        A-
    '''
    def __init__(self):
        pass

    def OpenExl(self,path):
        '''
        打开指定路径的Excel文件
        :param path:
        :return:
        '''
        self.excel = xlrd.open_workbook(path)
        self.data = self.excel.sheets()[0]#暂时只支持一个工作表

    def GetUserData(self, User):
        '''
        获取指定用户的成绩
        :param User:学生的学号
        :return:没获取到成绩则返回NONE，否则返回获取到的成绩
        '''
        result = ""
        nrows = self.data.nrows  # 获取总行数
        result = u"%s\n"%(self.util_result(self.data.row_values(0)))
        for i in range(nrows):
            if(User == self.data.row(i)[0].value):
                result = result + '\n' + self.util_result(self.data.row_values(i))
                return result
        return None

    def util_result(self,list_data):
        '''
        将列表数据转换成字符串
        :param list_data:
        :return:
        '''
        DATA = ""
        for data in list_data:
            DATA = DATA + " | " + str(data)
        return DATA

class GetUserWxName():
    '''
    通过学号获取到微信号(
    Excel格式
    学号--------姓名--------微信备注
    20160302   刘晓晓       刘晓晓爸爸
    20160302   刘晓晓       刘晓晓妈妈
    '''

    def __init__(self):
        pass

    def OpenExl(self, path):
        '''
        打开指定路径的Excel文件
        :param path:
        :return:
        '''
        self.excel = xlrd.open_workbook(path)
        self.data = self.excel.sheets()[0]  # 暂时只支持一个工作表
        self.nrows = self.data.nrows  # 获取总行数

    def GetWxName(self, User):
        '''
        获取指定用户的成绩
        :param User:学生的学号
        :return:返回获取到的微信号，否则返回None
        '''

        for i in range(self.nrows):
            if (User == self.data.row(i)[0].value):
                WxName = self.data.row(i)[2].value
                return WxName
        return None

    def GetNrowsOfTable(self):
        '''
        获取表的总行数
        :return:
        '''
        return (self.nrows)

    def GetIndexUser(self, index):
        '''
        获取指定行的学生学号
        :return:
        '''
        if(index > self.nrows - 1):
            print("Bad Input Param, No such Rows")
            return None

        return self.data.row(index)[0].value


