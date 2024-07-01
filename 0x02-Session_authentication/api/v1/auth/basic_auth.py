#!/usr/bin/env python3
"""class BasicAuth"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication"""
        if authorization_header is None or not isinstance(
                authorization_header, str
                ):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        base64_part = authorization_header.split(' ')[1]
        return base64_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """returns the decoded value of a Base64 string
        base64_authorization_header"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str
                ):
            return None

        try:
            decoded_bytes = base64.b64decode(
                    base64_authorization_header
                    )
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """returns the user email and password from the
        Base64 decoded value"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str
                ):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_pwd = decoded_base64_authorization_header.split(
                ':', 1
                )

        return user_email, user_pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
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
        """retrieves the User instance for a request"""
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')

        base64_auth_header = self.extract_base64_authorization_header(
                authorization_header
                )
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header
                )

        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                decoded_auth_header
                )

        if user_email is None or user_pwd is None:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
