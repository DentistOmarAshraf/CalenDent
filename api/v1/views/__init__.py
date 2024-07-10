#!/usr/bin/python3

from functools import wraps
from flask import Blueprint


API_KEY = "API_SECRET_KEY"

app_views = Blueprint("app", __name__, url_prefix="/api/v1")

def check_api_key(func):
    """WARPPER Functiont to Check that web_app is the reqest Sender"""
    @wraps(func)
    def intern_func(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return make_response(dumps({"error": "unauthorized"}), 403)
        return func(*args, **kwargs)
    return intern_func

from .user import *
from .city import *
from .neighborhood import *
from .clinic import *
from .reservation import *
