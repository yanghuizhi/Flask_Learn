### 开启 Debug 模式
export FLASK_DEBUG=1  

### 翻译
```python
'第一版翻译'
# 提取所有_()标记的文本，生成翻译源文件 messages.pot
pybabel extract -F babel.cfg -k _l -o messages.pot .
# 生成语言目录
pybabel init -i messages.pot -d app/translations -l en
# 应用翻译，将.po文件转换成.mo文件，mo文件会被应用程序加载并翻译
pybabel compile -d app/translations

'第二版翻译'
### 更新翻译
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/translations


'第三版翻译'，使用工作流
# 要添加新的语言，请使用：
flask translate init <language-code>
# 在更改_()和_l()语言标记后更新所有语言：
flask translate update
# 在更新翻译文件后编译所有语言：
flask translate compile

```