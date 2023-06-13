import re


class PasswordValidator:
    @staticmethod
    def is_strong(password):
        """Checks if the password meets the strong password requirements."""
        return (
            PasswordValidator.has_minimum_length(password)
            and PasswordValidator.has_uppercase_letter(password)
            and PasswordValidator.has_lowercase_letter(password)
            and PasswordValidator.has_digit(password)
            and PasswordValidator.has_special_character(password)
        )

    @staticmethod
    def has_minimum_length(password, length=8):
        """Checks if the password has the minimum required length."""
        return len(password) >= length

    @staticmethod
    def has_uppercase_letter(password):
        """Checks if the password contains at least one uppercase letter."""
        return re.search(r"[A-Z]", password) is not None

    @staticmethod
    def has_lowercase_letter(password):
        """Checks if the password contains at least one lowercase letter."""
        return re.search(r"[a-z]", password) is not None

    @staticmethod
    def has_digit(password):
        """Checks if the password contains at least one digit."""
        return re.search(r"\d", password) is not None

    @staticmethod
    def has_special_character(password):
        """Checks if the password contains at least one special character."""
        return re.search(r"[\!\@\#\$\%\^\&\*\(\)\-\=\_\+\{\}\[\]\|\;\\\:\"\<\>\,\.\/\?]", password) is not None


def valid_email(email):
    """Validates the email format"""
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(email_regex, email):
        return True
    else:
        return False


def valid_username(username):
    """Validates the username"""
    username_regex = r'^(?=.*[a-zA-Z])[a-zA-Z0-9_]{3,}$'

    if re.match(username_regex, username):
        return True
    else:
        return False
