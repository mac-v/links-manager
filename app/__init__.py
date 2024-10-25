from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# predeifned variable that set a reference (module name - "app")
load_dotenv(".flaskenv")
load_dotenv(".env")

app = Flask(__name__)

# JWT hashing
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
jwt = JWTManager(app)
db = SQLAlchemy(app)
# workaround for cyclic import

from app.routes.users import users_bp  # noqa: E402
from app.routes.links import links_bp  # noqa: E402
from app.routes.categories import categories_bp  # noqa: E402

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(links_bp, url_prefix="/links")
app.register_blueprint(categories_bp, url_prefix="/categories")


def handle_exception(e):
    if hasattr(e, "code"):
        response = {"message": e.description}
        return jsonify(response), e.code
    else:
        response = {"message": str(e)}
        return jsonify(response), 500


app.register_error_handler(Exception, handle_exception)

if os.getenv("CREATE_DB", "false").lower() == "true":
    with app.app_context():
        db.create_all()
        print("Database created!")
