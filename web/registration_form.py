#!/usr/bin/python3
"""
Registration Form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    """Registration form to handle user input in signUp"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                            validators=[Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password',
                             validators=[DataRequired(), Length(min=7, max=20)])
    confirm_password = PasswordField('Confirm Password',
                       validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
