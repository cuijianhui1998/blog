from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import BaseQuery,Pagination as _Pagination
from contextlib import contextmanager

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

    def setter_data(self,obj):
        for key,value in obj.items():
            if hasattr(self,key):
                setattr(self,key,value)
