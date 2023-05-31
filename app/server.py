import os
import psycopg2.errors
from flask import Flask, render_template, request, redirect, session, url_for
from flask_talisman import Talisman
from datetime import timedelta
from . import postgres


app = Flask("LoginSystem", static_folder='./app/static', template_folder='./app/templates')
app.secret_key = os.environ.get("SESSION_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Sign Up Portal
    """

    # Receiving the values
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        date_of_birth = request.form.get("date_of_birth")

        if username:
            try:
                postgres.register_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    date_of_birth=date_of_birth
                )
                success_message = "Account created Successfully! Tap Login Here."
                return render_template("signup.html", success_message=success_message)

            except psycopg2.errors.UniqueViolation as error:
                if "email" in str(error):
                    error_message = "A user with this email has already been registrated."
                    return render_template("signup.html", error_message=error_message)

                elif "username" in str(error):
                    error_message = "Username already Taken."
                    return render_template("signup.html", error_message=error_message)

            except psycopg2.Error:
                error_message = "Something happened during singing up, Try Again later"
                return render_template("signup.html", error_message=error_message)

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login Portal
    """
    if request.method == "POST":
        # Receiving the Values
        username = request.form.get("username")
        password = request.form.get("password")

        # Validating the credentials
        if username:
            if postgres.user_data_retrieval(
                username=username,
                password=password
            ):
                session["username"] = username
                return redirect(url_for("profile", username=username))

            else:
                error_message = "Invalid username or password"
                return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    """
    Users Profile Timeline
    """

    if "username" in session and session["username"] == username:
        return render_template("profile.html", username=username)

    return redirect("/login")


@app.route("/logout")
def logout():
    """
    Logout functionality to clear session data
    """
    session.clear()
    return redirect("/login")
