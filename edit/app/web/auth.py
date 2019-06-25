from flask import render_template,request,url_for,redirect,flash
from flask_login import login_user,login_required,logout_user

from . import web
from app.forms import AuthForm,RegisterForm,MessageForm
from app.models import Auth,db,Message

@web.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        user = Auth.query.filter_by(email=request.form.get('email')).first()
        if not user:
            auth = Auth()
            with db.submit_data():
                auth.setter_data(request.form)
                db.session.add(auth)
            return redirect(url_for('web.login'))
    return render_template('auth/register.html')


@web.route('/login',methods=['GET','POST'])
def login():
    form = AuthForm(request.form)
    if request.method=='POST' and form.validate():
        user = Auth.query.filter_by(username=request.form.get('username')).first_or_404()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('密码错误')
    else:
        flash('不存在该用户')

    return render_template('auth/login.html',form=form)

@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@web.route('/say_me',methods=['GET','POST'])
def say_me():
    '''
    留言
    '''
    leave_messages = Message.query.all()
    form = MessageForm(request.form)
    if request.method=='POST' and form.validate():
        with db.submit_data():
            message = Message()
            message.leave_message = request.form.get('leave_message')
            db.session.add(message)
        return redirect(url_for('web.say_me'))
    return render_template('sayme.html',form=form,leave_messages=leave_messages)