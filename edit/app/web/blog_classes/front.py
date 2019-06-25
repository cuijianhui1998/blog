from flask import render_template,request


from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

front = BlankPrint('front')






@front.route('/html5')
def front_html5():
    enum_value = 1021
    title = "html5"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)


@front.route('/css')
def front_css():
    enum_value = 1022
    title = "css"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)


@front.route('/js')
def front_js():
    enum_value = 1023
    title = "javascript"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)