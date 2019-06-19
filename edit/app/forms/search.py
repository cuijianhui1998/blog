from wtforms import Form,StringField
from wtforms.validators import DataRequired

class SearchForm(Form):
    keyboard = StringField(validators=[DataRequired(),])

    def validate_keyboard(self,field):
        #设置最长的检索字符
        if len(field.data)>20:
            field.data = field.data[:20]
