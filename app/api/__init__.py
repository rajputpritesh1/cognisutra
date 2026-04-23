"""
API Blueprint for REST endpoints
"""

from flask import Blueprint, request, current_app
from flask_login import current_user, login_required
from app.models import db, Tool, Blog, Freebie, User, Bookmark
from app.utils import APIResponse, Validators, Query
from app.utils.decorators import admin_required, rate_limit
import json

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# ======================
# Tools API
# ======================

@api_bp.route('/tools', methods=['GET'])
@rate_limit(max_requests=30, time_window=60)
def get_tools():
    """Get all published tools with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category', type=str)
        search = request.args.get('search', type=str)
        
        # Validate pagination
        page = max(1, page)
        per_page = min(100, max(1, per_page))
        
        query = Tool.query.filter_by(is_published=True)
        
        # Filter by category
        if category and Validators.validate_slug(category):
            query = query.filter_by(category=category)
        
        # Search
        if search and len(search) >= 2:
            search_term = f'%{search}%'
            query = query.filter(
                (Tool.name.ilike(search_term)) |
                (Tool.description.ilike(search_term))
            )
        
        total = query.count()
        tools = query.paginate(page=page, per_page=per_page)
        
        data = [{
            'id': str(tool.id),
            'name': tool.name,
            'slug': tool.slug,
            'description': tool.description,
            'category': tool.category,
            'price': tool.price,
            'revenue_model': tool.revenue_model
        } for tool in tools.items]
        
        return APIResponse.paginated(
            items=data,
            total=total,
            page=page,
            per_page=per_page
        )
    
    except Exception as e:
        current_app.logger.error(f'Error fetching tools: {str(e)}')
        return APIResponse.server_error()

@api_bp.route('/tools/<tool_id>', methods=['GET'])
def get_tool(tool_id):
    """Get single tool details"""
    try:
        tool = Tool.query.filter_by(id=tool_id, is_published=True).first()
        
        if not tool:
            return APIResponse.not_found('Tool not found')
        
        data = {
            'id': str(tool.id),
            'name': tool.name,
            'slug': tool.slug,
            'description': tool.description,
            'long_description': tool.long_description,
            'category': tool.category,
            'price': tool.price,
            'revenue_model': tool.revenue_model,
            'features': tool.features,
            'tech_stack': tool.tech_stack,
            'created_at': tool.created_at.isoformat(),
            'bookmarks_count': Bookmark.query.filter_by(tool_id=tool.id).count()
        }
        
        return APIResponse.success(data=data, message='Tool retrieved successfully')
    
    except Exception as e:
        current_app.logger.error(f'Error fetching tool: {str(e)}')
        return APIResponse.server_error()

@api_bp.route('/tools', methods=['POST'])
@admin_required
def create_tool():
    """Create new tool (admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return APIResponse.bad_request('No data provided')
        
        # Validate required fields
        required_fields = ['name', 'slug', 'description', 'category']
        for field in required_fields:
            if not data.get(field):
                return APIResponse.bad_request(f'Missing required field: {field}')
        
        # Check if tool already exists
        if Tool.query.filter_by(slug=data['slug']).first():
            return APIResponse.conflict('Tool with this slug already exists')
        
        # Create tool
        tool = Tool(
            name=data['name'],
            slug=data['slug'],
            description=data['description'],
            long_description=data.get('long_description'),
            category=data['category'],
            price=data.get('price', 'Free'),
            revenue_model=data.get('revenue_model', 'Freemium'),
            features=data.get('features', []),
            tech_stack=data.get('tech_stack', []),
            is_published=data.get('is_published', False)
        )
        
        db.session.add(tool)
        db.session.commit()
        
        return APIResponse.created(
            data={'id': str(tool.id)},
            message='Tool created successfully'
        )
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating tool: {str(e)}')
        return APIResponse.server_error()

# ======================
# Blogs API
# ======================

@api_bp.route('/blogs', methods=['GET'])
@rate_limit(max_requests=30, time_window=60)
def get_blogs():
    """Get all published blogs with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category', type=str)
        
        page = max(1, page)
        per_page = min(50, max(1, per_page))
        
        query = Blog.query.filter_by(is_published=True).order_by(Blog.published_at.desc())
        
        if category:
            query = query.filter_by(category=category)
        
        total = query.count()
        blogs = query.paginate(page=page, per_page=per_page)
        
        data = [{
            'id': str(blog.id),
            'title': blog.title,
            'slug': blog.slug,
            'excerpt': blog.excerpt,
            'category': blog.category,
            'author': blog.author,
            'published_at': blog.published_at.isoformat() if blog.published_at else None
        } for blog in blogs.items]
        
        return APIResponse.paginated(
            items=data,
            total=total,
            page=page,
            per_page=per_page
        )
    
    except Exception as e:
        current_app.logger.error(f'Error fetching blogs: {str(e)}')
        return APIResponse.server_error()

@api_bp.route('/blogs/<blog_id>', methods=['GET'])
def get_blog(blog_id):
    """Get single blog details"""
    try:
        blog = Blog.query.filter_by(id=blog_id, is_published=True).first()
        
        if not blog:
            return APIResponse.not_found('Blog not found')
        
        data = {
            'id': str(blog.id),
            'title': blog.title,
            'slug': blog.slug,
            'content': blog.content,
            'excerpt': blog.excerpt,
            'category': blog.category,
            'author': blog.author,
            'tags': blog.tags,
            'published_at': blog.published_at.isoformat() if blog.published_at else None
        }
        
        return APIResponse.success(data=data, message='Blog retrieved successfully')
    
    except Exception as e:
        current_app.logger.error(f'Error fetching blog: {str(e)}')
        return APIResponse.server_error()

# ======================
# Bookmarks API
# ======================

@api_bp.route('/bookmarks', methods=['GET'])
@login_required
def get_bookmarks():
    """Get user bookmarks"""
    try:
        bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
        
        data = [{
            'id': str(bookmark.id),
            'tool_id': str(bookmark.tool_id),
            'tool_name': bookmark.tool.name,
            'created_at': bookmark.created_at.isoformat()
        } for bookmark in bookmarks]
        
        return APIResponse.success(data=data, message='Bookmarks retrieved successfully')
    
    except Exception as e:
        current_app.logger.error(f'Error fetching bookmarks: {str(e)}')
        return APIResponse.server_error()

@api_bp.route('/bookmarks', methods=['POST'])
@login_required
def add_bookmark():
    """Add tool to bookmarks"""
    try:
        data = request.get_json()
        tool_id = data.get('tool_id') if data else None
        
        if not tool_id:
            return APIResponse.bad_request('tool_id is required')
        
        tool = Tool.query.get(tool_id)
        if not tool:
            return APIResponse.not_found('Tool not found')
        
        # Check if already bookmarked
        existing = Bookmark.query.filter_by(
            user_id=current_user.id,
            tool_id=tool_id
        ).first()
        
        if existing:
            return APIResponse.conflict('Tool already bookmarked')
        
        # Add bookmark
        bookmark = Bookmark(user_id=current_user.id, tool_id=tool_id)
        db.session.add(bookmark)
        db.session.commit()
        
        return APIResponse.created(
            data={'id': str(bookmark.id)},
            message='Tool bookmarked successfully'
        )
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error adding bookmark: {str(e)}')
        return APIResponse.server_error()

@api_bp.route('/bookmarks/<bookmark_id>', methods=['DELETE'])
@login_required
def remove_bookmark(bookmark_id):
    """Remove tool from bookmarks"""
    try:
        bookmark = Bookmark.query.filter_by(
            id=bookmark_id,
            user_id=current_user.id
        ).first()
        
        if not bookmark:
            return APIResponse.not_found('Bookmark not found')
        
        db.session.delete(bookmark)
        db.session.commit()
        
        return APIResponse.success(message='Bookmark removed successfully')
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error removing bookmark: {str(e)}')
        return APIResponse.server_error()

# ======================
# Statistics API
# ======================

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get public statistics"""
    try:
        stats = {
            'total_tools': Tool.query.filter_by(is_published=True).count(),
            'total_blogs': Blog.query.filter_by(is_published=True).count(),
            'total_users': User.query.count(),
            'total_bookmarks': Bookmark.query.count()
        }
        
        return APIResponse.success(data=stats, message='Statistics retrieved successfully')
    
    except Exception as e:
        current_app.logger.error(f'Error fetching stats: {str(e)}')
        return APIResponse.server_error()

# ======================
# Health Check
# ======================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return APIResponse.success(
        data={'status': 'healthy', 'version': '1.0'},
        message='API is running'
    )
