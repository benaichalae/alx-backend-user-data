#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Subclass of Auth implementing Basic Authentication"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the Base64 part from the Authorization header"""
        if not isinstance(authorization_header, str) or not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Base64 encoded string"""
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user email and password from a decoded Base64 string"""
        if not isinstance(decoded_base64_authorization_header, str) or ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on email and password"""
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            user_inst = User.search({'email': user_email})
            if user_inst is None:
                return None
        except Exception:
            return None

        for user in user_inst:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the User instance for a request"""
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        base64_auth_header = self.extract_base64_authorization_header(authorization_header)
        
        if base64_auth_header is None:
            return None
        
        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        
        if decoded_auth_header is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_auth_header)
        
        if user_email is None or user_pwd is None:
            return None
        
        return self.user_object_from_credentials(user_email, user_pwd)
