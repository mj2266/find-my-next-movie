from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import  DataRequired,Length,Email, EqualTo

class Registration(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    Animation = BooleanField('Animation', false_values=None)

    Comedy = BooleanField('Comedy', false_values=None)

    Children = BooleanField('Children', false_values=None)

    Romance = BooleanField('Romance', false_values=None)

    Adventure = BooleanField('Adventure', false_values=None)

    Drama = BooleanField('Drama', false_values=None)

    Action = BooleanField('Action', false_values=None)

    Crime = BooleanField('Crime', false_values=None)

    submit = SubmitField('Sign up')

# login form

class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login up')


class SearchBar(FlaskForm):
    search = StringField('Search',
                         validators=[DataRequired(),])
