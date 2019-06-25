from flask import render_template,abort,request

from app.models import Article
from app.lib.data_structure import BlogTypeEnum
from app.lib.blankprint import BlankPrint

linux = BlankPrint('linux')




@linux.route('/file')
def linux_file():
    enum_value = 1031
    title = "一切皆文件"
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)

@linux.route('/install')
def linux_install():
    enum_value = 1032
    page = request.args.get("page", 1, type=int)
    paginations = Article.query.filter_by(select=BlogTypeEnum(enum_value).name).order_by(
        Article.create_time.desc()).paginate(page, per_page=10)
    blogs = paginations.items
    title = "Linux的安装"
    return render_template('list.html', blogs=blogs, title=title,paginations=paginations)

@linux.route('/more')
def linux_more():
    abort(404)
    # return render_template('list.html')