#!/usr/bin/python3
"""
User SignUp, SignIn
"""

from flask import Flask, render_template, request, url_for, redirect
import requests
from .registration_form import RegistrationForm
from .login_form import LoginForm



app = Flask(__name__)
app.secret_key = "985e88a9260210904300cd5d50558197"


@app.route("/", strict_slashes=False, methods=["GET"])
def home_page():
    return render_template("home.html", title="Home")


@app.route("/signup", strict_slashes=False, methods=["GET"])
def sign_up():
    form = RegistrationForm()
    return render_template("signup.html", title="SignUp", form=form)


@app.route("/signin", strict_slashes=False, methods=["GET"])
def signin():
    form = LoginForm()
    return render_template("signin.html", title="SignIn", form=form)


@app.route("/signup", strict_slashes=False, methods=["POST"])
def sign_up_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {}
        data["username"] = request.form["username"]
        data["email"] = request.form["email"]
        data["password"] = request.form["password"]
        data["first_name"] = request.form["first_name"]
        data["last_name"] = request.form["last_name"]
        data["role"] = "user"

        res = requests.post("http://localhost:5001/api/v1/user", json=data)
        
        if res.status_code == 201:
            return redirect(url_for('home_page'))

        else:
            return res.text
    else:
        return render_template("signup.html", title="Signup", form=form)


@app.route("/signin", strict_slashes=False, methods=["POST"])
def signin_action():
    form = LoginForm()
    if form.validate_on_submit():
        data = {}
        data["email"] = request.form["email"]
        data["password"] = request.form["password"]

        return redirect(url_for('home_page'))
    else:
        return render_template("signin.html", title="signin", form=form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
