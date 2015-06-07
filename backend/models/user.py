from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, DateTime, Index

from flask import session

from flask.ext.login import UserMixin, login_user, logout_user
from sqlalchemy.dialects import postgres
from sqlalchemy_utils import Timestamp

from backend.utils.database import Base, CRUDMixinCached, BaseSchema


class User(Base, CRUDMixinCached, Timestamp, UserMixin):
    """
    Usermodel
    """
    __tablename__ = "prx_user"

    id = Column(postgres.UUID(as_uuid=False), default=lambda: str(uuid.uuid4()), primary_key=True)
    provider_id = Column(Integer, nullable=False)
    provider_name = Column(String, nullable=False)
    character_id = Column(Integer, unique=True, nullable=False)  #: eve character id
    character_name = Column(String, nullable=False)  #: eve character name
    last_login = Column(DateTime)
    email = Column(String)

    __table_args__ = (Index('provider', 'provider_id', 'provider_name', unique=True),)

    def login(self, remember=False):
        success = login_user(self, remember=remember)
        if success:
            self.last_login = datetime.utcnow()
        self.save(commit=True)
        return success

    def logout(self):
        logout_user()
        session.clear()

    @classmethod
    def get_user_for_session(cls, pid):
        """
        :param int id:
        :return: :py:class:`User`
        """
        return cls.get_by_id(pid)

    def __repr__(self):
        return '<User(name={self.character_name!r} provider={self.provider_name!r})>'.format(self=self)


class UserSchema(BaseSchema):
    class Meta:
        model = User
