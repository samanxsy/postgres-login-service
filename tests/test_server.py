import os
import unittest
from flask import Flask
from unittest import mock
from app.common import status
from app.server import signup, login, profile


class BaseTest(unittest.TestCase):
    """Base test class for all tests in this module."""
    def setUp(self):
        self.app = Flask("LoginSystem", static_folder="./app/static", template_folder="./app/templates")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app.secret_key = os.environ.get("SESSION_KEY")

        # URL RULES
        self.app.add_url_rule("/login", "login", login)
        self.app.add_url_rule("/profile/<username>", "profile", profile)
        self.app.add_url_rule("/signup", "signup", signup)


    def test_signup_route(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Signup</title>", response.data)


    def test_login_route(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Login</title>", response.data)


    def test_profile_route(self):
        with self.app.test_request_context("/profile/John"):
            with self.client.session_transaction() as session:
                session["username"] = "John"
            response = self.client.get("/profile/John")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(b"<title>Profile</title>", response.data)
