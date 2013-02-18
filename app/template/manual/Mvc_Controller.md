drape的controller有3个特点：自动路径加载、嵌套、伪静态

# 1.自动路径加载
例如：访问/user/Login时，
drape会从访问路径自动加载app.controller.user模块，实例化它的Login类，然后执行它。

app.controller是固定的controller前缀。

# 2.嵌套
controller可以互相嵌套。

例如，多个controller拥有相同的页面布局，
那么可以将它们的布局的代码提取到一个Layout controller中，
这样每个controller只需要关心不相同的内容。

一些模板引擎也提供模板嵌套的功能，
但是controller的嵌套可以提供更加强大的功能。

* controller中可以完成计算、数据库查询等动作，但是模板嵌套很难做到。
* controller可以无限层数的嵌套，但是少数模板引擎只能嵌套一层。

嵌套的特点，
有人说它好，有人说它不好。
我很喜欢嵌套，
但是对于不喜欢嵌套的开发者来说，
嵌套会将简单的事情变复杂。

# 3.伪静态
例如：访问/user/MainPage/id/32/section/blog时，
drape会实例化app.controller.user模块，实例化它的MainPage类。
然后将剩下的参数整理成字典{'id':'32','section':'blog'}，
传递给MainPage类，
然后执行它。
