from sqlalchemy.sql.expression import func
from sqlalchemy import and_
from app.models import Article

def _new():
    blogs = Article.query.order_by(Article.create_time.desc()).limit(3)
    return blogs

def _link(id):
    about = Article.query.get(id)
    blogs = Article.query.filter(and_(Article.select==about.select,Article.id!=about.id)).oder_by(func.rand()).limit(5)
    return blogs

def _twitter():
    #等添加了用户后设置用户喜好,添加参数key
    blogs = Article.query.oder_by(func.rand()).limit(6)
    return blogs

def right_show(id):
    return (_new(),_link(id),_twitter())


