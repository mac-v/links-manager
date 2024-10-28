from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import ForeignKeyConstraint
from app import db
import uuid
from marshmallow import Schema, fields, validate, pre_load


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        "modified_at", db.DateTime, nullable=True, onupdate=func.now()
    )
    url = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("auth.users.id"), nullable=False
    )
    category_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("categories.id"), nullable=True
    )
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"], ["categories.id"], ondelete="SET NULL"
        ),
    )
    category = db.relationship("Category", back_populates="links")


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=func.now())
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(
        "encrypted_password", db.Text, unique=True, nullable=False
    )
    links = db.relationship("Link", backref="user")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        "modified_at", db.DateTime, nullable=True, onupdate=func.now()
    )
    name = db.Column(db.Text, unique=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("auth.users.id"), nullable=False
    )
    links = db.relationship("Link", back_populates="category")


def strip_whitespace(data, fields_to_strip):
    for field in fields_to_strip:
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip()
    return data


class CreateUpdateCategorySchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ["name", "description"])


class CategorySchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ["name", "description"])


class AssignLinksSchema(Schema):
    link_ids = fields.List(fields.UUID(), required=True)


class LinkSchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    url = fields.Url(required=True, validate=validate.Length(min=10, max=2048))
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))
    category_name = fields.Method("get_category_name", dump_only=True)
    category_description = fields.Method(
        "get_category_description", dump_only=True
    )

    def get_category_name(self, link):
        return link.category.name if link.category else None

    def get_category_description(self, link):
        return link.category.description if link.category else None

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ["url", "name", "description"])


class ResponseLinkSchema(Schema):
    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    url = fields.Url(required=True, validate=validate.Length(min=10, max=2048))
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))


class CreateUpdateLinkSchema(Schema):
    url = fields.Url(required=True, validate=validate.Length(min=10, max=2048))
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ["url", "name", "description"])


class MinimalLinkSchema(Schema):
    id = fields.UUID()
    url = fields.Url(required=True, validate=validate.Length(min=10, max=2048))
    name = fields.Str(validate=validate.Length(min=3, max=100))
    description = fields.Str(validate=validate.Length(min=10, max=500))
    category_name = fields.Method("get_category_name", dump_only=True)
    category_description = fields.Method(
        "get_category_description", dump_only=True
    )

    def get_category_name(self, link):
        return link.category.name if link.category else None

    def get_category_description(self, link):
        return link.category.description if link.category else None

    @pre_load
    def process_text_fields(self, data, **kwargs):
        return strip_whitespace(data, ["url", "name", "description"])


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserWithLinksSchema(Schema):
    id = fields.UUID()
    email = fields.Email()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    links = fields.List(fields.Nested(LinkSchema))


class ResponseSchema(Schema):
    message = fields.Str()
