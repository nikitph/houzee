from flask_security.forms import RegisterForm
from wtforms import StringField, IntegerField, Form, FieldList
from wtforms.validators import Required
from flask.ext.mongoengine.wtf import model_form


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone = StringField('Phone')


