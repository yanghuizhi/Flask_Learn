# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/27 4:25 下午

# 做所有判断，实际只做了一个判断，即对输入的数据是否为空进行了判断

def CreatAndEdit_judge(name,sex,age,height,job,facelevel):
    ErrorMessage_tuple = (("姓名", name), ("性别", sex), ("年龄", age), ("身高", height), ("工作", job), ("颜值", facelevel))
    ErrorMessage = ""
    for i in ErrorMessage_tuple:
        if i[1]== "" or i[1]== None:
            ErrorMessage += i[0] +"不能为空；"
    return ErrorMessage