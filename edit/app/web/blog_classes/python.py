from flask import render_template,url_for,request

from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

python = BlankPrint('python')






@python.route('/base')
def python_base():
    enum_value = 1001
    title = "python的基础"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)

@python.route('/progress')
def python_progress():
    enum_value = 1002
    title = "python进阶"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)

@python.route('/new')
def python_new():
    enum_value = 1003
    title = "python新特性"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)