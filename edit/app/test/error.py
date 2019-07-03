from flask import render_template,abort
import sqlalchemy
from app.error.sql_error import UnSupportedException
from . import test

@test.route('/413')
def large_file():
    abort(413)

@test.route('/406')
def unsupported():
    raise UnSupportedException()
