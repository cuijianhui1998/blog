from wtforms.validators import ValidationError

def field_allow(form,field):
    print("执行一下这里啊")
    allow_later=['.jpg','.png','.gif','ico']
    if field.data.filename[-4:] not in allow_later:
        raise ValidationError("the file suffix must be jpg png gif or ico,not is {}".format(field.data.filename[-3:]))