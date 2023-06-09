FastAPI Product API
This is a sample FastAPI project that provides an API for managing products. It allows users to perform CRUD operations (Create, Read, Update, Delete) on products and categories.

Features
User authentication using JWT (JSON Web Tokens)
Secure password hashing with bcrypt
API endpoints for creating, reading, updating, and deleting products
API endpoints for retrieving a list of products and categories
Unit tests for API endpoints
Requirements
Python 3.7+
FastAPI
PyJWT
Passlib
bcrypt
Pydantic
MySQL Connector/Python
Requests (for unit testing)
Installation
Clone the repository:
git clone https://github.com/VikasRimmalapudi7/rest_api
Install the required dependencies:
pip install -r requirements.txt
Set up the database:
Create a MySQL database and update the database connection details in database.py.
Run the database migrations using the provided SQL script (migrations.sql) or your preferred migration tool.
Start the FastAPI server:
uvicorn main:app --reload
The API will be available at http://localhost:8000.
Running Unit Tests
The project includes unit tests for the API endpoints. To run the tests:
python -m unittest discover tests
