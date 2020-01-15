# Welcome to Flask_Learn!

### 运行Flask
`flask run`  

### 环境变量设置

1. 可配置`.flaskenv`文件，app既可以自动加载
2. 或者mac Terminal输入：`export FLASK_APP=Flask_Learn.py`
3. 或者Window Terminal输入：`set FLASK_APP=Flask_Learn.py`


### 配置DEBUG模式

`export FLASK_DEBUG=1`


### 依赖文件
```python
pip freeze > requirements.txt  # 输出/更新依赖文件
pip install -r requirements.txt  # 下载依赖文件
```

### 数据库
```python
flask db init                  # 创建迁移数据库，产生migrations的新目录
flask db migrate -m "。。。"    # 数据库迁移
flask db upgrade               # 将更改应用到数据库
flask db downgrade             # 回滚数据库迁移
```

### 翻译
```python
# pybabel extract命令读取-F选项中给出的配置文件，然后从命令给出的目录（当前目录或本处的. ）扫描与配置的源匹配的目录中的所有代码和模板文件。 默认情况下，pybabel将查找_()以作为文本标记，但我也使用了重命名为_l()的延迟版本，所以我需要用-k _l来告诉该工具也要查找它 。 -o选项提供输出文件的名称。
# 请注意，messages.pot文件不需要合并到项目中。 这是一个只要再次运行上面的命令，就可以在需要时轻松地重新生成的文件。 因此，不需要将该文件提交到源代码管理。
# 查看本机支持的语言
pybabel --list-locales
# 提取所有文本，生成翻译模版pot
pybabel extract -F babel.cfg -k _l -o messages.pot .
# 生成语言目录，中文，生成对应po文件
pybabel init -i messages.pot -d app/translations -l zh
# 编译上述po文件，生成mo文件，mo文件是加载翻译文件
pybabel compile -d app/translations
# 更新文件，这一步貌似没啥用处
pybabel update -i messages.pot -d app/translations 

# 简化版
flask translate update
flask translate compile
```