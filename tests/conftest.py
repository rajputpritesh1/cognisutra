"""
Testing utilities and fixtures
"""

import pytest
from app import create_app, db
from app.models import User, Tool, Blog
from config import config

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test runner for CLI commands"""
    return app.test_cli_runner()

@pytest.fixture
def auth_user(app):
    """Create authenticated test user"""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        user.set_password('TestPass123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def admin_user(app):
    """Create admin test user"""
    with app.app_context():
        admin = User(
            email='admin@example.com',
            username='adminuser',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('AdminPass123')
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def sample_tool(app):
    """Create sample tool for testing"""
    with app.app_context():
        tool = Tool(
            name='Test Tool',
            slug='test-tool',
            description='Test tool description',
            category='productivity',
            price='Free',
            is_published=True
        )
        db.session.add(tool)
        db.session.commit()
        return tool

@pytest.fixture
def sample_blog(app):
    """Create sample blog for testing"""
    with app.app_context():
        from datetime import datetime
        blog = Blog(
            title='Test Blog Post',
            slug='test-blog-post',
            content='<p>Test blog content</p>',
            excerpt='Test excerpt',
            category='tutorial',
            author='Test Author',
            is_published=True,
            published_at=datetime.utcnow()
        )
        db.session.add(blog)
        db.session.commit()
        return blog

class AuthClient:
    """Helper class for authentication testing"""
    
    def __init__(self, client):
        self.client = client
    
    def login(self, email, password):
        """Login user"""
        return self.client.post('/auth/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)
    
    def logout(self):
        """Logout user"""
        return self.client.post('/auth/logout', follow_redirects=True)
    
    def register(self, email, username, password, password_confirm, first_name, last_name):
        """Register new user"""
        return self.client.post('/auth/register', data={
            'email': email,
            'username': username,
            'password': password,
            'password_confirm': password_confirm,
            'first_name': first_name,
            'last_name': last_name
        }, follow_redirects=True)

@pytest.fixture
def auth_client(client):
    """Create authenticated client helper"""
    return AuthClient(client)

class APITestHelper:
    """Helper class for API testing"""
    
    def __init__(self, client):
        self.client = client
    
    def get_json(self, path):
        """GET request and parse JSON"""
        response = self.client.get(path)
        return response.get_json()
    
    def post_json(self, path, data):
        """POST request with JSON data"""
        response = self.client.post(
            path,
            json=data,
            content_type='application/json'
        )
        return response.get_json()
    
    def put_json(self, path, data):
        """PUT request with JSON data"""
        response = self.client.put(
            path,
            json=data,
            content_type='application/json'
        )
        return response.get_json()
    
    def delete(self, path):
        """DELETE request"""
        response = self.client.delete(path)
        return response.get_json() if response.data else None

@pytest.fixture
def api_helper(client):
    """Create API test helper"""
    return APITestHelper(client)

def assert_response_ok(response):
    """Assert response is successful"""
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

def assert_response_created(response):
    """Assert response is created (201)"""
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True

def assert_response_error(response, status_code):
    """Assert response is error"""
    assert response.status_code == status_code
    data = response.get_json()
    assert data['success'] is False

def assert_response_unauthorized(response):
    """Assert response is unauthorized"""
    assert_response_error(response, 401)

def assert_response_forbidden(response):
    """Assert response is forbidden"""
    assert_response_error(response, 403)

def assert_response_not_found(response):
    """Assert response is not found"""
    assert_response_error(response, 404)

def assert_response_bad_request(response):
    """Assert response is bad request"""
    assert_response_error(response, 400)
