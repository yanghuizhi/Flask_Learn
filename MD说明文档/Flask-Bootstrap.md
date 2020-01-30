## Bootstrap简介

最受欢迎的CSS框架之一是由Twitter推出的[Bootstrap](http://getbootstrap.com/)。 如果你想看看这个框架可以设计的页面类型，文档有一些[示例](https://getbootstrap.com/docs/3.3/getting-started/#examples)。

这些是使用Bootstrap来设置网页风格的一些好处：

*   在所有主流网页浏览器中都有相似的外观
*   自动处理PC桌面，平板电脑和手机屏幕尺寸
*   可定制的布局
*   精心设计的导航栏，表单，按钮，警示，弹出窗口等

使用Bootstrap最直接的方法是简单地在你的基本模板中导入*bootstrap.min.css*文件。 可以下载此文件并将其添加到你的项目中，或直接从[CDN](https://en.wikipedia.org/wiki/Content_delivery_network)导入。 然后，你可以根据其[文档](https://getbootstrap.com/docs/3.3/getting-started/)开始使用它提供的通用CSS类，实在是太棒了。 你可能还需要导入包含框架JavaScript代码的*bootstrap.min.js*文件，以便使用最先进的功能。

幸运的是，有一个名为[Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)的Flask插件，它提供了一个已准备好的基础模板，该模板引入了Bootstrap框架。 让我们来安装这个扩展：
```
(venv) $ pip install flask-bootstrap
```

## 使用Flask-Bootstrap

Flask-Bootstrap需要像大多数其他Flask插件一样被初始化：

*app/\_\_init\_\_.py*: Flask-Bootstrap实例。
```
# ...
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# ...
bootstrap = Bootstrap(app)
```

在初始化插件之后，*bootstrap/base.html*模板就会变为可用状态，你可以使用`extends`子句从应用模板中引用。

但是，回顾一下，我已经使用了`extends`子句来继承我的基础模板，这使我可以将页面的公共部分放在一个地方。 *base.html*模板定义了导航栏，其中包含几个链接，并且还导出了一个`content`块。 应用中的所有其他模板都从基础模板继承，并为内容块提供页面的主要内容。

那么我怎样才能适配Bootstrap基础模板呢？ 解决方案是从使用两个层级到使用三个层级。 *bootstrap/base.html*模板提供页面的基本结构，其中引入了Bootstrap框架文件。 这个模板为派生的模板定义了一些块，例如`title`，`navbar`和`content`（参见块的[完整列表](https://pythonhosted.org/Flask-Bootstrap/basic-usage.html#available-blocks)）。 我将更改*base.html*模板以从*bootstrap/base.html*派生，并提供`title`，`navbar`和`content`块的实现。 反过来，*base.html*将为从其派生的模板导出`app_content`块以定义页面内容。

下面你可以看到从Bootstrap基础模板派生的*base.html*的代码。 请注意，此列表不包含导航栏的整个HTML，但你可以在GitHub上或下载本章的代码来查看完整的实现。

*app/templates/base.html*：重新设计后的基础模板。
```
{% extends 'bootstrap/base.html' %}

{% block title %}
    {% if title %}{{ title }} - Microblog{% else %}Welcome to Microblog{% endif %}
{% endblock %}

{% block navbar %}
    <nav class="navbar navbar-default">
        ... navigation bar here (see complete code on GitHub) ...
    </nav>
{% endblock %}

{% block content %}
    <div class="container">
        {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
            <div class="alert alert-info" role="alert">{{ message }}</div>
            {% endfor %}
        {% endif %}
        {% endwith %}

        {# application content needs to be provided in the app_content block #}
        {% block app_content %}{% endblock %}
    </div>
{% endblock %}
```

从中你可以看到我如何从*bootstrap/base.html*派生此模板，接下来分别实现了页面标题、导航栏和页面内容的这三个模块。

`title`块需要使用`<title>`标签来定义用于页面标题的文本。 对于这个块我简单地挪用了原始基本模板中`<title>`标签内部的逻辑。

`navbar`块是一个可选块，用于定义导航栏。 对于此块，我调整了Bootstrap导航栏文档中的示例，以便它在左侧展示网站品牌，跟着是Home和Explore的链接。 然后我添加了个人主页和登录或注销链接并使其与页面的右边界对齐。 正如我上面提到的，我在上面的例子中省略了HTML，但是你可以从本章的下载包中获得完整的*base.html*模板。

最后，在`content`块中，我定义了一个顶级容器，并在其中设定了呈现闪现消息的逻辑，这些消息现在将显示为Bootstrap警示的样式。 接下来是一个新的`app_content`块，这个块用于从其派生的模板来定义他们自己的内容。

所有页面模板的原始版本在名为`content`的块中定义了它们的内容。 正如你在上面看到的，Flask-Bootstrap使用名为`content`的块，所以我将我的内容块重命名为`app_content`。 所以我所有的模板都必须重命名为使用`app_content`作为它们的内容块。 例如，这是*404.html*模板的修改后版本的展示：

*app/templates/404.html*：重新设计后的404错误模板。
```
{% extends "base.html" %}

{% block app_content %}
    <h1>File Not Found</h1>
    <p><a href="{{ url_for('index') }}">Back</a></p>
{% endblock %}
```

## 渲染Bootstrap表单

Flask-Bootstrap在渲染表单这方面做得非常出色。 Flask-Bootstrap不需要逐个设置表单字段，而是使用一个接受Flask-WTF表单对象作为参数的宏，并以Bootstrap样式渲染出完整的表单。

下面你可以看到重新设计后的*register.html*模板：

*app/templates/register.html*:：用户注册模板。

```
{% extends "base.html" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block app_content %}
    <h1>Register</h1>
    <div class="row">
        <div class="col-md-4">
            {{ wtf.quick_form(form) }}
        </div>
    </div>
{% endblock %}
```

是不是很棒？ 顶端附近的`import`语句与Python导入类似。 这增加了一个`wtf.quick_form()`宏，它在单行代码中渲染完整的表单，包括对显示验证错误的支持，并且适配Bootstrap框架的所有样式。

再一次地，我不会向你展示我为应用中的其他表单所做的所有更改，但这些更改都是可以在GitHub上下载或检查到的。

## 渲染用户动态

单条用户动态的渲染逻辑被提取到名为*_post.html*的子模板中。 我只需要在这个模板上做一些很小的调整，就可以使其在Bootstrap下看起来很棒了。

*app/templates/_post.html*: 重新设计后的用户动态子模板。
```
    <table class="table table-hover">
        <tr>
            <td width="70px">
                <a href="{{ url_for('user', username=post.author.username) }}">
                    <img src="{{ post.author.avatar(70) }}" />
                </a>
            </td>
            <td>
                <a href="{{ url_for('user', username=post.author.username) }}">
                    {{ post.author.username }}
                </a>
                says:
                <br>
                {{ post.body }}
            </td>
        </tr>
    </table>
```

## 渲染分页链接

分页链接是Bootstrap提供直接支持的另一个方面。 为此，我再一次访问Bootstrap [文档](https://getbootstrap.com/docs/3.3/components/#optional-disabled-state)，并修改了其中的一个示例。 以下是在*index.html*页面中的分页链接的代码：

*app/templates/index.html*: 重新设计后的分页链接。
```
    ...
    <nav aria-label="...">
        <ul class="pager">
            <li class="previous{% if not prev_url %} disabled{% endif %}">
                <a href="{{ prev_url or '#' }}">
                    <span aria-hidden="true">&larr;</span> Newer posts
                </a>
            </li>
            <li class="next{% if not next_url %} disabled{% endif %}">
                <a href="{{ next_url or '#' }}">
                    Older posts <span aria-hidden="true">&rarr;</span>
                </a>
            </li>
        </ul>
    </nav>
```

请注意，在分页链接的实现中，当某个方向没有更多内容时，不是隐藏该链接，而是使用禁用状态，这会使该链接显示为灰色。

类似的更改需要应用于*user.html*，但我不打算展示在此处。 本章的下载包中包含这些更改。