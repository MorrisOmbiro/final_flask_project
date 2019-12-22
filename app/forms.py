from wtforms import StringField, SubmitField, SelectField, validators, PasswordField, TextAreaField
from wtforms.validators import Regexp, Optional, Required, Length, EqualTo, ValidationError
from flask_wtf import Form
from string import *
from app import app
from app.models import *
import re

class LoginForm(Form):
    username = StringField('username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                         'Usernames must have only letters, ''numbers, dots or underscores')])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Log In')


class RegisterForm(Form):
    username = StringField('username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                            'Usernames must have only letters, ''numbers, dots or underscores')])
    password = PasswordField('password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('confirm password', validators=[Required()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That user name is taken, please select a new one')

class PasswordForm(Form):
    password = PasswordField('new password', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                         'Usernames must have only letters, ''numbers, dots or underscores')])
    submit = SubmitField('Reset')

class PostForm(Form):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    #Regexp(regex , 0, 'Input valid URL')
    img_url = StringField('img_url', validators=[Required()])
    title = StringField('img_title', validators=[Required()])
    submit = SubmitField('Post')


class CommentForm(Form):
    comment = TextAreaField('comment', validators=[Required()])
    submit = SubmitField('Post')