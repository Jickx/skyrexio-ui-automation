import os
from dotenv import load_dotenv

load_dotenv()


class UserFactory:
    @staticmethod
    def valid_user():
        email = os.getenv("VALID_USER_EMAIL")
        password = os.getenv("VALID_USER_PASSWORD")
        if not email or not password:
            raise ValueError("VALID_USER_EMAIL и/или VALID_USER_PASSWORD не заданы в .env")
        return {
            "email": email,
            "password": password
        }

    @staticmethod
    def invalid_user():
        return {
            "email": "invalid_user@example.com",
            "password": "invalid_password"
        }

    @staticmethod
    def invalid_email_user():
        return {
            "email": "notanemail",
            "password": "somepassword"
        }

    @staticmethod
    def empty_email_user():
        return {
            "email": "",
            "password": "somepassword"
        }

    @staticmethod
    def empty_password_user():
        return {
            "email": "test@example.com",
            "password": ""
        }
