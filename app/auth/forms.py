from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField,BooleanField,SubmitField, ValidationError
from wtforms.validators import Required,Email,EqualTo, Length
from ..models import User

class RegistrationForm(FlaskForm):
    # .......
    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
 
            raise ValidationError('That username is taken')

# registration/signup form
class RegistrationForm(FlaskForm):
    first_name = StringField('first name', validators=[Required(), Length(min=3, max=16)])
    last_name = StringField('last name', validators=[Required(), Length(min=3, max=16)])
    email = StringField('Email Address',validators=[Required(),Email()])
    username = StringField('Username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Password',validators = [Required()])

# login form
class LoginForm(FlaskForm):
    email = StringField('Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')

