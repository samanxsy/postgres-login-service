import os
import unittest
import psycopg2
import psycopg2.errors
import datetime
from app.postgres import database_connection, hash_password, register_user, user_data_retrieval, delete_user


class FunctionsTest(unittest.TestCase):
    """Test cases for the postgres.py functions"""

    def test_database_connection(self):
        connection = database_connection()
        self.assertIsNotNone(connection)
        connection.close()

    def test_database_connection_invalid_credentials(self):
        with self.assertRaises(psycopg2.OperationalError):
            connection = psycopg2.connect(
                host="db",
                port=5432,
                dbname=os.environ.get("DB_NAME"),
                # file deepcode ignore NoHardcodedCredentials/test: Invalid credential for testing purposes
                user="invalid_user",
                # file deepcode ignore NoHardcodedPasswords/test: Invalid credential for testing purposes
                password="invalid_password"
            )
            connection.close()

    def test_hash_password(self):
        password = "aVerySecurePasswordIs=123456"
        salt = "somesalt"
        hashed_pass = hash_password(password, salt)
        self.assertIsNotNone(hashed_pass)
        self.assertNotEqual(hashed_pass, password)
        self.assertEqual(hash_password(password, salt), hashed_pass)

    def test_register_user_success(self):
        first_name = "Saman"
        last_name = "Saybani"
        email = "saman@saybani.com"
        username = "samansaybani"
        password = "passwordis123456"
        date_of_birth = datetime.date(1995, 10, 23)

        register_user(first_name, last_name, email, username, password, date_of_birth)

        user_data = user_data_retrieval(username, password)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data[1], first_name)
        self.assertEqual(user_data[2], last_name)
        self.assertEqual(user_data[3], email)
        self.assertEqual(user_data[4], username)
        self.assertEqual(user_data[5], hash_password(password, user_data[6]))
        self.assertEqual(user_data[7], date_of_birth)

    def test_register_user_invalid_data(self):
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            register_user("", "", "", "", "", "")

    def test_user_data_retrieval_valid(self):

        username = "samansaybani"
        password = "passwordis123456"

        user_data = user_data_retrieval(username, password)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data[4], username)
        self.assertEqual(user_data[5], hash_password(password, user_data[6]))

    def test_user_data_retrieval_invalid_credentials(self):
        username = "johndoe"
        password = "incorrect_password"

        user_data = user_data_retrieval(username, password)
        self.assertIsNone(user_data)

    def test_delete_user(self):
        username = "samansaybani"
        password = "passwordis123456"

        delete_user(username)

        user_data = user_data_retrieval(username, password)
        self.assertIsNone(user_data)
