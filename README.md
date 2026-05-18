# InnerPeace Hub — Blog & Content Platform

> A professional, full-featured blog and podcast platform by **Ezinne Uduma**, focused on relationships, healing, faith-based living, and personal growth.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey?logo=flask)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)](https://innerpeacehub.onrender.com)

---

## ✨ Features

### Content Management
- **Draft / Published / Scheduled workflow** — Write drafts, schedule posts for future publishing
- **Post Scheduling** — Set a date/time; posts auto-publish when the time arrives
- **Featured Posts** — Pin important posts to the homepage
- **Categories & Tags** — Organise content with categories and comma-separated tags
- **Rich Text Editor** — CKEditor with image upload support
- **Cloud Image Upload** — Cloudinary for reliable, CDN-backed image hosting
- **Reading Progress Bar** — Visual scroll indicator on post pages
- **View Counter** — Tracks how many times each post has been viewed

### Guest Authors & Series (New)
- **Multi-Author / Guest Bloggers** — Create author profiles with bio, avatar, Twitter handle; credit guest contributors per post
- **Post Series** — Group related posts into named series (Part 1, 2, 3…); readers get prev/next navigation between parts

### Podcast
- **Audio Upload** — Upload episodes directly via browser (100MB+ supported); files hosted on Cloudinary
- **Custom Audio Player** — Accessible, styled HTML5 player on every episode page
- **Spotify Embed** — Optional Spotify embed alongside the hosted audio
- **Episode Management** — Draft/Published status, cover images, descriptions

### Discovery & SEO
- **Dedicated Search** (`/search`) — Full-text search across title, excerpt, tags, category, and body with result highlighting
- **RSS Feed** (`/rss.xml`) — Auto-generated RSS 2.0 feed; autodiscovered by feed readers
- **Sitemap** (`/sitemap.xml`) — Auto-generated XML sitemap for Google Search Console
- **Open Graph + Twitter Cards** — Each post shares its own featured image and description on social media

### Reader Interaction
- **Self-Hosted Comments** — Comment moderation queue; admin approves before public display
- **Emoji Reactions** — Like, love, inspire — stored in localStorage, no database needed
- **Newsletter Signup** — Subscribers stored in DB; admin sends HTML digest emails with one click

### Admin Dashboard
- **Full CRUD** — Posts, subscribers, messages, podcast episodes, authors, series
- **Comment Moderation** — Approve / reject incoming comments
- **Author Management** — Add and remove guest contributors
- **Series Management** — Create and organise multi-part post series
- **Image Upload via CKEditor** — Inline Cloudinary uploads in the editor

### Security
- **Two-Factor Authentication (TOTP)** — Google Authenticator / Authy compatible; setup and toggle from dashboard
- **CSRF Protection** — Flask-WTF covers all forms including CKEditor uploads
- **Env-based secrets** — No hardcoded credentials; all sensitive values live in `.env`
- **Session security** — HttpOnly + SameSite cookies; Secure flag in production
- **Custom error pages** — Branded 404 and 500 pages

### Performance & PWA
- **Progressive Web App** — Installable on mobile ("Add to Home Screen"); offline-capable via service worker
- **Offline Page** — Custom branded fallback when connection drops
- **Cache-first static assets** — Service worker caches CSS/JS for instant repeat loads

### Monitoring
- **Sentry** — Real-time error monitoring (plug in your `SENTRY_DSN` to activate)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask 3.1 |
| Database | PostgreSQL (Neon — production), SQLite (local dev) |
| ORM & Migrations | Flask-SQLAlchemy 3.1, Flask-Migrate (Alembic) |
| Auth | Flask-Login, Flask-WTF (CSRF), pyotp (2FA) |
| Rich Text | Flask-CKEditor |
| File Storage | Cloudinary (images + audio) |
| Email | SMTP via Gmail App Password |
| Error Monitoring | Sentry SDK |
| Deployment | Render (web service + Gunicorn) |
| Frontend | Vanilla JS, CSS custom properties (dark mode) |
| PWA | Service Worker, Web App Manifest |

---

## 🚀 Local Setup

### 1. Clone & create virtualenv
```bash
git clone https://github.com/Eminence-Pyro/InnerPeace_Hub.git
cd InnerPeace_Hub
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
SECRET_KEY=your-random-secret-key
ADMIN_PASSWORD=your-admin-password
DATABASE_URL=                        # leave blank to use local SQLite
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-gmail@gmail.com
SMTP_PASS=your-gmail-app-password    # NOT your regular password — use a Gmail App Password
SITE_URL=http://localhost:5000
SENTRY_DSN=                          # optional — get free DSN at sentry.io
```

> **Gmail App Password:** Google Account → Security → 2-Step Verification → App Passwords

### 3. Run
```bash
python app.py
```

The app auto-applies all database migrations on startup. No manual `flask db upgrade` needed.

Visit `http://localhost:5000` — admin login at `/admin/login` (default user: `ezinne`).

---

## 🗄 Database Migrations

Migrations are managed with **Flask-Migrate** (Alembic).

```bash
# Generate a new migration after changing models
flask db migrate -m "describe your change"

# Apply pending migrations (done automatically on startup too)
flask db upgrade
```

The app handles three startup scenarios automatically:
- **Fresh DB** — runs all migrations from scratch
- **Existing DB without migration history** — adds missing columns and stamps the version
- **Existing DB with history** — applies only pending migrations

---

## ☁️ Deployment (Render)

### Environment Variables (Render Dashboard → Environment)
```
SECRET_KEY=...
ADMIN_PASSWORD=...
DATABASE_URL=postgresql://neondb_owner:<pass>@ep-xxx.neon.tech/neondb?sslmode=require&channel_binding=require
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
SMTP_USER=...
SMTP_PASS=...
SITE_URL=https://innerpeacehub.onrender.com
FLASK_ENV=production
SENTRY_DSN=...   (optional)
```

### Build & Start Commands
| | Command |
|---|---|
| Build | `pip install -r requirements.txt` |
| Start | `gunicorn app:app` |

---

## 🔐 Two-Factor Authentication

1. Log in to the admin dashboard
2. Click the **2FA** button in the top-right header
3. Scan the QR code with **Google Authenticator** or **Authy**
4. Enter the 6-digit code to confirm and enable
5. On future logins you will be asked for your code after your password

To disable 2FA: go back to the 2FA page and click **Disable**.

---

## 🌐 Public Routes

| Route | Description |
|---|---|
| `/` | Homepage with featured posts and carousel |
| `/blog` | All posts with category filter and search |
| `/search?q=term` | Full-text search results |
| `/post/<slug>` | Individual post with series nav, comments, reactions |
| `/podcast` | Podcast episodes |
| `/about` | About page |
| `/contact` | Contact form |
| `/rss.xml` | RSS 2.0 feed |
| `/sitemap.xml` | XML sitemap |
| `/offline` | PWA offline fallback |

## 🔒 Admin Routes

| Route | Description |
|---|---|
| `/admin/login` | Admin login |
| `/admin/2fa` | TOTP verification step (when 2FA enabled) |
| `/admin` | Dashboard |
| `/admin/create-post` | Create / edit posts |
| `/admin/subscribers` | Newsletter subscribers |
| `/admin/comments` | Comment moderation queue |
| `/admin/authors` | Guest author management |
| `/admin/series` | Post series management |
| `/admin/podcast` | Podcast episode management |
| `/admin/2fa/setup` | Enable / disable 2FA |
| `/admin/change-password` | Change admin password |

---

## 📂 Project Structure

```
InnerPeace_Hub/
├── app.py                  # App factory, startup DB logic
├── config.py               # Dev / Production config classes
├── models/
│   └── __init__.py         # SQLAlchemy models (Post, Admin, Author, Series, Comment…)
├── routes/
│   ├── blog_routes.py      # Public blog, search, RSS, sitemap, PWA routes
│   ├── admin_routes.py     # Admin CRUD, author & series management
│   └── auth_routes.py      # Login, logout, change-password, 2FA
├── templates/
│   ├── base.html           # Base layout (dark mode, OG tags, SW registration)
│   ├── post.html           # Post detail (series nav, author byline, reactions)
│   ├── search.html         # Search results with highlighting
│   ├── offline.html        # PWA offline fallback
│   └── admin/              # Dashboard, create/edit post, authors, series, 2FA…
├── static/
│   ├── css/styles.css      # All styles including dark mode CSS variables
│   ├── js/script.js        # Carousel, reactions, dark mode, scroll-to-top
│   ├── sw.js               # Service worker (PWA)
│   ├── manifest.json       # PWA manifest
│   └── images/             # Static images (add icon-192.png + icon-512.png for PWA)
├── migrations/             # Alembic migration versions
├── requirements.txt
├── Procfile                # gunicorn app:app
├── .env.example
└── LICENSE                 # MIT
```

---

## 📋 PWA Icons

For full PWA installability, add two icons to `static/images/`:
- `icon-192.png` — 192×192px
- `icon-512.png` — 512×512px

You can use the existing site logo resized to these dimensions.

---

## 📄 License

[MIT License](LICENSE) — © 2026 Ezinne Uduma / InnerPeace Hub
