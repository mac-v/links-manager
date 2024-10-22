from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column("modified_at", db.DateTime, nullable=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.users.id"), nullable=False)

    def __repr__(self):
        return '<Link url %r, created %r>' % (self.url, self.created_at)

    def to_dict(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "url": self.url,
            "name": self.name,
            "description": self.description,
            "user_id": str(self.user_id)
        }

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'auth'}
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False)

    links = db.relationship("Link", backref='user', lazy=True)

    def __repr__(self):
        return '<User id %r, created %r>' % (self.id, self.created_at)

    def to_dict(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "email": self.email
        }
