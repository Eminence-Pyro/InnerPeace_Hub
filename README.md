# InnerPeace Hub — Blog & Content Platform

A professional, full-featured blog website for **InnerPeace Hub** by Ezinne Uduma, focusing on relationships, healing, faith-based living, and personal growth.

---

## 🌟 Features

### Content Management
- ✅ **Draft/Published Workflow** — Write and save drafts before going live
- ✅ **Featured Posts** — Pin important posts to the homepage
- ✅ **Categories & Tags** — Organize content with categories and searchable tags
- ✅ **Rich Text Editor** — CKEditor integration for professional formatting
- ✅ **Cloud Image Upload** — Cloudinary integration for reliable image hosting
- ✅ **Podcast Upload System** — Upload audio directly to Cloudinary from the browser (supports 100MB+); admin manages episodes with title, description, Spotify embed, cover image, and duration
- ✅ **Search Functionality** — Search posts by title, excerpt, tags, and categories
- ✅ **Pagination** — Blog posts paginated (6 per page)

### Admin Dashboard
- 📊 **Analytics Overview** — Published/draft post counts and unread messages
- 📝 **Post Management** — Create, edit, delete posts with status control
- 🎙️ **Podcast Management** — Add, edit, delete podcast episodes
- 💬 **Message Management** — View and manage contact form submissions
- 🔐 **Authentication** — Secure admin login with password strength validation
- 🛡️ **CSRF Protection** — Web form security on all forms

### User Experience
- 📱 **Fully Responsive** — Mobile, tablet, and desktop optimized (including admin panel)
- 🌙 **Dark Mode** — Floating toggle button; preference saved across sessions via `localStorage`
- 🎠 **Responsive Carousel** — Homepage post slider works on all screen sizes (1/2/3 cards)
- 🔝 **Scroll to Top** — Floating button, fades in after 300px scroll
- ❤️ **Post Reactions** — 5-emoji reaction system per post (stored in `localStorage`)
- 💬 **Native Comments** — Self-hosted comment system (no Disqus dependency)
- ⚡ **Performance** — Optimized images via Cloudinary, lazy loading
- 🔍 **SEO** — Meta tags, Open Graph, slug-based URLs
- 📊 **Reading Progress** — Progress bar while scrolling through posts
- ♿ **Accessible** — Semantic HTML and ARIA labels throughout

### Pages
- **Home** — Hero, featured podcast episode, and latest articles carousel
- **Blog** — Full listing with pagination, categories, and search
- **Post Detail** — Full post with reactions, comments, sharing, and related articles
- **About** — Founder story and mission
- **Podcast** — Episodes from database with native audio player + Spotify embed
- **Contact** — Contact form with message storage
- **Admin** — Full CMS (posts, podcast, messages)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask (Python 3.13)
- **Database:** PostgreSQL via Neon (prod) / SQLite (local dev)
- **ORM:** SQLAlchemy + Flask-Migrate
- **Authentication:** Flask-Login
- **Security:** Werkzeug (password hashing), Flask-WTF (CSRF)
- **Media:** Cloudinary (images + podcast audio)

### Frontend
- **HTML5** — Semantic markup
- **CSS3** — Single stylesheet with CSS variables (supports dark mode)
- **JavaScript** — Vanilla JS, no frameworks
- **Rich Text:** Flask-CKEditor
- **Icons:** Font Awesome 6.5

### Hosting & Services
- **App Hosting:** Render (or Heroku)
- **Database:** Neon (free, never-expiring serverless Postgres)
- **Media:** Cloudinary
- **Web Server:** Gunicorn

---

## 📁 Project Structure

