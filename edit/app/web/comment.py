import random

from flask import render_template,request,redirect,url_for,current_app,flash
from flask_login import current_user,login_required
from sqlalchemy.sql.expression import func


from app.models import Comment,Reply,Article,Tips,db
from app.forms import CommentForm,ReplyForm
from . import web

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
        print("回复成功")
        return render_template('404.html')
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
