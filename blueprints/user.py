from flask import Blueprint, request, jsonify
from db import orm
from models import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(name=name, email=email)
    orm.session.add(new_user)
    orm.session.commit()

    return jsonify({"message": "User created", "user": new_user.to_dict()}), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if name:
        user.name = name
    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({"error": "Email already exists"}), 400
        user.email = email

    orm.session.commit()
    return jsonify({"message": "User updated", "user": user.to_dict()}), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.blogs and len(user.blogs) > 0:
        return jsonify({"error": "Cannot delete user with existing blogs"}), 400

    orm.session.delete(user)
    orm.session.commit()
    return jsonify({"message": "User deleted"}), 200
