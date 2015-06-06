from sqlalchemy import Column, String
import uuid
from marshmallow import fields
from sqlalchemy.databases import postgres
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Timestamp
from backend.database import Base, BaseSchema, db
from backend.database import CRUDMixin
from backend.models.user import User, UserSchema


class TodoModel(Base, CRUDMixin, Timestamp):

    __tablename__ = "prx_todo"

    id = Column(postgres.UUID(as_uuid=False), default=lambda: str(uuid.uuid4()), primary_key=True)
    creator_id = Column(postgres.UUID(as_uuid=False), db.ForeignKey(User.id), nullable=False)
    task = Column(String())

    creator = relationship(User)

    def __repr__(self):
        return '<Todo(id={self.id!r})>'.format(self=self)


class TodoSchema(BaseSchema):
    creator = fields.Nested(UserSchema, only=('character_name','character_id','id' ))

    class Meta:
        model = TodoModel
