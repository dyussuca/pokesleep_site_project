const CACHE_NAME = 'pokesleep-calc-v2';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  // ネットワークを優先し、接続不可時のみキャッシュを使用（ERR_FAILED防止）
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
