"""
Database utilities and migration helpers for Cognisutra
"""

from app.models import db, User, Tool, Blog, Freebie, ContactMessage
from datetime import datetime
import csv
import json

class DBManager:
    """Database management utilities"""
    
    @staticmethod
    def init_db():
        """Initialize database with all tables"""
        db.create_all()
        return True
    
    @staticmethod
    def drop_db():
        """Drop all tables - WARNING: Destructive"""
        db.drop_all()
        return True
    
    @staticmethod
    def reset_db():
        """Reset database - WARNING: Destructive"""
        DBManager.drop_db()
        DBManager.init_db()
        return True
    
    @staticmethod
    def get_db_stats():
        """Get database statistics"""
        return {
            'users': User.query.count(),
            'tools': Tool.query.count(),
            'blogs': Blog.query.count(),
            'freebies': Freebie.query.count(),
            'messages': ContactMessage.query.count(),
        }

class ImportExport:
    """Import/Export utilities for data migration"""
    
    @staticmethod
    def export_tools_csv(filename='tools_export.csv'):
        """Export all tools to CSV"""
        tools = Tool.query.all()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Category', 'Price', 'Description', 'Published'])
            
            for tool in tools:
                writer.writerow([
                    tool.id,
                    tool.name,
                    tool.category,
                    tool.price,
                    tool.description[:100],
                    'Yes' if tool.is_published else 'No'
                ])
        
        return filename
    
    @staticmethod
    def export_tools_json(filename='tools_export.json'):
        """Export all tools to JSON"""
        tools = Tool.query.all()
        
        data = []
        for tool in tools:
            data.append({
                'id': tool.id,
                'name': tool.name,
                'slug': tool.slug,
                'description': tool.description,
                'category': tool.category,
                'price': tool.price,
                'revenue_model': tool.revenue_model,
                'features': tool.features,
                'is_published': tool.is_published
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    @staticmethod
    def import_tools_json(filename):
        """Import tools from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for item in data:
            # Check if tool already exists
            if not Tool.query.filter_by(slug=item.get('slug')).first():
                tool = Tool(
                    name=item.get('name'),
                    slug=item.get('slug'),
                    description=item.get('description'),
                    long_description=item.get('long_description'),
                    category=item.get('category'),
                    price=item.get('price'),
                    revenue_model=item.get('revenue_model'),
                    features=item.get('features', []),
                    is_published=item.get('is_published', True)
                )
                db.session.add(tool)
                count += 1
        
        db.session.commit()
        return count
    
    @staticmethod
    def export_users_csv(filename='users_export.csv'):
        """Export all users to CSV (excluding passwords)"""
        users = User.query.all()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Username', 'Name', 'Admin', 'Active', 'Joined'])
            
            for user in users:
                writer.writerow([
                    user.email,
                    user.username,
                    f"{user.first_name} {user.last_name}".strip(),
                    'Yes' if user.is_admin else 'No',
                    'Yes' if user.is_active else 'No',
                    user.created_at.strftime('%Y-%m-%d')
                ])
        
        return filename

class Seeder:
    """Database seeding utilities"""
    
    @staticmethod
    def seed_sample_tools():
        """Seed database with sample tools"""
        sample_tools = [
            {
                'name': 'Focus Timer Pro',
                'slug': 'focus-timer-pro',
                'description': 'Pomodoro timer with team analytics and productivity tracking',
                'category': 'productivity',
                'price': '₹149/mo',
                'revenue_model': 'Freemium',
                'effort': '1-2 weeks',
                'audience': 'Remote teams, Students, Freelancers',
                'pain_point': 'Difficulty maintaining focus during work sessions',
                'features': ['Timer with presets', 'Team analytics', 'Daily reports', 'Slack integration'],
                'tech_stack': ['Flask', 'React', 'WebSocket'],
                'is_published': True
            },
            {
                'name': 'Invoice Generator',
                'slug': 'invoice-generator',
                'description': 'Create professional invoices instantly with GST support',
                'category': 'business',
                'price': '₹299/mo',
                'revenue_model': 'Freemium',
                'effort': '3-4 days',
                'audience': 'Freelancers, Small businesses',
                'pain_point': 'Manual invoice creation is time-consuming',
                'features': ['Professional templates', 'GST calculation', 'PDF export', 'Auto-numbering'],
                'tech_stack': ['Flask', 'ReportLab', 'SQLAlchemy'],
                'is_published': True
            },
            {
                'name': 'Email Campaign Manager',
                'slug': 'email-campaign-manager',
                'description': 'Simple email marketing without the complexity',
                'category': 'marketing',
                'price': '₹199/mo',
                'revenue_model': 'Freemium',
                'effort': '2-3 weeks',
                'audience': 'Small businesses, E-commerce',
                'pain_point': 'Complex email marketing tools are overkill for small teams',
                'features': ['Email templates', 'Subscriber list', 'Analytics', 'Schedule campaigns'],
                'tech_stack': ['Flask', 'Celery', 'SendGrid'],
                'is_published': True
            }
        ]
        
        count = 0
        for tool_data in sample_tools:
            if not Tool.query.filter_by(slug=tool_data['slug']).first():
                tool = Tool(**tool_data)
                db.session.add(tool)
                count += 1
        
        db.session.commit()
        return count
    
    @staticmethod
    def seed_sample_blogs():
        """Seed database with sample blog posts"""
        sample_blogs = [
            {
                'title': 'How to Build Your First Micro SaaS in 30 Days',
                'slug': 'build-first-micro-saas-30-days',
                'content': '<h1>Getting Started</h1><p>Building a micro SaaS has become more accessible than ever...</p>',
                'excerpt': 'Complete guide to launching your first SaaS product',
                'category': 'tutorial',
                'tags': ['micro-saas', 'startup', 'guide'],
                'author': 'Cognisutra Team',
                'is_published': True,
                'published_at': datetime.utcnow()
            },
            {
                'title': '10 Profitable Micro SaaS Ideas for 2026',
                'slug': '10-profitable-micro-saas-ideas-2026',
                'content': '<h1>Top Ideas</h1><p>Here are the most promising SaaS ideas validated by market research...</p>',
                'excerpt': 'Discover the most profitable micro SaaS opportunities',
                'category': 'ideas',
                'tags': ['ideas', 'saas', 'business'],
                'author': 'Cognisutra Team',
                'is_published': True,
                'published_at': datetime.utcnow()
            }
        ]
        
        count = 0
        for blog_data in sample_blogs:
            if not Blog.query.filter_by(slug=blog_data['slug']).first():
                blog = Blog(**blog_data)
                db.session.add(blog)
                count += 1
        
        db.session.commit()
        return count
    
    @staticmethod
    def seed_freebies():
        """Seed database with free resources"""
        freebies = [
            {
                'title': 'JSON Formatter & Validator',
                'description': 'Format, validate and minify JSON online',
                'category': 'developer-tools',
                'url': 'https://jsonlint.com',
                'source': 'JSONLint',
                'is_published': True
            },
            {
                'title': 'Color Palette Generator',
                'description': 'Generate beautiful color palettes automatically',
                'category': 'design-tools',
                'url': 'https://coolors.co',
                'source': 'Coolors',
                'is_published': True
            },
            {
                'title': 'Figma - Design & Prototyping',
                'description': 'Collaborative design tool with free tier',
                'category': 'design-tools',
                'url': 'https://www.figma.com',
                'source': 'Figma',
                'is_published': True
            },
            {
                'title': 'VS Code - Code Editor',
                'description': 'Free, open-source code editor',
                'category': 'developer-tools',
                'url': 'https://code.visualstudio.com',
                'source': 'Microsoft',
                'is_published': True
            },
        ]
        
        count = 0
        for freebie_data in freebies:
            if not Freebie.query.filter_by(url=freebie_data['url']).first():
                freebie = Freebie(**freebie_data)
                db.session.add(freebie)
                count += 1
        
        db.session.commit()
        return count

class Query:
    """Common database queries"""
    
    @staticmethod
    def get_featured_tools(limit=6):
        """Get featured published tools"""
        return Tool.query.filter_by(is_published=True).limit(limit).all()
    
    @staticmethod
    def get_tools_by_category(category, limit=None):
        """Get tools by category"""
        query = Tool.query.filter_by(category=category, is_published=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @staticmethod
    def search_tools(search_term):
        """Search tools by name or description"""
        return Tool.query.filter(
            (Tool.name.ilike(f'%{search_term}%')) |
            (Tool.description.ilike(f'%{search_term}%'))
        ).filter_by(is_published=True).all()
    
    @staticmethod
    def get_recent_blogs(limit=10):
        """Get recent published blogs"""
        return Blog.query.filter_by(is_published=True).order_by(
            Blog.published_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_blogs_by_category(category, limit=None):
        """Get blogs by category"""
        query = Blog.query.filter_by(category=category, is_published=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @staticmethod
    def get_user_bookmarks(user_id):
        """Get all bookmarks for a user"""
        from app.models import Bookmark
        return Bookmark.query.filter_by(user_id=user_id).all()
