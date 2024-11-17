#!/usr/bin/env python3
"""
    This Module contains the SessionAuth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
        This class inherits from the Auth class and would be updated
        soon
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            This Method creates a session Id for the user_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
