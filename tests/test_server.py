import os
import unittest
import datetime
from flask import Flask, session
from app.common import status
from app.server import signup, login, profile, home
from app.postgres import delete_user


class TestServer(unittest.TestCase):
    """Base test class for all tests in this module."""
    def setUp(self):
        self.app = Flask("LoginSystem", static_folder="./app/static", template_folder="./app/templates")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app.secret_key = os.environ.get("SESSION_KEY")

        # URL RULES
        self.app.add_url_rule("/", "home", home)
        self.app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
        self.app.add_url_rule("/profile/<username>", "profile", profile)
        self.app.add_url_rule("/signup", "signup", signup, methods=["GET", "POST"])


    def test_home_redirect(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.headers["Location"], "/signup")


    def test_signup_route(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Signup</title>", response.data)


    def test_signup(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Saman",
            "last_name": "Saybani",
            "email": "samanxsy@sre.com",
            "username": "samanxsy",
            "password": "1123djnka&Pp",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Account created Successfully!", response.data)


    def test_signup_duplicate_email(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Saman",
            "last_name": "Saybani",
            "email": "samanxsy@sre.com", # Duplicate email
            "username": "somethingelse",
            "password": "1123djnka&Pp",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"A user with this email has already been registrated.", response.data)


    def test_signup_duplicate_username(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Saman",
            "last_name": "Saybani",
            "email": "somethingelse@sre.com",
            "username": "samanxsy", # Duplicate username
            "password": "1123djnka&Pp",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Username already Taken.", response.data)


    def test_signup_post_exception(self):
        response = self.client.post("/signup", data={
            "first_name": "Rahil",
            "last_name": "Moradi",
            "email": "Rahil@example.com",
            "username": "Rahilzz",
            "password": "password123",
            "date_of_birth": "invalid-date"  # Invalid date format
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Something happened during singing up, Try Again later", response.data)


    def test_login_route(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Login</title>", response.data)


    def test_delete_user_cleanUp(self):
        username1 = "samanxsy"
        username2 = "somethingelse"
        delete_user(username1)
        delete_user(username2)
