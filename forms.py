from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(min=-1, max=80, message='Field must not have more than 80 characters.')])
    surname = StringField('Last Name', validators=[Length(min=-1, max=100, message='Field must not have more than 100 characters.')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='Field must not have more than 200 characters.')])
    phone = StringField('Phone', validators=[Length(min=-1, max=20, message='Field must not have more than 20 characters.')])
