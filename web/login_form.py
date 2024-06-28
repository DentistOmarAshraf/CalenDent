#!/usr/bin/python3
"""
Login Form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """Login form to handle user input in signIn"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=7, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Sign In")
