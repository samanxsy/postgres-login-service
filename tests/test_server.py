import os
import json
import unittest
import datetime
from flask import Flask
from backend.common import status
from backend.postgres import delete_user
from backend.server import signup, login, auth, home, delete_account, logout


class TestServer(unittest.TestCase):
    """Base test class for all tests in this module."""
    def setUp(self):
        self.app = Flask("LoginSystem")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app.secret_key = os.environ.get("SESSION_KEY")

        # URL RULES
        self.app.add_url_rule("/", "home", home)
        self.app.add_url_rule("/signup", "signup", signup, methods=["POST"])
        self.app.add_url_rule("/login", "login", login, methods=["POST"])
        self.app.add_url_rule("/auth", "auth", auth, methods=["POST"])
        self.app.add_url_rule("/delete", "delete_account", delete_account, methods=["POST"])
        self.app.add_url_rule("/logout", "logout", logout)

    def test_main_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_signup_route(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_signup_not_strong_password(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Test",
                "last_name": "TestingTest",
                "email": "Test@test.com",
                "username": "test24",
                "password": "123456",
                "password_confirm": "123456",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Password is not strong enough")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_signup_password_not_match(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Test",
                "last_name": "TestingTest",
                "email": "Test@test.com",
                "username": "test24",
                "password": "123123JjJj$$$",
                "password_confirm": "akjkadsj@",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Passwords do not match")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_signup_invalid_email(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Test",
                "last_name": "TestingTest",
                "email": "Test@test",
                "username": "test24",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Email must have a correct format")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_signup_invalid_username(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Test",
                "last_name": "TestingTest",
                "email": "Test@test.com",
                "username": "ts",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "The username is not valid")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_signup_empty_fields(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "",
                "last_name": "TestingTest",
                "email": "Test@test.com",
                "username": "helloworld",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "All fields are required")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_signup(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "samanxsy@devops.com",
                "username": "samandev",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Account created Successfully! Tap Login Here.")
            status = response_data.get("status")
            self.assertEqual(status, True)

    def test_signup_duplicate_email(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "samanxsy@sre.com",
                "username": "someotherusername",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/signup",data=json.dumps({
                    "first_name": "Saman",
                    "last_name": "Saybani",
                    "email": "samanxsy@sre.com",
                    "username": "xsdw",
                    "password": "12456%mM",
                    "password_confirm": "12456%mM",
                    "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
                }), content_type='application/json')

                response_data = json.loads(response.data)
                backend_message = response_data.get("backend_message")
                self.assertEqual(backend_message, "A user with this email has already been registrated.")
                status = response_data.get("status")
                self.assertEqual(status, False)

    def test_signup_duplicate_username(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "otheremail@sre.com",
                "username": "user46",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/signup",data=json.dumps({
                    "first_name": "Saman",
                    "last_name": "Saybani",
                    "email": "just@sre.com",
                    "username": "user46",
                    "password": "12456%mM",
                    "password_confirm": "12456%mM",
                    "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
                }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Username already Taken.")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_signup_post_exception(self):
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "otheremail@sre.com",
                "username": "otherusername",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": "invalid-date"
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Something happened during singing up, Try Again later")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_login_with_valid_credentials(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "somegmail@gmail.com",
                "username": "ausername",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/login",data=json.dumps({
                    "username": "ausername",
                    "password": "12456%mM",
                }), content_type='application/json')

                response_data = json.loads(response.data)
                username = response_data.get("username")
                self.assertEqual(username, "ausername")
                status = response_data.get("status")
                self.assertEqual(status, True)

    def test_login_with_invalid_credentials(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "hello@gmail.com",
                "username": "ausername",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/login",data=json.dumps({
                    "username": "ausername",
                    "password": "asdadasdasd@asEA@3",
                }), content_type='application/json')

                response_data = json.loads(response.data)
                backend_message = response_data.get("backend_message")
                self.assertEqual(backend_message, "Invalid username or password")
                status = response_data.get("status")
                self.assertEqual(status, False)

    def test_login_without_credentials(self):
        with self.app.test_request_context():
            response = self.client.post("/login",data=json.dumps({
                "username": "ausername"
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Username and Password are required")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_auth_true_response(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "somegmail@gmail.com",
                "username": "ausername",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/login",data=json.dumps({
                    "username": "ausername",
                    "password": "12456%mM",
                }), content_type='application/json')

                with self.app.test_request_context():
                    response = self.client.post("/auth",data=json.dumps({
                        "username": "ausername"
                    }), content_type='application/json')

                    response_data = json.loads(response.data)
                    status = response_data.get("status")
                    self.assertEqual(status, True)

    def test_auth_false_response(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "somegmail@gmail.com",
                "username": "ausername",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/login",data=json.dumps({
                    "username": "ausername",
                    "password": "12456%mM",
                }), content_type='application/json')

                with self.app.test_request_context():
                    response = self.client.post("/auth",data=json.dumps({
                        "username": "samanxsy"
                    }), content_type='application/json')

                response_data = json.loads(response.data)
                status = response_data.get("status")
                self.assertEqual(status, False)

    def test_delete_route(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "somegmail@gmail.com",
                "username": "samanxsy",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/login",data=json.dumps({
                    "username": "samanxsy",
                    "password": "12456%mM"
                }), content_type='application/json')

                response_data = json.loads(response.data)
                username = response_data.get("username")
                self.assertEqual(username, "samanxsy")
                status = response_data.get("status")
                self.assertEqual(status, True)

                with self.app.test_request_context():
                    response = self.client.post("/delete",data=json.dumps({
                        "username": "samanxsy"
                    }), content_type='application/json')

                    response_data = json.loads(response.data)
                    backend_message = response_data.get("backend_message")
                    self.assertEqual(backend_message, "Account Deleted")
                    status = response_data.get("status")
                    self.assertEqual(status, True)

                    with self.app.test_request_context():
                        response = self.client.post("/login",data=json.dumps({
                            "username": "samanxsy",
                            "password": "12456%mM"
                        }), content_type='application/json')

                        response_data = json.loads(response.data)
                        backend_message = response_data.get("backend_message")
                        self.assertEqual(backend_message, "Invalid username or password")
                        status = response_data.get("status")
                        self.assertEqual(status, False)

    def test_delete_route_without_logging_in(self):
        with self.app.test_request_context():
            response = self.client.post("/delete",data=json.dumps({
                "username": "samanxsy"
            }), content_type='application/json')

            response_data = json.loads(response.data)
            backend_message = response_data.get("backend_message")
            self.assertEqual(backend_message, "Please Login First")
            status = response_data.get("status")
            self.assertEqual(status, False)

    def test_logout_route(self):
        date_of_birth = datetime.date(1995, 10, 23)
        with self.app.test_request_context():
            response = self.client.post("/signup",data=json.dumps({
                "first_name": "Saman",
                "last_name": "Saybani",
                "email": "helloxx@gmail.com",
                "username": "helloxx",
                "password": "12456%mM",
                "password_confirm": "12456%mM",
                "date_of_birth": date_of_birth.strftime('%Y-%m-%d')
            }), content_type='application/json')

            with self.app.test_request_context():
                response = self.client.post("/login",data=json.dumps({
                    "username": "helloxx",
                    "password": "12456%mM"
                }), content_type='application/json')

                response_data = json.loads(response.data)
                username = response_data.get("username")
                self.assertEqual(username, "helloxx")
                status = response_data.get("status")
                self.assertEqual(status, True)

                with self.app.test_request_context():
                    response = self.client.post("/auth",data=json.dumps({
                        "username": "helloxx"
                    }), content_type='application/json')

                    response_data = json.loads(response.data)
                    status = response_data.get("status")
                    self.assertEqual(status, True)

                    with self.app.test_request_context():
                        response = self.client.get("/logout")

                        with self.app.test_request_context():
                            response = self.client.post("/auth",data=json.dumps({
                                "username": "helloxx"
                            }), content_type='application/json')

                            response_data = json.loads(response.data)
                            status = response_data.get("status")
                            self.assertEqual(status, False)

    def test_delete_user_cleanUp(self):
        username1 = "samanxsy"
        username2 = "somethingelse"
        username3 = "ausername"
        username4 = "samandev"
        delete_user(username1)
        delete_user(username2)
        delete_user(username3)
        delete_user(username4)
