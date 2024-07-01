#!/usr/bin/env python3
"""
SessionExpAuth class for session-based authentication with expiration.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth inherits from SessionAuth and adds session expiration functionality.
    """

    def __init__(self):
        """
        Initializes SessionExpAuth with session duration from environment variable.
        """
        super().__init__()
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        Creates a session ID for a user_id and stores session creation time.

        Args:
            user_id: ID of the user for whom the session is created.

        Returns:
            str: Session ID.
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves user ID from session dictionary based on session ID.

        Args:
            session_id: Session ID to look up.

        Returns:
            str: User ID if session is valid and not expired, otherwise None.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration > 0:
            if 'created_at' not in session_dict:
                return None

            exp_time = session_dict['created_at'] + timedelta(seconds=self.session_duration)
            if exp_time < datetime.now():
                return None

        return session_dict.get('user_id')
