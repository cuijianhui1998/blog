import random

from flask import render_template,request,redirect,url_for,current_app,flash,jsonify
from flask_login import current_user,login_required
from sqlalchemy.sql.expression import func


from app.models import Comment,Reply,Article,Tips,db
from app.forms import CommentForm,ReplyForm
from app.lib.redis_thumb import myredis
from . import web

redis = myredis()

@web.route('/detail',methods=['GET','POST'])
def detail():
    comment_form = CommentForm(request.form)
    reply_form = ReplyForm(request.form)
    key = request.args.get('id')
    page = request.args.get('page',1,type=int)
    tips = Tips.query.order_by(func.rand()).first()
    message = random.choice(current_app.config['FINISHED_MESSAGE'])
    tips = (message,tips.tip)
    blog = Article.query.get_or_404(key)
    pageinations = Comment.query.with_parent(blog).order_by(Comment.create_time.asc()).paginate(page,per_page=5)
    comments = pageinations.items


    if reply_form.reply_submit.data and reply_form.validate():
        return render_template('error/404.html')
    return render_template('detail.html',blog=blog,tips=tips,comment_form=comment_form,
                           reply_form=reply_form,pageinations=pageinations,comments=comments)


@web.route('/comment',methods=['POST'])
@login_required
def comment():
    comment_form = CommentForm(request.form)
    reply_form = ReplyForm(request.form)
    key = request.args.get('id')
    tips = Tips.query.order_by(func.rand()).first()
    message = random.choice(current_app.config['FINISHED_MESSAGE'])
    tips = (message, tips.tip)
    blog = Article.query.get_or_404(key)
    if comment_form.comment_submit.data and comment_form.validate():
        article_id = key
        content = request.form.get('comment')
        auth_id = current_user.id
        with db.submit_data():
            comment = Comment()
            comment.auth_id=auth_id
            comment.content=content
            comment.article_id = article_id
            db.session.add(comment)
        return redirect(url_for('web.detail',id=article_id))
    return render_template('detail.html',blog=blog,tips=tips,comment_form=comment_form,
                           reply_form=reply_form)


@web.route('/reply',methods=['POST'])
@login_required
def reply():
    comment_form = CommentForm(request.form)
    reply_form = ReplyForm(request.form)
    key = request.args.get('id')
    tips = Tips.query.order_by(func.rand()).first()
    message = random.choice(current_app.config['FINISHED_MESSAGE'])
    tips = (message, tips.tip)
    blog = Article.query.get_or_404(key)
    if reply_form.reply_submit.data and reply_form.validate():
        comment = Comment.query.get(request.args.get('comment_id'))
        if current_user.username!=comment.auth.username:
            content = request.form.get('reply')
            with db.submit_data():
                reply = Reply()
                reply.content = content
                reply.auth_id = current_user.id
                reply.comment_id = request.args.get('comment_id')
                db.session.add(reply)
            return redirect(url_for('web.detail', id=key))
        flash("你不能回复自己")
    return render_template('detail.html',blog=blog,tips=tips,comment_form=comment_form,
                           reply_form=reply_form)

@web.route('/thumb/<uid>/<aid>')
def thumb(uid,aid):
    if _is_thumb(uid,aid) and not redis.sismember('thumb-'+aid,uid):
        redis.sadd('thumb-'+aid,uid)
        return jsonify({'code':200,'message':'点赞成功'})
    return jsonify({'code':403,'message':'你已经点赞过了'})

@web.route('/thumb_total/<aid>')
def thumb_total(aid):
    none = request.args.get("_")
    print(redis.hget('thumbs_total',aid))
    if redis.hget('thumbs_total',aid) is None:
        total = len(redis.smembers('thumb-'+aid))
        result = dict(total=total,aid=aid)
    else:
        total = int(redis.hget('thumbs_total',aid))+len(redis.smembers('thumb-'+aid))
        result = dict(total=total,aid=aid)
    return jsonify(result)

def _is_thumb(uid,aid):
    article = Article.query.get_or_404(aid)
    res = [thumb for thumb in article.thumbs if thumb.auth_id==uid]
    return  False if res else True

@web.route('/last')
def last():
    id = request.args.get('id')
    select =request.args.get('select')
    last_article = Article.query.filter_by(select=select).filter(Article.id>id).order_by(Article.id.asc()).first()
    if last_article:
        last_article = dict(url=url_for('web.detail',id=last_article.id), title=last_article.title,code=200)
        return jsonify(last_article)
    else:
        last_article = dict(code=404,message="这才是第一篇文章哦")
        return jsonify(last_article)

@web.route('/next')
def next():
    id = request.args.get('id')
    select = request.args.get('select')
    next_article = Article.query.filter_by(select=select).filter(Article.id < id).order_by(Article.id.desc()).first()
    if next_article:
        next_article = dict(url=url_for('web.detail',id=next_article.id), title=next_article.title,code=200)
        return jsonify(next_article)
    else:
        next_article = dict(code=404,message="这是最后一篇哦")
        return jsonify(next_article)


@web.route('/article/link')
def link():
    select = request.args.get('select')
    id = request.args.get('id')
    link_articles = Article.query.filter_by(select=select).filter(Article.id!=id).order_by(func.rand()).limit(10)
    result = {}

    if link_articles:
        data=[dict(url=url_for(
            'web.detail',id=link_article.id),title=link_article.title) for link_article in link_articles]
        result['data'] = data
        result['code'] = 200
        return jsonify(result)
    return jsonify(dict(code=404,message='暂时还没有相关的文章'))