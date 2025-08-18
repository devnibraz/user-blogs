from flask import Blueprint, request, jsonify, current_app
from db import orm
from models import User
import os
from werkzeug.utils import secure_filename
from flask import current_app

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')



def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@user_bp.route('/upload/<int:user_id>', methods=['POST'])
def upload_avatar(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'avatar' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['avatar']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allow_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True) 
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        user.avatar = filename
        orm.session.commit()

        return jsonify({"message": "Avatar uploaded", "user": user.to_dict()}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400


@user_bp.route('/', methods=['GET'])
def get_users():
    from app import cache
    @cache.cached(timeout=30)
    def get_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200
    return get_users()
@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    full_name = data.get("full_name", None)

    if not name or not email or not full_name:
        return jsonify({"error": "Name ,Email and are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(name=name, email=email, full_name=full_name)
    orm.session.add(new_user)
    orm.session.commit()

    return jsonify({"message": "User created", "user": new_user.to_dict()}), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    full_name = data.get("full_name", None)

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if name:
        user.name = name
    if full_name:
        user.full_name = full_name
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
