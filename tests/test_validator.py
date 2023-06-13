import unittest
from backend.validator import PasswordValidator, valid_email, valid_username


class PasswordValidatorTests(unittest.TestCase):
    def test_is_strong(self):
        # STRONG
        self.assertTrue(PasswordValidator.is_strong("StrongPass123!$"))

        # NOT STRONG
        self.assertFalse(PasswordValidator.is_strong("weakpassword"))
        self.assertFalse(PasswordValidator.is_strong("password123"))
        self.assertFalse(PasswordValidator.is_strong("Password!"))
        self.assertFalse(PasswordValidator.is_strong("Strongpass"))

    def test_has_minimum_length(self):
        # LONG ENOUGHT
        self.assertTrue(PasswordValidator.has_minimum_length("password123", length=8))

        # NOT LONG ENOUGH
        self.assertFalse(PasswordValidator.has_minimum_length("pass", length=8))

    def test_has_uppercase_letter(self):
        # HAS UPPERCASE
        self.assertTrue(PasswordValidator.has_uppercase_letter("Password123!"))
        # NO UPPERCASE
        self.assertFalse(PasswordValidator.has_uppercase_letter("password123!"))

    def test_has_lowercase_letter(self):
        # HAS LOWERCASE INCLUDED
        self.assertTrue(PasswordValidator.has_lowercase_letter("Password123!"))
        # NO LOWERCASE INCLUDED
        self.assertFalse(PasswordValidator.has_lowercase_letter("PASSWORD123!"))

    def test_has_digit(self):
        # HAS DIGIT INCLUDED
        self.assertTrue(PasswordValidator.has_digit("Password123!"))
        # NO DIGIT INCLUDED
        self.assertFalse(PasswordValidator.has_digit("Password!"))

    def test_has_special_character(self):
        # WITH SPECIALS
        self.assertTrue(PasswordValidator.has_special_character("Password123!"))
        self.assertTrue(PasswordValidator.has_special_character("S4$w4sd!"))
        self.assertTrue(PasswordValidator.has_special_character("jnjka$#1!"))
        self.assertTrue(PasswordValidator.has_special_character("**sdnjn!"))

        # WITHOUT SPECIALS
        self.assertFalse(PasswordValidator.has_special_character("Password123"))


class EmailValidationTests(unittest.TestCase):
    def test_valid_email(self):
        # VALID EMAILS
        self.assertTrue(valid_email("user@example.com"))
        self.assertTrue(valid_email("john.doe@example.co.uk"))
        self.assertTrue(valid_email("john-doe@example.co.uk"))
        self.assertTrue(valid_email("john_doe@example.com"))

        # INVALID EMAILS
        self.assertFalse(valid_email("invalid.email"))
        self.assertFalse(valid_email("user@example"))


class UsernameValidationTests(unittest.TestCase):
    def test_valid_username(self):
        # VALID USERNAMES
        self.assertTrue(valid_username("john_doe123"))
        self.assertTrue(valid_username("user_name"))
        self.assertTrue(valid_username("PTC"))

        # INVALID USERNAMES
        self.assertFalse(valid_username("123456"))
        self.assertFalse(valid_username("hi"))
