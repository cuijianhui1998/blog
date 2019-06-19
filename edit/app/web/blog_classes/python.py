from flask import render_template,url_for,request


from app.web.blog_classes import python,linux
from app.model.article import Article
from app.lib.blog_type import BlogTypeEnum
from app.lib.blankprint import BlankPrint

python = BlankPrint('python')



@python.route('/')
def python_all():
    enum_values = [1001,1002,1003]
    blogs = []
    for enum_value in enum_values:
        blogs.extend(Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()))

    title = "万能的python"
    return render_template('list.html', blogs=blogs, title=title)


@python.route('/base')
def python_base():
    '''
    學無止境
    '''
    enum_value = 1001
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "python的基础"
    return render_template('list.html', blogs=blogs, title=title)

@python.route('/progress')
def python_progress():
    enum_value = 1002
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "python进阶的知识"
    return render_template('list.html', blogs=blogs, title=title)

@python.route('/new')
def python_new():
    enum_value = 1003
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "python新特性"
    return render_template('list.html', blogs=blogs, title=title)