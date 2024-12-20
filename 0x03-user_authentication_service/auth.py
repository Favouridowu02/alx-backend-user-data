#!/usr/bin/env python3
"""
    This module contains the authorization methods
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


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

            Return: The session_id
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
            This Method is used to get the user by session_id

            Arguments:
                session_id: the session id in Str

            Return: returns the user or none
        """
        try:
            if session_id is None:
                return None
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return User
            return None
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
            This method is used to destroy a session_id by assigning
            the user session_id to None

            Arguments:
                user_id: the user id in String

            Returns: None
        """
        try:
            if user_id is None:
                return None
            user = self._db.find_user_by(id=user_id)
            if user:
                user.session_id = None
                self._db._session.commit()
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
            This Method is used to get reste password token

            Arguments:
                email: The user email (String)
            Returns: the token for the user password reset
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        reset_token = _generate_uuid()
        user.reset_token = reset_token
        self._db._session.commit()
        return reset_token