```
InnerPeace_Hub/
├── app.py                    # Application factory & entry point
├── config.py                 # Environment-based configuration
├── requirements.txt          # Python dependencies
├── Procfile                  # Render/Heroku deployment
│
├── models/
│   └── __init__.py           # DB models: Admin, Post, Comment, Message, Subscriber, PodcastEpisode
│
├── routes/
│   ├── blog_routes.py        # Public pages + comment submission
│   ├── auth_routes.py        # Admin login/logout
│   └── admin_routes.py       # Admin dashboard, post CRUD, podcast CRUD, CKEditor upload
│
├── utils/
│   ├── __init__.py
│   └── helpers.py            # allowed_file(), generate_slug(), validate_password_strength()
│
├── static/
│   ├── css/styles.css        # Full stylesheet (dark mode vars, responsive, admin, podcast)
│   ├── js/script.js          # Carousel, scroll-to-top, reactions, hamburger, progress bar
│   └── images/               # Favicons, logo, brand assets
│
├── templates/
│   ├── base.html             # Base layout (FAB cluster: dark mode + scroll-to-top)
│   ├── index.html            # Home page
│   ├── blog.html             # Blog listing
│   ├── post.html             # Post detail (reactions + native comments)
│   ├── about.html
│   ├── podcast.html          # Podcast page (DB-driven episodes)
│   ├── contact.html
│   ├── errors/               # Custom 404 & 500 pages
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── create_post.html  # CKEditor post editor
│       ├── podcast_list.html
│       └── create_episode.html  # Podcast episode form + direct Cloudinary upload
│
└── migrations/               # Flask-Migrate migration history
```

---

## 🚀 Quick Start

### Local Development

1. **Clone & Setup**
```bash
git clone https://github.com/Eminence-Pyro/InnerPeace_Hub.git
cd InnerPeace_Hub
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Variables**
Create a `.env` file:
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/innerpeacehub
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
ADMIN_PASSWORD=your-admin-password
```
> For local dev without Postgres, omit `DATABASE_URL` — SQLite is used automatically.

3. **Run Migrations & Start**
```bash
flask db upgrade
python app.py
```
Visit: `http://localhost:5000` | Admin: `http://localhost:5000/admin/login`

---

## 🗄️ Database — Moving from Render to Neon

> **Why move?** Render free Postgres now expires after just **30 days** (no extension). Neon is free forever with 512MB storage — no credit card required.

### Step 1 — Back up your Render DB
```bash
pg_dump -Fc --no-acl --no-owner -h <render-host> -U <user> <dbname> > backup.dump
```

