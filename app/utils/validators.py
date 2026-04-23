"""
Input validation utilities
"""

import re
from datetime import datetime

class Validators:
    """Input validation helper class"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username (alphanumeric and underscore only, 3-20 chars)"""
        if not username or len(username) < 3 or len(username) > 20:
            return False
        return re.match(r'^[a-zA-Z0-9_]+$', username) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength (min 8 chars, at least 1 uppercase, 1 lowercase, 1 digit)"""
        if not password or len(password) < 8:
            return False
        
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'[0-9]', password)
        
        return bool(has_upper and has_lower and has_digit)
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (10 digits)"""
        pattern = r'^\d{10}$'
        return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None
    
    @staticmethod
    def validate_url(url):
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url, re.IGNORECASE) is not None
    
    @staticmethod
    def validate_slug(slug):
        """Validate slug format (lowercase, alphanumeric, hyphens only)"""
        pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
        return re.match(pattern, slug) is not None
    
    @staticmethod
    def validate_date(date_string, format='%Y-%m-%d'):
        """Validate date string"""
        try:
            datetime.strptime(date_string, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_length(value, min_length=None, max_length=None):
        """Validate string length"""
        length = len(value) if value else 0
        
        if min_length and length < min_length:
            return False
        if max_length and length > max_length:
            return False
        
        return True
    
    @staticmethod
    def sanitize_string(value):
        """Remove potentially harmful characters"""
        if not value:
            return value
        
        # Remove script tags
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
        # Remove event handlers
        value = re.sub(r'on\w+\s*=\s*["\'].*?["\']', '', value, flags=re.IGNORECASE)
        
        return value
    
    @staticmethod
    def validate_json(json_string):
        """Validate JSON string"""
        import json
        try:
            json.loads(json_string)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    @staticmethod
    def validate_required(value):
        """Check if value is not empty"""
        return value is not None and (isinstance(value, str) and len(value.strip()) > 0 or value)
    
    @staticmethod
    def validate_choices(value, choices):
        """Validate value is in choices"""
        return value in choices
    
    @staticmethod
    def validate_integer(value, min_value=None, max_value=None):
        """Validate integer value"""
        try:
            int_value = int(value)
            
            if min_value is not None and int_value < min_value:
                return False
            if max_value is not None and int_value > max_value:
                return False
            
            return True
        except (ValueError, TypeError):
            return False

class FormValidator:
    """Form validation helper"""
    
    def __init__(self):
        self.errors = {}
    
    def add_error(self, field, message):
        """Add validation error"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
    
    def is_valid(self):
        """Check if form has no errors"""
        return len(self.errors) == 0
    
    def get_errors(self):
        """Get all errors"""
        return self.errors
    
    def validate_field(self, field_name, field_value, validators_list):
        """Validate a single field with multiple validators"""
        for validator_name, validator_func, message in validators_list:
            if not validator_func(field_value):
                self.add_error(field_name, message)
        
        return field_name not in self.errors
