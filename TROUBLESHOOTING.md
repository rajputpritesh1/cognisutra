# Troubleshooting & FAQ

## Troubleshooting Guide

### Installation Issues

#### Problem: `ModuleNotFoundError: No module named 'flask'`
**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Problem: `command not found: python` or `python: command not found`
**Solution:**
```bash
# Try python3
python3 --version
python3 -m venv venv
python3 run.py

# Or add alias
alias python=python3
```

#### Problem: `Permission denied` when activating venv
**Solution:**
```bash
# Give execute permission
chmod +x venv/bin/activate

# Or use bash directly
bash venv/bin/activate
```

---

### Database Issues

#### Problem: `sqlite3.OperationalError: database is locked`
**Solution:**
```bash
# Kill existing connections
pkill -f "flask run"

# Remove lock file if it exists
rm cognisutra.db-journal

# Reinitialize database
rm cognisutra.db
flask init-db
```

#### Problem: `psycopg2.OperationalError: could not connect to server`
**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql

# Test connection
psql -U postgres -c "SELECT 1"

# Check DATABASE_URL
echo $DATABASE_URL
```

#### Problem: `OperationalError: (psycopg2.errors.InvalidDatabaseName)`
**Solution:**
```bash
# Create database first
createdb cognisutra

# Then run
flask init-db
```

#### Problem: Migration/Table creation fails
**Solution:**
```bash
# Reset database (destructive)
flask shell
>>> from app import db
>>> db.drop_all()
>>> db.create_all()
>>> exit()

# Or from command line
rm cognisutra.db
flask init-db
```

---

### Authentication Issues

#### Problem: "Invalid email or password" but credentials are correct
**Solution:**
```bash
# Check user exists
flask shell
>>> from app.models import User
>>> User.query.filter_by(email='admin@example.com').first()

# Reset password by creating new admin
flask create-admin

# Or reset in database
>>> user = User.query.filter_by(email='admin@example.com').first()
>>> user.set_password('newpassword123')
>>> from app import db
>>> db.session.commit()
```

#### Problem: "User is not admin" error
**Solution:**
```bash
# Check if user is admin
flask shell
>>> user = User.query.filter_by(username='admin').first()
>>> user.is_admin
>>> user.is_admin = True
>>> db.session.commit()
```

#### Problem: Session expires immediately
**Solution:**
```bash
# Check .env file
SESSION_COOKIE_SECURE=False  # For development
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=2592000  # 30 days

# Restart Flask
flask run
```

---

### API Issues

#### Problem: `404 Not Found` on API endpoints
**Solution:**
```bash
# Check if API blueprint is registered
# In app/__init__.py should have:
# from app.api import api_bp
# app.register_blueprint(api_bp)

# Test health endpoint
curl http://localhost:5000/api/v1/health

# Check Flask debug mode
export FLASK_DEBUG=1
flask run
```

#### Problem: `405 Method Not Allowed`
**Solution:**
```bash
# Check HTTP method is correct
# GET, POST, PUT, DELETE are different endpoints

# Use correct method:
curl -X GET http://localhost:5000/api/v1/tools
curl -X POST http://localhost:5000/api/v1/tools \
  -H "Content-Type: application/json" \
  -d '{"name":"Tool"}'
```

#### Problem: `500 Internal Server Error`
**Solution:**
```bash
# Check Flask logs
tail -f logs/cognisutra.log
tail -f logs/errors.log

# Enable debug mode
export FLASK_DEBUG=1
flask run

# Check console output for full traceback
```

#### Problem: Rate limiting too strict
**Solution:**
```python
# In app/api/__init__.py, adjust rate limits:
@rate_limit(max_requests=50, time_window=60)  # Increase limits
def get_tools():
    ...
```

---

### Frontend Issues

#### Problem: Static files (CSS, JS) not loading
**Solution:**
```bash
# Check static folder exists
ls -la static/

# Verify file paths in templates
# Should use: {{ url_for('static', filename='css/style.css') }}

# Restart Flask
flask run

