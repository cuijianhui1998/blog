from flask import render_template,request
from sqlalchemy import and_,or_

from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

web_frame = BlankPrint('web_frame')


@web_frame.route('/flask')
def web_flask():
    enum_value = 1011
    page = request.args.get("page",1,type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page,per_page=10)
    blogs = paginations.items
    title = "最爱之flask"
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)


@web_frame.route('/django')
def web_django():
    enum_value = 1012
    title = "讨厌的Django"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)


@web_frame.route('/tornado')
def web_tornado():
    enum_value = 1013
    title = "神秘的tornado"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title)