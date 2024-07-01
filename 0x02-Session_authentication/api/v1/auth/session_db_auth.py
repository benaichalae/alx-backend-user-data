#!/usr/bin/env python3
"""
SessionDBAuth class for authentication based on Session IDs stored in a database.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth extends SessionExpAuth to manage authentication with database-stored Session IDs.
    """

    def create_session(self, user_id=None):
        """
        Create a new session for a user and store it in the database.

        Args:
            user_id (str): ID of the user for whom the session is created.

        Returns:
            str: Session ID if successful, otherwise None.
        """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the User ID associated with a session ID from the database.

        Args:
            session_id (str): Session ID to look up.

        Returns:
            str: User ID if session is found in the database, otherwise None.
        """
        user_id = super().user_id_for_session_id(session_id)
        if user_id:
            user_sessions = UserSession.search({'session_id': session_id})
            if user_sessions:
                return user_sessions[0].user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroy the session based on the session ID retrieved from the request cookie.

        Args:
            request: Flask request object containing cookies.

        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id:
            user_sessions = UserSession.search({'session_id': session_id})
            if user_sessions:
                for session in user_sessions:
                    session.remove()
                return True
        return False
