const CACHE_NAME = 'yakir-bikes-v1';
const MINIMAL_CACHE = [
    '/static/images/logo.png',
    '/static/manifest.json'
];

// Install event - cache only essential assets
self.addEventListener('install', event => {
    console.log('🔧 Service Worker installing with minimal cache');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('📦 Caching minimal assets');
                return cache.addAll(MINIMAL_CACHE);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
    console.log('✅ Service Worker activated');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('🗑️ Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - network first strategy (minimal offline support)
self.addEventListener('fetch', event => {
    // Only handle GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    // Skip non-http(s) requests
    if (!event.request.url.startsWith('http')) {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then(response => {
                // If network request succeeds, return it
                return response;
            })
            .catch(() => {
                // Only serve from cache for essential assets
                return caches.match(event.request)
                    .then(response => {
                        if (response) {
                            console.log('📱 Serving from cache:', event.request.url);
                            return response;
                        }
                        // For everything else, show network error
                        throw new Error('Network unavailable and not in cache');
                    });
            })
    );
});

// Background sync for future use (optional)
self.addEventListener('sync', event => {
    console.log('🔄 Background sync triggered:', event.tag);
    // Future: handle offline form submissions
});

// Push notifications (optional for future use)
self.addEventListener('push', event => {
    console.log('📬 Push notification received');
    // Future: repair status notifications
});
