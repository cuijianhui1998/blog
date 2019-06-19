from flask import request,render_template,redirect,url_for


from . import web
from app.forms.search import SearchForm
from app.model.article import Article
from app.lib.unique_list import UniqueList


@web.route('/search',methods=['GET','POST'])
def search():
    form = SearchForm(request.form)
    blogs = UniqueList()
    if request.method=='POST' and form.validate():
        key = request.form.get("keyboard")
        blogs.extend(Article.query.filter_by(select=key).all())
        blogs.extend(Article.query.filter(Article.title.like("%{}%".format(key))).all())
        blogs.extend(Article.query.filter(Article.body.like("%{}%".format(key))).all())
        return render_template('control/search.html',key=key,blogs=blogs)
    return render_template('control/search.html', blogs=blogs,form=form)



