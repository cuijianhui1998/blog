from flask_login import UserMixin
from sqlalchemy import Column,String,Integer

from app.model.base import Base

class Auth(Base,UserMixin):
    __tablename__ = 'auth'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20))
    password = Column(String(20))


