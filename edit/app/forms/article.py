from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Length,DataRequired,Optional,ValidationError
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





