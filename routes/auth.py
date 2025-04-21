from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from models.user import User

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email    = data.get("email")
    password = data.get("password")
    phone    = data.get("phone")

    if email and User.find_by_email(email):
        return jsonify({"error": "Email already taken"}), 400
    if phone and User.find_by_phone(phone):
        return jsonify({"error": "Phone already taken"}), 400

    try:
        user_id = User.create(email=email, password=password, phone=phone)
        return jsonify({"msg": "User created", "user_id": str(user_id)}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email    = data.get("email")
    password = data.get("password")
    phone    = data.get("phone")

    user = None
    if email and password:
        user = User.find_by_email(email)
        if not user or not User.check_password(user, password):
            return jsonify({"error": "Invalid email or password"}), 401
    elif phone:
        user = User.find_by_phone(phone)
        if not user:
            return jsonify({"error": "Invalid phone number"}), 401
    else:
        return jsonify({"error": "Provide email+password or phone"}), 400

    identity = user.get("email") or user.get("phone")
    token = create_access_token(identity=identity)
    return jsonify({"access_token": token}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    return jsonify({"me": identity}), 200
