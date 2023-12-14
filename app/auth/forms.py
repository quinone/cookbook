from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.model import User

"""This script contains all authentication forms for the CookBook web application"""


class SignUpForm(FlaskForm):
    # email is required and must be valid
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    # Username is required and must not contain special characters
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots'
               ' or underscores')])
    # Password is validated to ensure OWASP compliant level of complexity
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(1, 128),
                                                     EqualTo('confirm_password', message='Passwords must match.'),
                                                     Regexp(
                                                         regex="^(?=.*[a-z])(?=.*[A-Z])"
                                                               "(?=.*\\d)(?=.*[@$!%*?&])"
                                                               "[A-Za-z\\d@$!%*?&]{10,}$",
                                                         message="Password must be at least 10 characters long,"
                                                                 " contain at least one uppercase letter, "
                                                                 "one lowercase letter, "
                                                                 "one digit, and one special character.")
                                                     ])
    # Password is entered twice to help guard against typos
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    # Function to check DB for email
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    # Function to check DB for username
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset password')


class RenewPasswordForm(FlaskForm):
    # Password is validated to ensure OWASP compliant level of complexity
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(1, 128),
                                                     EqualTo('confirm_password', message='Passwords must match.'),
                                                     Regexp(
                                                         regex="^(?=.*[a-z])(?=.*[A-Z])"
                                                               "(?=.*\\d)(?=.*[@$!%*?&])"
                                                               "[A-Za-z\\d@$!%*?&]{10,}$",
                                                         message="Password must be at least 10 characters long,"
                                                                 " contain at least one uppercase letter, "
                                                                 "one lowercase letter, "
                                                                 "one digit, and one special character.")
                                                     ])
    # Password is entered twice to help guard against typos
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Confirm new password')


class ChangePasswordForm(FlaskForm):
    # Old password entered to prevent session hijacking
    old_password = PasswordField('Enter current password', validators=[DataRequired()])
    # Password is validated to ensure OWASP compliant level of complexity
    new_password = PasswordField('Password', validators=[DataRequired(),
                                                         Length(1, 128),
                                                         EqualTo('confirm_password', message='Passwords must match.'),
                                                         Regexp(
                                                             regex="^(?=.*[a-z])(?=.*[A-Z])"
                                                                   "(?=.*\\d)(?=.*[@$!%*?&])"
                                                                   "[A-Za-z\\d@$!%*?&]{10,}$",
                                                             message="Password must be at least 10 characters long,"
                                                                     " contain at least one uppercase letter, "
                                                                     "one lowercase letter, "
                                                                     "one digit, and one special character.")
                                                         ])
    # Password is entered twice to help guard against typos
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Confirm new password')
