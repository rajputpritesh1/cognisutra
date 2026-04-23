# Cognisutra - Complete Technical Documentation

## 📋 Table of Contents
1. Architecture Overview
2. Database Schema
3. API Routes
4. Security Implementation
5. Deployment Guide
6. Troubleshooting

---

## 🏗️ Architecture Overview

### Application Stack
- **Framework**: Flask 2.3.3
- **Database**: SQLAlchemy ORM (SQLite/PostgreSQL)
- **Frontend**: Tailwind CSS + Vanilla JavaScript
- **Authentication**: Flask-Login + Werkzeug (PBKDF2:SHA256)
- **Forms**: Flask-WTF with CSRF Protection
- **Deployment**: Vercel / Docker / Traditional Server

### Application Flow
```
Request → WSGI Server → Flask App → Blueprint Routes → View Functions → Response
         ↓
    Middleware (Auth, Error Handling)
         ↓
    Database Models (SQLAlchemy)
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tools Table
```sql
CREATE TABLE tools (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    price VARCHAR(100),
    revenue_model VARCHAR(100),
    effort VARCHAR(100),
    audience TEXT,
    features JSON,
    tech_stack JSON,
    pain_point TEXT,
    is_published BOOLEAN DEFAULT TRUE,
    demo_url VARCHAR(500),
    github_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Blogs Table
```sql
CREATE TABLE blogs (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt VARCHAR(500),
    author VARCHAR(255),
    category VARCHAR(100),
    tags JSON,
    featured_image VARCHAR(500),
    is_published BOOLEAN DEFAULT FALSE,
    published_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🛣️ API Routes & Endpoints

### Authentication Routes
```
POST   /auth/register        → Create new user account
POST   /auth/login           → Log in to account
GET    /auth/logout          → Log out (requires auth)
```

### Main Routes (Public)
```
GET    /                     → Landing page
GET    /tools                → Browse tools (paginated)
GET    /tools/<id>           → Single tool details
GET    /blogs                → Blog listing (paginated)
GET    /blogs/<id>           → Single blog post
GET    /freebies             → Free resources
GET    /pricing              → Pricing page
GET    /about                → About page
GET    /contact              → Contact page (GET form / POST submit)
GET    /devspace             → Developer space
```

### Protected Routes (User)
```
POST   /tools/<id>/bookmark  → Bookmark/unbookmark tool (requires auth)
```

### Admin Routes (Admin only)
```
GET    /admin/dashboard      → Admin dashboard
GET    /admin/tools          → List all tools
POST   /admin/tools/create   → Create new tool
GET    /admin/tools/<id>/edit → Edit tool
POST   /admin/tools/<id>/edit → Update tool
POST   /admin/tools/<id>/delete → Delete tool

GET    /admin/blogs          → List all blogs
POST   /admin/blogs/create   → Create new blog
GET    /admin/blogs/<id>/edit → Edit blog
POST   /admin/blogs/<id>/delete → Delete blog

GET    /admin/users          → List all users
POST   /admin/users/<id>/toggle-admin → Change user role

GET    /admin/messages       → List contact messages
POST   /admin/messages/<id>/read → Mark as read
```

### SEO Routes
```
GET    /sitemap.xml          → XML sitemap for search engines
GET    /robots.txt           → Robots file for crawlers
```

---

## 🔐 Security Implementation

### 1. Password Security
```python
# Password Hashing
user.set_password(password)  # PBKDF2:SHA256 with salt
user.check_password(password)  # Compare hash

# Validation
- Minimum 8 characters
- No special requirements (customizable)
- Salted hash (automatic via Werkzeug)
```

### 2. Session Security
```python
# Session Configuration
SESSION_COOKIE_SECURE = True       # HTTPS only
SESSION_COOKIE_HTTPONLY = True     # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF protection
PERMANENT_SESSION_LIFETIME = 7 days
```

### 3. CSRF Protection
```html
<!-- In all forms -->
{{ form.hidden_tag() }}  <!-- Adds CSRF token -->
```

### 4. SQL Injection Prevention
```python
# Using SQLAlchemy ORM - no raw SQL
user = User.query.filter_by(email=user_input).first()  # Safe

# NOT THIS (vulnerable)
query = f"SELECT * FROM users WHERE email = '{user_input}'"
```

### 5. XSS Protection
```html
<!-- Jinja2 auto-escapes by default -->
{{ user.name }}  <!-- < > " & automatically escaped -->
{{ blog.content|safe }}  <!-- Only for trusted HTML -->
```

### 6. Input Validation
```python
# WTForms validators
email = StringField('Email', validators=[
    DataRequired(),
    Email(),
    Length(min=5, max=255)
])
```

### 7. Rate Limiting (To implement)
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@limiter.limit("5 per minute")
@app.route('/login', methods=['POST'])
def login():
    pass
```

### 8. Admin Access Control
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Permission denied', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
```

---

## 🚀 Deployment Guide

### Environment Variables Required
```
FLASK_ENV=production
SECRET_KEY=your-secure-random-key-min-32-chars
DATABASE_URL=postgresql://user:pass@host:5432/cognisutra
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@cognisutra.in
```

### Vercel Deployment

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Configure vercel.json** (already included)

3. **Deploy**
```bash
vercel --prod
```

4. **Set Environment Variables**
```bash
vercel env add FLASK_ENV production
vercel env add SECRET_KEY <your-key>
vercel env add DATABASE_URL <postgres-url>
```

### Docker Deployment

1. **Build Image**
```bash
docker build -t cognisutra .
```

2. **Run Container**
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=<key> \
  -e DATABASE_URL=<url> \
  cognisutra
```

3. **Using Docker Compose**
```bash
docker-compose up -d
```

### Traditional Server (AWS, DigitalOcean, etc.)

1. **Install Python & Dependencies**
```bash
sudo apt-get install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Create Systemd Service**
```ini
[Unit]
Description=Cognisutra Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/app/cognisutra
Environment="PATH=/app/cognisutra/venv/bin"
ExecStart=/app/cognisutra/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
```

3. **Setup Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name cognisutra.in;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Database Connection Error
```
Error: Could not load database
Solution: 
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Run: flask db upgrade
```

#### 2. Admin Dashboard 404
```
Solution:
- User must be admin (is_admin=True)
- Run: flask create-admin
- Then use admin credentials to log in
```

#### 3. Static Files Not Found
```
Solution:
- Check STATIC_FOLDER configuration
- Run: flask collect-static
- Rebuild Docker image
```

#### 4. Email Not Sending
```
Solution:
- Check MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD
- Use app password (not regular password)
- Enable less secure apps if using Gmail
```

#### 5. Password Hash Error
```
Error: "xxx is not a valid bcrypt hash"
Solution:
- Check password_hash in database
- Re-create user with new password
- Use: flask create-admin
```

#### 6. CSRF Token Missing
```
Solution:
- Ensure {{ form.hidden_tag() }} in all forms
- Check WTF_CSRF_ENABLED=True in config
- Clear browser cookies
```

---

## 📊 Monitoring & Analytics

### Recommended Tools
- **Error Tracking**: Sentry
- **Analytics**: Google Analytics / Plausible
- **Performance**: New Relic / DataDog
- **Logging**: CloudWatch / Papertrail

### Add Google Analytics
```html
<!-- In templates/base.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_ID');
</script>
```

---

## 🔄 Backup & Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump cognisutra > backup.sql

# SQLite
cp cognisutra.db backup.db
```

### Restore Database
```bash
# PostgreSQL
psql cognisutra < backup.sql

# SQLite
cp backup.db cognisutra.db
```

---

## 📈 Performance Optimization

### Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/tools')
@cache.cached(timeout=300)
def get_tools():
    pass
```

### Database Indexing
```python
# Already indexed in models:
- email (unique)
- username (unique)
- slug (unique)
- category
- is_published
```

### CDN Integration
- Use Cloudflare for static files
- Enable gzip compression
- Minimize CSS/JS

---

## 📝 License & Credits

Built with:
- Flask by Pallets
- Tailwind CSS
- SQLAlchemy
- Flask-Login

---

For more help, visit: https://docs.cognisutra.in
