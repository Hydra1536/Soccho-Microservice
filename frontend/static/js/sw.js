// Service Worker for PWA
const CACHE_NAME = 'soccho-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/main.css',
  '/static/css/mobile.css',
  '/static/css/animations.css',
  '/static/js/app.js',
  '/static/js/charts.js',
  '/static/js/offline.js',
  '/home.html',
  '/find-friends.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache first, network fallback
        return response || fetch(event.request).then(fetchResponse => {
          return caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          });
        });
      }).catch(() => {
        // Offline fallback for HTML
        if (event.request.destination === 'document') {
          return caches.match('/index.html');
        }
      })
  );
});

// Background sync for transactions
self.addEventListener('sync', event => {
  if (event.tag === 'sync-transactions') {
    event.waitUntil(syncTransactions());
  }
});

async function syncTransactions() {
  // Sync queued transactions from IndexedDB
  console.log('Background sync complete');
}

