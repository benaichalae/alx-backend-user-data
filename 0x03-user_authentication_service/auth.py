#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt
import uuid
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def hash_password(password: str) -> bytes:
    """Hashes a password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def generate_uuid() -> str:
    """Generates a UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance.
        """
        self.db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            self.db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = hash_password(password)
            return self.db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.
        """
        try:
            user = self.db.find_user_by(email=email)
            hashed_pw = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.
        """
        try:
            user = self.db.find_user_by(email=email)
            session_id = generate_uuid()
            self.db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.
        """
        if session_id is None:
            return None
        try:
            return self.db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a given user.
        """
        if user_id is not None:
            self.db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.
        """
        try:
            user = self.db.find_user_by(email=email)
            reset_token = generate_uuid()
            self.db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.
        """
        try:
            user = self.db.find_user_by(reset_token=reset_token)
            hashed_password = hash_password(password)
            user_id = user.id
            self.db.update_user(user_id,
                                hashed_password=hashed_password,
                                reset_token=None)
        except NoResultFound:
            raise ValueError()
