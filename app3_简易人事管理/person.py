# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/27 4:25 下午


# coding=utf-8
from flask import Flask,render_template,flash,request,redirect,flash
from flask_wtf import FlaskForm, Form
import wtforms
from db import *
from all_judge import *

app = Flask(__name__) # 创建了一个Flask类的实例
app.secret_key="123"

# 登录页面
class loginform(Form):# 创建一个用于获取html页面数据的类，它必须继承自wtforms类的Form子类
    username=wtforms.StringField('用户名：') # 设置username，html页面将从这里取数据
    password=wtforms.PasswordField('密码：')# 设置password，html页面将从这里取数据

class person_showform(Form):
    searchstring=wtforms.StringField("输入姓名：")

# login() 视图函数
# 1. 在该函数的前面定义了两个类，他们分别为login.html和person_show.html的模型，即这两个页面的form表单里的输入项的模型
# 2. 定义了login.html的地址为/，它就是跟地址，同时定义该函数的传递数据方式为POST和GET
# 3. 把login.html页面和person_show.html页面的表单分别进行实例化
# 4. 如果数据传递方式为POST，即当有数据使用POST方式传递时（只有当点击提交按钮时才会发生POST传递，而在login.html中，已经定义了form表单的数据传递方式为POST，所以只要在表单里点击了提交按钮，即发生POST传递），就通过username=ins_loginform.username.data和password=ins_loginform.password.data来获取页面上输入的数据，即用户名和密码
# 如果用户名和密码正确，则调用db.py里的get_data()方法，获取表中的所有数据，接着，通过return render_template("person_show.html", AllResult_tuple=AllResult_tuple,form=ins_person_showform)把页面跳转至person_show.html，同时把通过get_data()方法获取到的表中的所有值和person_show.html页面的表单实例也传递给person_show.html
# 如果用户名和密码错误，则通过return render_template("login.html", ErrorMessage=ErrorMessage, form=ins_loginform)把ErrorMessage传递给person_show.html，当然，person_show.html页面的表单的实例也要传递给person_show.html
# 如果数据传递方式不是POST，那么就证明是通过输入网址直接进入登录页面（因为通过输入网址进入某个页面时，使用的数据传递方式就是GET），那么此时，就通过return render_template("login.html",form=ins_loginform)来说告诉系统，我要进入的页面是login.html页面，同时把该页面的表单实例也传给该页面
@app.route("/",methods=["POST","GET"]) # 用route()装饰器来自定义自己的URL
def login():
    ins_loginform=loginform(request.form)# 创建loginform类的实例
    ins_person_showform= person_showform(request.form)  # 把person_showform类实例化
    if request.method=="POST":
        username=ins_loginform.username.data # 通过类的实例化来获取表单中的username值
        password=ins_loginform.password.data# 通过类的实例化来获取表单中的password值
        if username=="1"and password=="1":
            AllResult_tuple = get_data()
            return render_template("person_show.html", AllResult_tuple=AllResult_tuple,form=ins_person_showform)
        else:
            ErrorMessage="用户名或密码错误"
            returnrender_template("login.html", ErrorMessage=ErrorMessage,form=ins_loginform)
    return render_template("login.html",form=ins_loginform)

# person_show(id) 视图函数
# 1. 定义了person_show .html的地址为/person_show/，id是从person_show .html页面传递过来的值，这个id是直接跟在地址后面传递过来的，也就是说，它是通过GET方式传递过来的。同时，指定了数据提交方式为GET
# 2. 把person_show .html页面中的表单所对应的模型类实例化（该模型类在def login()函数前面已经定义过），得到ins_person_showform.   注意：person_show .html页面中的表单并不是用来展示数据的，而是专门用于查询的，这个表单里只有一个输入项，那就是查询所用的关键字
# 3. 调用db.py里的get_data()方法获取表中的所有值
# 4. 如果id值不等于-1，则证明这个请求是从delete.html页面中通过点击【确定删除】按钮跳转过来的，那么，需要调用db.py里的delete_data(id)方法把相关id的数据删除掉，那么再通过return render_template("person_show.html",AllResult_tuple=AllResult_tuple,form=ins_person_showform)还跳转到person_show.html，而由于已经删除了相关id的数据，所以AllResult_tuple元祖中已不包含相关id的数据
# 5. 如果id值等于-1，则证明这个请求是从delete.html页面中通过点击【放弃删除】按钮跳转过来的，此时就不需要再调用db.py里的delete_data(id)方法，那么此时，由于没有对数据库做删除操作，所以同样使用return render_template("person_show.html",AllResult_tuple=AllResult_tuple,form=ins_person_showform)跳转回person_show.html后会发现数据一条没少，还是那么多
@app.route("/person_show/<id>",methods=["GET"])
def person_show(id):
    ins_person_showform=person_showform(request.form) # 把模型类实例化
    AllResult_tuple= get_data()
    if id!=-1:
        delete_data(id)
        return render_template("person_show.html",AllResult_tuple=AllResult_tuple,form=ins_person_showform)
    else:
        return render_template("person_show.html", AllResult_tuple=AllResult_tuple,form=ins_person_showform)


