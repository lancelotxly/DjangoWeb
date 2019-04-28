from django.forms import *

wid_01 = widgets.TextInput()
wid_02 = widgets.PasswordInput()

class MyForm(forms.Form):
    name = fields.CharField(
        max_length=20,
        widget=wid_01,
        error_messages={
            'required':'用户名不能为空',
            'max_length':'用户名过长'
        }
    )
    pwd = fields.CharField(
        max_length=32,
        widget=wid_02,
    )
    r_pwd = fields.CharField(
        max_length=32,
        widget=wid_02
    )
    email = fields.EmailField(
        widget=wid_01
    )
    tel = fields.CharField(
        widget=wid_01
    )
