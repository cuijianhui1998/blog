from flask import render_template,current_app,request

from . import web
from app.models import Article


@web.route('/')
def index():
    '''
    博客的首頁
    '''
    recommend = Article.query.filter_by(is_recommend=1).limit(3)
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    flask_blogs = Article.query.filter_by(select='flask').limit(2)
    return render_template('index.html',recommend=recommend,blogs=blogs,paginations=paginations,flask_blogs=flask_blogs)

@web.route('/about')
def about():
    return render_template('about.html')

@web.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('icon.ico')



@web.route('/life/notes')
def life_notes():
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select='other').order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    title = "我的树洞"
    return render_template('list.html',blogs=blogs,title=title,paginations=paginations)

@web.route('/life/photo')
def life_photo():
    return render_template('share.html')



