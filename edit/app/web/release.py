import datetime
import random

from flask import render_template,request,jsonify,redirect,url_for,flash,current_app
from flask_login import login_required
from sqlalchemy.sql.expression import func,select

from app.lib.photo_shop import uploadImg,get_specification_image
from app.lib.data_structure import UniqueList
from app.models import Article,Tips
from app.extension import db
from app.forms import ArticleForm,SearchForm
from . import web
from app.lib.common_data import right_show


'''
主要描述的时是关于通过富文本编辑器添加博客的视图函数
'''

@web.route("/publish", methods=["GET", "POST"])
@login_required
def publish():
    form = ArticleForm(request.form)
    if request.method == "GET":
        return render_template("control/publish.html", form=form)

    if form.validate_on_submit():
        # 获取博客内容
        TextContent = request.form.get("TextContent")

        # 获取上传的文件,并对图片进行预处理,上传到七牛云,然后获取url地址
        poster = None
        if request.files.get('poster'):
            file = request.files.get('poster')
            imgData = get_specification_image(file)
            poster = uploadImg(imgData)

        with db.submit_data():
            data = Article()
            data.setter_data(request.form)
            data.body = TextContent
            data.poster = poster
            db.session.add(data)
        return redirect(url_for('web.index'))
    else:
        for errorMessage in form.errors:
            flash(errorMessage)
        return redirect(url_for('web.publish'))


@web.route('/uploads/', methods=['POST'])
def uploads():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        # 图片上传七牛云
        imgData = file.read()
        imgUrl = uploadImg(imgData)
        print("七牛云返回图片URL", imgUrl)
        if imgUrl:
            res = {
                'success': 1,
                'message': '上传成功',
                'url': imgUrl
            }
        else:
            res = {
                'success': 0,
                'message': '上传失败'
            }
    return jsonify(res)


@web.route('/detail')
def detail():
    key = request.args.get('id')
    tips = Tips.query.order_by(func.rand()).first()
    message = random.choice(current_app.config['FINISHED_MESSAGE'])
    tips = (message,tips.tip)
    blog = Article.query.get_or_404(key)
    return render_template('detail.html',blog=blog,tips=tips)

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


@web.route('/time')
def time_axis():
    '''
    時間軸
    '''
    logs = Article.query.order_by(Article.create_time.desc()).all()
    logs = [(datetime.date(l.create_time),l.title,l.id) for l in logs]

    return render_template('time.html',logs=logs)