### Step 2 — Create a Neon project
1. Go to [neon.tech](https://neon.tech) → Sign up (free, no credit card)
2. Create a new project → copy the **connection string** (looks like `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require`)

### Step 3 — Restore your data to Neon
```bash
pg_restore --no-acl --no-owner -d "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require" backup.dump
```

### Step 4 — Update your environment
On **Render dashboard** (or `.env` locally), update:
```
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
```

### Step 5 — Redeploy
```bash
git push  # triggers Render auto-deploy
```

> ✅ No code changes needed. SQLAlchemy auto-handles Neon's standard Postgres URL.

---

## 🚀 Deployment (Render)

```bash
# Set environment variables in Render dashboard, then:
git push origin main   # Render auto-deploys on push
```

**Required env vars on Render:**
- `SECRET_KEY`
- `DATABASE_URL` (your Neon connection string)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- `ADMIN_PASSWORD`
- `FLASK_ENV=production`

---

## 🔐 Security

- ✅ Password hashing with Werkzeug
- ✅ CSRF protection on all forms (Flask-WTF)
- ✅ Session security (HttpOnly, Secure, SameSite=Lax)
- ✅ Password strength validation
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ File upload whitelist (png, jpg, jpeg, webp, gif, avif, heic)
- ✅ Direct Cloudinary upload for audio (bypasses Flask server entirely)
- ✅ Environment-variable-based secrets (no hardcoded credentials)

---

## 📝 Database Models

| Model | Key Fields |
|-------|-----------|
| `Post` | title, slug (unique), category, excerpt, content, image, status, is_featured, tags, date_posted |
| `Comment` | post_id (FK), name, email, body, date_posted |
| `Message` | name, email, subject, message, date_sent, is_read |
| `Subscriber` | email, date_subscribed |
| `PodcastEpisode` | title, episode_number, description, audio_url, spotify_url, cover_image, duration, status, date_published |
| `Admin` | username, password (hashed) |

---

## 🎨 Design System

| Token | Value |
|-------|-------|
| Primary | `#6B2D8B` (Purple) |
| Accent | `#D4A843` (Gold) |
| Background | `#FFF9F5` (Off-white) |
| Text | `#2C2C2C` |
| Dark bg | `#1a1a2e` |
| Dark card | `#16213e` |

**Fonts:** Playfair Display (headings) · Lato (body)

---

## 🔄 Content Workflow

### Blog Post
1. Admin → Create Post → fill title, category, excerpt, content (CKEditor), image, tags
2. Save as **Draft** (invisible to public) or **Publish** (live immediately)
3. Edit anytime; slug only regenerates if title changes

### Podcast Episode
1. Admin → Podcast → New Episode
2. Upload audio **directly from browser** to Cloudinary (no server file size limit; shows upload progress)
3. Optionally add Spotify embed URL, cover image, episode number
4. Publish or save as draft

---

## 🚀 Future Improvements

### High Priority
1. **View Counter** — Track how many times each post has been read; display on post and dashboard
2. **Newsletter Integration** — Connect subscriber list to Mailchimp or send weekly digest emails automatically via a cron job
3. **Admin Comment Moderation** — Let admin approve/reject comments before they appear publicly; add moderation queue to dashboard
4. **Post Scheduling** — Set a future publish date/time so posts go live automatically without logging in

### Medium Priority
5. **Search Page Results** — Dedicated `/search` results page with highlighted query matches, not just filtered listing
6. **Related Posts (AI)** — Use text similarity on tags/category/excerpt to auto-suggest 3 related articles at bottom of each post
7. **Social Sharing Metadata** — Per-post Open Graph image using the featured image (not just the logo) so shares on Instagram/WhatsApp show the right thumbnail
8. **RSS Feed** — Generate an `/rss.xml` feed so readers can subscribe in podcast/blog apps
9. **Sitemap** — Auto-generate `/sitemap.xml` on publish for better Google indexing

### Nice to Have
10. **Multi-author Support** — Add a `Author` model so guest bloggers can be credited per post
11. **Post Series** — Group related posts into a series (e.g. "Healing from Heartbreak — Part 1, 2, 3") with prev/next navigation
12. **Offline Caching (PWA)** — Add a service worker so the site loads even with poor internet (important for mobile users in Nigeria)
13. **Performance Monitoring** — Add Sentry (free tier) for real-time error tracking in production
14. **Two-Factor Auth (2FA)** — TOTP-based 2FA for the admin login to strengthen security

---

## 🐛 Known Issues & Fixes

| Issue | Status | Fix |
|-------|--------|-----|
| Favicon missing in deployment | ✅ Fixed | Multiple favicon formats added |
| CSRF on CKEditor uploads | ✅ Fixed | `CKEDITOR_ENABLE_CSRF=True` |
| Postgres SSL "unexpected EOF" | ✅ Fixed | `pool_pre_ping=True`, `pool_recycle=180` |
| Scroll-to-top invisible | ✅ Fixed | Moved button before `<script>` tag; CSS conflict removed |
| Carousel broken on desktop | ✅ Fixed | Full rewrite with dynamic card widths per breakpoint |
| Admin table overflow on mobile | ✅ Fixed | `overflow-x: auto` wrapper + `min-width` on table |
| Post slug collision on edit | ✅ Fixed | Only regenerates slug if title actually changed |
| Podcast audio 22MB+ upload fail | ✅ Fixed | Direct browser-to-Cloudinary upload (bypasses Flask) |
| Render Postgres expiry (30 days) | ✅ Resolved | Migrated to Neon (free, never expires) — see DB section above |

---

## 📞 Contact & Support

**Site Owner:** Ezinne Uduma · info.innerpeacehub@gmail.com

**Developer:** Divine Nnata · [LinkedIn](https://www.linkedin.com/in/divine-nnata-0203b7225)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with Flask · PostgreSQL on Neon · Media on Cloudinary · Icons by Font Awesome · Editor by CKEditor

---

**Last Updated:** May 17, 2026
**Version:** 3.0 — Dark mode, native comments, podcast system, Neon DB migration
