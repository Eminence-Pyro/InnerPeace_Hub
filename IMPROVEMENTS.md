# InnerPeace Hub — Improvements Tracker

## ✅ Completed This Session

### 1. View Counter
- `Post.view_count` column added to database model
- Increments on every public post visit (admin previews excluded)
- Displayed in admin dashboard posts table with eye icon
- Requires DB migration (see below)

### 2. Newsletter Digest
- Subscribers page now shows active count + "Send Digest" button
- One-click sends latest 3 posts to all active subscribers via SMTP email
- Beautiful HTML email template matching brand colours
- Admin can activate/deactivate individual subscribers
- **Setup required:** Add `SMTP_USER`, `SMTP_PASS`, `SITE_URL` to `.env` (see README)

### 3. Comment Moderation
- New comments go to a pending queue (not visible publicly until approved)
- Admin sees pending count in dashboard stats card (turns amber if > 0)
- `/admin/comments` moderation page: approve or delete each comment
- "Comments" button added to dashboard header with live badge count
- Flash message on submission: "Your comment is awaiting moderation"

### 4. Post Scheduling
- New "Scheduled" status option in create/edit post form
- Date-time picker appears when "Scheduled" is selected
- Post auto-publishes when scheduled time passes (checked on every page load)
- Dashboard shows "scheduled" badge in status column
- Requires DB migration (see below)

---

## ⚠️ Required: Run DB Migrations Locally

After pulling, run these commands to apply the new columns:

```bash
git pull
flask db migrate -m "Add view_count, scheduled_for to Post; add approved to Comment"
flask db upgrade
```

Then restart your server:
```bash
python app.py
```

---

## ⚠️ Required: Configure SMTP for Newsletter

Add to your `.env` file:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-gmail@gmail.com
SMTP_PASS=your-gmail-app-password
SITE_URL=https://innerpeacehub.onrender.com
```

> For Gmail: use an **App Password** (Google Account → Security → 2-Step Verification → App Passwords), not your regular password.

---

## 📋 Remaining Improvements (from README)

### Medium Priority
5. **Search Page** — dedicated `/search` with highlighted matches
6. **Related Posts (AI)** — text similarity on tags/category
7. **Social Sharing OG Image** — per-post Open Graph image
8. **RSS Feed** — `/rss.xml` for blog/podcast apps
9. **Sitemap** — auto-generate `/sitemap.xml` on publish

### Nice to Have
10. **Multi-author** — guest blogger credits per post
11. **Post Series** — group posts with prev/next navigation
12. **PWA / Offline** — service worker for poor connections
13. **Sentry** — real-time error tracking (free tier)
14. **2FA** — TOTP admin login security
