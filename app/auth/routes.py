from flask import Blueprint, request, jsonify
from app.models.users import UserModel
from app.jwt_utils import generate_jwt_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.database_manager import DatabaseManager

auth_bp = Blueprint("auth", __name__)
db = DatabaseManager().get_db()

@auth_bp.route("/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        existing_user = db.users.find_one({"email": data["email"]})
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400
        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
        user = UserModel(email=data["email"], password=hashed_password)
        db.users.insert_one(user.model_dump())
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = db.users.find_one({"email": data["email"]})
        if not user or not check_password_hash(user["password"], data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401
        jwt_token = generate_jwt_token(str(user["_id"]))
        return jsonify({"token": jwt_token, "message": "Login successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, KeyError):
        code = 400
    return jsonify({"error": str(e)}), code
