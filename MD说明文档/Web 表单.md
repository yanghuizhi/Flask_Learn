# Flask - WTF

[WTForms支持的HTML标准字段](#WTForms支持的HTML标准字段)<br/>
[WTForms常用验证函数](#WTForms常用验证函数)<br/>
[在HTML页面中直接写form表单](#在html页面中直接写form表单)<br/>
[使用Flask-WTF实现表单](#使用flask-wtf实现表单)<br/>
<br/>



web表单是web应用程序的基本功能。集成WTForms，并带有 csrf 令牌的安全表单和全局的 csrf 保护的功能。

它是HTML页面中负责数据采集的部件。表单有三个部分组成：表单标签、表单域、表单按钮。表单允许用户输入数据，负责HTML页面数据采集，通过表单将用户输入的数据提交给服务器。

在Flask中，为了处理web表单，我们一般使用Flask-WTF扩展，它封装了WTForms，并且它有验证表单数据的功能。

使用Flask-WTF需要配置参数SECRET_KEY。

CSRF_ENABLED是为了CSRF（跨站请求伪造）保护。 SECRET_KEY用来生成加密令牌，当CSRF激活的时候，该设置会根据设置的密匙生成加密令牌。


```python
form.hidden_tag()  # 自定义表单一定要加上，否则会提交不成功。这一行代码实质上是添加了一个隐藏字段csrf_token,这是一个随机生成的token，用来防范黑客攻击。
form.validate_on_submit()  # 实例方法会执行form校验的工作, 全部通过之后就会返回True
wtf.quick_form() #  宏，它在单行代码中渲染完整的表单，包括对显示验证错误的支持，并且适配Bootstrap框架的所有样式。-->
```











## WTForms支持的HTML标准字段

<table>
<thead>
<tr>
<th style="text-align:left">字段对象</th>
<th style="text-align:left">说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>StringField</td>
<td>文本字段</td></tr>
<tr>
<td>TextAreaField</td>
<td>多行文本字段</td></tr>
<tr>
<td>PasswordField</td>
<td>密码文本字段</td></tr>
<tr>
<td>HiddenField</td>
<td>隐藏文本字段</td></tr>
<tr>
<td>DateField</td>
<td>文本字段，值为datetime.date格式</td></tr>
<tr>
<td>DateTimeField</td>
<td>文本字段，值为datetime.datetime格式</td></tr>
<tr>
<td>IntegerField</td>
<td>文本字段，值为整数</td></tr>
<tr>
<td>DecimalField</td>
<td>文本字段，值为decimal.Decimal</td></tr>
<tr>
<td>FloatField</td>
<td>文本字段，值为浮点数</td>
</tr>
<tr>
<td>BooleanField</td>
<td style="text-align:left">&#x590D;&#x9009;&#x6846;&#xFF0C;&#x503C;&#x4E3A;True&#x548C;False</td>
</tr>
<tr>
<td style="text-align:left">RadioField</td>
<td style="text-align:left">&#x4E00;&#x7EC4;&#x5355;&#x9009;&#x6846;</td>
</tr>
<tr>
<td style="text-align:left">SelectField</td>
<td style="text-align:left">&#x4E0B;&#x62C9;&#x5217;&#x8868;</td>
</tr>
<tr>
<td style="text-align:left">SelectMultipleField</td>
<td style="text-align:left">&#x4E0B;&#x62C9;&#x5217;&#x8868;&#xFF0C;&#x53EF;&#x9009;&#x62E9;&#x591A;&#x4E2A;&#x503C;</td>
</tr>
<tr>
<td style="text-align:left">FileField</td>
<td style="text-align:left">&#x6587;&#x672C;&#x4E0A;&#x4F20;&#x5B57;&#x6BB5;</td>
</tr>
<tr>
<td style="text-align:left">SubmitField</td>
<td style="text-align:left">&#x8868;&#x5355;&#x63D0;&#x4EA4;&#x6309;&#x94AE;</td>
</tr>
<tr>
<td style="text-align:left">FormField</td>
<td style="text-align:left">&#x628A;&#x8868;&#x5355;&#x4F5C;&#x4E3A;&#x5B57;&#x6BB5;&#x5D4C;&#x5165;&#x53E6;&#x4E00;&#x4E2A;&#x8868;&#x5355;</td>
</tr>
<tr>
<td style="text-align:left">FieldList</td>
<td style="text-align:left">&#x4E00;&#x7EC4;&#x6307;&#x5B9A;&#x7C7B;&#x578B;&#x7684;&#x5B57;&#x6BB5;</td>
</tr>
</tbody>
</table>
<h3 id="wtforms&#x5E38;&#x7528;&#x9A8C;&#x8BC1;&#x51FD;&#x6570;">WTForms&#x5E38;&#x7528;&#x9A8C;&#x8BC1;&#x51FD;&#x6570;</h3>
<table>
<thead>
<tr>
<th style="text-align:left">&#x9A8C;&#x8BC1;&#x51FD;&#x6570;</th>
<th style="text-align:left">&#x8BF4;&#x660E;</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">DataRequired</td>
<td style="text-align:left">&#x786E;&#x4FDD;&#x5B57;&#x6BB5;&#x4E2D;&#x6709;&#x6570;&#x636E;</td>
</tr>
<tr>
<td style="text-align:left">EqualTo</td>
<td style="text-align:left">&#x6BD4;&#x8F83;&#x4E24;&#x4E2A;&#x5B57;&#x6BB5;&#x7684;&#x503C;&#xFF0C;&#x5E38;&#x7528;&#x4E8E;&#x6BD4;&#x8F83;&#x4E24;&#x6B21;&#x5BC6;&#x7801;&#x8F93;&#x5165;</td>
</tr>
<tr>
<td style="text-align:left">Length</td>
<td style="text-align:left">&#x9A8C;&#x8BC1;&#x8F93;&#x5165;&#x7684;&#x5B57;&#x7B26;&#x4E32;&#x957F;&#x5EA6;</td>
</tr>
<tr>
<td style="text-align:left">NumberRange</td>
<td style="text-align:left">&#x9A8C;&#x8BC1;&#x8F93;&#x5165;&#x7684;&#x503C;&#x5728;&#x6570;&#x5B57;&#x8303;&#x56F4;&#x5185;</td>
</tr>
<tr>
<td style="text-align:left">URL</td>
<td style="text-align:left">&#x9A8C;&#x8BC1;URL</td>
</tr>
<tr>
<td style="text-align:left">AnyOf</td>
<td style="text-align:left">&#x9A8C;&#x8BC1;&#x8F93;&#x5165;&#x503C;&#x5728;&#x53EF;&#x9009;&#x5217;&#x8868;&#x4E2D;</td>
</tr>
<tr>
<td style="text-align:left">NoneOf</td>
<td style="text-align:left">&#x9A8C;&#x8BC1;&#x8F93;&#x5165;&#x503C;&#x4E0D;&#x5728;&#x53EF;&#x9009;&#x5217;&#x8868;&#x4E2D;</td>
</tr>
</tbody>
</table>










## WTForms常用验证函数
<table>
<thead>
<tr>
<th>验证函数</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>DataRequired</td>
<td>确保字段中有数据</td></tr>
<tr>
<td>EqualTo</td>
<td>比较两个字段的值&#xFF0C;&#x5E38;&#x7528;&#x4E8E;&#x6BD4;&#x8F83;&#x4E24;&#x6B21;&#x5BC6;&#x7801;&#x8F93;&#x5165;</td>
</tr>
<tr>
<td style="text-align:left">Length</td>
<td>验证输入的字符串长度</td>
</tr>
<tr>
<td>NumberRange</td>
<td>验证输入的值在数字范围内</td>
</tr>
<tr>
<td>URL</td>
<td>验证URL</td>
</tr>
<tr>
<td>AnyOf</td>
<td>验证输入值在可选列表中</td>
</tr>
<tr>
<td>NoneOf</td>
<td>验证输入值不在可选列表中</td>
</tr>
</tbody>
</table>  









### 在HTML页面中直接写form表单

```
#模板文件
<form method='post'>
    <input type="text" name="username" placeholder='Username'>
    <input type="password" name="password" placeholder='password'>
    <input type="submit">
</form>
```

### 视图函数中获取表单数据：
```
from flask import Flask,render_template,request

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
    return render_template('login.html',method=request.method)
```

### 使用Flask-WTF实现表单

#### 配置参数：
```python
app.config['SECRET_KEY'] = 'silents is gold'
``` 
#### 模板页面：
```python
 <form method="post">
        #设置csrf_token
        {{ form.csrf_token() }}
        {{ form.username.label }}
        <p>{{ form.username }}</p>
        {{ form.password.label }}
        <p>{{ form.password }}</p>
        {{ form.password2.label }}
        <p>{{ form.password2 }}</p>
        <p>{{ form.submit() }}</p>
        {% for x in get_flashed_messages() %}
            {{ x }}
        {% endfor %}
 </form>
```

#### 视图函数：
```python
#coding=utf-8
from flask import Flask,render_template,\
    redirect,url_for,session,request,flash

#导入wtf扩展的表单类
from flask_wtf import FlaskForm
#导入自定义表单需要的字段
from wtforms import SubmitField,StringField,PasswordField
#导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired,EqualTo
app = Flask(__name__)
app.config['SECRET_KEY']='1'

#自定义表单类，文本字段、密码字段、提交按钮
class Login(Form):
    username = StringField(label=u'用户：',validators=[DataRequired()])
    password = PasswordField(label=u'密码',validators=[DataRequired(),EqualTo('ps2','err')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
    submit = SubmitField(u'提交')

@app.route('/login')
def login():
    return render_template('login.html')

#定义根路由视图函数，生成表单对象，获取表单数据，进行表单数据验证
@app.route('/',methods=['GET','POST'])
def index():
    form = Login()
    if form.validate_on_submit():
        name = form.username.data
        pass1 = form.password.data
        pass2 = form.password2.data
        print(name,pass1,pass2)
        return redirect(url_for('login'))
    else:
        if request.method=='POST':
            flash(u'信息有误，请重新输入！')
        print(form.validate_on_submit())

    return render_template('index.html',form=form)
if __name__ == '__main__':
    app.run(debug=True)
```