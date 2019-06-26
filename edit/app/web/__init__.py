from flask import Blueprint

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

from app.web import index
from app.web import release
from app.web import auth
from app.web import comment
from app.web import test
