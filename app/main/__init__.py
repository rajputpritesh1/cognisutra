from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import db, Tool, Blog, Bookmark, ContactMessage
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import uuid

main_bp = Blueprint('main', __name__)

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=255)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

@main_bp.route('/')
def index():
    """Landing page."""
    featured_tools = Tool.query.filter_by(is_published=True).limit(6).all()
    recent_blogs = Blog.query.filter_by(is_published=True).order_by(Blog.published_at.desc()).limit(3).all()
    
    return render_template('main/index.html', featured_tools=featured_tools, recent_blogs=recent_blogs)

@main_bp.route('/tools')
def tools():
    """Tools listing page."""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    query = Tool.query.filter_by(is_published=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            (Tool.name.ilike(f'%{search}%')) |
            (Tool.description.ilike(f'%{search}%'))
        )
    
    tools = query.order_by(Tool.created_at.desc()).paginate(page=page, per_page=12)
    categories = db.session.query(Tool.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('main/tools.html', tools=tools, categories=categories, search=search, category=category)

@main_bp.route('/tools/<tool_id>')
def tool_detail(tool_id):
    """Single tool page."""
    tool = Tool.query.get_or_404(tool_id)
    
    if not tool.is_published and (not current_user.is_authenticated or not current_user.is_admin):
        return render_template('errors/404.html'), 404
    
    bookmarked = False
    if current_user.is_authenticated:
        bookmarked = Bookmark.query.filter_by(user_id=current_user.id, tool_id=tool_id).first() is not None
    
    return render_template('main/tool_detail.html', tool=tool, bookmarked=bookmarked)

@main_bp.route('/tools/<tool_id>/bookmark', methods=['POST'])
@login_required
def bookmark_tool(tool_id):
    """Bookmark a tool."""
    tool = Tool.query.get_or_404(tool_id)
    
    existing = Bookmark.query.filter_by(user_id=current_user.id, tool_id=tool_id).first()
    
    if existing:
        db.session.delete(existing)
        bookmarked = False
        message = 'Removed from bookmarks'
    else:
        bookmark = Bookmark(user_id=current_user.id, tool_id=tool_id)
        db.session.add(bookmark)
        bookmarked = True
        message = 'Added to bookmarks'
    
    db.session.commit()
    return jsonify({'bookmarked': bookmarked, 'message': message})

@main_bp.route('/blogs')
def blogs():
    """Blogs listing page."""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    query = Blog.query.filter_by(is_published=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            (Blog.title.ilike(f'%{search}%')) |
            (Blog.content.ilike(f'%{search}%'))
        )
    
    blogs = query.order_by(Blog.published_at.desc()).paginate(page=page, per_page=10)
    categories = db.session.query(Blog.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('main/blogs.html', blogs=blogs, categories=categories, search=search, category=category)

@main_bp.route('/blogs/<blog_id>')
def blog_detail(blog_id):
    """Single blog page."""
    blog = Blog.query.get_or_404(blog_id)
    
    if not blog.is_published and (not current_user.is_authenticated or not current_user.is_admin):
        return render_template('errors/404.html'), 404
    
    recent_blogs = Blog.query.filter_by(is_published=True).filter(Blog.id != blog_id).order_by(Blog.published_at.desc()).limit(5).all()
    
    return render_template('main/blog_detail.html', blog=blog, recent_blogs=recent_blogs)

@main_bp.route('/freebies')
def freebies():
    """Freebies listing page."""
    from app.models import Freebie
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    
    query = Freebie.query.filter_by(is_published=True)
    
    if category:
        query = query.filter_by(category=category)
    
    freebies = query.order_by(Freebie.created_at.desc()).paginate(page=page, per_page=20)
    categories = db.session.query(Freebie.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('main/freebies.html', freebies=freebies, categories=categories, category=category)

@main_bp.route('/pricing')
def pricing():
    """Pricing page."""
    return render_template('main/pricing.html')

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html')

@main_bp.route('/devspace')
def devspace():
    """Developer space page."""
    return render_template('main/devspace.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page."""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            flash('Thank you for your message. We will get back to you soon!', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('main/contact.html', form=form)

# --- SEO URLs ---

@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap."""
    from flask import Response
    
    base_url = request.host_url.rstrip('/')
    urls = [
        {'url': base_url, 'priority': 1.0},
        {'url': f'{base_url}/tools', 'priority': 0.9},
        {'url': f'{base_url}/blogs', 'priority': 0.9},
        {'url': f'{base_url}/freebies', 'priority': 0.8},
        {'url': f'{base_url}/pricing', 'priority': 0.8},
        {'url': f'{base_url}/about', 'priority': 0.7},
        {'url': f'{base_url}/contact', 'priority': 0.7},
    ]
    
    # Add tool URLs
    for tool in Tool.query.filter_by(is_published=True).all():
        urls.append({'url': f'{base_url}/tools/{tool.id}', 'priority': 0.6})
    
    # Add blog URLs
    for blog in Blog.query.filter_by(is_published=True).all():
        urls.append({'url': f'{base_url}/blogs/{blog.id}', 'priority': 0.6})
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url_item in urls:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{url_item["url"]}</loc>\n'
        sitemap_xml += f'    <priority>{url_item["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    return Response(sitemap_xml, mimetype='application/xml')

@main_bp.route('/robots.txt')
def robots():
    """Generate robots.txt."""
    from flask import Response
    
    robots_txt = 'User-agent: *\n'
    robots_txt += 'Allow: /\n'
    robots_txt += f'Sitemap: {request.host_url.rstrip("/")}/sitemap.xml\n'
    
    return Response(robots_txt, mimetype='text/plain')
