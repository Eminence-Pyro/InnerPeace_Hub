# InnerPeace Hub - Blog & Content Platform

A professional, full-featured blog website for **InnerPeace Hub** by Ezinne Uduma, focusing on relationships, healing, faith-based living, and personal growth.

## 🌟 Features

### Content Management
- ✅ **Draft/Published Status** - Create and save posts as drafts before publishing
- ✅ **Featured Posts** - Mark important posts as featured on homepage
- ✅ **Categories & Tags** - Organize content with categories and searchable tags
- ✅ **Rich Text Editor** - CKEditor 5 integration for professional formatting
- ✅ **Cloud Image Upload** - Cloudinary integration for reliable image hosting
- ✅ **Search Functionality** - Search posts by title, excerpt, tags, and categories
- ✅ **Pagination** - Blog posts paginated (6 per page)

### Admin Dashboard
- 📊 **Analytics Overview** - View published/draft post counts and unread messages
- 📝 **Post Management** - Create, edit, delete posts with status control
- 💬 **Message Management** - View and manage contact form submissions
- 🔐 **Authentication** - Secure admin login with password strength validation
- 🛡️ **CSRF Protection** - Web form security against cross-site attacks

### User Experience
- 📱 **Fully Responsive** - Mobile, tablet, and desktop optimized
- 🎨 **Modern Design** - Gradient-based color scheme (purple #6B2D8B, gold #D4A843)
- ⚡ **Fast Performance** - Optimized images and lazy loading
- 🔍 **SEO Optimized** - Meta tags, Open Graph, and structured data
- 📊 **Progress Tracking** - Visual progress bar while scrolling
- ♿ **Accessible** - Semantic HTML and ARIA labels

### Pages
- **Home** - Hero section with featured posts and latest articles
- **Blog** - Full blog listing with pagination, categories, and search
- **Post Details** - Individual post with related articles and reactions
- **About** - Founder story and mission statement
- **Podcast** - Podcast information and episode links
- **Contact** - Contact form with message storage
- **Admin Dashboard** - Complete content management system

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask (Python)
- **Database:** SQLAlchemy (PostgreSQL/SQLite)
- **Authentication:** Flask-Login
- **Security:** Werkzeug (password hashing), Flask-WTF (CSRF protection)
- **File Upload:** Cloudinary API

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modular stylesheets with flexbox/grid
- **JavaScript** - Vanilla JS (no frameworks)
- **Rich Text:** CKEditor 5
- **Icons:** Font Awesome 6.5

### Tools & Services
- **Image Hosting:** Cloudinary
- **Deployment:** Heroku (Procfile included)
- **Web Server:** Gunicorn

## 📁 Project Structure

```
InnerPeace_Hub/
├── app.py                    # Application factory & entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment
│
├── models/
│   └── __init__.py          # Database models (Admin, Post, Comment, Message)
│
├── routes/
│   ├── blog_routes.py       # Public blog pages
│   ├── auth_routes.py       # Admin authentication
│   └── admin_routes.py      # Admin dashboard & management
│
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Utility functions
│
├── static/
│   ├── css/
│   │   ├── styles.css       # Main stylesheet (imports modular files)
│   │   ├── base.css         # Base styles & typography
│   │   ├── navbar.css       # Navigation
│   │   ├── footer.css       # Footer
│   │   ├── buttons-forms.css # Buttons & form elements
│   │   ├── utilities.css    # Helper classes
│   │   └── pages.css        # Page-specific styles
│   ├── js/
│   │   └── script.js        # Main JavaScript
│   └── images/
│       ├── favicon.ico      # Favicon files
│       └── [Logo & brand assets]
│
├── templates/
│   ├── base.html            # Base layout template
│   ├── index.html           # Home page
│   ├── blog.html            # Blog listing
│   ├── post.html            # Individual post
│   ├── about.html           # About page
│   ├── podcast.html         # Podcast page
│   ├── contact.html         # Contact page
│   └── admin/
│       ├── login.html       # Admin login
│       ├── dashboard.html   # Admin dashboard
│       └── create_post.html # Post editor
│
└── instance/
    └── innerpeacehub.db     # SQLite database (local development)
```

## 🚀 Quick Start

### Local Development

1. **Clone & Setup**
```bash
git clone https://github.com/Eminence-Pyro/InnerPeace_Hub.git
cd InnerPeace_Hub
python -m venv .venv-1
source .venv-1/bin/activate  # Windows: .venv-1\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Variables**
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/innerpeacehub
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

4. **Run Application**
```bash
python app.py
```
Visit: `http://localhost:5000`

5. **Admin Access**
- Default admin credentials are set via environment variables (see `.env.example`)
- Change password immediately after first login
- Admin panel: `http://localhost:5000/admin/login`

### Deployment (Heroku)

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

## 🔐 Security Features

- ✅ Password hashing with Werkzeug
- ✅ CSRF token protection on all forms
- ✅ Session security (HttpOnly, Secure, SameSite)
- ✅ Password strength validation (8+ chars, uppercase, lowercase, numbers, special chars)
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ File upload validation (whitelist: png, jpg, jpeg, webp)

## 📝 Database Schema

### Post Model
```python
- id (Integer, PK)
- title (String, 200)
- slug (String, 200, unique)
- category (String, 80)
- excerpt (String, 300)
- content (Text) - Rich HTML content
- image (String, 500) - Cloudinary URL
- date_posted (DateTime)
- read_time (String, 20)
- status (String) - 'draft' or 'published'
- is_featured (Boolean) - Featured on homepage
- tags (String, 200) - Comma-separated
- comments (Relationship) - Related comments
```

### Admin Model
```python
- id (Integer, PK)
- username (String, 80, unique)
- password (String, 200) - Hashed
```

### Message Model
```python
- id (Integer, PK)
- name (String, 100)
- email (String, 100)
- subject (String, 200)
- message (Text)
- date_sent (DateTime)
- is_read (Boolean)
```

## 🎨 Design System

### Color Palette
- **Primary:** #6B2D8B (Purple)
- **Accent:** #D4A843 (Gold)
- **Secondary:** #F2A7BB (Pink)
- **Background:** #FFF9F5 (Off-white)
- **Text:** #2C2C2C (Dark gray)

### Typography
- **Headings:** Playfair Display (serif)
- **Body:** Lato (sans-serif)

## 🔄 Workflow

### Creating a New Post
1. Go to Admin Dashboard
2. Click "Create Post"
3. Fill in:
   - Title (auto-generates slug)
   - Category
   - Excerpt (for preview)
   - Content (WYSIWYG editor)
   - Featured image
   - Tags
   - Read time estimate
4. Save as Draft or Publish immediately
5. View on blog when published

### Publishing Workflow
- Write as **Draft** → Preview and edit → **Publish**
- Only published posts appear on public site
- Drafts visible only in admin dashboard

## 📊 Analytics

Dashboard displays:
- Total published posts
- Draft posts count
- Unread messages count
- Recent posts & messages

## 🔍 SEO

- Meta descriptions per post
- Open Graph tags for social sharing
- Sitemap-friendly URLs with slugs
- H1-H3 hierarchy
- Image alt text

## 🚀 Future Improvements

1. **Comments System** - Allow readers to comment on posts
2. **Newsletter** - Email subscription for new posts
3. **Analytics** - Traffic, views, engagement tracking
4. **Social Sharing** - Share buttons on posts
5. **Related Articles** - AI-powered related post recommendations
6. **Performance** - Caching, CDN optimization
7. **Advanced Search** - Full-text search with filters
8. **Multi-author** - Support for guest bloggers
9. **API** - REST API for external integrations
10. **Dark Mode** - User preference for dark theme

## 🐛 Known Issues & Fixes

### Favicon Not Showing in Deployment
- **Fixed:** Added multiple favicon formats (32x32, 16x16, .ico)
- **Fixed:** Updated manifest.json with proper paths
- **Solution:** Browser cache cleared; Heroku slug recompiled

### Large CSS File
- **Fixed:** Split styles.css into modular files:
  - base.css, navbar.css, footer.css
  - buttons-forms.css, utilities.css, pages.css
- **Result:** Better maintainability and faster load times

## 📞 Contact & Support

**Site Owner:** Ezinne Uduma
- **Email:** [from .env]
- **Social:** [Add your social links]

## 📄 License

MIT License

## 🙏 Acknowledgments

- Built with Flask
- Images via Cloudinary
- Icons via Font Awesome
- Editor via CKEditor
- Developed by Divine Nnata

---

**Last Updated:** May 11, 2026  
**Version:** 2.0 (Refactored with modular architecture)
