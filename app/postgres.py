import os
import psycopg2
import hashlib


connection = psycopg2.connect(
    host="db",
    port=5432,
    dbname="postgres",
    user="postgres",
    password=os.environ.get("POSTGRES_PASSWORD")
)


def register_user(first_name, last_name, email, username, password, date_of_birth):
    """
    This function will take user data, hashes the password, and registers the data in the postgres database
    """

    # Hashing the password
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()

    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO users (first_name, last_name, email, username, password, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s)""", (first_name, last_name, email, username, hashed_pass, date_of_birth)
            )
        connection.commit()

    except psycopg2.errors.UniqueViolation as error:
        if "email" in str(error):
            return "A user with this email has already been registrated"

        elif "username" in str(error):
            return "The Username is taken"

    except psycopg2.Error:
        return "Something happened during singing up, Try Again later"

    finally:
        cursor.close()


def user_data_retrieval(username, password):
    """
    This function will take username and password as arguments, and returns True if the data matches with the databasee
    """
    if password:
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()

        cursor = connection.cursor()
        cursor.execute(
            """SELECT * FROM users
            WHERE username = %s AND password = %s""", (username, hashed_pass)
        )
        return cursor.fetchone()

# # DATABASE CREATION FUNCTION
#def create_database():
#    """
#    This function will create the database IF it does not already exist
#    """
#    try:
#        cursor = connection.cursor()
#        # Creating The Table
#        cursor.execute(
#            """CREATE TABLE IF NOT EXISTS users (
#                id BIGSERIAL PRIMARY KEY NOT NULL,
#                first_name VARCHAR(255) NOT NULL,
#                last_name VARCHAR(255) NOT NULL,
#                email VARCHAR(255) UNIQUE NOT NULL,
#                username VARCHAR(255) UNIQUE NOT NULL,
#                password VARCHAR(255) NOT NULL,
#                date_of_birth DATE NOT NULL
#            )"""
#        )
#        connection.commit()
#        print("Database Created Succussfully")
#
#    except psycopg2.Error:
#        print("An error occured during database creation")
#
#    finally:
#        cursor.close()
