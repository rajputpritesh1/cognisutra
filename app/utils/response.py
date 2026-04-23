"""
API Response utilities for consistent response formatting
"""

from flask import jsonify

class APIResponse:
    """Standardized API response format"""
    
    @staticmethod
    def success(data=None, message='Success', status_code=200):
        """Return successful API response"""
        response = {
            'success': True,
            'message': message,
            'data': data
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message='Error', error_code=None, status_code=400, details=None):
        """Return error API response"""
        response = {
            'success': False,
            'message': message,
            'error_code': error_code
        }
        if details:
            response['details'] = details
        
        return jsonify(response), status_code
    
    @staticmethod
    def paginated(items, total, page, per_page, message='Success'):
        """Return paginated API response"""
        response = {
            'success': True,
            'message': message,
            'data': items,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        }
        return jsonify(response), 200
    
    @staticmethod
    def created(data, message='Resource created successfully'):
        """Return created response"""
        return APIResponse.success(data, message, 201)
    
    @staticmethod
    def bad_request(message='Bad request', details=None):
        """Return bad request response"""
        return APIResponse.error(message, 'BAD_REQUEST', 400, details)
    
    @staticmethod
    def unauthorized(message='Unauthorized'):
        """Return unauthorized response"""
        return APIResponse.error(message, 'UNAUTHORIZED', 401)
    
    @staticmethod
    def forbidden(message='Forbidden'):
        """Return forbidden response"""
        return APIResponse.error(message, 'FORBIDDEN', 403)
    
    @staticmethod
    def not_found(message='Resource not found'):
        """Return not found response"""
        return APIResponse.error(message, 'NOT_FOUND', 404)
    
    @staticmethod
    def conflict(message='Resource already exists'):
        """Return conflict response"""
        return APIResponse.error(message, 'CONFLICT', 409)
    
    @staticmethod
    def server_error(message='Internal server error'):
        """Return server error response"""
        return APIResponse.error(message, 'SERVER_ERROR', 500)
