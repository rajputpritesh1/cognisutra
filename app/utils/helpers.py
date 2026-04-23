"""
Helper functions for common tasks
"""

from flask import url_for, current_app, render_template_string
from datetime import datetime, timedelta
import json

def format_date(date_obj, format='%B %d, %Y'):
    """Format datetime object to string"""
    if not date_obj:
        return ''
    
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj)
    
    return date_obj.strftime(format)

def time_ago(date_obj):
    """Convert datetime to 'time ago' format"""
    if not date_obj:
        return ''
    
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj)
    
    now = datetime.utcnow()
    diff = now - date_obj
    
    if diff.days > 365:
        return f'{diff.days // 365} year{"s" if diff.days // 365 != 1 else ""} ago'
    elif diff.days > 30:
        return f'{diff.days // 30} month{"s" if diff.days // 30 != 1 else ""} ago'
    elif diff.days > 0:
        return f'{diff.days} day{"s" if diff.days != 1 else ""} ago'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    else:
        return 'just now'

def truncate_text(text, length=100, suffix='...'):
    """Truncate text to specified length"""
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    return text[:length].rsplit(' ', 1)[0] + suffix

def format_currency(amount, currency='₹'):
    """Format amount as currency"""
    if not amount:
        return f'{currency}0'
    
    try:
        return f'{currency}{float(amount):,.2f}'
    except (ValueError, TypeError):
        return f'{currency}0'

def slugify(text):
    """Convert text to URL-friendly slug"""
    if not text:
        return ''
    
    text = text.lower().strip()
    text = ''.join(c if c.isalnum() or c in '-_ ' else '' for c in text)
    text = '-'.join(text.split())
    
    return text

def get_page_from_request(request, default=1):
    """Get page number from request args"""
    try:
        page = int(request.args.get('page', default))
        return max(1, page)
    except (ValueError, TypeError):
        return default

def get_search_from_request(request, default=''):
    """Get search query from request args"""
    return request.args.get('q', default, type=str).strip()

def get_category_from_request(request, default=''):
    """Get category filter from request args"""
    return request.args.get('category', default, type=str).strip()

def safe_json_parse(json_string, default=None):
    """Safely parse JSON string"""
    try:
        return json.loads(json_string) if json_string else default
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_stringify(obj, default=None):
    """Safely convert object to JSON string"""
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return default

def get_gravatar_url(email, size=80):
    """Get Gravatar URL for email"""
    from app.utils.security import EncryptionHelper
    
    email_hash = EncryptionHelper.hash_email(email)
    return f'https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon'

def send_email(subject, recipients, body_html, body_text=None):
    """
    Send email (requires Flask-Mail configuration)
    """
    try:
        from flask_mail import Mail, Message
        
        mail = Mail(current_app)
        
        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            html=body_html,
            body=body_text or 'Please view this email in HTML mode'
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f'Email sending failed: {str(e)}')
        return False

def generate_pagination_links(page, total_pages, per_page=10):
    """Generate pagination links"""
    links = {}
    
    if page > 1:
        links['first'] = 1
        links['prev'] = page - 1
    
    if page < total_pages:
        links['next'] = page + 1
        links['last'] = total_pages
    
    return links

def get_file_extension(filename):
    """Get file extension"""
    if not filename or '.' not in filename:
        return ''
    
    return filename.rsplit('.', 1)[1].lower()

def is_allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension"""
    return '.' in filename and get_file_extension(filename) in allowed_extensions

def get_total_pages(total_items, per_page):
    """Calculate total pages"""
    return (total_items + per_page - 1) // per_page

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def format_bytes(bytes_size):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f'{bytes_size:.2f} {unit}'
        bytes_size /= 1024
    
    return f'{bytes_size:.2f} TB'

def get_user_agent(request):
    """Get user agent from request"""
    return request.headers.get('User-Agent', 'Unknown')

def get_referer(request):
    """Get referer from request"""
    return request.headers.get('Referer', '')

def is_mobile(request):
    """Check if request is from mobile device"""
    user_agent = get_user_agent(request).lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'tablet']
    
    return any(keyword in user_agent for keyword in mobile_keywords)

def build_query_string(params):
    """Build query string from params dict"""
    return '&'.join(f'{k}={v}' for k, v in params.items() if v)

def merge_dicts(*dicts):
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result

def group_by(items, key_func):
    """Group list items by key function"""
    groups = {}
    for item in items:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    
    return groups
