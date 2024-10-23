from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app import db
import uuid
from marshmallow import Schema, fields
class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column("modified_at", db.DateTime, nullable=True, onupdate=func.now())
    url = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.users.id"), nullable=False)

    def __repr__(self):
        return '<Link url %r, created %r>' % (self.url, self.created_at)


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'auth'}
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=func.now())
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column("encrypted_password", db.Text, unique=True, nullable=False)
    links = db.relationship("Link", backref='user', lazy=True)

    def __repr__(self):
        return '<User id %r, created %r>' % (self.id, self.created_at)

class LinkSchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    url = fields.Str()
    name = fields.Str()
    description = fields.Str()
    user_id = fields.UUID()

class UserSchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    email = fields.Email(required=True)
    password = fields.Str(required=True)

user_schema = UserSchema()
link_schema = LinkSchema()
