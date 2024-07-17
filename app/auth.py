from flask import Blueprint
from flask import request, jsonify
from flask_login import login_required, login_user, logout_user

from .models.user import User

# Define the authentication blueprint
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    """
    Handle user signup requests.
    
    Expects a JSON payload with 'username' and 'password'.
    Create a new user if the username does not already exist.

    Returns:
        JSON response indicating the result of the signup process.
    """
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Check if the user already exists
    user = User.get_by_username(username)
    
    if user:
        return jsonify({"message": "User already exists"}), 400
    
    # Create a new user
    new_user = User.create(username, password)
    
    return jsonify({"message": "User created successfully", "user_id": new_user.id})

@auth.route('/login', methods=['POST'])
def login():
    """
    Handle user login requests.
    
    Expects a JSON payload with 'username' and 'password'.
    Authenticates the user and logs them in if the credentials are valid.

    Returns:
        JSON response indicating the result of the login process.
    """
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Retrieve the user by username
    user = User.get_by_username(username)
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Log in the user
    login_user(user)
    return jsonify({"message": "Login successful"}), 200

@auth.route('/logout')
@login_required
def logout():
    """
    Handle user logout requests.
    
    Logs out the currently logged-in user.

    Returns:
        JSON response indicating the result of the logout process.
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200