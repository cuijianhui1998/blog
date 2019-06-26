from flask import render_template

from . import web

@web.route('/hhhh')
def hhhhh():
    return render_template('test/test1.html')