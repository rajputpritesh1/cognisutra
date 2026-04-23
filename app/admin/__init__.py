from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import db, User, Tool, Blog, Subscription, ContactMessage
from functools import wraps
from datetime import datetime
import json

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to check if user is admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard."""
    total_users = User.query.count()
    total_tools = Tool.query.count()
    total_blogs = Blog.query.count()
    active_subscriptions = Subscription.query.filter_by(status='active').count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    context = {
        'total_users': total_users,
        'total_tools': total_tools,
        'total_blogs': total_blogs,
        'active_subscriptions': active_subscriptions,
        'unread_messages': unread_messages
    }
    return render_template('admin/dashboard.html', **context)

# --- TOOLS MANAGEMENT ---

@admin_bp.route('/tools')
@login_required
@admin_required
def tools():
    """Manage tools."""
    page = request.args.get('page', 1, type=int)
    tools = Tool.query.paginate(page=page, per_page=20)
    return render_template('admin/tools.html', tools=tools)

@admin_bp.route('/tools/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_tool():
    """Create new tool."""
    if request.method == 'POST':
        try:
            tool = Tool(
                name=request.form.get('name'),
                slug=request.form.get('slug'),
                description=request.form.get('description'),
                long_description=request.form.get('long_description'),
                category=request.form.get('category'),
                price=request.form.get('price'),
                revenue_model=request.form.get('revenue_model'),
                effort=request.form.get('effort'),
                audience=request.form.get('audience'),
                pain_point=request.form.get('pain_point'),
                demo_url=request.form.get('demo_url'),
                github_url=request.form.get('github_url'),
                is_published=request.form.get('is_published') == 'on'
            )
            
            # Parse features and tech_stack as JSON
            features = request.form.get('features', '[]')
            tech_stack = request.form.get('tech_stack', '[]')
            
            try:
                tool.features = json.loads(features) if features else []
                tool.tech_stack = json.loads(tech_stack) if tech_stack else []
            except json.JSONDecodeError:
                flash('Invalid JSON in features or tech_stack', 'error')
                return render_template('admin/create_tool.html')
            
            db.session.add(tool)
            db.session.commit()
            flash(f'Tool "{tool.name}" created successfully.', 'success')
            return redirect(url_for('admin.tools'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating tool: {str(e)}', 'error')
    
    return render_template('admin/create_tool.html')

@admin_bp.route('/tools/<tool_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tool(tool_id):
    """Edit tool."""
    tool = Tool.query.get_or_404(tool_id)
    
    if request.method == 'POST':
        try:
            tool.name = request.form.get('name')
            tool.slug = request.form.get('slug')
            tool.description = request.form.get('description')
            tool.long_description = request.form.get('long_description')
            tool.category = request.form.get('category')
            tool.price = request.form.get('price')
            tool.revenue_model = request.form.get('revenue_model')
            tool.effort = request.form.get('effort')
            tool.audience = request.form.get('audience')
            tool.pain_point = request.form.get('pain_point')
            tool.demo_url = request.form.get('demo_url')
            tool.github_url = request.form.get('github_url')
            tool.is_published = request.form.get('is_published') == 'on'
            
            features = request.form.get('features', '[]')
            tech_stack = request.form.get('tech_stack', '[]')
            
            try:
                tool.features = json.loads(features) if features else []
                tool.tech_stack = json.loads(tech_stack) if tech_stack else []
            except json.JSONDecodeError:
                flash('Invalid JSON in features or tech_stack', 'error')
                return render_template('admin/edit_tool.html', tool=tool)
            
            db.session.commit()
            flash(f'Tool "{tool.name}" updated successfully.', 'success')
            return redirect(url_for('admin.tools'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating tool: {str(e)}', 'error')
    
    return render_template('admin/edit_tool.html', tool=tool)

@admin_bp.route('/tools/<tool_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tool(tool_id):
    """Delete tool."""
    tool = Tool.query.get_or_404(tool_id)
    try:
        db.session.delete(tool)
        db.session.commit()
        flash(f'Tool "{tool.name}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting tool: {str(e)}', 'error')
    
    return redirect(url_for('admin.tools'))

# --- BLOGS MANAGEMENT ---

@admin_bp.route('/blogs')
@login_required
@admin_required
def blogs():
    """Manage blogs."""
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.paginate(page=page, per_page=20)
    return render_template('admin/blogs.html', blogs=blogs)

@admin_bp.route('/blogs/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_blog():
    """Create new blog post."""
    if request.method == 'POST':
        try:
            blog = Blog(
                title=request.form.get('title'),
                slug=request.form.get('slug'),
                content=request.form.get('content'),
                excerpt=request.form.get('excerpt'),
                category=request.form.get('category'),
                featured_image=request.form.get('featured_image'),
                is_published=request.form.get('is_published') == 'on'
            )
            
            if blog.is_published:
                blog.published_at = datetime.utcnow()
            
            tags = request.form.get('tags', '[]')
            try:
                blog.tags = json.loads(tags) if tags else []
            except json.JSONDecodeError:
                blog.tags = []
            
            db.session.add(blog)
            db.session.commit()
            flash(f'Blog post "{blog.title}" created successfully.', 'success')
            return redirect(url_for('admin.blogs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating blog: {str(e)}', 'error')
    
    return render_template('admin/create_blog.html')

@admin_bp.route('/blogs/<blog_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog(blog_id):
    """Edit blog post."""
    blog = Blog.query.get_or_404(blog_id)
    
    if request.method == 'POST':
        try:
            blog.title = request.form.get('title')
            blog.slug = request.form.get('slug')
            blog.content = request.form.get('content')
            blog.excerpt = request.form.get('excerpt')
            blog.category = request.form.get('category')
            blog.featured_image = request.form.get('featured_image')
            blog.is_published = request.form.get('is_published') == 'on'
            
            if blog.is_published and not blog.published_at:
                blog.published_at = datetime.utcnow()
            
            tags = request.form.get('tags', '[]')
            try:
                blog.tags = json.loads(tags) if tags else []
            except json.JSONDecodeError:
                blog.tags = []
            
            db.session.commit()
            flash(f'Blog post "{blog.title}" updated successfully.', 'success')
            return redirect(url_for('admin.blogs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating blog: {str(e)}', 'error')
    
    return render_template('admin/edit_blog.html', blog=blog)

@admin_bp.route('/blogs/<blog_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_blog(blog_id):
    """Delete blog post."""
    blog = Blog.query.get_or_404(blog_id)
    try:
        db.session.delete(blog)
        db.session.commit()
        flash(f'Blog post "{blog.title}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting blog: {str(e)}', 'error')
    
    return redirect(url_for('admin.blogs'))

# --- USERS MANAGEMENT ---

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users."""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for user."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot change your own admin status.', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin status updated for {user.email}.', 'success')
    return redirect(url_for('admin.users'))

# --- MESSAGES MANAGEMENT ---

@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    """Manage contact messages."""
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/messages/<msg_id>/read', methods=['POST'])
@login_required
@admin_required
def mark_message_read(msg_id):
    """Mark message as read."""
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    return jsonify({'success': True})
