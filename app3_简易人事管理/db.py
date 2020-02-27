# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/27 4:25 下午

# 用于对数据库进行各种增删改改查操作

# coding=utf-8
import pymysql
import time
from datetime import timedelta,date
import locale

locale.setlocale(locale.LC_CTYPE, 'en_US.UTF-8')
def date_time_chinese():
    u"returnsthe current time string,format for YYYY年mm月dd日 HH时MM分SS秒"
    return time.strftime("%Y年%m月%d日，%H时%M分%S秒",time.localtime())

def get_data():
    db = pymysql.connect("localhost", "root", "123456", "app3")
    cursor = db.cursor()  # 创建游标
    select_sql="select * from person"
    cursor.execute(select_sql)
    resultall = cursor.fetchall()
    cursor.close()
    return resultall

def creat_data(name,sex,age,height,job,facelevel):
    db = pymysql.connect("localhost", "tester1", "123456", "testdb")
    cursor = db.cursor()  # 创建游标
    insert_sql="insert into person(name, sex, age, Height_cm, Job, FaceaLevel, CreatTime)values(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_sql,(name,sex,age,height,job,facelevel,date_time_chinese()))
    db.commit()
    cursor.close()
    return True

def get_one_data(id):
    db = pymysql.connect("localhost", "root", "123456", "app3")
    cursor = db.cursor()  # 创建游标
    seletc_sql="select * from person where id=%s"
    cursor.execute(seletc_sql,(id))
    resultone = cursor.fetchone()
    cursor.close()
    return resultone

def edit_data(id, name, sex, age, height, job,facelevel):
    db = pymysql.connect("localhost", "root", "123456", "app3")
    cursor = db.cursor()  # 创建游标
    updata_sql="update person set name=%s,sex=%s,age=%s,Height_cm=%s,job=%s,FaceaLevel=%s,CreatTime=%swhere id=%s"
    cursor.execute(updata_sql,(name, sex, age, height, job, facelevel, date_time_chinese(),id))
    db.commit()
    cursor.close()
    return True

def search(searchstring):
    db = pymysql.connect("localhost", "root", "123456", "app3")
    cursor = db.cursor()  # 创建游标
    select_sql="select * from person where name like '%"+searchstring+"%'"
    cursor.execute(select_sql)
    resultone = cursor.fetchall()
    cursor.close()
    return resultone

def delete_data(id):
    db = pymysql.connect("localhost", "root", "123456", "app3")
    cursor = db.cursor()  # 创建游标
    delete_sql="delete from person where id=%s"
    cursor.execute(delete_sql,(id))
    db.commit()
    cursor.close()
    return True

if __name__ == '__main__':
    print(get_data())
    print(get_one_data(5))
    print(edit_data("6","李玉","女","29","166","前端工程师","100"))
    print(delete_data(23))
    print(search("老师"))