from flask import render_template

from . import web

@web.route('/say_me')
def say_me():
    '''
    留言
    '''
    return render_template('sayme.html')