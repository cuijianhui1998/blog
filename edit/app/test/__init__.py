from flask import Blueprint

test = Blueprint('test',__name__,url_prefix='/test')

from app.test import error