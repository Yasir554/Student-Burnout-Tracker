from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.User import User
from db.Burnout_Tracker import db
from utils.auth_utils import role_required
from utils.jwt_blocklist import jwt_blocklist
from utils.validators import is_strong_password  

auth_bp = Blueprint('auth_bp', __name__)

# ==================== Home ====================
@auth_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Student Burnout Tracker API!"})


# ==================== SIGNUP ====================
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'staff').lower()

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required."}), 400

    if not is_strong_password(password):
        return jsonify({
            "error": "Password must be at least 8 characters long and include an uppercase letter, lowercase letter, number, and special character."
        }), 400

    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify({"error": "User with that username or email already exists."}), 409

    # Create new user
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully.",
        "user": new_user.to_dict()
    }), 201


# ==================== LOGIN ====================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({"error": "Username/email and password are required."}), 400

    # Finding a user by username or email
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username/email or password."}), 401

    access_token = create_access_token(identity={
        "id": user.id,
        "role": user.role,
        "username": user.username
        })

    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200



# ==================== LOGOUT ====================
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt().get("jti")
    jwt_blocklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200


# ==================== DUMMY ROUTE TO TEST RBAC Admin ====================
@auth_bp.route('/admin-only', methods=['GET'])
@role_required(['admin'])
def admin_only_route():
    return jsonify({"message": "You are an admin!"})


# ==================== DUMMY ROUTE TO TEST RBAC Staff ====================
@auth_bp.route('/staff-only', methods=['GET'])
@role_required(['staff'])
def staff_only_route():
    return jsonify({"message": "You are a staff member!"})
