#!/usr/bin/python3

from .views import app_views
from flask import Flask, request, make_response
from json import dumps
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exceptions):
    """remove session each request"""
    storage.close()


@app.errorhandler(404)
def handle(error):
    """Error Handle if route is not found"""
    data = {"error": "Not Found"}
    res = make_response(dumps(data, indent=4), 404)
    res.headers["Content-type"] = "application/json"
    return res


if __name__ == "__main__":
    """Start App"""
    app.run(host="0.0.0.0", port="5001", threaded=True)
