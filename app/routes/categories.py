from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import (
    Category,
    CategorySchema,
    AssignLinksSchema,
    CreateUpdateCategorySchema,
    ResponseSchema,
    Link,
)
from app import db

blp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories",
    description="Operations on categories",
)


@blp.route("/")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        """List all categories for the authenticated user"""
        user_id = get_jwt_identity()
        categories = Category.query.filter_by(user_id=user_id).all()
        return categories, 200


@blp.route("/")
class CategoryResource(MethodView):
    @jwt_required()
    @blp.arguments(CreateUpdateCategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        """Add a new category for the authenticated user"""
        user_id = get_jwt_identity()
        existing_category = Category.query.filter_by(
            user_id=user_id, name=category_data["name"]
        ).first()
        if existing_category:
            abort(400, message="This category already exists for the user.")
        category_data["user_id"] = user_id
        category = Category(**category_data)
        db.session.add(category)
        db.session.commit()
        return category, 201


@blp.route("/<uuid:category_id>/links")
class CategoryLinks(MethodView):
    @jwt_required()
    @blp.arguments(AssignLinksSchema)
    @blp.response(200, ResponseSchema)
    def patch(self, link_data, category_id):
        """Assign category to links for the authenticated user"""
        user_id = get_jwt_identity()
        category = Category.query.filter_by(
            id=category_id, user_id=user_id
        ).first()
        if not category:
            abort(404, message="Category not found")
        link_ids = link_data["link_ids"]
        links = Link.query.filter(
            Link.id.in_(link_ids), Link.user_id == user_id
        ).all()
        if len(links) != len(link_ids):
            abort(
                400,
                message="Some links not found or belong to a different user",
            )
        for link in links:
            link.category_id = category_id
        db.session.commit()
        return jsonify({"message": "Links assigned to category"})


@blp.route("/<uuid:category_id>")
class CategoryById(MethodView):
    @jwt_required()
    @blp.arguments(CreateUpdateCategorySchema)
    @blp.response(200, CategorySchema)
    def put(self, updated_data, category_id):
        """Modify an existing category by ID for the authenticated user"""
        user_id = get_jwt_identity()
        category = Category.query.get(category_id)
        if not category:
            abort(404, message="Category not found")
        existing_category = Category.query.filter(
            Category.user_id == user_id,
            Category.name == updated_data["name"],
            Category.id != category_id,
        ).first()
        if existing_category:
            abort(400, message="This name already exists for the user.")
        for key, value in updated_data.items():
            setattr(category, key, value)
        db.session.commit()
        return category, 200

    @jwt_required()
    @blp.response(204, ResponseSchema)
    def delete(self, category_id):
        """Delete a category by ID for the authenticated user"""
        category = Category.query.get(category_id)
        if not category:
            abort(404, description="Category not found")
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully!"})
