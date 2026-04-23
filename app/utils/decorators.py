"""
Custom decorators for authentication, authorization, and utilities
"""

from functools import wraps
from flask import redirect, url_for, abort, current_app
from flask_login import current_user
import time
from collections import defaultdict

# Rate limiting store (in production, use Redis)
_rate_limit_store = defaultdict(lambda: defaultdict(list))

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin:
            abort(403)
        
        return f(*args, **kwargs)
    
    return decorated_function

def login_required_custom(f):
    """Decorator to require login (custom implementation)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def guest_only(f):
    """Decorator to allow only guest users"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit(max_requests=10, time_window=60):
    """
    Rate limiting decorator
    max_requests: number of requests allowed
    time_window: time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = current_user.id if current_user.is_authenticated else 'anonymous'
            endpoint = f.__name__
            
            current_time = time.time()
            
            # Clean old requests
            _rate_limit_store[user_id][endpoint] = [
                req_time for req_time in _rate_limit_store[user_id][endpoint]
                if current_time - req_time < time_window
            ]
            
            # Check limit
            if len(_rate_limit_store[user_id][endpoint]) >= max_requests:
                abort(429)  # Too Many Requests
            
            # Add current request
            _rate_limit_store[user_id][endpoint].append(current_time)
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def require_ajax(f):
    """Decorator to require AJAX request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        
        if not request.is_xhr and not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            abort(400)
        
        return f(*args, **kwargs)
    
    return decorated_function

def log_action(action_name):
    """Decorator to log user actions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.utils.logger import LoggerSetup
            logger = LoggerSetup.get_logger(__name__)
            
            user_id = current_user.id if current_user.is_authenticated else 'anonymous'
            logger.info(f'Action: {action_name} by user {user_id}')
            
            try:
                result = f(*args, **kwargs)
                logger.info(f'Action completed: {action_name}')
                return result
            except Exception as e:
                logger.error(f'Action failed: {action_name} - {str(e)}')
                raise
        
        return decorated_function
    
    return decorator

def require_roles(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            # Check if user has required role(s)
            user_has_role = False
            for role in roles:
                if role == 'admin' and current_user.is_admin:
                    user_has_role = True
                elif role == 'user' and current_user.is_authenticated:
                    user_has_role = True
            
            if not user_has_role:
                abort(403)
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def cache_view(timeout=300):
    """Decorator to cache view responses"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, make_response
            from time import time as time_func
            
            # Generate cache key
            cache_key = f'{f.__name__}:{request.path}:{request.args}'
            
            # For simplicity, caching is not implemented here
            # In production, use Flask-Caching
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def handle_errors(f):
    """Decorator to handle common errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            from app.utils.logger import LoggerSetup
            logger = LoggerSetup.get_logger(__name__)
            logger.error(f'Error in {f.__name__}: {str(e)}')
            abort(500)
        
        return decorated_function
    
    return decorator

def validate_form(form_class):
    """Decorator to validate form before passing to handler"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            form = form_class()
            
            if form.validate_on_submit():
                kwargs['form'] = form
                return f(*args, **kwargs)
            else:
                # Handle form errors
                from flask import render_template, flash
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'{field}: {error}', 'error')
                
                abort(400)
        
        return decorated_function
    
    return decorator
