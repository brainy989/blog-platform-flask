from flask import Blueprint
from flask import request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from .models.blog import BlogPost
from .auth import signup, login

# Define the main blueprint for the application
main = Blueprint('main', __name__)

@main.route('/signup', methods=['POST'])
def handle_signup():
    """
    Handle user signup requests.
    
    Returns:
        JSON response indicating the result of the signup process.
    """
    return signup()

@main.route('/login', methods=['POST'])
def handle_login():
    """
    Handle user login requests.
    
    Returns:
        JSON response indicating the result of the login process.
    """
    return login()

@main.route('/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all blog posts.
    
    Returns:
        JSON response containing a list of all blog posts.
    """
    posts = BlogPost.get_posts()
    return jsonify(posts), 200

@main.route('/posts', methods=['POST'])
@login_required
def create_post():
    """
    Create a new blog post.
    
    Expects a JSON payload with 'title' and 'content'.
    Requires the user to be logged in.
    
    Returns:
        JSON response containing the ID of the newly created post.
    """
    data = request.get_json()
    new_post = {
        'title': data['title'],
        'content': data['content'],
        'author': current_user.username,
        'created_at': datetime.utcnow()
    }
    
    post_id = BlogPost.create_post(new_post)
    return jsonify({"id": post_id}), 200

@main.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """
    Retrieve a single blog post by its ID.
    
    Args:
        post_id (str): The ID of the blog post to retrieve.
    
    Returns:
        JSON response containing the blog post if found, otherwise a 404 error message.
    """
    post = BlogPost.get_post(post_id)
    if post:
        return jsonify(post), 200
    else:
        return jsonify({"error": "Post not found"}), 404
    
@main.route('/posts/<post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    """
    Update a blog post by its ID.
    
    Expects a JSON payload with 'title' and 'content'.
    Requires the user to be logged in.
    
    Args:
        post_id (str): The ID of the blog post to update.
    
    Returns:
        JSON response indicating success or failure of the update operation.
    """
    data = request.get_json()
    updated_post = {
        'title': data['title'],
        'content': data['content'],
        'author': current_user.username,
        'created_at': datetime.utcnow()
    }
    
    success = BlogPost.update_post(post_id, updated_post)
    if success:
        return jsonify({"success": "Post updated"}), 200
    else:
        return jsonify({"error": "Post not found or no changes made"}), 404

@main.route('/posts/<post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    """
    Delete a blog post by its ID.
    
    Requires the user to be logged in.
    
    Args:
        post_id (str): The ID of the blog post to delete.
    
    Returns:
        JSON response indicating success or failure of the deletion operation.
    """
    success = BlogPost.delete_post(post_id)
    if success:
        return jsonify({"success": "Post deleted"}), 200
    else:
        return jsonify({"error": "Post not found"}), 404