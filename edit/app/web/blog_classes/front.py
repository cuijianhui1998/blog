from flask import render_template,request


from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

front = BlankPrint('front')


@front.route('/')
def front_all():
    enum_values = [1021, 1022, 1023]
    blogs = []
    for enum_value in enum_values:
        blogs.extend(
            Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all())
    title = "花俏的前端"
    return render_template('list.html', blogs=blogs, title=title)



@front.route('/html5')
def front_html5():
    enum_value = 1021
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "html5"
    return render_template('list.html', blogs=blogs, title=title)


@front.route('/css')
def front_css():
    enum_value = 1022
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "css"
    return render_template('list.html', blogs=blogs, title=title)


@front.route('/js')
def front_js():
    enum_value = 1023
    blogs = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(Article.create_time.desc()).all()
    title = "javascript"
    return render_template('list.html', blogs=blogs, title=title)