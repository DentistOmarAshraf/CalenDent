#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint("app", __name__, url_prefix="/api/v1")

from .user import *
