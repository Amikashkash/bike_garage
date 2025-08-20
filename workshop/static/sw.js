const CACHE_NAME = 'yakir-bikes-v1';
const MINIMAL_CACHE = [
    '/static/images/logo.png',
    '/static/manifest.json',
    '/static/pwa-icon.svg'
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

// Push notifications - handle incoming notifications
self.addEventListener('push', event => {
    console.log('📬 Push notification received:', event);
    
    // Default notification data
    let notificationData = {
        title: 'מוסך האופניים',
        body: 'יש לך עדכון חדש',
        icon: '/static/images/logo.png',
        badge: '/static/images/logo.png',
        data: {
            action_url: '/'
        },
        actions: [
            {
                action: 'view',
                title: 'צפה בפרטים',
                icon: '/static/icons/view.png'
            },
            {
                action: 'dismiss',
                title: 'ביטול',
                icon: '/static/icons/close.png'
            }
        ],
        requireInteraction: false,
        vibrate: [100, 50, 100]
    };
    
    // Parse notification data if provided
    if (event.data) {
        try {
            const pushData = event.data.json();
            notificationData = { ...notificationData, ...pushData };
        } catch (e) {
            console.error('Error parsing push data:', e);
        }
    }
    
    // Show the notification
    event.waitUntil(
        self.registration.showNotification(notificationData.title, {
            body: notificationData.body,
            icon: notificationData.icon,
            badge: notificationData.badge,
            data: notificationData.data,
            actions: notificationData.actions,
            requireInteraction: notificationData.requireInteraction,
            vibrate: notificationData.vibrate,
            tag: 'bike-garage-notification',
            renotify: true
        })
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    console.log('� Notification clicked:', event);
    
    event.notification.close();
    
    const action = event.action;
    const data = event.notification.data || {};
    
    if (action === 'dismiss') {
        // Just close the notification
        return;
    }
    
    // Default action or 'view' action
    let urlToOpen = data.action_url || '/';
    
    // Ensure URL is absolute
    if (!urlToOpen.startsWith('http')) {
        urlToOpen = self.location.origin + urlToOpen;
    }
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then(clientList => {
                // Check if there's already a window/tab open with this URL
                for (let client of clientList) {
                    if (client.url === urlToOpen && 'focus' in client) {
                        return client.focus();
                    }
                }
                // If no existing window/tab, open a new one
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
            .then(windowClient => {
                // Mark notification as clicked (optional API call)
                if (data.notification_id) {
                    fetch('/api/notifications/mark-read/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            notification_id: data.notification_id,
                            clicked: true
                        })
                    }).catch(e => console.log('Failed to mark notification as clicked:', e));
                }
                
                return windowClient;
            })
    );
});

// Background sync for future use (optional)
self.addEventListener('sync', event => {
    console.log('� Background sync triggered:', event.tag);
    // Future: handle offline form submissions
    
    if (event.tag === 'background-notification-sync') {
        event.waitUntil(
            // Sync any pending notifications when back online
            fetch('/api/notifications/sync/')
                .then(response => response.json())
                .then(data => {
                    console.log('Background sync completed:', data);
                })
                .catch(error => {
                    console.error('Background sync failed:', error);
                })
        );
    }
});
