from flask import Flask, render_template, request, session
from flask_talisman import Talisman


app = Flask("YourO News", static_folder='./app/static', template_folder='./app/templates')
app.secret_key = "A very secret key" #  Set a secret key for session cookies

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
    force_https=False,  #  Set to True in production
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

    return render_template("home.html")
