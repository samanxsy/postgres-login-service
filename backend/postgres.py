import os
import psycopg2
import psycopg2.errors
import hashlib


def database_connection():
    """
    Establishes a connection to the PostgreSQL database.
    """
    connection = psycopg2.connect(
        host="db",
        port=5432,
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("POSTGRES_PASSWORD")
    )

    return connection


def hash_password(password, salt):
    """
    Hashes the provided password using SHA-256 algorithm with salting.
    """
    hashed_pass = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100000
    ).hex()

    return hashed_pass


def register_user(first_name, last_name, email, username, password, date_of_birth):
    """
    This function will take user data, hashes the password, and registers the data in the postgres database
    """
    # Forcing NOT NULL constraint for all
    input = [first_name, last_name, email, username, password, date_of_birth]
    if any(value == "" for value in input):
        raise psycopg2.errors.NotNullViolation("Fields cannot be empty")

    salt = str(os.urandom(16).hex())
    hashed_pass = hash_password(password, salt)

    connection = database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO users (first_name, last_name, email, username, password, salt, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""", (first_name, last_name, email, username, hashed_pass, salt, date_of_birth)
        )
    connection.commit()

    cursor.close()
    connection.close()


def user_data_retrieval(username, password):
    """
    This function will take username and password as arguments, and returns True if the data matches with the databasee
    """
    connection = database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """SELECT * FROM users
        WHERE username = %s""", (username,)
    )
    result = cursor.fetchone()

    if result:
        stored_hashed_pass = result[5]
        salt = result[6]

        hashed_pass = hash_password(password, salt)

        if stored_hashed_pass == hashed_pass:
            cursor.execute(
                """SELECT * FROM users
                WHERE username = %s AND password = %s""", (username, hashed_pass)
            )
            user_data = cursor.fetchone()
            cursor.close()
            connection.close()

            return user_data

    cursor.close()
    connection.close()

    return None


def delete_user(username):
    """
    This function deletes the user from database
    """
    connection = database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """DELETE FROM users
        WHERE username = %s""", (username,)
    )
    connection.commit()

    cursor.close()
    connection.close()