# person_show_search() 视图函数
# 1. person_show_search.html的作用是，当在person_show.html或person_show_search.html中的搜索框里输入关键字并点击搜索按钮后，后台查询出了相关数据，页面就会跳转至这个页面，这个页面和person_show.html是一样的。
# 那么为什么不直接跳转至person_show.html呢？那是因为如果仍然跳转至person_show.html，就会导致视图函数def person_show(id)过于复杂，不便于编写和排查问题，同时也会发生很多意想不到的问题
# 注意：视图函数的编写原则是，一个视图函数尽量只做一件事，如果想做多件事，那就多写一些视图函数，视图函数不怕多，就怕一个视图函数里面过于复杂。通常，除了创建和修改可以共用一个视图函数外，其他方法都要尽量做到以上原则
# 2. 这里没有任何通过地址栏的传参
# 3. 既然和person_show.html一样，那么就也需要person_show.html页面中表单的实例，在本函数中叫做ins_person_showform
# 4. 通过searchstring = request.args.get('searchstring', "")来获得通过地址栏传递给后台的参数searchstring，后面的""代表如果searchstring没有值就给个空字符串
# 5. searchstring这个参数是通过person_show.html或person_show_search.html页面中表单的GET方法，由地址栏传递过来的，虽然该试图函数所对应的页面在进入时本身并没有地址栏传参，但GET方法的值仍然可以通过地址栏传递
# 6. 通过调用db.py中的search(searchstring)方法来获取查询结果，如果searchstring是个空字符串，那么则返回全部数据
@app.route("/person_show_search/")
def person_show_search():
    ins_person_showform =person_showform(request.form)  # 把模型类实例化
    searchstring =request.args.get('searchstring', "")
    Search_AllResult_tuple =search(searchstring)
    return render_template("person_show_search.html",AllResult_tuple=Search_AllResult_tuple,form=ins_person_showform)


# 创建或修改页面的字段类
class CreatOrEdit_form(Form):
    name=wtforms.StringField("姓名：")
    sex=wtforms.SelectField("性别：",choices=[("男","男"),("女","女")])
    age=wtforms.IntegerField("年龄：")
    height=wtforms.IntegerField("身高：")
    job=wtforms.StringField("职业：")
    facelevel=wtforms.IntegerField("颜值：")


# creat() 视图函数
# 1. 在该函数之前首先定义了一个类CreatOrEdit_form，它是creat.html和edit.html两个页面共用的模型类，该类中定义了所有的输入元素
# 注意：性别下拉框中的choices=[("男","男"),("女","女")]两个元组里的值要一致，不能写成choices=[("1","男"),("2","女")]，否则在编辑页面中，无法把被编辑数据的原始性别值展现在页面上，页面上展示的只能是1或2，而不是男或女
# 2. 把CreatOrEdit_form和之前创建的person_showform分别实例化
# 3. 如果form表单传递数据的方式为POST，即当在creat.html页面点击提交按钮时，通过name=ins_creatform.name.data等语句获取页面输入数据
# 4. 通过all_judge.py文件里的CreatAndEdit_judge(name,sex,age,height,job,facelevel)函数来判断每一个输入字段是否为空，并获得返回值即提示信息ErrorMessage，如果ErrorMessage不等于空，则证明有未填写的字段，那么就通过return render_template("creat.html", ErrorMessage=ErrorMessage, form=ins_creatform)重新返回到creat.html页面，注意，返回时要把ErrorMessage也传给creat.html
# 5. 如果ErrorMessage不为空，那么就证明所有字段都填写完毕了，没有为空的字段，那么就调用db.py里的creat_data(name, sex, age, height, job, facelevel)方法，如果该方法的返回值为True，则证明数据插入成功，如果插入不成功怎么办？creat_data()函数并没有做处理
# 6. 插入成功后，调用db.py里的get_data()函数获取到表中的所有数据，并通过return render_template("person_show.html",AllResult_tuple=AllResult_tuple,form=ins_person_showform)把页面跳转至person_show.html
# 7. 如果提交方式不是POST，即通过【新建人员】链接进入到creat.html页面（再次强调，凡是通过链接或输入网址直接进入某页面的操作都是GET），那么就return render_template("creat.html",form=ins_creatform)来跳转至creat.html页面，同时把该页面的表单的实例ins_creatform)传递给该页面
# 创建页面
@app.route("/creat/",methods=["POST","GET"])
def creat():
    ins_person_showform =person_showform(request.form)  # 把模型类实例化
    ins_creatform= CreatOrEdit_form(request.form)
    if request.method=="POST":
        name=ins_creatform.name.data
        sex=ins_creatform.sex.data
        age=ins_creatform.age.data
        height=ins_creatform.height.data
        job=ins_creatform.job.data
        facelevel=ins_creatform.facelevel.data
        ErrorMessage=CreatAndEdit_judge(name,sex,age,height,job,facelevel)
        if ErrorMessage!="":
            return render_template("creat.html", ErrorMessage=ErrorMessage,form=ins_creatform)
        else:
            if creat_data(name,sex, age, height, job, facelevel)==True:
                AllResult_tuple =get_data()
                returnrender_template("person_show.html",AllResult_tuple=AllResult_tuple,form=ins_person_showform)
    return render_template("creat.html",form=ins_creatform)


