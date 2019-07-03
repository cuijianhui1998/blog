from werkzeug.exceptions import HTTPException
from flask import render_template

class UnSupportedException(HTTPException):
    code = 406
    description = "存在非法字符"
    def get_body(self, environ=None):
        return render_template('error/406.html')
