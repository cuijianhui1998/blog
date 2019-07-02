from datetime import datetime
import random
from contextlib import contextmanager

from werkzeug.security import generate_password_hash,check_password_hash
import bleach
from markdown import markdown
from flask_login import UserMixin
from sqlalchemy import Column,String,Integer,Text,Boolean,DateTime,ForeignKey
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy



class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def submit_data(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    create_time = Column(DateTime)
    def __init__(self):
        self.create_time = datetime.utcnow()

    def setter_data(self,obj):
        for key,value in obj.items():
            if hasattr(self,key):
                setattr(self,key,value)

class Auth(Base,UserMixin):
    __tablename__ = 'auth'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),unique=True)
    email = Column(String(50),unique=True)
    _password = Column('password',String(100))

    articles = db.relationship('Article',back_populates='auth')

    comments = db.relationship('Comment',back_populates='auth')

    replys = db.relationship('Reply',back_populates='auth')

    thumbs = db.relationship('Thumb',back_populates='auth')


    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,value):
        self._password = generate_password_hash(value)
    def check_password(self,value):
        return check_password_hash(self._password,value)

class Tips(Base):
    __tablename__ = 'tips'
    id = Column(Integer,primary_key=True,autoincrement=True)
    tip = Column(String(200),unique=True)

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50))
    leave_message = Column(Text)

    def __init__(self):
        super().__init__()
        self.name ='用户'+''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789',8))
class Comment(Base):
    # 评论
    __tablename__ = 'comment'
    id = Column(Integer,primary_key=True,autoincrement=True)
    content = Column(String(100))

    article_id = Column(Integer,ForeignKey('article.id'))
    article = db.relationship('Article',back_populates='comments')

    auth_id = Column(Integer,ForeignKey('auth.id'))
    auth = db.relationship('Auth', back_populates='comments')

    replys = db.relationship('Reply',back_populates='comment')

class Thumb(Base):
    __tablename__ = 'thumb'
    id = Column(Integer,primary_key=True,autoincrement=True)

    auth_id = Column(Integer,ForeignKey('auth.id'))
    auth = db.relationship('Auth', back_populates='thumbs')

    article_id = Column(Integer,ForeignKey('article.id'))
    article = db.relationship('Article', back_populates='thumbs')


class Reply(Base):
    #回复
    __tablename__ = 'reply'
    id = Column(Integer,primary_key=True,autoincrement=True)
    content = Column(String(100))

    auth_id = Column(Integer,ForeignKey('auth.id'))
    auth = db.relationship('Auth', back_populates='replys')

    comment_id = Column(Integer,ForeignKey('comment.id'))
    comment = db.relationship('Comment',back_populates='replys')


class Article(Base):
    '''
    存储博客的数据类
    '''
    __tablename__ = "article"
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(128),index=True)
    body = Column(Text)
    body_html = Column(Text)
    select = Column(String(20))
    is_recommend = Column(Boolean,default=False)
    poster = Column(String(100))

    auth_id = Column(Integer, ForeignKey('auth.id'))
    auth = db.relationship('Auth',back_populates='articles')

    comments = db.relationship('Comment',back_populates='article')

    thumbs = db.relationship('Thumb',back_populates='article')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3','h4','h5','h6', 'p', 'img', 'video', 'div', 'iframe',  'br', 'span', 'hr', 'src', 'class']
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}
        config = {
            'markdown.extensions.codehilite': {
                'use_pygments': False,
                'css_class':'prettyprint linenums',
            }
        }
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html',extensions=['markdown.extensions.extra',
                                                   'markdown.extensions.codehilite',
                                                   'markdown.extensions.toc',
                                                   'markdown.extensions.attr_list',
                                                   'markdown.extensions.fenced_code',
                                                   'markdown.extensions.tables',],extension_configs=config),
            tags=allowed_tags, strip=True, attributes=allowed_attrs))

    def setter_data(self,obj):
        for key,value in obj.items():
            if hasattr(self,key):
                setattr(self, key, int(value)) if key=='is_recommend' else setattr(self,key,value)

db.event.listen(Article.body, 'set', Article.on_changed_body)
