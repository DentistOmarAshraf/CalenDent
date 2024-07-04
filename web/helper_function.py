#!/usr/bin/python3
"""
Helper Function
"""

import jwt
from datetime import datetime
from datetime import timedelta
from flask import request, redirect


def create_token(data, key, expire_date=None):
    """JWT token creation with expiration data"""
    payload = {
        "user_id" : data["id"],
        "exp" : datetime.utcnow() + (expire_date or timedelta(hours=1))
        }
    token = jwt.encode(payload, key, algorithm="HS256")
    return token


def decode_token(token, key):
    """JWT token decode"""
    try:
        to_ret = jwt.decode(token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Signature has expired")

    return to_ret
