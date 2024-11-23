#!/usr/bin/env python3
"""
    This module contains the authorization methods
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
        This method is used to hash the password

        Arguments:
            password: This is rthe password to be hashed

        Return: this method return the hashed password in the using
                bcrypt
    """
    b_password = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b_password, salt)

    return hashed_password


def _generate_uuid() -> str:
    """
        This Method is used to generate a uuid

        Arguments:
            None

        Return: returns the newly created uuid4
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ This method is used to initialize the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            This method is used to regiister a new user

            Arguments:
                email: This is the user email
                password: This is the user password

            Return: This returns the newly registered user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError('{} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
            This method is used to check if it is a valid user login

            Arguments:
                email: The user email(Str)
                password: The user password(Str)

            Return: returns a boolean value true if the user exists
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password = password.encode('utf-8')
                result = bcrypt.checkpw(password, user.hashed_password)
                return result
            return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """
            This method is used to create a session ID

            Arguments:
                email: The user email in Str
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id

                self._db._session.commit()
                return session_id
        except Exception:
            pass
