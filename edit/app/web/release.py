from flask import render_template,request,jsonify,redirect,url_for,flash
from flask_login import login_required

from app.tools.qstorge import uploadImg
from app.model.article import Article
from app.model.base import db
from app.tools.cut_image import get_specification_image
from app.forms.article import ArticleForm
from . import web


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



