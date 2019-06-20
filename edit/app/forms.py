from wtforms import Form,StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Optional
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


class SearchForm(Form):
    keyboard = StringField(validators=[DataRequired(),])
    def validate_keyboard(self,field):
        #设置最长的检索字符
        if len(field.data)>20:
            field.data = field.data[:20]