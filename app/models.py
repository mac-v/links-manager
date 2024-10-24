from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app import db
import uuid
from marshmallow import Schema, fields, validate, pre_load


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column("modified_at", db.DateTime, nullable=True, onupdate=func.now())
    url = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.users.id"), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("Category", backref="links")


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'auth'}
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=func.now())
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column("encrypted_password", db.Text, unique=True, nullable=False)
    links = db.relationship("Link", backref="user")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column("modified_at", db.DateTime, nullable=True, onupdate=func.now())
    name = db.Column(db.Text, unique=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.users.id"), nullable=False)


def strip_whitespace(data, fields_to_strip):
    for field in fields_to_strip:
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip()
    return data


class CategorySchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))
    user_id = fields.UUID()

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ['name', 'description'])


class LinkSchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    url = fields.Url(required=True, validate=validate.Length(min=10, max=2048))
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))
    user_id = fields.UUID()
    category_id = fields.UUID()

    category_name = fields.Method("get_category_name")
    category_description = fields.Method("get_category_description")

    def get_category_name(self, link):
        return link.category.name if link.category else None

    def get_category_description(self, link):
        return link.category.description if link.category else None

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ['url', 'name', 'description'])


class UserSchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    email = fields.Email(required=True)
    password = fields.Str(required=True)
