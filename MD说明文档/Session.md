# Welcome to Session!

### 概念：<br/>
1. **web请求是无状态的**，这个意思是说，当你向服务器发送了一个request请求，服务器又给你返回了一个response回复，你得到了你想要的页面，得到后，你和服务器的连接就断开了，如果你需要另一个页面，那就需再次发送request并接收response，然后再断开，所以，**页面与页面之间就是相互独立的，他们并不存在什么天然的数据共享**
2. 但是，有一些数据是需要被每一个页面共享的，比如你的用户名，当你访问网站的每一个页面的时候，页面顶端都会显示【XXX，你好】，这就是公共数据，它必须在每一个独立的页面之外被存储。如何存储这些公共的数据呢？我们就需要引入一个概念叫做会话状态，它就是session
3. 绝大部分编程语言都封装了session的相关类，Python的flask也同样封装了session类
4. session存储在哪呢？由于页面的request和response完成交互后就断开连接了，所以就注定了session必须在本地和服务器各存储一份。存储在本地的那一份被安排在了浏览器的cookie里，存储在服务器的那一份可以把它理解成一个字典
5. 当你登录成功时，flask会生成session存储在你的浏览器cookie里，同时在服务器的相关字典里也存储一份，然后，连接就断开了。当你发起下一次请求时，会把session信息放在请求头里发送给服务器，服务器接收到之后，会跟自己存储的字典进行对比，如果字典里有你这个session，则认为你已登录，可以访问相关资源，如果没有，则禁止你访问任何资源，通常会给你链接到登录页面去
6. session还可以实现让不同的用户使用不同的资源，如用户admin登录，flask会给他生成一个session，比如叫做s1（只是举个例子，通常的session不会这么简单），于是，在admin登录成功时，flask在admin的本地浏览器的cookie里存储了{"admin":"s1"}，同时在浏览器的相关字典里也存储了{"admin":"s1"}，同时会在数据库的相关表里找到admin对应的资源，并把这些资源展示出来。
7. 当一个人，采用猜地址的方式，直接在浏览器地址栏里输入了正确的admin的系统管理首页的地址，但服务器收到请求后发现他的请求头里没有admin键及其值，或者有admin键，但值不对，于是给他返回了登录页面。

8. 又有一个人，他也通过猜地址的方式，直接在浏览器里输入了admin的系统管理首页的地址，但他的请求头里包含了{"admin":"s1"}（他怎么获得的不得而知），那么，服务器通过比对后发现没有问题，他就登录成功了，这个人叫黑客


### session能解决哪些问题
1. 跨页面数据共享
2. 不同的页面对于不同的用户实现区别对待，如，某些页面只能管理员可见等

3. 防止某些人通过猜地址的方式访问到不该他访问的页面，如直接输入192.168.88.88/edit/8

### session的工作原理
当我们登录时，利用session类为登录用户创建一条session信息，这条信息被存储在浏览器的cookie里，同时，为了安全，flask会强制你设置一个密码app.secret_key="xxx"，以保证cookie不被恶意访问

当请求页面时，flask会从cookie里获取当前用户的session

如果你要做的事是跨页面数据共享，取到cookie里的session的相关数据后，flask会把它显示在页面上
如果你要做的事是让某些用户能或不能访问某些页面，上一小节已阐述

如果你要做的事是防止某些人猜到地址，上一小节已阐述
注意：

session是全局的，也就是说，在任意函数，任意模板里都可以直接使用session，而无需为模板传递session

### 打印session真容
详情可见 app2/app30_session
 ```python
    form =LoginForm(request.form)
    print("session=",session)
    print("session=",session['csrf_token'])
``` 
打印出来如下：
    
    session= <SecureCookieSession {'csrf_token': '6ac702c14f6baf24dacd9785abf0b01d88cde287'}>
    session= 6ac702c14f6baf24dacd9785abf0b01d88cde287

### 设置session
详情可见 app2/app31

### 设置session有效时间

第一步先引入

    from flask import session
    from datetime import timedelta
第二步在登录函数里写上如下语句

    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
第一句是让session永久生效，必须要有这句，否则后面一句也无效

第二句是设置session生存时间为多少分钟，通常使用分钟即可，如果是天，则为day

超出设置的时间，不论点击什么，都会跳转至登录页面
