#!/usr/bin/python3
"""
Login Form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """Login form to handle user input in signIn"""
    email = StringField('Email',
                        validator=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validator=[DataRequired(), Length(min=7, max=20)])
