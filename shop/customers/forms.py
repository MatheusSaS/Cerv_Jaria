from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register
class CustomerRegisterForm(FlaskForm):
    name = StringField('Nome: ',[validators.DataRequired()])
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired(), validators.EqualTo('confirm',
    message='Both password must match!')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    profile = FileField('Profile',validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only please')])
    
    def validate_username(self,username):
        if Register.query.filter_by(username=username.data).first():
            raise validators.ValidationError('Usuario ja existe!')
    
    def validate_email(self,email):
        if Register.query.filter_by(email=email.data).first():
            raise validators.ValidationError('Email ja existe!')

class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])
    


    