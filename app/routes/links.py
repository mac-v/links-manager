from flask_smorest import Blueprint, abort
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import (
    Link,
    User,
    MinimalLinkSchema,
    CreateUpdateLinkSchema,
    ResponseSchema,
    ResponseLinkSchema,
)

blp = Blueprint(
    "links", "links", url_prefix="/links", description="Operation on links"
)


@blp.route("/<uuid:user_id>")
class UserLinks(MethodView):
    @blp.response(200, MinimalLinkSchema(many=True))
    def get(self, user_id):
        """Get all user links"""
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        links = Link.query.filter_by(user_id=user_id).all()
        return links


@blp.route("/")
class LinkResource(MethodView):
    @jwt_required()
    @blp.arguments(CreateUpdateLinkSchema)
    @blp.response(201, ResponseLinkSchema)
    def post(self, new_data):
        """Add a new link for the authenticated user"""
        user_id = get_jwt_identity()
        existing_link = Link.query.filter_by(
            user_id=user_id, url=new_data["url"]
        ).first()
        if existing_link:
            abort(400, message="This URL already exists for the user.")
        new_data["user_id"] = user_id
        link = Link(**new_data)
        db.session.add(link)
        db.session.commit()
        return link


@blp.route("/<uuid:link_id>")
class LinkById(MethodView):
    @jwt_required()
    @blp.arguments(CreateUpdateLinkSchema)
    @blp.response(200, ResponseLinkSchema)
    def put(self, update_data, link_id):
        """Update link by ID for the authenticated user"""
        user_id = get_jwt_identity()
        link = Link.query.get(link_id)
        if not link:
            abort(404, message="Link not found")
        existing_link = Link.query.filter(
            Link.user_id == user_id,
            Link.url == update_data["url"],
            Link.id != link_id,
        ).first()
        if existing_link:
            abort(400, message="This URL already exists for the user.")
        for key, value in update_data.items():
            setattr(link, key, value)
        db.session.commit()
        return link

    @jwt_required()
    @blp.response(204, ResponseSchema)
    def delete(self, link_id):
        """Delete link by ID for the authenticated user"""
        link = Link.query.get(link_id)
        if not link:
            abort(404, message="Link not found")
        db.session.delete(link)
        db.session.commit()
        return jsonify({"message": "Link deleted successfully!"})
