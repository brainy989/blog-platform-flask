# Blog Application

This is a simple blog application built with Flask, Flask-Login, and Flask-PyMongo. It allow users to sign up, log in, create, update, and delete blog posts. The application also includes features to view all posts and view individual posts.

## Design Decisions

### Structure

- **Blueprints**: The application is divided into blueprints to separate authentication (`auth`) and main application logic (`main`). This modularity improves code organization and maintainability.
- **Models**: The `User` and `BlogPost` models are separated from the application logic. This separation follows the MVC pattern and makes the code cleaner and more manageable.
- **Database**: MongoDB is used for data storage due to its flexibility and ease of integration with Flask through Flask-PyMongo.

### Security

- **Password Hashing**: Passwords are hashed using `werkzeug.security`'s `generate_password_hash` and `check_password_hash` to ensure that passwords are stored securely.
- **Login Management**: Flask-Login is used to handle user session management.

### Trade-Offs
- **No Front-End Framework**: The application does not include a front-end framework. While this keeps the project simple and focused on the backend, it also means that the user interface is not as polished as it could be.
- **Basic Error Handling**: Error handling is minimal. In a production environment, more comprehensive error handling and logging would be necessary.
- **Limited Features**: The application includes basic CRUD operations for blog posts and user authentication.

## Potential Improvements

Given more time, the following features and improvements could be implemented:

- **Front-End Integration**: Integrate a front-end framework such as React or Vue.js.
- **User Roles**: Implement user roles and permissions to allow for more fine-grained access control.
- **Rich Text Editor**: Add a rich text editor for creating and editing blog posts to allow for more complex content formatting.
- **Comments and Likes**: Add functionality for users to comment on and like blog posts to increase user engagement.

## Setup Instructions

### Prerequisites

- Python 3.6+
- MongoDB
- pip (Python package installer)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/blog-application.git
    cd blog-application
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add the following variables:
        ```
        MONGO_URI=mongodb://localhost:27017/blogdb
        SECRET_KEY=your_secret_key

        TEST_MONGO_URI=mongodb://localhost:27017/blogdb_test
        TEST_SECRET_KEY=your_test_secret_key
        ```

5. ***Run the application***:
    ```bash
    flask run
    ```

    or

    ```bash
    python3 run.py
    ```