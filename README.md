# Cognisutra - 100 Micro SaaS Ideas Platform

A comprehensive platform for discovering and building 100+ profitable micro SaaS products. Built with Flask, Tailwind CSS, and designed for rapid deployment.

## 🚀 Features

- **100+ Micro SaaS Ideas** - Market research-backed, ready to build
- **User Authentication** - Secure registration and login
- **Admin Dashboard** - Manage tools, blogs, users, and messages
- **Tool Marketplace** - Browse, bookmark, and filter by category
- **Blog Platform** - Read guides and tutorials
- **Free Resources** - Curated list of 100+ free tools
- **Responsive Design** - Works on all devices with Tailwind CSS
- **SEO Optimized** - Sitemap, robots.txt, meta tags
- **Production Ready** - Security best practices implemented

## 📋 Tech Stack

- **Backend**: Flask 2.3+
- **Database**: SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Tailwind CSS, Vanilla JavaScript
- **Deployment**: Vercel, GitHub
- **Authentication**: Flask-Login with bcrypt password hashing

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- pip and venv
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cognisutra.git
cd cognisutra
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
flask db init  # If migrations don't exist
flask db migrate
flask db upgrade
```

Or use CLI command:
```bash
flask init-db
```

6. **Create admin user**
```bash
flask create-admin
# Follow prompts to set email, username, and password
```

7. **Seed demo data (optional)**
```bash
flask seed-demo-data
```

8. **Run development server**
```bash
python run.py
# Visit http://localhost:5000
```

## 📁 Project Structure

```
cognisutra/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   ├── admin/               # Admin panel blueprint
│   ├── main/                # Main routes blueprint
│   └── utils/               # Utility functions
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template
│   ├── main/               # Main page templates
│   ├── auth/               # Auth templates
│   ├── admin/              # Admin templates
│   └── errors/             # Error pages
├── static/                  # Static files (CSS, JS, images)
├── migrations/              # Database migrations
├── config.py               # Configuration
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## 🔐 Security Features

- **CSRF Protection** - Flask-WTF CSRF tokens
- **Password Hashing** - PBKDF2:SHA256
- **Session Security** - HTTPOnly, Secure, SameSite cookies
- **SQL Injection Prevention** - SQLAlchemy ORM
- **XSS Protection** - Jinja2 automatic escaping
- **Input Validation** - WTForms validators
- **Role-Based Access** - Admin decorator for protection

## 🌐 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Configure serverless**
```bash
vercel
# Follow prompts
```

3. **Set environment variables in Vercel dashboard**

### Docker Deployment

```bash
docker build -t cognisutra .
docker run -p 5000:5000 cognisutra
```

### Traditional Server

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📊 Database Models

- **User** - User accounts with authentication
- **Tool** - Micro SaaS tool ideas
- **Blog** - Blog posts and articles
- **BlogComment** - Comments on blogs
- **Subscription** - User subscriptions
- **Bookmark** - User bookmarks
- **Freebie** - Free tools and resources
- **ContactMessage** - Contact form submissions

## 🛣️ URL Routes

### Public Routes
- `/` - Landing page
- `/tools` - Tools listing
- `/tools/<id>` - Tool details
- `/blogs` - Blog listing
- `/blogs/<id>` - Blog details
- `/freebies` - Free resources
- `/pricing` - Pricing page
- `/about` - About page
- `/contact` - Contact page
- `/devspace` - Developer resources

### Auth Routes
- `/auth/register` - Sign up
- `/auth/login` - Log in
- `/auth/logout` - Log out

### Admin Routes (Requires authentication)
- `/admin/dashboard` - Admin dashboard
- `/admin/tools` - Manage tools
- `/admin/blogs` - Manage blogs
- `/admin/users` - Manage users
- `/admin/messages` - View messages

### SEO Routes
- `/sitemap.xml` - XML sitemap
- `/robots.txt` - Robots file

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Support

- Email: support@cognisutra.in
- Discord: [Join Community](https://discord.gg/cognisutra)
- GitHub Issues: [Report Bug](https://github.com/cognisutra/issues)

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Deployed on [Vercel](https://vercel.com/)

---

**Made with ❤️ by Cognisutra Team**
