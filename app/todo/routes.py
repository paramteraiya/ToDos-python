from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pydantic import ValidationError
from app.models.todo import ItemModel, GetItemModel, UpdateItemModel
from datetime import datetime
from bson import ObjectId
from app.middleware import auth_required
from app.database_manager import DatabaseManager


todo_bp = Blueprint('todo', __name__)
db = DatabaseManager().get_db()

@todo_bp.route("/")
def index():
    return jsonify({"message": "Server up & running", "status": 200})

@todo_bp.route("/items", methods=["POST"])
@auth_required
def create_todo():
    try:
        item_data = request.json
        item_data["created_at"] = datetime.now()
        item = ItemModel(**item_data)
        db.items.insert_one(item.model_dump(by_alias=True))
        return jsonify(GetItemModel(**item.model_dump(by_alias=True)).model_dump(by_alias=True)), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
@todo_bp.route("/items", methods=["GET"])
@auth_required
def get_todos():
    items_cursor = db.items.find()
    return jsonify([GetItemModel(**item).model_dump(by_alias=True) for item in items_cursor])

@todo_bp.route("/items/<item_id>", methods=["GET"])
@auth_required
def get_todo_by_id(item_id):
    item = db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        return jsonify(GetItemModel(**item).model_dump(by_alias=True))
    return jsonify({"error": "Item not found"}), 404

@todo_bp.route("/items/<item_id>", methods=["PUT"])
@auth_required
def update_todo_by_id(item_id):
    try:
        item_data = request.json
        item_data["updated_at"] = datetime.now()
        item = UpdateItemModel(**item_data)
        db.items.update_one({"_id": ObjectId(item_id)}, {"$set": item.model_dump()})
        updated_item = db.items.find_one({"_id": ObjectId(item_id)})
        return jsonify(GetItemModel(**updated_item).model_dump(by_alias=True))
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except:
        return jsonify({"error": "Item not found"}), 404
    
@todo_bp.route("/items/<item_id>", methods=["DELETE"])
@auth_required
def delete_todo_by_id(item_id):
    result = db.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({"message": "Item deleted"})
    return jsonify({"error": "Item not found"}), 404