from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_smorest import Api

# predeifned variable that set a reference (module name - "app")
load_dotenv(".flaskenv")
load_dotenv(".env")

app = Flask(__name__)

app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)

# JWT hashing
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["PROPAGATE_EXCEPTIONS"] = True
jwt = JWTManager(app)
db = SQLAlchemy(app)
# workaround for cyclic import

from app.routes.users import blp as UserBlueprint  # noqa: E402
from app.routes.links import blp as LinkBlueprint  # noqa: E402
from app.routes.categories import blp as CategoriesBlueprint  # noqa: E402

api = Api(app)
api.register_blueprint(UserBlueprint)
api.register_blueprint(LinkBlueprint)
api.register_blueprint(CategoriesBlueprint)

if os.getenv("CREATE_DB", "false").lower() == "true":
    with app.app_context():
        db.create_all()
        print("Database created!")
