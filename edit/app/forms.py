import requests
import json

from wtforms import Form,StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Optional,Email,Length,ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed

class ArticleForm(FlaskForm):
    title = StringField(validators=[DataRequired(message="你必须输入一个标题")])
    is_recommend = StringField(validators=[DataRequired(),])
    select = StringField(validators=[DataRequired(),])
    TextContent = TextAreaField(validators=[DataRequired(),])
    author = StringField(validators=[DataRequired(),])
    poster = FileField(validators=[Optional(),FileAllowed(['gif','png','jpg','ico'])])
    submit = SubmitField()


class AuthForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

class RegisterForm(AuthForm):
    email = StringField(validators=[Email(),DataRequired()])


    def validate_email(self,field):
        # 调用了第三方API验证邮箱的合法性
        url = 'https://www.mail-verifier.com/do/api?key={key}&verify={email}'.format(
            key='309F51D4A00791A82E88AF530B8B4E75',email=field.data)
        data = json.loads(requests.get(url).text)
        if data['code'] != 1:
            raise ValidationError("邮箱不合法")

class MessageForm(Form):
    leave_message = TextAreaField(validators=[DataRequired(),Length(max=400)])

class CommentForm(Form):
    comment = TextAreaField(validators=[DataRequired(),Length(max=400)])
    comment_submit = SubmitField()

class ReplyForm(Form):
    reply = TextAreaField(validators=[DataRequired(),Length(max=400)])
    reply_submit = SubmitField()

class SearchForm(Form):
    keyboard = StringField(validators=[DataRequired(),])
    def validate_keyboard(self,field):
        #设置最长的检索字符
        if len(field.data)>20:
            field.data = field.data[:20]