# Hard refresh browser
Ctrl+Shift+R (Chrome)
Cmd+Shift+R (Mac)
```

#### Problem: Tailwind CSS not working (styles not applied)
**Solution:**
```bash
# Tailwind is loaded via CDN, should always work
# If not, check:
# 1. Internet connection (CDN requires external access)
# 2. Browser console for errors
# 3. HTML has correct Tailwind classes

# For development, build locally:
npm install -D tailwindcss
npx tailwindcss -i ./static/input.css -o ./static/output.css
```

#### Problem: JavaScript console errors
**Solution:**
```bash
# Open browser DevTools (F12)
# Check Console tab for errors
# Common issues:
# - Undefined variables
# - Missing DOM elements
# - CORS issues
# - API endpoint 404s

# Check static/js/utils.js exists and is loaded
```

---

### Performance Issues

#### Problem: Slow API response times
**Solution:**
```bash
# Check database query performance
export SQLALCHEMY_ECHO=True  # Log all SQL queries
flask run

# Add database indexes
# In models.py:
class Tool(db.Model):
    category = db.Column(db.String(50), db.ForeignKey('category.id'), index=True)
    
flask init-db  # Recreate with indexes
```

#### Problem: High memory usage
**Solution:**
```bash
# Check for memory leaks
# Limit worker processes
gunicorn -w 2 -b 0.0.0.0:5000 run:app

# Monitor memory
watch -n 1 'ps aux | grep python'

# Restart service periodically
```

#### Problem: Slow page loads
**Solution:**
```bash
# Enable caching
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300

# Add pagination
# Check query performance with SQLAlchemy echo
# Add database indexes
```

---

### Deployment Issues

#### Problem: Environment variables not loading
**Solution:**
```bash
# Check .env file exists
ls -la .env

# Source variables manually
export $(cat .env | xargs)
echo $FLASK_ENV

# Or use python-dotenv
from dotenv import load_dotenv
load_dotenv()
```

#### Problem: Docker container won't start
**Solution:**
```bash
# Check logs
docker logs <container_id>

# Verify Dockerfile
docker build -t cognisutra .

# Run with output
docker run -it cognisutra

# Check ports aren't in use
lsof -i :5000
```

#### Problem: Vercel deployment fails
**Solution:**
```bash
# Check build logs in Vercel dashboard
# Common issues:
# - Missing environment variables
# - Poetry/pip dependency issues
# - Application import errors

# Test locally first
pip install -r requirements.txt
python run.py

# Check vercel.json configuration
# Verify package.json exists if using Node
```

---

## Frequently Asked Questions (FAQ)

### General

**Q: What Python version do I need?**
A: Python 3.8 or higher. Recommended: 3.10+
```bash
python3 --version
```

**Q: Can I use Windows?**
A: Yes! Just use the Windows-specific commands:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**Q: How do I change the port?**
A: Use `flask run --port 8000` or set in config.py

**Q: Is this production-ready?**
A: Yes! All security best practices are implemented. See DEPLOYMENT.md for production setup.

---

### Database

**Q: Can I use SQLite for production?**
A: Not recommended. Use PostgreSQL for production. SQLite is good for development.

**Q: How do I backup my database?**
A: 
```bash
# PostgreSQL
pg_dump cognisutra > backup.sql

# SQLite
cp cognisutra.db cognisutra.db.backup
```

**Q: How do I reset my database?**
A:
```bash
# WARNING: This deletes everything
rm cognisutra.db
flask init-db
flask create-admin
```

**Q: Can I export data?**
A: Yes, use the import/export utilities:
```python
from app.utils.db_utils import ImportExport
ImportExport.export_tools_csv('tools.csv')
ImportExport.export_tools_json('tools.json')
```

---

### Authentication & Security

**Q: How do I reset a user's password?**
A:
```bash
flask shell
>>> from app.models import User
>>> user = User.query.filter_by(email='user@example.com').first()
>>> user.set_password('newpassword123')
>>> from app import db
>>> db.session.commit()
```

**Q: Is password reset via email implemented?**
A: Not yet, but the email framework is ready. See TECHNICAL_DOCS.md for adding it.

**Q: How do I make a user an admin?**
A:
```bash
flask shell
>>> user = User.query.filter_by(username='username').first()
>>> user.is_admin = True
>>> db.session.commit()
```

**Q: Where are passwords stored?**
A: Hashed with PBKDF2:SHA256 in database. Never stored in plain text.

---

### API

**Q: What's the API base URL?**
A: `http://localhost:5000/api/v1` (development)

