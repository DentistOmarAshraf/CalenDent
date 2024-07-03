#!/usr/bin/python3
"""
Login Form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.validators import NumberRange


class ClinicForm(FlaskForm):
    """Login form to handle user input in signIn"""
    
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField('Address',
                          validators=[DataRequired(), Length(min=2, max=30)])
    visit_price = IntegerField('Visit Price',
                              validators=[DataRequired(), NumberRange(min=0, max=500)])
    time_from = TimeField('Time From')
    time_to = TimeField('To')
    submit = SubmitField("Save")
