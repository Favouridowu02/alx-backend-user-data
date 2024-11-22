#!/usr/bin/env python3
"""
    This module contains the authorization methods
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
