from datetime import datetime

import bleach
from markdown import markdown
from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean

from app.model.base import Base,db



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
    author = Column(String(20))
    poster = Column(String(100))
    create_time = Column(DateTime)

    def __init__(self):
        self.create_time = datetime.utcnow()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3','h4','h5','h6', 'p', 'img', 'video', 'div', 'iframe',  'br', 'span', 'hr', 'src', 'class']
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}

        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html',extensions=['markdown.extensions.extra',
                                                   'markdown.extensions.codehilite',
                                                   'markdown.extensions.toc',]),
            tags=allowed_tags, strip=True, attributes=allowed_attrs))

    def setter_data(self,obj):
        for key,value in obj.items():
            if hasattr(self,key):
                setattr(self, key, int(value)) if key=='is_recommend' else setattr(self,key,value)

db.event.listen(Article.body, 'set', Article.on_changed_body)