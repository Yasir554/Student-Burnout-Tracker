from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Loading environment variables.
load_dotenv()

from db.Burnout_Tracker import db

# ========== EXTENSION INSTANCES ==========
migrate = Migrate()
jwt = JWTManager()
api = Api()

app = Flask(__name__)

# App Configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize Extensions 
db.init_app(app)
migrate.init_app(app, db, directory="db/migrations")

jwt.init_app(app)
from utils.jwt_blocklist import jwt_blocklist

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload.get("jti")
    return jti in jwt_blocklist

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has been revoked. Please log in again."}), 401

api.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

from models import * 
from routes import all_routes

for bp in all_routes:
    app.register_blueprint(bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
