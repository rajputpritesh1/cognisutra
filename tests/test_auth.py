"""
Unit tests for authentication
"""

import pytest

class TestRegistration:
    """Test user registration"""
    
    def test_register_valid_user(self, auth_client):
        """Test successful registration"""
        response = auth_client.register(
            email='newuser@example.com',
            username='newuser',
            password='SecurePass123',
            password_confirm='SecurePass123',
            first_name='New',
            last_name='User'
        )
        assert response.status_code == 200
    
    def test_register_duplicate_email(self, client, auth_user):
        """Test registration with duplicate email"""
        response = client.post('/auth/register', data={
            'email': 'test@example.com',
            'username': 'newuser',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'first_name': 'New',
            'last_name': 'User'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_register_password_mismatch(self, client):
        """Test registration with mismatched passwords"""
        response = client.post('/auth/register', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'SecurePass123',
            'password_confirm': 'DifferentPass123',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        assert response.status_code == 200

class TestLogin:
    """Test user login"""
    
    def test_login_valid_credentials(self, auth_client, auth_user):
        """Test login with valid credentials"""
        response = auth_client.login('test@example.com', 'TestPass123')
        assert response.status_code == 200
    
    def test_login_invalid_email(self, auth_client):
        """Test login with invalid email"""
        response = auth_client.login('nonexistent@example.com', 'password')
        assert response.status_code == 200
    
    def test_login_invalid_password(self, auth_client, auth_user):
        """Test login with invalid password"""
        response = auth_client.login('test@example.com', 'WrongPassword')
        assert response.status_code == 200
    
    def test_logout(self, auth_client, auth_user):
        """Test user logout"""
        auth_client.login('test@example.com', 'TestPass123')
        response = auth_client.logout()
        assert response.status_code == 200

class TestAuthPages:
    """Test auth-related pages"""
    
    def test_register_page_get(self, client):
        """Test GET register page"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data
    
    def test_login_page_get(self, client):
        """Test GET login page"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
