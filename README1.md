# Welcome to Flask_Learn!

#### 运行
```python
flask run   # 运行flask

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
# 查看本机支持的语言
pybabel --list-locales
# 生成翻译模版
pybabel extract -F babel.cfg -o messages.pot .
# 创建中文翻译，生成对应po文件
pybabel init -i messages.pot -d app/translations -l zh_Hans_CN
# 编译需要使用的文本，生成对应mo文件（复用）
pybabel compile -d app/translations


# 更新翻译
# 重新生成messages.pot 文件
pybabel extract -F babel.cfg -k _l -o messages.pot .
# 更新你语言下的mo文件（有2步）
# 第一步重新生成mo文件，第二步更新文件
pybabel compile -d app/translations
pybabel update -i messages.pot -d app/translations

```
