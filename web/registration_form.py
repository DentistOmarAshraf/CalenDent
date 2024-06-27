#!/usr/bin/python3
"""
Registration Form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    """Registration form to handle user input in signUp"""
    username = StringField('Username',
                           validator=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validator=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validator=[DataRequired(), Length(min=7, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validator=[DataRequired(), EqualTo('password')])
