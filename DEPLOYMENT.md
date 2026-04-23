# Deployment Guide

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Vercel Deployment](#vercel-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Production Setup](#production-setup)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

## Local Deployment

### Prerequisites
- Python 3.8+
- pip and venv
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/cognisutra.git
cd cognisutra
```

### Step 2: Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Initialize Database
```bash
flask init-db
flask create-admin
flask seed-demo-data
```

### Step 6: Run Development Server
```bash
python run.py
# Server runs on http://localhost:5000
```

## Vercel Deployment

### Prerequisites
- Vercel account
- GitHub repository with your code
- PostgreSQL database (Vercel Postgres or external)

### Step 1: Prepare Repository
```bash
git push origin main
```

### Step 2: Create Vercel Project
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select Python as runtime
5. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`

### Step 3: Set Environment Variables
In Vercel dashboard, add under Settings > Environment Variables:
```
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-key-here
DATABASE_URL=postgresql://user:password@host/dbname
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Step 4: Deploy
- Push to main branch triggers automatic deployment
- Or click "Deploy" in Vercel dashboard

### Step 5: Verify Deployment
```bash
# Test production URL
curl https://your-project.vercel.app/api/v1/health
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t cognisutra:latest .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -e DATABASE_URL=sqlite:///cognisutra.db \
  -e SECRET_KEY=your-secret-key \
  cognisutra:latest
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# Create admin user
docker-compose exec web flask create-admin

# Stop services
docker-compose down
```

## Production Setup

### 1. Use PostgreSQL
```bash
# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/cognisutra
```

### 2. Use Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 3. Setup Nginx Reverse Proxy
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

### 4. Setup SSL with Let's Encrypt
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d cognisutra.in
```

### 5. Create Systemd Service
Create `/etc/systemd/system/cognisutra.service`:
```ini
[Unit]
Description=Cognisutra Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/cognisutra
Environment="PATH=/var/www/cognisutra/venv/bin"
ExecStart=/var/www/cognisutra/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cognisutra
sudo systemctl start cognisutra
```

### 6. Setup Backup Strategy
```bash
# Daily database backups
0 2 * * * pg_dump cognisutra > /backups/cognisutra-$(date +\%Y\%m\%d).sql
```

## Monitoring & Maintenance

### Health Checks
```bash
# Check API health
curl https://cognisutra.in/api/v1/health

# Check database connection
python run.py
```

### Log Monitoring
```bash
# View application logs
tail -f logs/cognisutra.log

# View error logs
tail -f logs/errors.log
```

### Database Maintenance
```bash
# Backup database
pg_dump cognisutra > cognisutra-backup.sql

# Restore database
psql cognisutra < cognisutra-backup.sql
```

### Performance Monitoring
- Use Vercel Analytics for deployment monitoring
- Setup CloudFlare for CDN and DDoS protection
- Monitor application performance with APM tools

## Troubleshooting

### Database Connection Issues
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### Missing Dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Static Files Not Loading
```bash
# Collect static files
flask static-collect

# Clear cache
rm -rf __pycache__
```

### Session/Cache Issues
```bash
# Clear session
flask shell
>>> from app.models import db
>>> db.session.remove()
```

### Email Not Sending
```bash
# Check email configuration
echo $MAIL_SERVER
echo $MAIL_USERNAME

# Test email function
flask shell
>>> from app.utils.helpers import send_email
>>> send_email('Test', 'your-email@example.com', '<p>Test</p>')
```

### Memory Leaks
```bash
# Monitor memory usage
watch -n 1 'ps aux | grep gunicorn'

# Restart service
sudo systemctl restart cognisutra
```

## Performance Optimization

### Caching
```python
# Enable Redis caching
# In config.py
CACHE_TYPE = 'RedisCache'
CACHE_REDIS_URL = 'redis://localhost:6379/0'
```

### CDN Setup
```nginx
# CloudFlare
# -> Add DNS records to CloudFlare
# -> Enable caching for static assets
# -> Setup page rules
```

### Database Indexing
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_tools_category ON tools(category);
CREATE INDEX idx_blogs_published ON blogs(is_published, published_at);
CREATE INDEX idx_users_email ON users(email);
```

## Rollback Procedure

### Git Rollback
```bash
# View commit history
git log --oneline

# Rollback to previous version
git revert HEAD
git push origin main
```

### Database Rollback
```bash
# Restore from backup
psql cognisutra < cognisutra-backup.sql

# Run migrations if needed
flask db upgrade
```
