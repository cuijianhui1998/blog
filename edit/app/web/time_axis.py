from datetime import datetime

from flask import render_template

from . import web
from app.model.article import Article

@web.route('/time')
def time_axis():
    '''
    時間軸
    '''
    logs = Article.query.order_by(Article.create_time.desc()).all()
    logs = [(datetime.date(l.create_time),l.title,l.id) for l in logs]

    return render_template('time.html',logs=logs)