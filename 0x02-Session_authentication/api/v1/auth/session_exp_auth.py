#!/usr/bin/env python3
"""
    This module contains a class SessionExpAuth that inherits from
    SessionAuth
"""
from flask import request
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
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
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None

        self.user_id_for_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            This method is used to handle the get user id from session_id
        """
        if type(session_id) != str:
            return None
        user_id = self.user_id_by_session_id(session_id)
        if user_id is None:
            return None
        if self.session_duration <= 1:
            return None
        if user_id.get('created_at') is None:
            return None
        time_span = timedelta(seconds=self.session_duration)
        if user_id['created_at'] + time_span < datetime.now():
            return None
        return user_id['user_id']
