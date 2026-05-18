# InnerPeace Hub — Improvements Tracker

## ✅ Completed — Batch 1 (Improvements 1–4)

### 1. View Counter
- `Post.view_count` column — increments on every public post visit
- Shown in admin dashboard posts table

### 2. Newsletter Digest
- One-click send to all active subscribers from Subscribers page
- HTML email with latest 3 posts, matching brand colours
- Admin can activate/deactivate individual subscribers
- **Requires:** `SMTP_USER`, `SMTP_PASS`, `SITE_URL` in `.env`

### 3. Comment Moderation Queue
- New comments held pending until admin approves
- `/admin/comments` page: approve or delete each comment
- Dashboard shows live pending count (turns amber when > 0)

### 4. Post Scheduling
- "Scheduled" status + datetime picker in create/edit post form
- Auto-publishes when scheduled time passes (checked on every request)

---

## ✅ Completed — Batch 2 (Improvements 5–9)

### 5. Dedicated Search Page (`/search`)
- Full-text search across title, excerpt, tags, category, and content
- Query term highlighted in yellow in results (title + excerpt)
- Card layout with thumbnail, category tag, date, excerpt
- Search bar with autofocus, accessible, dark mode compatible

### 6. Related Posts (Tag Similarity)
- Scores candidate posts by shared tags — most shared tags = top result
- Falls back to same-category if no tag overlap
- Shows up to 3 related posts (previously 2)

### 7. Per-Post Open Graph + Twitter Card Images
- `post.html` now overrides `og:image` and `twitter:image` with the post's own featured image
- Falls back to site logo if no post image
- Also sets `og:type=article`, `og:description`, `twitter:card=summary_large_image`
- When you share a post link on WhatsApp, Instagram, Twitter — the correct thumbnail now shows

### 8. RSS Feed (`/rss.xml`)
- Auto-generated RSS 2.0 feed of latest 20 published posts
- RSS autodiscovery `<link>` in `<head>` so feed readers detect it automatically
- RSS icon added to footer social links

### 9. Sitemap (`/sitemap.xml`)
- Auto-generated XML sitemap with all published post URLs
- Includes static pages (/, /blog, /podcast, /about, /contact, /search)
- Priority and changefreq set per page type
- Sitemap link in footer
- Submit URL to Google Search Console: `https://yoursite.com/sitemap.xml`

---

## 🗄️ Database — Migrated to Neon

- Render DB expires June 3 — migration to Neon complete ✅
- Both databases verified identical (all tables, all rows, alembic version matched)
- **Action required:** Update `DATABASE_URL` env var on Render dashboard to:
  ```
  postgresql://neondb_owner:npg_UomfCu6pq5RI@ep-empty-base-aqc2hk3i-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
  ```

---

## ⚠️ Action Items

### 1. Update DATABASE_URL on Render
In Render dashboard → your web service → Environment → update `DATABASE_URL` to the Neon connection string above.

### 2. Configure SMTP (for newsletter)
Add to `.env` and Render environment:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-gmail@gmail.com
SMTP_PASS=your-gmail-app-password
SITE_URL=https://innerpeacehub.onrender.com
```
Use a Gmail **App Password** (Google Account → Security → 2-Step Verification → App Passwords).

### 3. Submit sitemap to Google Search Console
Once deployed: go to [Google Search Console](https://search.google.com/search-console), add your property, then submit `https://innerpeacehub.onrender.com/sitemap.xml`.

---

## 📋 Remaining Improvements (10–14)

| # | Feature | Notes |
|---|---------|-------|
| 10 | Multi-author / guest bloggers | Add `Author` model, credit on posts |
| 11 | Post series (Part 1, 2, 3) | Group posts, prev/next navigation |
| 12 | PWA / offline caching | Service worker for poor connections |
| 13 | Sentry error monitoring | Free tier, real-time crash reports |
| 14 | 2FA admin login | TOTP — Google Authenticator compatible |
