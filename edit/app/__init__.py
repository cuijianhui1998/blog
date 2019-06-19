
from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from app.model.base import db
from app.model.article import Article
from app.model.auth import Auth

from app.lib.admin import ArticleView,MyIndexView

login_manager = LoginManager()

def create_app():
    app =Flask(__name__)
    app.config.from_object("app.setting")
    app.config.from_object("app.secret")

    admin_register(app)
    blueprint_register(app)
    db_register(app)
    login_register(app)

    return app

def login_register(app):
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'


def db_register(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def blueprint_register(app):
    from app.web import web
    app.register_blueprint(web)


def admin_register(app):
    admin = Admin(app, name='博客后台',index_view= MyIndexView(name="首页"),template_mode='bootstrap3')
    # admin.add_view(ModelView(Auth, db.session, name='用户'))
    admin.add_view(ArticleView(Article, db.session,name='博客列表'))
    admin.add_view(ModelView(Auth, db.session, name='用户列表'))
    # admin.add_view(AdminCreateBlogView(name='发表博客',endpoint='create'))

@login_manager.user_loader
def get_user(uid):
    return Auth.query.get(int(uid))