from flask import render_template,request,url_for,redirect,flash
from flask_login import login_user

from . import web
from app.forms.auth import AuthForm
from app.model.auth import Auth


@web.route('/login',methods=['GET','POST'])
def login():
    form = AuthForm(request.form)
    if request.method=='POST' and form.validate():
        user = Auth.query.filter_by(username=request.form.get('username')).first()
        if user and user.password==request.form.get('password'):
            login_user(user)
            next = request.args.get('next')
            print(next)
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('密码错误')
    else:
        flash('不存在该用户')

    return render_template('auth/login.html',form=form)