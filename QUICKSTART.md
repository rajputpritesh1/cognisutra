# COGNISUTRA QUICK START GUIDE

## 🚀 INSTALLATION (5 minutes)

### Step 1: Clone & Setup
```bash
cd cognisutra
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 3: Initialize Database
```bash
flask init-db
flask create-admin
flask seed-demo-data
```

### Step 4: Run Development Server
```bash
python run.py
# Visit: http://localhost:5000
```

---

## 📊 ADMIN CREDENTIALS

**First Admin User:**
- Email: admin@cognisutra.in
- Password: (You set this when running `flask create-admin`)

**Access Admin Panel:**
- URL: http://localhost:5000/admin/dashboard
- Only accessible when logged in as admin

---

## 🛠️ ADMIN FEATURES

### 1. Tools Management
- Create, edit, delete micro SaaS tools
- Publish/unpublish tools
- Manage pricing and descriptions
- Add demo URLs and GitHub links

### 2. Blog Management
- Create and publish blog posts
- Manage categories and tags
- Set featured images
- Schedule publications

### 3. User Management
- View all registered users
- Toggle admin status
- Deactivate/activate users

### 4. Message Management
- View contact form submissions
- Mark messages as read
- Reply to inquiries

---

## 📱 KEY PAGES

### Public Pages
- `/` - Landing page
- `/tools` - Browse all 100 tools
- `/blogs` - Read articles
- `/freebies` - Free resources
- `/pricing` - Subscription plans
- `/contact` - Contact form

### Protected Pages
- `/auth/register` - Sign up
- `/auth/login` - Log in
- `/admin/dashboard` - Admin panel

---

## 🔐 SECURITY CHECKLIST

Before deploying to production:

- [ ] Change `SECRET_KEY` in .env
- [ ] Set `FLASK_ENV=production`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Enable HTTPS/SSL
- [ ] Setup CSRF protection
- [ ] Configure email settings
- [ ] Enable password requirements (8+ chars)
- [ ] Setup rate limiting
- [ ] Configure CORS if needed
- [ ] Add security headers

---

## 📦 PRODUCTION DEPLOYMENT

### Option 1: Vercel
```bash
npm install -g vercel
vercel
# Set env variables in dashboard
```

### Option 2: Docker
```bash
docker-compose up -d
# Visit: http://localhost:5000
```

### Option 3: Traditional Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 🐛 TROUBLESHOOTING

### Port Already in Use
```bash
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows
```

### Database Issues
```bash
flask db reset  # WARNING: Deletes all data
flask db init
flask db migrate
flask db upgrade
```

### Static Files Not Loading
```bash
flask collect-static
```

---

## 📚 PROJECT STRUCTURE

```
app/
├── models.py       → Database models
├── auth/           → Login/Register
├── admin/          → Admin panel
└── main/           → Public pages

templates/
├── base.html       → Main layout
├── main/           → Public templates
├── auth/           → Auth forms
└── admin/          → Admin pages

static/
├── css/            → Tailwind CSS
└── js/             → JavaScript
```

---

## 🎯 NEXT STEPS

1. **Customize branding** - Update logo, colors, text
2. **Add 100 tools** - Populate from saas-project-idea.txt
3. **Write blog posts** - Share insights and tutorials
4. **Setup email** - Configure SMTP for notifications
5. **Deploy to Vercel** - Make it live at cognisutra.in
6. **Setup analytics** - Add Google Analytics
7. **Create freebies list** - Import from 100-micro-saas.html
8. **Setup monitoring** - Add error tracking (Sentry)

---

## 💡 COMMON CUSTOMIZATIONS

### Change Colors
Edit `templates/base.html` Tailwind config:
```javascript
colors: {
    primary: '#e8380d',      // Red/orange
    secondary: '#1b4fd8',    // Blue
    accent: '#1a6b3c'        // Green
}
```

### Add Social Links
Update footer in `templates/base.html`

### Customize Email Templates
Create `app/email/` folder with templates

### Add Payment Integration
Install: `pip install stripe`
Add Stripe keys to .env

---

## 📞 SUPPORT & RESOURCES

- **Documentation**: See README.md
- **GitHub Issues**: Report bugs
- **Discord**: Join community
- **Email**: support@cognisutra.in

---

**Happy Building! 🚀**
