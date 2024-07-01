#!/usr/bin/env python3
"""
API authentication module
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The path of the request.
            excluded_paths (List[str]): List of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            elif path.rstrip('/') == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: Value of the Authorization header, or None if not found.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method to retrieve the current user.

        Args:
            request: Flask request object.

        Returns:
            TypeVar('User'): Placeholder for returning the current user.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from the request.

        Args:
            request: Flask request object.

        Returns:
            str: Value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
