#!/usr/bin/env python3
"""
    This Module contains the authentication api
"""
from flask import request
from api.v1.views import app_views
from typing import List, TypeVar


class Auth:
    """
        This class is used to manage the API authentication

        Methods:
          - require_auth: This is the require_auth method
          - authorization_header:
          - current_user:
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            This is the require_auth method

            Arguments:
              - path: the paths
              - excluded_path: The excluded path

            Return:
              - True if path is None, True if excluded_paths is None
                or empty, False if path is in excluded_paths
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths is []:
            return True
        if path[-1] != "/":
            path = "{}/".format(path)
        if path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
            This Method returns the authorization header or None is
            request is None
        """
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
            This method returns None
        """
        return None
