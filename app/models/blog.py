from bson.objectid import ObjectId
from .. import mongo

class BlogPost:
    @staticmethod
    def create_post(data):
        """
        Create a new blog post in the database.

        Args:
            data (dict): The data for the new blog post.

        Returns:
            str: The ID of the newly created post as a string.
        """
        post_id = mongo.db.posts.insert_one(data).inserted_id
        return str(post_id)
    
    @staticmethod
    def get_posts():
        """
        Retrieve all blog posts from the database.

        Returns:
            list: A list of all blog posts with their IDs converted to strings.
        """
        posts = mongo.db.posts.find()
        result = []
        for post in posts:
            post['_id'] = str(post['_id'])  # Convert ObjectId to string
            result.append(post)
        
        return result
        
    @staticmethod
    def get_post(post_id):
        """
        Retrieve a single blog post by its ID.

        Args:
            post_id (str): The ID of the blog post to retrieve.

        Returns:
            dict or None: The blog post if found, otherwise None.
        """
        post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
        if post:
            post['_id'] = str(post['_id'])
            return post
        else:
            return None
    
    @staticmethod
    def update_post(post_id, data):
        """
        Update a blog post by its ID.

        Args:
            post_id (str): The ID of the blog post to update.
            data (dict): The new data for the blog post.

        Returns:
            bool: True if the post was updated, False otherwise.
        """
        result = mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": data})
        return result.modified_count > 0
    
    @staticmethod
    def delete_post(post_id):
        """
        Delete a blog post by its ID.

        Args:
            post_id (str): The ID of the blog post to delete.

        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        result = mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
        return result.deleted_count > 0