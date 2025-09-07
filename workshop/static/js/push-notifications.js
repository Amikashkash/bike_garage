/**
 * Push Notifications Manager
 * Handles push notification subscription and management
 */

class PushNotificationManager {
    constructor() {
        this.publicKey = null;
        this.subscription = null;
        this.isSupported = this.checkSupport();
        
        if (this.isSupported) {
            this.init();
        }
    }
    
    checkSupport() {
        // Check if service workers and push notifications are supported
        return 'serviceWorker' in navigator && 
               'PushManager' in window && 
               'Notification' in window;
    }
    
    async init() {
        try {
            // Register service worker if not already registered
            await this.registerServiceWorker();
            
            // Get VAPID public key from server
            await this.getVapidPublicKey();
            
            // Check existing subscription
            await this.checkExistingSubscription();
            
        } catch (error) {
            console.error('Push notification initialization failed:', error);
        }
    }
    
    async registerServiceWorker() {
        if (!navigator.serviceWorker.controller) {
            const registration = await navigator.serviceWorker.register('/sw.js');
            console.log('Service Worker registered:', registration);
        }
    }
    
    async getVapidPublicKey() {
        try {
            const response = await fetch('/api/vapid-public-key/', {
                credentials: 'include'
            });
            const data = await response.json();
            this.publicKey = data.public_key;
        } catch (error) {
            console.error('Failed to get VAPID public key:', error);
            throw error;
        }
    }
    
    async checkExistingSubscription() {
        const registration = await navigator.serviceWorker.ready;
        this.subscription = await registration.pushManager.getSubscription();
        
        if (this.subscription) {
            console.log('Existing push subscription found');
            // Verify subscription with server
            await this.verifySubscriptionWithServer();
        }
    }
    
    async verifySubscriptionWithServer() {
        try {
            const response = await fetch('/api/customer/push/status/', {
                credentials: 'include'
            });
            const data = await response.json();
            
            if (!data.has_subscriptions && this.subscription) {
                // Server doesn't have our subscription, send it
                await this.sendSubscriptionToServer(this.subscription);
            }
        } catch (error) {
            console.error('Failed to verify subscription with server:', error);
        }
    }
    
    async requestPermissionAndSubscribe() {
        if (!this.isSupported) {
            throw new Error('Push notifications are not supported');
        }
        
        // Request permission
        const permission = await Notification.requestPermission();
        
        if (permission === 'granted') {
            await this.subscribe();
            return true;
        } else {
            console.log('Push notification permission denied');
            return false;
        }
    }
    
    async subscribe() {
        try {
            const registration = await navigator.serviceWorker.ready;
            
            // Convert VAPID public key to Uint8Array
            const applicationServerKey = this.urlBase64ToUint8Array(this.publicKey);
            
            // Subscribe to push notifications
            this.subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: applicationServerKey
            });
            
            console.log('Push subscription successful:', this.subscription);
            
