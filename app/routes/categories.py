from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Category, CategorySchema
from app import db
from marshmallow import ValidationError

categories_bp = Blueprint("categories", __name__)

category_schema = CategorySchema(exclude=["user_id", "id"])


@categories_bp.route("", methods=["POST"])
@jwt_required()
def add_category():
    user_id = get_jwt_identity()

    try:
        category = category_schema.load(request.json)
        existing_category = Category.query.filter_by(
            user_id=user_id, name=category["name"]
        ).first()
        if existing_category:
            return abort(
                400, description="This URL already exists for the user."
            )
        category["user_id"] = user_id
        category = Category(**category)
        db.session.add(category)
        db.session.commit()
        return (
            jsonify(
                {
                    "category_id": category.id,
                    "message": "Category added!",
                }
            ),
            201,
        )
    except ValidationError as e:
        return abort(400, description=e.messages)
    pass


@categories_bp.route("/<uuid:category_id>", methods=["PUT"])
@jwt_required()
def modify_category(category_id):
    user_id = get_jwt_identity()

    category = Category.query.get(category_id)

    if not category:
        return abort(404, description="Category not found")
    try:
        new_category_data = category_schema.load(request.json)

        existing_category = Category.query.filter(
            Category.user_id == user_id,
            Category.name == new_category_data["name"],
            Category.id != category_id,
        ).first()
        if existing_category:
            return abort(
                400, description="This name already exists for the user."
            )

        for key, value in new_category_data.items():
            setattr(category, key, value)

        db.session.commit()
        return (
            jsonify(
                {
                    "category_id": category.id,
                    "message": "Category Modified!",
                }
            ),
            201,
        )
    except ValidationError as e:
        return abort(400, description=e.messages)


@categories_bp.route("/<uuid:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return abort(400, description="Category not found")
    db.session.delete(category)
    db.session.commit()
    return (
        jsonify(
            {
                "category_id": category.id,
                "message": "Category deleted!",
            }
        ),
        201,
    )