# edit(id) 视图函数
# 1. 接收从页面传过来的id值
# 2. 把person_showform和CreatOrEdit_form两个类实例化
# 3. 如果数据提交方式是POST，则证明是点击了提交按钮，那么就通过name=ins_editform.name.data等语句获取所有页面提交上来的字段数据
# 4. 通过all_judge.py文件里的CreatAndEdit_judge(name,sex,age,height,job,facelevel)函数来判断每一个输入字段是否为空，并获得返回值即提示信息ErrorMessage，如果ErrorMessage不等于空，则证明有未填写的字段，那么就通过return render_template("edit.html", ErrorMessage=ErrorMessage, form=ins_editform)重新返回到edit.html页面，注意，返回时要把ErrorMessage也传给edit.html
# 5. 如果ErrorMessage不为空，那么就证明所有字段都填写完毕了，没有为空的字段，那么就调用db.py里的edit_data (name, sex, age, height, job, facelevel)方法，如果该方法的返回值为True，则证明数据更新成功，如果更新不成功怎么办？edit_data()函数并没有做处理
# 6. 如果提交方式不为POST，那么就证明是通过点击编辑按钮进入edit.html页面的操作，此时，我们需要把原始数据展现在页面上，我们先通过result_tuple = get_one_data(id)获得该条数据的所有字段值，再通过ins_editform.name.data=result_tuple[1]等语句把这些原始值写入到页面上。最后，再通过return render_template("edit.html",result_tuple=result_tuple,form=ins_editform)进入edit.html，注意，被编辑数据的所有字段值result_tuple也被传入了该页面
# 修改页面
@app.route("/edit/<id>",methods=["POST","GET"])
def edit(id):
    ins_person_showform =person_showform(request.form)  # 把模型类实例化
    ins_editform=CreatOrEdit_form(request.form)
    if request.method=="POST":
        name=ins_editform.name.data
        sex=ins_editform.sex.data
        age=ins_editform.age.data
        height=ins_editform.height.data
        job=ins_editform.job.data
        facelevel=ins_editform.facelevel.data
        ErrorMessage=CreatAndEdit_judge(name,sex,age,height,job,facelevel)
        if ErrorMessage!="":
            return render_template("edit.html", ErrorMessage=ErrorMessage,form=ins_editform,id=id)
        elif edit_data(id,name, sex, age, height, job, facelevel)==True:
            AllResult_tuple = get_data()
            return render_template("person_show.html",AllResult_tuple= AllResult_tuple,form=ins_person_showform)
    else:
        result_tuple = get_one_data(id)
        ins_editform.name.data=result_tuple[1]
        ins_editform.sex.data = result_tuple[2]
        ins_editform.age.data =result_tuple[3]
        ins_editform.height.data =result_tuple[4]
        ins_editform.job.data =result_tuple[5]
        ins_editform.facelevel.data =result_tuple[6]
        return render_template("edit.html",result_tuple=result_tuple,form=ins_editform)


# delete(id) 视图函数
# 1. 通过点击person_show.html或person_show_search.html页面上的删除按钮即可进入到delete.html页面
# 2. 通过id值来查询到该条数据的所有字段值，即通过get_one_data(id)把该条数据的所有字段值都存储在一个元祖OneResult_tuple中
# 3. 通过return render_template("delete.html",OneResult_tuple=OneResult_tuple,form=ins_person_showform)跳转至delete.html页面，同时把被删除人员的所有字段值 OneResult_tuple和person_showform 类的实例ins_person_showform也传递给delete.html
# 删除数据
@app.route("/delete/<id>")
def delete(id):
    ins_person_showform =person_showform(request.form)  # 把模型类实例化
    OneResult_tuple= get_one_data(id)
    return render_template("delete.html",OneResult_tuple=OneResult_tuple,form=ins_person_showform)


if __name__ == '__main__':
    app.debug = True
    app.run()



