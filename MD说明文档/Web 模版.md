# Welcome to Templates!

1.	模板实际就是一个文件，文件里有一个字符串（通常很长），字符串的内容就是html代码，其中用变量来表示动态部分

2.	使用真实的值来替换字符串中的变量，再返回最终结果的过程叫做渲染，Flask使用jinja2这个模板引擎来渲染模板

3. Jinja2模板使用双大括号，即{{变量名}}来代表变量，如<标签>{{变量名}}<标签>

4. Flask的render_template函数封装了Jinja2模板的引擎，render_template函数的第一个参数是模板名称，后面的参数代表了模板中对应变量的真实值

5.	render_template函数会把变量传递给Jinja2模板来替换Jinja2模板中预先定义好的变量

6.	所有的模板文件必须放到一个名为templates的文件夹里（注意，是文件夹，不是python包），路由文件必须和templates在同一级目录下

7.	templates文件夹里也可以有多级文件夹，若在多级文件夹下，则需要如下方式写：render_template("admin/login.html")

8.	再次强调，在调试代码时，如果只修改了路由文件，无需重启服务，直接在地址栏输入地址即可进入新修改的程序，如果修改了模板文件，则需重启服务，否则报错


[变量](#变量) &nbsp; &nbsp; &nbsp;  <br/>
[反向路由](#反向路由) &nbsp; &nbsp; &nbsp;  <br/>
[过滤器](#过滤器)
1. [字符串操作](#字符串操作) 
2. [列表操作](#列表操作) 
3. [自定义过滤器](#自定义过滤器)

[判断与循环](#判断与循环)
[模版继承](#模版继承) &nbsp; &nbsp; &nbsp;  <br/>



## 变量

模板语句的标识：

    {% 模板语句 %}
    如：{% for ir in AllResult_tuple %}
    注意：与python不同，所有的关键字后面都不带冒号

模板语句的变量：<br/>
是一种特殊的占位符，告诉模板引擎这个位置的值，从渲染模板时使用的数据中获取；Jinja2除了能识别基本类型的变量，还能识别{ }；

    {{ 变量名 }}
    如：{{form.password}}

模板语句的注释
    
    {# 注释内容 #}







## 反向路由

Flask提供了 `url_for()` 辅助函数，它使用URL到视图函数的内部映射关系来生成URL。 接收视图函数名作为参数，返回对应的URL。

`url_for()`函数的一个有趣的地方是，你可以添加任何关键字参数，如果这些参数的名字没有直接在URL中匹配使用，那么Flask将它们设置为URL的查询字符串参数。

```python
@app.route('/index')
def index():
    return render_template('index.html')  # 返回的是 /index

@app.route('/user/')
def redirect():
    return url_for('index',_external=True)  # 返回绝对地址
    
# 路由传递的参数默认当做string处理，尖括号<和>包裹中的内容是动态的
# 可以指定参数类型，例如('/user/<int:id>')，指定int类型    
@bp.route('/user/<username>')
@bp.route('/user/<int:id>')
def user(username):
    pass
```






## 过滤器

过滤器的本质就是函数。有时候我们不仅仅只是需要输出变量的值，我们还需要修改变量的显示，甚至格式化、运算等等，这就用到了过滤器。 过滤器的使用方式为：变量名 | 过滤器。 过滤器名写在变量名后面，中间用 | 分隔。如：`{{variable | capitalize}}`，这个过滤器的作用：把变量variable的值的首字母转换为大写，其他字母转换为小写。 其他常用过滤器如下：

### 字符串操作

safe：禁用转义；

      <p>{{ '<em>hello</em>' | safe }}

capitalize：把变量值的首字母转成大写，其余字母转小写；
```
  <p>{{ 'hello' | capitalize }}</p>
```

lower：把值转成大写、小写；
    
    <p>{{ 'hello' | upper }}</p>
    <p>{{ 'HELLO' | lower }}</p>

title：把值中的每个单词的首字母都转成大写；
```
  <p>{{ 'hello' | title }}</p>
```
trim：把值的首尾空格去掉；
```
  <p>{{ ' hello world ' | trim }}</p>
```

reverse:字符串反转；
```
  <p>{{ 'olleh' | reverse }}</p>
```

format:格式化输出；
```
  <p>{{ '%s is %d' | format('name',17) }}</p>
```
  
striptags：渲染之前把值中所有的HTML标签都删掉；
```
  <p>{{ '<em>hello</em>' | striptags }}</p>
```

### 列表操作

first：取第一个元素
```
  <p>{{ [1,2,3,4,5,6] | first }}</p>
```
  
last：取最后一个元素
```
  <p>{{ [1,2,3,4,5,6] | last }}</p>
```

*length：获取列表长度*
```
  <p>{{ [1,2,3,4,5,6] | length }}</p>
```

sum：列表求和
```
  <p>{{ [1,2,3,4,5,6] | sum }}</p>
```

sort：列表排序
```
  <p>{{ [6,2,3,1,5,4] | sort }}</p>
```

语句块过滤(不常用)：
```
  {% filter upper %}
    this is a Flask Jinja2 introduction
  {% endfilter %}
```

### 自定义过滤器

过滤器的本质是函数。当模板内置的过滤器不能满足需求，可以自定义过滤器。自定义过滤器有两种实现方式：一种是通过Flask应用对象的add_template_filter方法。还可以通过装饰器来实现自定义过滤器。

自定义的过滤器名称如果和内置的过滤器重名，会覆盖内置的过滤器。

实现方式一：通过调用应用程序实例的add_template_filter方法实现自定义过滤器。该方法第一个参数是函数名，第二个参数是自定义的过滤器名称。

```
def filter_double_sort(ls):
    return ls[::2]
app.add_template_filter(filter_double_sort,'double_2')
```

实现方式二：用装饰器来实现自定义过滤器。装饰器传入的参数是自定义的过滤器名称。
```
@app.template_filter('db3')
def filter_double_sort(ls):
    return ls[::-3]
```    




## 判断与循环

- `{% block navbar %} ... {% endblock %}` : `navbar`块是一个可选块，用于自定义模块


#### **if-else语句**

    {% if 判定项 %}        
        <title>{{ 判定项 }} - Microblog</title>
    {% else %}
        <title>Welcome to Microblog</title>
    {% endif %}

#### **for 循环语句**        
        
    {% for A in B %}
       。。。
    {% endfor %}

#### 序号

     {% for i in user_list %}
        <tr>
            <td>{{loop.index}}</td>
            <td>{{i}}</td>
        </tr>
     {% endfor %}
 注意：loop.index不是python的语法，而是jinja2的语法，用于在模板上生成一个显示用的序号

注意：
1.	这个序号只是显示用的，与数据库里的ID无关

2.	由于不是python的语法，而是用来显示在模板上给用户看的是，所以它从1开始，而不像python从0开始

3.	{{loop.index}}通常和table配合使用，因为只有table才能循环展示数据




## 模版继承

父模版接手布局, `extends`语句用来建立了两个模板之间的继承关系，这样Jinja2就会按照要求展示网页.

而两个模板中匹配的`block`语句和其名称`content`, 让Jinja2知道如何将这两个模板合并成在一起. `block`控制语句来定义派生模板可以插入代码的位置

现在，扩展应用程序的页面就变得极其方便了，我可以创建从同一个基础模板`base.html`继承的派生模板，这就是我让应用程序的所有页面拥有统一外观布局而不用重复编写代码的秘诀。

- 父模板：base.html  

      {% block top %}
        顶部菜单
      {% endblock top %}
    
      {% block content %}
        # 将两个模版中间的语句合并在一起
      {% endblock content %}
    
      {% block bottom %}
        底部
      {% endblock bottom %}

- 子模版
```
   {% extends 'base.html' %}  # 继承模版
   
   {% block content %}
       # 将两个模版中间的语句合并在一起
   {% endblock content %}
```

模板继承使用时注意点：
- 不支持多继承。
- 为了便于阅读，在子模板中使用extends时，尽量写在模板的第一行。
- 不能在一个模板文件中定义多个相同名字的block标签。
- 当在页面中使用多个block标签时，建议给结束标签起个名字，当多个block嵌套时，阅读性更好。