            // Send subscription to server
            await this.sendSubscriptionToServer(this.subscription);
            
        } catch (error) {
            console.error('Push subscription failed:', error);
            throw error;
        }
    }
    
    async sendSubscriptionToServer(subscription) {
        try {
            const response = await fetch('/api/customer/push/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                },
                credentials: 'include',
                body: JSON.stringify(subscription.toJSON())
            });
            
            const result = await response.json();
            
            if (response.ok) {
                console.log('Subscription sent to server:', result);
                this.showNotificationStatus('success', 'התראות פעילות! תקבל עדכונים על התיקונים שלך');
            } else {
                throw new Error(result.error || 'Failed to send subscription');
            }
            
        } catch (error) {
            console.error('Failed to send subscription to server:', error);
            throw error;
        }
    }
    
    async unsubscribe() {
        if (!this.subscription) {
            return;
        }
        
        try {
            // Unsubscribe from push manager
            await this.subscription.unsubscribe();
            
            // Notify server
            await fetch('/api/customer/push/unsubscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                },
                credentials: 'include',
                body: JSON.stringify({
                    endpoint: this.subscription.endpoint
                })
            });
            
            this.subscription = null;
            console.log('Successfully unsubscribed from push notifications');
            this.showNotificationStatus('info', 'התראות בוטלו בהצלחה');
            
        } catch (error) {
            console.error('Failed to unsubscribe:', error);
            throw error;
        }
    }
    
    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');
        
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
    
    showNotificationStatus(type, message) {
        // Create a temporary notification
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg text-white max-w-sm shadow-lg ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 
            'bg-blue-500'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
    
    // Public API methods
    
    async getSubscriptionStatus() {
        try {
            const response = await fetch('/api/customer/push/status/', {
                credentials: 'include'
            });
            return await response.json();
        } catch (error) {
            console.error('Failed to get subscription status:', error);
            return { has_subscriptions: false, subscription_count: 0 };
        }
    }
    
    isSubscribed() {
        return this.subscription !== null;
    }
    
    isPermissionGranted() {
        return Notification.permission === 'granted';
    }
    
    async showTestNotification(title = 'התראת בדיקה', message = 'המערכת עובדת כראוי!') {
        if (this.isPermissionGranted()) {
            new Notification(title, {
                body: message,
                icon: '/static/images/logo.png',
                badge: '/static/pwa-icon.svg'
            });
        }
    }
}

// Global instance
window.pushManager = new PushNotificationManager();

// Helper function to create notification permission UI
function createNotificationPermissionBanner() {
    if (window.pushManager.isSupported && 
        Notification.permission === 'default' && 
        document.querySelector('[data-user-type="customer"]')) {
        
        const banner = document.createElement('div');
        banner.className = 'fixed top-0 left-0 right-0 bg-blue-500 text-white p-4 z-40 flex items-center justify-between';
        banner.innerHTML = `
            <div class="flex items-center gap-3">
                <i class="fas fa-bell text-xl"></i>
                <div>
                    <div class="font-semibold">קבל התראות על התיקונים שלך</div>
                    <div class="text-sm opacity-90">עדכונים מיידיים על סטטוס התיקון ואישורים נדרשים</div>
                </div>
            </div>
            <div class="flex gap-2">
                <button id="enable-notifications-btn" class="bg-white text-blue-500 px-4 py-2 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
                    אפשר התראות
                </button>
                <button id="dismiss-notifications-btn" class="text-white px-3 py-2 hover:bg-blue-600 rounded transition-colors">
                    ✕
                </button>
            </div>
        `;
        
        document.body.prepend(banner);
        
        // Add main content margin to account for banner
        document.body.style.paddingTop = '80px';
        
        // Event handlers
        document.getElementById('enable-notifications-btn').addEventListener('click', async () => {
            try {
                const success = await window.pushManager.requestPermissionAndSubscribe();
                if (success) {
                    banner.remove();
                    document.body.style.paddingTop = '0';
                }
            } catch (error) {
                console.error('Failed to enable notifications:', error);
                window.pushManager.showNotificationStatus('error', 'שגיאה בהפעלת התראות');
            }
        });
        
        document.getElementById('dismiss-notifications-btn').addEventListener('click', () => {
            banner.remove();
            document.body.style.paddingTop = '0';
            localStorage.setItem('notifications-dismissed', 'true');
        });
        
        // Don't show if user has dismissed it recently
        if (localStorage.getItem('notifications-dismissed')) {
            // Show again after 24 hours
            const dismissedTime = localStorage.getItem('notifications-dismissed-time');
            if (!dismissedTime || Date.now() - parseInt(dismissedTime) > 24 * 60 * 60 * 1000) {
                localStorage.removeItem('notifications-dismissed');
                localStorage.removeItem('notifications-dismissed-time');
            } else {
                banner.remove();
                document.body.style.paddingTop = '0';
            }
        }
    }
}

// Initialize permission banner when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit for the page to load
    setTimeout(createNotificationPermissionBanner, 2000);
});

// Export for global access
window.PushNotificationManager = PushNotificationManager;