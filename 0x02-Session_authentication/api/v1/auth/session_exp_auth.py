#!/usr/bin/env python3
"""
    This module contains a class SessionExpAuth that inherits from
    SessionAuth
"""
from flask import request
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuith(SessionAuth):
    """
        This Class is used to handle the session expiration
    """
    def __init_(self):
        """
            This is the initialization of the class instances
        """
        if isinstance(getenv('SESSION_DURATION'), int):
            self.session_duration = int(getenv('SESSION_DURATION'))
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
            This Method is used to handle the creation of sessions
        """
        session_id = super().create_session(self, user_id)
        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id,
                              "created_at": datetime.now()}
