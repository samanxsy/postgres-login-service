import os
from flask import Flask, render_template, redirect
from flask_talisman import Talisman


app = Flask("LoginSystem", static_folder='./app/static', template_folder='./app/templates')
app.secret_key = os.environ.get("SESSION_KEY")

csp = {
    'default-src': '\'self\'',
    'img-src': '*',
    'navigate-to': '*',
    'script-src': '\'self\' https://code.jquery.com/jquery-3.6.0.min.js',
    'style-src': '\'self\''
}

talisman = Talisman(
    app,
    content_security_policy=csp,
    force_https=False,  # Set to True in production
    strict_transport_security=True,
    session_cookie_secure=True,
    session_cookie_http_only=True,
    frame_options="DENY",
)


@app.route("/")
def home():
    """
    Home page
    """

    return redirect("/signup")


@app.route("/signup")
def signup():
    """
    Sign Up Portal
    """

    return render_template("signup.html")


@app.route("/login")
def login():
    """
    Login Portal
    """

    return render_template("login.html")


@app.route("/profile")
def profile():
    """
    Users Profile Timeline
    """

    return render_template("profile.html")
