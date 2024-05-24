#!/usr/bin/env python3
"""Authentication module for the API.
"""
from typing import List, TypeVar, Optional
from flask import request
import re


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: Optional[str], excluded_paths: Optional[List[str]]) -> bool:
        """Checks if a path requires authentication.
        """
        if not path or not excluded_paths:
            return True

        path = path.rstrip('/')
        for exclusion_path in map(lambda x: x.rstrip('/'), excluded_paths):
            if exclusion_path.endswith('*'):
                if path.startswith(exclusion_path[:-1]):
                    return False
            elif exclusion_path == path:
                return False

        return True

    def authorization_header(self, request: Optional[request] = None) -> Optional[str]:
        """Gets the authorization header field from the request.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request: Optional[request] = None) -> Optional[TypeVar('User')]:
        """Gets the current user from the request.
        """
        return None
