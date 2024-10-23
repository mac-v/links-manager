from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# predeifned variable that set a reference (module name - "app")

load_dotenv('.flaskenv')
load_dotenv('.env')


app = Flask(__name__)

# JWT hashing
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
jwt = JWTManager(app)
db = SQLAlchemy(app)
# workaround for cyclic import
from app import routes

if os.getenv("CREATE_DB", "false").lower() == "true":
    with app.app_context():
        db.create_all()
        print("Database created!")
