const CACHE = 'rivers-rock-setlist-v1';
const URLS = ['index.html', 'manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin === location.origin && URLS.includes(url.pathname.split('/').pop())) {
    e.respondWith(
      caches.open(CACHE).then(c => c.match(e.request).then(r => r || fetch(e.request)))
    );
  }
});
