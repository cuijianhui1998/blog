from flask import render_template,request

from . import web
from app.model.article import Article

@web.route('/detail')
def detail():
    key = request.args.get('id')
    blog = Article.query.get_or_404(key)
    return render_template('detail.html',blog=blog)