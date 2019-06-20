from flask import render_template

from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

web_frame = BlankPrint('web_frame')

@web_frame.route('/')
def frame_all():
    enum_values = [1011, 1012, 1013]
    blogs = []
    for enum_value in enum_values:
        blogs.extend(
            Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all())
    title = "web框架"
    return render_template('list.html', blogs=blogs, title=title)

@web_frame.route('/flask')
def web_flask():
    enum_value = 1011
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "最爱之flask"
    return render_template('list.html', blogs=blogs, title=title)


@web_frame.route('/django')
def web_django():
    enum_value = 1012
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "讨厌的Django"
    return render_template('list.html', blogs=blogs, title=title)


@web_frame.route('/tornado')
def web_tornado():
    enum_value = 1013
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "神秘的tornado"
    return render_template('list.html', blogs=blogs, title=title)