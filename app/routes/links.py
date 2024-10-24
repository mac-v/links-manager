from werkzeug.exceptions import HTTPException
from flask import Blueprint, jsonify, request, abort
from app.models import Link, LinkSchema, Category
from app import db, app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import json

links_bp = Blueprint('links', __name__)

link_schema = LinkSchema(exclude=['user_id', 'category_id', 'id'])


@links_bp.route('/<uuid:user_id>', methods=['GET'])
def get_user_links(user_id):
    by_categories = request.args.get('by_categories', 'false') == 'true'
    if by_categories:
        categories = Category.query.filter_by(user_id=user_id).all()
        categories_with_links = []
        for category in categories:
            category_data = {
                "name": category.name,
                "description": category.description,
                "links": link_schema.dump(category.links, many=True)
            }
            categories_with_links.append(category_data)

        return jsonify({"categories": categories_with_links}), 200
    else:
        links = link_schema.dump(Link.query.filter_by(user_id=user_id).all(), many=True)
        return jsonify({
            "links": links
        }), 200


@links_bp.route('', methods=['POST'])
@jwt_required()
def add_link():
    user_id = get_jwt_identity()

    try:
        link = link_schema.load(request.json)
        existing_link = Link.query.filter_by(user_id=user_id, url=link['url']).first()
        if existing_link:
            return abort(400, description="This URL already exists for the user.")
        link['user_id'] = user_id
        link = Link(**link)
        db.session.add(link)
        db.session.commit()
        return jsonify({
            "link_id": link.id,
            "message": "Link added!",
        }), 201
    except ValidationError as e:
        return abort(400, description=e.messages)


@links_bp.route('/<uuid:link_id>', methods=['PUT'])
@jwt_required()
def modify_link(link_id):
    user_id = get_jwt_identity()

    link = Link.query.get(link_id)

    if not link:
        return abort(404, description='Link not found')
    try:
        new_link_data = link_schema.load(request.json)

        existing_link = Link.query.filter(Link.user_id == user_id, Link.url == new_link_data['url'],
                                          Link.id != link_id).first()
        if existing_link:
            return abort(400, description="This URL already exists for the user.")

        for key, value in new_link_data.items():
            setattr(link, key, value)

        db.session.commit()
        return jsonify({
            "link_id": link.id,
            "message": "Link Modified!",
        }), 201
    except ValidationError as e:
        return abort(400, description=e.messages)


@links_bp.route('/<uuid:link_id>', methods=['DELETE'])
def delete_link(link_id):
    pass
