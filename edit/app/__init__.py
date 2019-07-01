import os
import sys
import logging
import atexit
try:
    #windows下并没有这个模块,只存在于Linux下
    import fcntl
except ModuleNotFoundError:
    pass

from logging.handlers import RotatingFileHandler

from flask import Flask,request,render_template
from flask_apscheduler import APScheduler
from flask_moment import Moment

from app.setting import config
from app.models import Auth,Article,Tips,Message
from app.extension import login_manager,admin_register,db,bootstrap

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))





def create_app(config_name=None):
    if config_name is None:
        win = sys.platform.startswith('win')
        config_name = 'development' if win else 'production'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    blueprint_register(app)
    logging_register(app)
    error_register(app)
    mine_info_register(app)

    extension_register(app)
    moment = Moment(app)

    apscheduler_register(app)

    return app


def apscheduler_register(app):
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)


def extension_register(app):
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'Your custom message'
    login_manager.login_message_category = 'warning'

    bootstrap.init_app(app)
    db.init_app(app)

    admin_register(app)


def blueprint_register(app):
    from app.web import web
    app.register_blueprint(web)

def logging_register(app):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter,self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir,'logs/blog.log'),maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)

def error_register(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'),404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'),500

def mine_info_register(app):
    #自定义上下文变量和函数
    @app.context_processor
    def appinfo():
        #设置了一个上下文函数,获取全局变量,渲染公共模板
        new = Article.query.order_by(Article.create_time.desc()).limit(3)
        reco = Article.query.filter_by(select='other').limit(2)
        top = Article.query.filter_by(select='css').limit(2)
        return dict(new=new,reco=reco,top=top)


