#!/usr/bin/python3
"""
Registration Form
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequierd, Length


class Registration(FlaskForm):
    """Form to generete HTML form and validate User entires"""
    username = StringField('Username', validators=[DataRequierd(), Length(min=2])
