from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember_me = BooleanField("Remember Me")
  submit = SubmitField("Sign In")

# registration form 
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_user(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      return ValidationError("Please use a a different username!")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      return ValidationError("Please use a different Email!")


# profile edit form
class EditProfileForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  about_me = TextAreaField('About me', validators=[Length(min=0, max=160)])
  submit = SubmitField('Update')


# blog form upload
class UploadPostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  body = TextAreaField('My post', validators=[DataRequired(), Length(min=0, max=200)])
  submit = SubmitField('Submit')