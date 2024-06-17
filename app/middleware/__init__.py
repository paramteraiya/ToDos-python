from functools import wraps
from flask import request, jsonify
from app.jwt_utils import decode_jwt_token
from bson import ObjectId
from app.database_manager import DatabaseManager

db = DatabaseManager().get_db()

def authenticate():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401
    
    token = auth_header.split(" ")[1]
    user_id = decode_jwt_token(token)
    
    if not user_id:
        return jsonify({"message": "Invalid token"}), 401
    
    if user_id == "Signature expired. Please log in again.":
        return jsonify({"message": "Signature expired. Please log in again."}), 401
    elif user_id == "Invalid token. Please log in again.":
        return jsonify({"message": "Invalid token. Please log in again."}), 401
    
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"message": "Invalid token"}), 401
    return None

def auth_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_result = authenticate()
        if auth_result:
            return auth_result
        return func(*args, **kwargs)
    return decorated_function