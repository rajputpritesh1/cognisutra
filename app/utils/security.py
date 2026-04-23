"""
Security utilities for the application
"""

import hmac
import hashlib
import secrets
import string
from urllib.parse import urlencode

class PasswordManager:
    """Password management utilities"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using Werkzeug (called automatically by User model)"""
        from werkzeug.security import generate_password_hash
        return generate_password_hash(password, method='pbkdf2:sha256')
    
    @staticmethod
    def verify_password(hashed_password, password):
        """Verify password against hash"""
        from werkzeug.security import check_password_hash
        return check_password_hash(hashed_password, password)
    
    @staticmethod
    def generate_password(length=12):
        """Generate random strong password"""
        if length < 8:
            length = 8
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        return password
    
    @staticmethod
    def check_password_strength(password):
        """Check password strength and return score"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        if any(c.isupper() for c in password):
            score += 1
        
        if any(c.islower() for c in password):
            score += 1
        
        if any(c.isdigit() for c in password):
            score += 1
        
        if any(c in string.punctuation for c in password):
            score += 1
        
        strength = {
            0: 'Very Weak',
            1: 'Weak',
            2: 'Fair',
            3: 'Good',
            4: 'Strong',
            5: 'Very Strong',
            6: 'Very Strong',
            7: 'Very Strong'
        }
        
        return {
            'score': score,
            'strength': strength.get(score, 'Unknown'),
            'max_score': 7
        }

class TokenManager:
    """Token generation and verification"""
    
    @staticmethod
    def generate_token(length=32):
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_verification_token(data, secret_key):
        """Generate HMAC token for verification"""
        return hmac.new(
            secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def verify_token(data, token, secret_key):
        """Verify HMAC token"""
        expected_token = hmac.new(
            secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(token, expected_token)

class CSRFManager:
    """CSRF token management (Flask-WTF handles this)"""
    
    @staticmethod
    def generate_csrf_token():
        """Generate new CSRF token (Flask-WTF handles this automatically)"""
        from flask import session
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_urlsafe(32)
        return session['_csrf_token']

class EncryptionHelper:
    """Encryption utilities"""
    
    @staticmethod
    def hash_email(email):
        """Hash email for privacy"""
        return hashlib.sha256(email.lower().encode()).hexdigest()
    
    @staticmethod
    def obfuscate_email(email):
        """Obfuscate email for display"""
        parts = email.split('@')
        if len(parts) != 2:
            return email
        
        username, domain = parts
        
        # Show first and last char of username, hide middle
        if len(username) <= 2:
            obfuscated_username = username[0] + '*' if len(username) > 1 else username
        else:
            obfuscated_username = username[0] + '*' * (len(username) - 2) + username[-1]
        
        return f'{obfuscated_username}@{domain}'
    
    @staticmethod
    def hash_phone(phone):
        """Hash phone number"""
        return hashlib.sha256(phone.encode()).hexdigest()

class RateLimitHelper:
    """Rate limiting helpers"""
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        if request.environ.get('HTTP_CF_CONNECTING_IP'):
            return request.environ.get('HTTP_CF_CONNECTING_IP')
        elif request.environ.get('HTTP_X_FORWARDED_FOR'):
            return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
        else:
            return request.remote_addr

class InputSanitizer:
    """Input sanitization utilities"""
    
    @staticmethod
    def sanitize_html(html_string):
        """Sanitize HTML input (basic)"""
        import re
        
        # Remove dangerous tags
        dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form']
        for tag in dangerous_tags:
            html_string = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_string, flags=re.IGNORECASE | re.DOTALL)
            html_string = re.sub(f'<{tag}[^>]*/>', '', html_string, flags=re.IGNORECASE)
        
        return html_string
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for safe storage"""
        import re
        
        # Keep only alphanumeric, dash, and underscore
        filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        
        # Limit length
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename

class SecurityHeaders:
    """Security headers to add to responses"""
    
    @staticmethod
    def get_security_headers():
        """Get security headers dict"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
    
    @staticmethod
    def apply_security_headers(response):
        """Apply security headers to Flask response"""
        for header, value in SecurityHeaders.get_security_headers().items():
            response.headers[header] = value
        
        return response
