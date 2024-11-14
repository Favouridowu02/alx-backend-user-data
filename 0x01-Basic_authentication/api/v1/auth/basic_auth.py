#!/usr/bin/env python3
"""
    This Module contains class BasicAuth that inherits from Auth class
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """
        This Class is used to handle the basic Authentication for
        the api

        Methods:
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
            Arguments:
                authorization_header: The Authorization Header
            Return:
                The Base64 part of the AUthorization header for a
                Basic Authentication or None is Authorization is None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
            Arguments:
                base64_authorization_header: The Base64 Authorization Header
            Return:
                The decoded value of a Base64 string
                base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        base64_decoded = None
        try:
            base64_decoded = base64.b64decode(base64_authorization_header,
                                              validate=True)
        except Exception as e:
            return None
        return base64_decoded.decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
            Arguments:
                decoded_base64_authorization_header:  The decoded Authorization
                header
            Return: the user name and the password or None, None
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
            This method is used to return the user object from the credentials

            Arguments:
                user_email: the user email(Str)
                user_pwd: the user password(Str)
            Returns: an instrnace of the User class based on the email and
                     the password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User()
        users.load_from_file()
        test_searched = {"email": user_email}
        users_searched = users.search(attributes=test_searched)
        if users_searched is None or users_searched == []:
            return None
        if users_searched[0].is_valid_password(user_pwd):
            return users_searched[0]
        return None
