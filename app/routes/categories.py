from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['POST'])
@jwt_required()
def add_category():
    pass

@categories_bp.route('/<uuid:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    pass
