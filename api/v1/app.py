#!/usr/bin/python3

from .views import app_views
from flask import Flask, request, make_response
from json import dumps

app = Flask(__name__)

app.register_blueprint(app_views)

@app.route("/signup", strict_slashes=False, methods=["POST"])
def recived():
    try:
        data = request.get_json()
    except Exception:
        return make_response("Error", 400)

    res = make_response(dumps(data, indent=4), 201)
    res.headers["content-type"] = "application/json"
    return res

@app.route("/")
def ok():
    return "hello from app\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")
