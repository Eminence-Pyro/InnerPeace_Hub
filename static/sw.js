// InnerPeace Hub Service Worker — Improvement 12
const CACHE_NAME = 'innerpeace-v1';
const OFFLINE_URL = '/offline';

// Assets to pre-cache on install
const PRECACHE_ASSETS = [
  '/',
  '/blog',
  '/offline',
  '/static/css/styles.css',
  '/static/manifest.json',
];

// ── Install: pre-cache shell ─────────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_ASSETS))
  );
  self.skipWaiting();
});

// ── Activate: remove old caches ──────────────────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// ── Fetch: network-first for HTML, cache-first for static assets ──────────────
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Static assets — cache first, then network
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // HTML pages — network first, fall back to offline page
  if (event.request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.match(event.request).then(cached => cached || caches.match(OFFLINE_URL))
      )
    );
    return;
  }
});
