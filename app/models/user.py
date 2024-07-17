from bson.objectid import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import mongo

class User(UserMixin):
    """
    A class to represent a user in the system.
    Extends Flask-Login's UserMixin to provide default implementations for required user methods.
    """

    def __init__(self, user_id, username, password):
      """
      Initialize a new User object

      Args:
          user_id (str): The unique ID of the user.
          username (str): The username of the user.
          password (str): The hashed password of the user.
      """
      self.id = user_id
      self.username = username
      self.password = password
    
    @staticmethod
    def get(user_id):
      """
      Retrieve a user from the database by their user ID.

      Args:
          user_id (str): The unique ID of the user to retrieve.

      Returns:
          User or None: The User object if found, otherwise None.
      """
      user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
      if user_data:
        return User(str(user_data["_id"]), user_data["username"], user_data["password"])
      
      return None
    
    @staticmethod
    def get_by_username(username):
      """
      Retrieve a user from the database by their username.

      Args:
          username (str): The username of the user to retrieve.

      Returns:
          User or None: The User object if found, otherwise None.
      """
      user_data = mongo.db.users.find_one({"username": username})
      
      if user_data:
          return User(str(user_data["_id"]), user_data["username"], user_data["password"])
      return None
    
    @staticmethod
    def create(username, password):
      """
      Create a new user in the database.

      Args:
          username (str): The username of the new user.
          password (str): The plaintext password of the new user.

      Returns:
          User: The newly created User object.
      """
      hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
      
      user_id = mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password
      }).inserted_id
      
      return User(str(user_id), username, hashed_password)
    
    def check_password(self, password):
      """
      Check if the provided password matches the stored hashed password.

      Args:
          password (str): The plaintext password to check.

      Returns:
          bool: True if the password matches, False otherwise.
      """
      return check_password_hash(self.password, password)