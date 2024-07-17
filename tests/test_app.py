import os
import sys
import unittest
from dotenv import load_dotenv
from flask import json

# Add the parent directory to the system path to enable imports
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, ".."))

from app import create_app, mongo

# Load environment variables from a .env file
load_dotenv()

class BlogTest(unittest.TestCase):
    """
    A class to represent the test suite for the Blog application.
    Inherits from unittest.TestCase to provide testing capabilities.
    """
    
    def setUp(self):
        """
        Set up a test instance of the Flask application and a test client.
        Initialize a clean database before each test.
        """
        self.app = create_app()
        self.app.config["MONGO_URI"] = os.getenv('TEST_MONGO_URI', 'mongodb://localhost:27017/blogdb_test')
        self.app.config["SECRET_KEY"] = os.getenv('TEST_SECRET_KEY', '')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            # Drop all collections and create necessary indexes
            mongo.db.users.drop()
            mongo.db.posts.drop()
            mongo.db.users.create_index("username", unique=True)
    
    def tearDown(self):
        """
        Tear down the test database after each test.
        """
        with self.app.app_context():
            mongo.db.users.drop()
            mongo.db.posts.drop()
    
    def test_user_signup(self):
        """
        Test the user signup functionality.
        """
        response = self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User created successfully', data['message'])
        
    def test_user_login(self):
        """
        Test the user login functionality.
        """
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        response = self.client.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', data['message'])
    
    def test_create_post(self):
        """
        Test the creation of a new blog post.
        """
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.client.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        response = self.client.post('/posts', data=json.dumps({
            'title': 'Test Post',
            'content': 'This is a test post.'
        }), content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)
    
    def test_get_posts(self):
        """
        Test retrieving all blog posts.
        """
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.client.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.client.post('/posts', data=json.dumps({
            'title': 'Test Post',
            'content': 'This is a test post.'
        }), content_type='application/json')
        
        response = self.client.get('/posts')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
    
    def test_get_single_post(self):
        """
        Test retrieving a single blog post by ID.
        """
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.client.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        response = self.client.post('/posts', data=json.dumps({
            'title': 'Test Post',
            'content': 'This is a test post.'
        }), content_type='application/json')
        
        post_id = json.loads(response.data)['id']
        response = self.client.get(f'/posts/{post_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', data)
        self.assertIn('content', data)
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['content'], 'This is a test post.')
    
    def test_update_post(self):
        """
        Test updating a blog post.
        """
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.client.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        response = self.client.post('/posts', data=json.dumps({
            'title': 'Test Post',
            'content': 'This is a test post.'
        }), content_type='application/json')
        
        post_id = json.loads(response.data)['id']
        response = self.client.put(f'/posts/{post_id}', data=json.dumps({
            'title': 'Updated Test Post',
            'content': 'This is an updated test post.'
        }), content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Post updated', data['success'])
    
    def test_delete_post(self):
        """
        Test deleting a blog post.
        """
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        self.client.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        
        response = self.client.post('/posts', data=json.dumps({
            'title': 'Test Post',
            'content': 'This is a test post.'
        }), content_type='application/json')
        
        post_id = json.loads(response.data)['id']
        response = self.client.delete(f'/posts/{post_id}')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Post deleted', data['success'])

if __name__ == '__main__':
    unittest.main()