**Q: Do I need authentication for all API calls?**
A: No, only for bookmarks. Tools and blogs are public.

**Q: Can I get API documentation?**
A: Yes! See [API.md](API.md)

**Q: How do I test the API?**
A:
```bash
# Using curl
curl http://localhost:5000/api/v1/health

# Using Postman/Insomnia
GET http://localhost:5000/api/v1/tools
```

**Q: Can I use the API from frontend?**
A: Yes, but handle CORS. See app/__init__.py for CORS setup.

---

### Deployment

**Q: How do I deploy to production?**
A: See DEPLOYMENT.md for step-by-step guide.

**Q: What's the easiest way to deploy?**
A: Vercel is easiest. Just push to GitHub and it deploys automatically.

**Q: How much does it cost to deploy?**
A: Most hosting is free for hobby projects. Production costs vary by platform.

**Q: Can I deploy to AWS/Heroku/DigitalOcean?**
A: Yes, see DEPLOYMENT.md for guides.

---

### Development

**Q: How do I run tests?**
A:
```bash
pytest                    # All tests
pytest -v                 # Verbose
pytest --cov=app          # With coverage
```

**Q: How do I add a new page?**
A:
```bash
# 1. Create template
# 2. Add route in app/main/__init__.py
# 3. Add link in navigation
```

**Q: How do I add an API endpoint?**
A:
```bash
# Add to app/api/__init__.py
@api_bp.route('/endpoint')
def my_endpoint():
    return APIResponse.success(...)
```

**Q: How do I add a new database model?**
A:
```bash
# 1. Add to app/models.py
# 2. Run flask init-db
# 3. Update admin panel if needed
```

---

### Support

**Q: Where do I report bugs?**
A: Open an issue on GitHub with:
- Error message/logs
- Steps to reproduce
- System information (OS, Python version)

**Q: How do I request features?**
A: Open a GitHub issue with "Feature request" label and description.

**Q: Is there a community?**
A: Check GitHub discussions and issues for community support.

**Q: Where's the documentation?**
A: See the docs/ directory:
- README.md
- QUICKSTART.md
- TECHNICAL_DOCS.md
- DEVELOPMENT.md
- DEPLOYMENT.md
- API.md

**Q: I found a security issue, how do I report it?**
A: Email security details privately instead of opening public issues.

---

## Quick Reference

### Common Commands
```bash
# Start development server
python run.py

# Run tests
pytest --cov=app

# Format code
black app

# Check code quality
flake8 app

# Database operations
flask init-db
flask create-admin
flask seed-demo-data

# Flask shell (Python REPL)
flask shell

# Access database from shell
>>> from app.models import User
>>> User.query.all()
```

### Important Files
- `app/__init__.py` - Application factory
- `app/models.py` - Database models
- `config.py` - Configuration
- `run.py` - Entry point
- `.env` - Environment variables
- `requirements.txt` - Dependencies

### Useful URLs (Development)
- Home: http://localhost:5000
- Admin: http://localhost:5000/admin
- Login: http://localhost:5000/auth/login
- API Health: http://localhost:5000/api/v1/health

---

## Still Having Issues?

1. **Check the logs:**
   ```bash
   tail -f logs/cognisutra.log
   tail -f logs/errors.log
   ```

2. **Enable debug mode:**
   ```bash
   export FLASK_DEBUG=1
   flask run
   ```

3. **Check documentation:**
   - TECHNICAL_DOCS.md - Architecture
   - DEVELOPMENT.md - Local setup
   - DEPLOYMENT.md - Production
   - API.md - API reference

4. **Search GitHub issues** for similar problems

5. **Join the community** for support

---

**Last Updated:** 2024  
**Version:** 1.0  
**Status:** Active Development
