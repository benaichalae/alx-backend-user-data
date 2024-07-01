#!/usr/bin/env python3
"""
UserSession model representing a user's session.
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class inherits from Base and represents a user's session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a UserSession instance.

        Args:
            *args (list): Positional arguments passed to the parent constructor.
            **kwargs (dict): Keyword arguments to initialize attributes.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', '')
