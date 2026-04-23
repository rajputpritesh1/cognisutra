# Development Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Environment Setup](#environment-setup)
4. [Database Setup](#database-setup)
5. [Running Locally](#running-locally)
6. [Development Workflows](#development-workflows)
7. [Debugging](#debugging)
8. [Best Practices](#best-practices)

## Prerequisites

### System Requirements
- Python 3.8+
- pip (Python package manager)
- Git
- PostgreSQL 12+ (optional, for production-like setup)
- Node.js 16+ (optional, for front-end development)

### Tools
- VS Code or PyCharm IDE
- Git CLI
- Postman or Insomnia (for API testing)
- Database client (pgAdmin, DBeaver, etc.)

## Project Structure

```
cognisutra/
├── app/
│   ├── __init__.py              # App factory
│   ├── models.py                # Database models
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py
│   │   ├── db_utils.py          # Database utilities
│   │   ├── logger.py            # Logging setup
│   │   ├── response.py          # API response helpers
│   │   ├── validators.py        # Input validation
│   │   ├── decorators.py        # Custom decorators
│   │   ├── security.py          # Security utilities
│   │   └── helpers.py           # Common helpers
│   ├── auth/                    # Authentication module
│   ├── admin/                   # Admin module
│   ├── main/                    # Main/public module
│   └── api/                     # REST API module
├── templates/
│   ├── base.html                # Base template
│   ├── main/                    # Public templates
│   ├── auth/                    # Auth templates
│   ├── admin/                   # Admin templates
│   └── errors/                  # Error pages
├── static/
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Images and assets
├── tests/                       # Test files
│   ├── conftest.py              # Pytest configuration
│   ├── test_auth.py             # Auth tests
│   └── test_api.py              # API tests
├── config.py                    # Configuration
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── README.md                    # Project overview
├── QUICKSTART.md                # Quick start guide
├── DEPLOYMENT.md                # Deployment guide
├── API.md                       # API documentation
└── TECHNICAL_DOCS.md            # Technical documentation
```

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/cognisutra.git
cd cognisutra
```

### 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-dev-secret-key-min-32-chars
DATABASE_URL=sqlite:///cognisutra.db
DEBUG=True
```

## Database Setup

### SQLite (Development)
```bash
# Already configured in .env
# Database will be created on first run
```

### PostgreSQL (Production-like)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Linux
brew install postgresql                              # macOS

# Create database
createdb cognisutra

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/cognisutra

# Initialize database
flask init-db
```

### Initialize Database
```bash
# Create tables
flask init-db

# Create admin user
flask create-admin
# Enter:
# Email: admin@example.com
# Username: admin
# Password: SecurePassword123

# Seed demo data
flask seed-demo-data
```

## Running Locally

### Start Development Server
```bash
python run.py
# Or
flask run
```

Server runs on `http://localhost:5000`

### Access the Application
- **Home**: http://localhost:5000
- **Admin**: http://localhost:5000/admin (login required)
- **API Docs**: Check API.md
- **API Health**: http://localhost:5000/api/v1/health

### Default Admin Credentials
```
Email: admin@example.com
Username: admin
Password: (from setup)
```

## Development Workflows

### Feature Development

#### 1. Create Feature Branch
```bash
git checkout -b feature/my-feature
```

#### 2. Make Changes
```bash
# Edit files
# Test changes locally
```

#### 3. Run Tests
```bash
pytest
pytest -v  # Verbose
pytest --cov=app  # With coverage
```

#### 4. Code Quality
```bash
# Format code
black app

# Check imports
isort app

# Lint
flake8 app
```

#### 5. Commit and Push
```bash
git add .
git commit -m "feat: Add my feature"
git push origin feature/my-feature
```

#### 6. Create Pull Request
- Go to GitHub
- Create PR against main/develop branch
- Wait for CI/CD checks to pass

### Database Migration

#### Add New Model
```python
# In app/models.py
class NewModel(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### Apply Changes
```bash
flask init-db
```

### API Development

#### Add New Endpoint
```python
# In app/api/__init__.py

@api_bp.route('/endpoint', methods=['GET'])
@rate_limit(max_requests=30, time_window=60)
def my_endpoint():
    return APIResponse.success(data={'key': 'value'})
```

#### Test Endpoint
```bash
curl http://localhost:5000/api/v1/endpoint
```

### Template Development

#### Add New Page
```html
<!-- Create templates/main/new_page.html -->
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}
<div class="container">
    <h1>Page Content</h1>
</div>
{% endblock %}
```

#### Add Route
```python
# In app/main/__init__.py

@main_bp.route('/new-page')
def new_page():
    return render_template('main/new_page.html')
```

## Debugging

### Enable Debug Mode
```bash
# In .env
DEBUG=True
FLASK_ENV=development

# Then run
python run.py
```

### Print Debugging
```python
from app.utils.logger import LoggerSetup
logger = LoggerSetup.get_logger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message')
```

### Database Debugging
```bash
# Access Flask shell
flask shell

# Then:
>>> from app.models import User, Tool
>>> User.query.all()
>>> Tool.query.filter_by(category='productivity').all()
```

### Interactive Debugger
```python
# In your code
import pdb; pdb.set_trace()

# VS Code launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "run.py",
                "FLASK_ENV": "development"
            },
            "args": ["run"],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

## Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Max line length: 127 characters
- Use meaningful variable names

### Git Workflow
- Create feature branches for each task
- Write descriptive commit messages
- Keep commits small and focused
- Use conventional commits:
  - `feat:` new feature
  - `fix:` bug fix
  - `docs:` documentation
  - `refactor:` code refactoring
  - `test:` test updates

### Database Best Practices
- Always use ORM (SQLAlchemy), never raw SQL
- Use transactions for multi-step operations
- Add database indexes for frequently queried columns
- Keep models normalized and follow 3NF

### API Design
- Use RESTful conventions
- Return consistent response format
- Implement proper error handling
- Add rate limiting for public endpoints
- Document all endpoints in API.md

### Security
- Never commit secrets to git
- Use environment variables for sensitive data
- Validate all user inputs
- Use parameterized queries (ORM handles this)
- Implement CSRF protection (Flask-WTF handles)
- Use HTTPS in production
- Add rate limiting to prevent abuse
- Keep dependencies up to date

### Testing
- Write tests for new features
- Aim for >80% code coverage
- Test both success and failure cases
- Use fixtures for test data
- Mock external services

### Documentation
- Update docstrings when changing functions
- Keep README.md up to date
- Document new configuration options
- Add comments for complex logic

### Performance
- Use pagination for large datasets
- Add database indexes strategically
- Cache frequently accessed data
- Monitor query performance
- Use connection pooling

## Common Commands

```bash
# Run development server
python run.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app

# Check code quality
flake8 app

# Access database
flask shell

# Create admin user
flask create-admin

# Seed demo data
flask seed-demo-data

# Database operations
flask init-db
flask db upgrade  # (if using migrations)

# Install new package
pip install package_name

# Update requirements
pip freeze > requirements.txt

# Git workflow
git checkout -b feature/name
git add .
git commit -m "message"
git push origin feature/name
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process using port 5000
lsof -i :5000
kill -9 <PID>

# Or use different port
flask run --port 5001
```

### Database Connection Error
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Reset database
rm cognisutra.db  # For SQLite
flask init-db
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Template Not Found
- Check file path in templates/
- Ensure template is in correct subdirectory
- Check indentation in Flask blueprint template_folder

### Static Files Not Loading
```bash
# Check static file path
# Restart Flask dev server
# Clear browser cache
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Python Testing with Pytest](https://docs.pytest.org/)
