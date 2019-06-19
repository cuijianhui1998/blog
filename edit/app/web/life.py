from flask import render_template

from . import web

@web.route('/life')
def life_all():
    '''
    记录生活
    '''
    return render_template('list.html')

@web.route('/life/notes')
def life_notes():
    '''
    记录生活
    '''
    return render_template('list.html')

@web.route('/life/photo')
def life_photo():
    '''
    记录生活
    '''
    return render_template('share.html')