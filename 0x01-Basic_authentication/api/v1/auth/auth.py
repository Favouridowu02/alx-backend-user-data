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
          - require_auth:
          - authorization_header:
          - current_user:
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            This method return false
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
            This Method returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            This method returns None
        """
        return None
