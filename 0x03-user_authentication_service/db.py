#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self.engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self._session = None

    def get_session(self) -> Session:
        """Create and return a new session object.
        """
        if self._session is None:
            DBSession = sessionmaker(bind=self.engine)
            self._session = DBSession()
        return self._session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        session = self.get_session()
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        try:
            session.commit()
        except Exception:
            session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user based on a set of filters.
        """
        session = self.get_session()
        query = session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
            query = query.filter(getattr(User, key) == value)
        result = query.first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user based on a given id.
        """
        session = self.get_session()
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            raise NoResultFound()
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            setattr(user, key, value)
        session.commit()
