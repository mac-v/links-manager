from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.config import supabase
from app.models import (
    Link,
    User,
    UserSchema,
    UserWithLinksSchema,
    ResponseSchema,
)
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    "users", "users", url_prefix="/users", description="Operation on users"
)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, ResponseSchema)
    def post(self):
        """Register a new user"""
        user_data = UserSchema().loads(request.data)
        supabase.auth.sign_up(user_data)
        return jsonify({"message": "User Registered in successfully!"})


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, ResponseSchema)
    def post(self, user_data):
        """Log in user"""
        supabase.auth.sign_in_with_password(user_data)
        return jsonify({"jwt_token": supabase.auth.get_session().access_token})


@blp.route("/")
class UserWithLinks(MethodView):
    @jwt_required()
    @blp.response(200, UserWithLinksSchema)
    def get(self):
        """Get authenticated user profile with links"""
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        links = Link.query.filter_by(user_id=user_id).all()
        user_data = {
            "id": user.id,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "email": user.email,
            "links": links,
        }
        return user_data
