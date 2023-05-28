import unittest
from unittest import mock
from app import postgres

class PostgresTestCase(unittest.TestCase):

    @mock.patch('app.postgres.connection')
    def test_register_user(self, mock_connection):
        # Mock the connection object and cursor
        mock_cursor = mock_connection.cursor.return_value

        # Test case 1: Register a new user
        postgres.register_user("Saman", "xsy", "Saman@example.com", "Samanxsy", "password123", "1990-01-01")
        mock_cursor.execute.assert_called_once()

        # Test case 2: Register a user with an existing email
        mock_cursor.execute.reset_mock()
        mock_cursor.execute.side_effect = [Exception('A user with this email has already been registered')]

        with self.assertRaises(Exception) as context:
            postgres.register_user("Jane", "Smith", "Saman@example.com", "janesmith", "password456", "1992-02-02")

        self.assertEqual(str(context.exception), 'A user with this email has already been registered')
        mock_cursor.execute.assert_called_once()

        # Test case 3: Register a user with an existing username
        mock_cursor.execute.reset_mock()
        mock_cursor.execute.side_effect = [Exception('The Username is taken')]

        with self.assertRaises(Exception) as context:
            postgres.register_user("Jane", "Smith", "jane@example.com", "Samanxsy", "password789", "1994-03-03")

        self.assertEqual(str(context.exception), 'The Username is taken')
        mock_cursor.execute.assert_called_once()

    @mock.patch('app.postgres.connection')
    def test_user_data_retrieval(self, mock_connection):
        # Mock the connection object and cursor
        mock_cursor = mock_connection.cursor.return_value

        # Test case 1: Retrieve user data with valid credentials
        mock_cursor.fetchone.return_value = ('Saman', 'xsy', 'Saman@example.com', 'Samanxsy', 'hashed_password', '1990-01-01')
        user = postgres.user_data_retrieval("Samanxsy", "password123")

        self.assertEqual(user, ('Saman', 'xsy', 'Saman@example.com', 'Samanxsy', 'hashed_password', '1990-01-01'))
        mock_cursor.execute.assert_called_once()

        # Test case 2: Retrieve user data with invalid credentials
        mock_cursor.fetchone.return_value = None
        user = postgres.user_data_retrieval("Samanxsy", "wrongpassword")

        self.assertIsNone(user)
