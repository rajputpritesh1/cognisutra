import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Tool, Blog, Subscription, Bookmark, ContactMessage, Freebie, BlogComment

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

# Shell context for Flask CLI
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Tool': Tool,
        'Blog': Blog,
        'Subscription': Subscription,
        'Bookmark': Bookmark,
        'ContactMessage': ContactMessage,
        'Freebie': Freebie,
        'BlogComment': BlogComment
    }

# CLI Commands
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command()
def create_admin():
    """Create an admin user."""
    import click
    
    email = click.prompt('Admin email')
    username = click.prompt('Admin username')
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    
    if User.query.filter_by(email=email).first():
        print('Email already exists.')
        return
    
    if User.query.filter_by(username=username).first():
        print('Username already exists.')
        return
    
    admin = User(email=email, username=username, is_admin=True)
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    print(f'Admin user {email} created successfully.')

@app.cli.command()
def seed_demo_data():
    """Seed database with demo data."""
    from app.models import Tool, Blog, Freebie
    from datetime import datetime
    
    # Sample tools
    tools_data = [
        {
            'name': 'Focus Timer Pro',
            'slug': 'focus-timer-pro',
            'description': 'Pomodoro timer with team analytics',
            'category': 'productivity',
            'price': '₹149/mo',
            'revenue_model': 'Freemium',
            'effort': '1 day',
            'features': ['5 timers/day', 'Unlimited + Analytics', 'Team view'],
            'tech_stack': ['HTML/JS', 'localStorage']
        },
        {
            'name': 'Invoice Generator',
            'slug': 'invoice-generator',
            'description': 'Create and manage invoices instantly',
            'category': 'finance',
            'price': '₹299/mo',
            'revenue_model': 'Freemium',
            'effort': '3 days',
            'features': ['Create invoices', 'GST calculation', 'PDF export'],
            'tech_stack': ['React', 'jsPDF', 'localStorage']
        },
    ]
    
    for tool_data in tools_data:
        if not Tool.query.filter_by(slug=tool_data['slug']).first():
            tool = Tool(**tool_data, is_published=True)
            db.session.add(tool)
    
    # Sample blogs
    blogs_data = [
        {
            'title': 'How to Build Your First Micro SaaS',
            'slug': 'how-to-build-first-micro-saas',
            'excerpt': 'A guide to building your first micro SaaS product',
            'content': '<h1>How to Build Your First Micro SaaS</h1><p>Building a micro SaaS is more accessible than ever...</p>',
            'category': 'tutorial',
            'is_published': True,
            'published_at': datetime.utcnow()
        },
        {
            'title': 'Top 10 Micro SaaS Ideas in 2024',
            'slug': 'top-10-micro-saas-ideas-2024',
            'excerpt': 'Discover the most profitable micro SaaS ideas',
            'content': '<h1>Top 10 Micro SaaS Ideas</h1><p>Here are the best performing micro SaaS products...</p>',
            'category': 'ideas',
            'is_published': True,
            'published_at': datetime.utcnow()
        },
    ]
    
    for blog_data in blogs_data:
        if not Blog.query.filter_by(slug=blog_data['slug']).first():
            blog = Blog(**blog_data)
            db.session.add(blog)
    
    # Sample freebies
    freebies_data = [
        {
            'title': 'JSON Formatter',
            'description': 'Format and validate JSON online',
            'category': 'developer-tools',
            'url': 'https://jsonlint.com',
            'source': 'JSONLint',
            'is_published': True
        },
        {
            'title': 'Color Palette Generator',
            'description': 'Generate beautiful color palettes',
            'category': 'design-tools',
            'url': 'https://coolors.co',
            'source': 'Coolors',
            'is_published': True
        },
    ]
    
    for freebie_data in freebies_data:
        if not Freebie.query.filter_by(url=freebie_data['url']).first():
            freebie = Freebie(**freebie_data)
            db.session.add(freebie)
    
    db.session.commit()
    print('Demo data seeded successfully.')

if __name__ == '__main__':
    app.run(debug=True)
