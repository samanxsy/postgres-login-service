import os
import unittest
from flask import Flask
from app.common import status
from app.server import home, signup, login, profile


class BaseTest(unittest.TestCase):
    """Base test class for all tests in this module."""
    def setUp(self):
        self.app = Flask("LoginSystem", static_folder="./app/static", template_folder="./app/templates")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app.add_url_rule("/login", "login", login)
        self.app.add_url_rule("/profile", "profile", profile)
        self.app.add_url_rule("/signup", "signup", signup)
        self.app.secret_key = os.environ.get("SESSION_KEY")


    def test_signup_rout(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Signup</title>", response.data)


    def test_login_rout(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Login</title>", response.data)


    def test_profile_rout(self):
        response = self.client.get("/profile")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Profile</title>", response.data)
