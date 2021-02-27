from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Usuario', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Senha', [validators.DataRequired()])
    accept_tos = BooleanField('Declaro que tenho mais de 18 anos', [validators.DataRequired()])
    
class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Senha', [validators.DataRequired()])