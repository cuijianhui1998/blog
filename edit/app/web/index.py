from flask import render_template,current_app

from . import web
from app.models import Article


@web.route('/')
def index():
    '''
    博客的首頁
    '''
    recommend = Article.query.filter_by(is_recommend=1).limit(3)
    list = Article.query.order_by(Article.create_time.desc()).all()
    new = Article.query.order_by(Article.create_time.desc()).limit(3)
    return render_template('index.html',recommend=recommend,list=list,new_blog=new)


@web.route('/about')
def about():
    return render_template('about.html')


@web.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('icon.ico')


@web.route('/life')
def life_all():
    return render_template('list.html')

@web.route('/life/notes')
def life_notes():
    return render_template('list.html')

@web.route('/life/photo')
def life_photo():
    return render_template('share.html')
