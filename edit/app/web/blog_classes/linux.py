from flask import render_template,abort

from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

linux = BlankPrint('linux')

@linux.route('/')
def linux_all():
    enum_values = [1031, 1032]
    blogs = []
    for enum_value in enum_values:
        blogs.extend(
            Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all())
    title = "可恶的Linux"
    return render_template('list.html', blogs=blogs, title=title)


@linux.route('/file')
def linux_file():
    enum_value = 1031
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "一切皆文件"
    return render_template('list.html', blogs=blogs, title=title)

@linux.route('/install')
def linux_install():
    enum_value = 1032
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "Linux的安装"
    return render_template('list.html', blogs=blogs, title=title)

@linux.route('/more')
def linux_more():
    abort(404)
    # return render_template('list.html')