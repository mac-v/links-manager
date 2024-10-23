from app import app, db
from sqlalchemy import text
from app.models import Link, User, user_schema, link_schema
from flask import request, jsonify, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from errors import error_response
from marshmallow import ValidationError
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
# decorator - modifies function that follows it

load_dotenv('.env')
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(url, key)



@app.route('/register', methods=['POST'])
def register():
    try:
        user_data = user_schema.loads(request.data)
        response = supabase.auth.sign_up(user_data)
        return jsonify({
            "id": response.user.id,
            "email": response.user.email,
            "message": "User registered successfully!"
        }), 200
    except json.JSONDecodeError:
        return error_response(400, "Invalid JSON format")
    except ValidationError as e:
        return error_response(400, e.messages)
    except Exception as e:
        return error_response(500, str(e))

@app.route('/login', methods=['POST'])
def login():
    try:
        response = supabase.auth.sign_in_with_password(
            user_schema.loads(request.data)
        )
        return jsonify({
            "id": response.user.id,
            "message": "User loggged in!",
            "jwt_token:": supabase.auth.get_session().access_token
        }), 200

    except json.JSONDecodeError:
        return error_response(400, "Invalid JSON format")

    except ValidationError as e:
        return error_response(400, e.messages)

    except Exception as e:
        return error_response(500, str(e))


@app.route('/')
@app.route('/profile')
@jwt_required()
def index():
    user_id = get_jwt_identity()
    print(user_id)
    user = user_schema.dump(User.query.filter_by(id=user_id).first())
    links = link_schema.dump(Link.query.filter_by(user_id=user_id).all(), many=True)
    return jsonify({
        "user": user,
        "links": links
    }), 200
# @app.route("/links")
# @jwt_required()
# def get_user_with_links():
#     user_id = get_jwt_identity()
#     links = Link.query.filter_by(user_id=user_id).all()
#     return jsonify([link.to_dict() for link in links]), 200
