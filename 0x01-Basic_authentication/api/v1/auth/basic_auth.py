#!/usr/bin/env python3
"""
    This Module contains class BasicAuth that inherits from Auth class
"""
from api.v1.auth.auth import Auth


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
