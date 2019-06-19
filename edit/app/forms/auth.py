from wtforms import Form,StringField,PasswordField
from wtforms.validators import DataRequired


class AuthForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])