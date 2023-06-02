import os
import unittest
import datetime
from flask import Flask
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

    def test_signup_not_strong_password(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Test",
            "last_name": "TestingTest",
            "email": "Test@test.com",
            "username": "test24",
            "password": "123456test",
            "password_confirm": "123456test",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Password is not strong enough", response.data)

    def test_signup_password_not_match(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Test",
            "last_name": "TestingTest",
            "email": "Test@test.com",
            "username": "test24",
            "password": "123123JjJj$$$",
            "password_confirm": "akjkadsj@",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Passwords do not match", response.data)

    def test_signup_invalid_email(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Test",
            "last_name": "TestingTest",
            "email": "Test@test",
            "username": "test24",
            "password": "SJHhabdjh*72$$",
            "password_confirm": "SJHhabdjh*72$$",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Email must have a correct format", response.data)

    def test_signup_invalid_username(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Test",
            "last_name": "TestingTest",
            "email": "Test@test.com",
            "username": "ty",
            "password": "SJHhabdjh*72$$",
            "password_confirm": "SJHhabdjh*72$$",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"The username is not valid", response.data)

    def test_signup_empty_fields(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "",
            "last_name": "TestingTest",
            "email": "Test@test.com",
            "username": "justtesting",
            "password": "SJHhabdjh*72$$",
            "password_confirm": "SJHhabdjh*72$$",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"All fields are required", response.data)

    def test_signup(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Saman",
            "last_name": "Saybani",
            "email": "samanxsy@sre.com",
            "username": "samanxsy",
            "password": "PassWord$212!!",
            "password_confirm": "PassWord$212!!",
            "date_of_birth": date_of_birth
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Account created Successfully!", response.data)

    def test_signup_duplicate_email(self):
        date_of_birth = datetime.date(1995, 10, 23)
        response = self.client.post("/signup", data={
            "first_name": "Saman",
            "last_name": "Saybani",
            "email": "samanxsy@sre.com",  # Duplicate email
            "username": "somethingelse",
            "password": "PassWord$212!!",
            "password_confirm": "PassWord$212!!",
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
            "username": "samanxsy",  # Duplicate username
            "password": "PassWord$212!!",
            "password_confirm": "PassWord$212!!",
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
            "password": "PassWord$212!!",
            "password_confirm": "PassWord$212!!",
            "date_of_birth": "invalid-date"  # Invalid date format
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Something happened during singing up, Try Again later", response.data)

    def test_login_route(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<title>Login</title>", response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post("/login", data={
            "username": "samanxsy",
            "password": "Pw&&hbhbsWdasdasd",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Invalid username or password", response.data)

    def test_profile_not_allowed(self):
        response = self.client.get("/profile/rahilzz")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.headers["Location"], "/login")

    def test_profile_not_allowed_sessioned(self):
        with self.client as client:
            with client.session_transaction() as session:
                session["username"] = "samanxsy"

            response = self.client.get("/profile/rahilzz")
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertEqual(response.headers["Location"], "/login")

    def test_login_with_valid_credentials(self):
        with self.client.session_transaction() as session:
            session["username"] = "samanxsy"

        response = self.client.get("/profile/samanxsy")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"<h3>Welcome back samanxsy!</h3>", response.data)

    def test_delete_user_cleanUp(self):
        username1 = "samanxsy"
        username2 = "somethingelse"
        delete_user(username1)
        delete_user(username2)
