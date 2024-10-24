from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.config import supabase
from app.models import Link, User, UserSchema, LinkSchema
from marshmallow import ValidationError
import json


users_bp = Blueprint('users', __name__)

user_schema = UserSchema()
user_schema_profile = UserSchema(exclude=['password'])
link_schema_profile = LinkSchema(exclude=['user_id'])

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        user_data = user_schema.loads(request.data)
        response = supabase.auth.sign_up(user_data)
        return jsonify({
            "id": response.user.id,
            "email": response.user.email,
            "message": "User registered successfully!"
        }), 201
    except ValidationError as e:
        return abort(400, description=e.messages)

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        response = supabase.auth.sign_in_with_password(
            user_schema.loads(request.data)
        )
        return jsonify({
            "user_id": response.user.id,
            "message": "User logged in!",
            "jwt_token": supabase.auth.get_session().access_token
        }), 200
    except ValidationError as e:
        return abort(400, description=e.messages)


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = user_schema_profile.dump(User.query.filter_by(id=user_id).first())
    links = link_schema_profile.dump(Link.query.filter_by(user_id=user_id).all(), many=True)
    return jsonify({
        "user": user,
        "links": links
    }), 200
