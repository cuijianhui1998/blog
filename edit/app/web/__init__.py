from flask import Blueprint,render_template

from app.web.blog_classes.python import python
from app.web.blog_classes.linux import linux
from app.web.blog_classes.frame import web_frame
from app.web.blog_classes.front import front



def create_blueprint():
    web = Blueprint("web", __name__)

    #关于博客分类的视图
    python.register(web)
    front.register(web)
    web_frame.register(web)
    linux.register(web)
    return web

web = create_blueprint()



@web.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@web.app_errorhandler(500)
def internal(error):
    return render_template('500.html'),500



from app.web import detail
from app.web import index
from app.web import life
from app.web import release
from app.web import say_me
from app.web import time_axis
from app.web import auth
from app.web import serach