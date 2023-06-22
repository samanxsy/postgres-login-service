import os
from . import postgres
import psycopg2.errors
from datetime import timedelta
from flask_talisman import Talisman
from flask import Flask, jsonify, request, redirect, session
from .validator import PasswordValidator, valid_email, valid_username

app = Flask("LoginSystem")
app.secret_key = os.environ.get("SESSION_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

csp = {
    'default-src': '\'self\'',
    'connect-src': ['\'self\'', 'http://frontend:80'],
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

    return redirect("/signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    """
    Sign Up Portal
    """

    data = request.get_json()

    # Receiving the values
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password_confirm = data.get("password_confirm")
    date_of_birth = data.get("date_of_birth")

    if password:
        if not PasswordValidator.is_strong(password):
            backend_message = "Password is not strong enough"
            status = False
            return jsonify({"backend_message": backend_message, "status": status})
        elif password != password_confirm:
            backend_message = "Passwords do not match"
            status = False
            return jsonify({"backend_message": backend_message, "status": status})

    if email:
        if not valid_email(email):
            backend_message = "Email must have a correct format"
            status = False
            return jsonify({"backend_message": backend_message, "status": status})

    if username:
        if not valid_username(username):
            backend_message = "The username is not valid"
            status = False
            return jsonify({"backend_message": backend_message, "status": status})

    if all([first_name, last_name, email, username, password, date_of_birth]):
        try:
            postgres.register_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                date_of_birth=date_of_birth
            )
            backend_message = "Account created Successfully! Tap Login Here."
            status = True
            return jsonify({"backend_message": backend_message, "status": status})

        except psycopg2.errors.UniqueViolation as error:
            if "email" in str(error):
                backend_message = "A user with this email has already been registrated."
                status = False
                return jsonify({"backend_message": backend_message, "status": status})

            elif "username" in str(error):
                backend_message = "Username already Taken."
                status = False
                return jsonify({"backend_message": backend_message, "status": status})

        except psycopg2.Error:
            backend_message = "Something happened during singing up, Try Again later"
            status = False
            return jsonify({"backend_message": backend_message, "status": status})

    else:
        backend_message = "All fields are required"
        status = False
        return jsonify({"backend_message": backend_message, "status": status})


@app.route("/login", methods=["POST"])
def login():
    """
    Login Portal
    """

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Validating the credentials
    try:
        if username and password:
            if postgres.user_auth(
                username=username,
                password=password
            ):
                session["username"] = username
                status = True
                return jsonify({"username": username, "status": status})

            else:
                backend_message = "Invalid username or password"
                status = False
                return jsonify({"backend_message": backend_message, "status": status})
        else:
            backend_message = "Username and Password are required"
            status = False
            return jsonify({"backend_message": backend_message, "status": status})

    except psycopg2.Error:
        backend_message = "Something happened during login, Try Again later"
        status = False
        return jsonify({"backend_message": backend_message, "status": status})


@app.route("/auth", methods=["POST"])
def auth():
    """
    Users session check
    """
    data = request.get_json()
    username = data.get("username")

    if "username" in session and session["username"] == username:
        data = postgres.user_data_retrieval(username)
        first_name = data[1]
        last_name = data[2]
        email = data[3]
        return jsonify(
            {
                "status": True,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        )

    else:
        return jsonify({"status": False})


@app.route("/delete", methods=["POST"])
def delete_account():
    """
    This route will receive a username and deletes its corrisponding account
    """

    data = request.get_json()
    username = data.get("username")

    if "username" in session and session["username"] == username:
        postgres.delete_user(username=username)
        backend_message = "Account Deleted"
        status = True
        return jsonify({"backend_message": backend_message, "status": status})

    else:
        backend_message = "Please Login First"
        status = False
        return jsonify({"backend_message": backend_message, "status": status})


@app.route("/logout")
def logout():
    """
    Logout functionality to clear session data
    """
    session.clear()
    return redirect("/login.html")
