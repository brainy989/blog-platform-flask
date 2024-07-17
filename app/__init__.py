import os
from dotenv import load_dotenv

from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

# Load environment variables from a .env file
load_dotenv()

# Initialize PyMongo
mongo = PyMongo()

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    
    # Configure the MongoDB URI and secret key from environment variables
    app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/blogdb')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', '')
    
    # Initialize PyMongo with the Flask app
    mongo.init_app(app)
    
    # Initialize the LoginManager and set the login view
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback function to reload the user object from the user ID stored in the session.

        Args:
            user_id (str): The ID of the user to load.

        Returns:
            User: The loaded User object.
        """
        return User.get(user_id)
    
    # Register the authentication blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # Register the main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app