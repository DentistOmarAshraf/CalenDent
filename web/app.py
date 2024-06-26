#!/usr/bin/python3

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/signup", strict_slashes=False, methods=["GET"])
def sign_up():
    return render_template("signup.html")


@app.route("/signup", strict_slashes=False, methods=["POST"])
def sign_up_register():
    data = {}
    data["email"] = request.form["email"]
    data["password"] = request.form["password"]
    data["first_name"] = request.form["first_name"]
    data["last_name"] = request.form["last_name"]
    data["role"] = "user"

    res = requests.post("http://localhost:5001/api/v1/user", json=data)
        
    if res.status_code == 201:
        return res.json()

    else:
        return res.json()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
