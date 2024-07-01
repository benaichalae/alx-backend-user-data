#!/usr/bin/env python3
"""
SessionAuth class that inherits from Auth
"""
from .auth import Auth
import uuid
import os
from models.user import User


class SessionAuth(Auth):
    """
    Session authentication mechanism using session IDs.
    Inherits from Auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user ID.

        Args:
            user_id (str): ID of the user.

        Returns:
            str: Session ID created.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): Session ID to look up.

        Returns:
            str: User ID associated with the session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """
        Retrieves the session ID from cookies in the request.

        Args:
            request: Flask request object.

        Returns:
            str: Session ID retrieved from cookies.
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session ID in the request cookies.

        Args:
            request: Flask request object.

        Returns:
            User: User instance associated with the session ID.
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        Destroys the session by removing the session ID from the storage.

        Args:
            request: Flask request object.

        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
