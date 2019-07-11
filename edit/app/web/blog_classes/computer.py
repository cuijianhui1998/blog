from flask import render_template,request


from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

computer = BlankPrint('computer')






@computer.route('/data_structure')
def data_structure():
    enum_value = 1021
    title = "数据结构"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)


@computer.route('/sql')
def sql():
    enum_value = 1022
    title = "数据库"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)


@computer.route('/network')
def network():
    enum_value = 1023
    title = "计算机网络"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)