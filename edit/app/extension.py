from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from app.models import Article,Auth,db,Tips,Message
from app.lib.admin import ArticleView,MyIndexView


login_manager = LoginManager()

def login_register(app):
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'Your custom message'
    login_manager.login_message_category = 'warning'

def db_register(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def admin_register(app):
    admin = Admin(app, name='博客后台',index_view= MyIndexView(name="首页"),template_mode='bootstrap3')
    # admin.add_view(ModelView(Auth, db.session, name='用户'))
    admin.add_view(ArticleView(Article, db.session,name='博客列表'))
    admin.add_view(ModelView(Auth, db.session, name='用户列表'))
    admin.add_view(ModelView(Tips,db.session,name='小技巧'))
    admin.add_view(ModelView(Message, db.session, name='游客留言'))
    # admin.add_view(AdminCreateBlogView(name='发表博客',endpoint='create'))

@login_manager.user_loader
def get_user(uid):
    return Auth.query.get(int(uid))