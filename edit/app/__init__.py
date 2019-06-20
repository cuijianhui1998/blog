import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask,request,render_template

from app.setting import config
from app.models import Auth,Article
from app.extension import login_register,admin_register,db_register

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        win = sys.platform.startswith('win')
        config_name = 'development' if win else 'production'

    app =Flask(__name__)
    app.config.from_object(config[config_name])

    admin_register(app)
    db_register(app)
    login_register(app)

    blueprint_register(app)
    logging_register(app)
    error_register(app)

    return app


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

