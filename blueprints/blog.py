from flask import Blueprint, request, jsonify
from db import orm
from models import Blog
from models import User

blog_bp = Blueprint('blog_bp', __name__, url_prefix='/blog')

@blog_bp.route('/', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([b.to_dict() for b in blogs]), 200

@blog_bp.route('/', methods=['POST'])
def add_blog():
    data = request.get_json()
    user_id = data.get("user_id")
    detail = data.get("detail")

    if not user_id or not detail:
        return jsonify({"error": "User ID and detail are required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": f"No user with id {user_id} exists"}), 400


    new_blog = Blog(user_id=user_id, detail=detail)
    orm.session.add(new_blog)
    orm.session.commit()

    return jsonify({"message": "Blog created", "blog": new_blog.to_dict()}), 201

@blog_bp.route('/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.get_json()
    detail = data.get("detail")
    user_id = data.get("user_id")

    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), 404

    if user_id:
        user= User.query.get(user_id)
        if not user:
            return jsonify({"error": f"No user with id {user_id} exists"}), 400
        blog.user_id = user_id
    if detail:
        blog.detail = detail

    orm.session.commit()
    return jsonify({"message": "Blog updated", "blog": blog.to_dict()}), 200

@blog_bp.route('/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), 404

    orm.session.delete(blog)
    orm.session.commit()
    return jsonify({"message": "Blog deleted"}), 200

