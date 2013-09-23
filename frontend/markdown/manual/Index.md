drape是一个Python语言的web框架。
目标是做一个我喜欢的Python的web框架。

# 吸取众家之长
在开发drape之前，
我使用过很多开源的web框架，
不仅是Python，还包括一些php的框架。

drape融合了其它框架中的一些我个人比较喜欢的特性，
参考了它们的代码。

## 1.ThinkPHP
* 伪静态
* 链式模型操作
* 简单的入口
* 子目录

## 2.web.py
* 自动加载模块和类
* wsgi接口
* 不同实现的session
* 自由地指定模板引擎

## 3.JeCat
* 自动反射表的字段名
* 在字段名前加上表名以避免冲突

# 其它一些特点
## 子目录
有些Python框架只能在网站根目录下运行，但是drape在子目录下，只需要稍加配置，就可以正常运行。

## 多种接口
* 支持cgi接口、wsgi接口等多种部署方式
* 支持SAE

我写了篇文章总结python的cgi接口，
见[【apache+cgi+python】cgi接口浅析][1]

[1]:https://github.com/lexdene/md-blog/blob/master/python/webpy/apache-cgi-python.md "apache+cgi+python"
