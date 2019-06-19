# blog
这是我私人博客的仓库

讲一下各个文件的意义:

1. app.py 项目的启动文件,如果要启动项目,只需要python app.py就可以了;
2. girl.png:项目产生的中间文件,后期会处理掉
3. .qiniu_pythonsdk_hostscache.json:存放文件到七牛云产生的文件
4. app 项目内容的文件;
5. app/web:存放视图函数的文件夹;
6. app/static:存放项目静态文件的地方包括css,js,images;
7. app/templates:存项HTML页面的文件;
8. app/lib:存放一些功能函数;
9. app/tool:也是存放功能函数,后期会合并到lib中;
10. app/model:ORM对象;
11. app/forms:表单验证对象;
12. app/__init__.py:拓展flask核心对象Flask()的文件,将所有的拓展都注册到实例app中;
13. app/secret.py,app/setting.py都是配置文件,secret用来存放敏感的配置;
