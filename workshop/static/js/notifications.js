/**
 * Push Notification Manager for Bike Garage
 * Handles push notification subscriptions and display
 */

class BikeGarageNotifications {
    constructor() {
        this.vapidPublicKey = null;
        this.customerId = null;
        this.isSupported = this.checkSupport();
        this.isSubscribed = false;
        this.subscription = null;
        
        this.init();
    }
    
    checkSupport() {
        return 'serviceWorker' in navigator && 
               'PushManager' in window && 
               'Notification' in window;
    }
    
    async init() {
        if (!this.isSupported) {
            console.log('Push notifications not supported');
            return;
        }
        
        // Get customer ID from session/DOM
        this.customerId = this.getCustomerId();
        
        // Register service worker
        await this.registerServiceWorker();
        
        // Get VAPID public key
        await this.getVapidKey();
        
        // Check current subscription status
        await this.checkSubscriptionStatus();
        
        // Show notification permission request if needed
        this.showNotificationPrompt();
    }
    
    getCustomerId() {
        // Try to get customer ID from various sources
        const customerIdElement = document.querySelector('[data-customer-id]');
        if (customerIdElement) {
            return customerIdElement.dataset.customerId;
        }
        
        // Try session storage
        return sessionStorage.getItem('customer_id') || localStorage.getItem('customer_id');
    }
    
    async registerServiceWorker() {
        try {
            const registration = await navigator.serviceWorker.register('/sw.js');
            console.log('Service Worker registered:', registration);
            this.swRegistration = registration;
            return registration;
        } catch (error) {
            console.error('Service Worker registration failed:', error);
            throw error;
        }
    }
    
    async getVapidKey() {
        try {
            const response = await fetch('/api/notifications/vapid-key/');
            const data = await response.json();
            this.vapidPublicKey = data.publicKey;
            console.log('VAPID key retrieved');
        } catch (error) {
            console.error('Failed to get VAPID key:', error);
        }
    }
    
    async checkSubscriptionStatus() {
        if (!this.swRegistration) return;
        
        try {
            this.subscription = await this.swRegistration.pushManager.getSubscription();
            this.isSubscribed = !!this.subscription;
            console.log('Subscription status:', this.isSubscribed);
        } catch (error) {
            console.error('Error checking subscription:', error);
        }
    }
    
    async requestNotificationPermission() {
        if (!this.isSupported) return false;
        
        try {
            const permission = await Notification.requestPermission();
            console.log('Notification permission:', permission);
            return permission === 'granted';
        } catch (error) {
            console.error('Error requesting notification permission:', error);
            return false;
        }
    }
    
    async subscribe() {
        if (!this.vapidPublicKey || !this.customerId) {
            console.error('Missing VAPID key or customer ID');
            return false;
        }
        
        const hasPermission = await this.requestNotificationPermission();
        if (!hasPermission) {
            console.log('Notification permission denied');
            return false;
        }
        
        try {
            const applicationServerKey = this.urlB64ToUint8Array(this.vapidPublicKey);
            
            this.subscription = await this.swRegistration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: applicationServerKey
            });
            
            // Send subscription to server
            const response = await fetch('/api/notifications/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    customer_id: this.customerId,
                    endpoint: this.subscription.endpoint,
                    keys: {
                        p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(this.subscription.getKey('p256dh')))),
                        auth: btoa(String.fromCharCode.apply(null, new Uint8Array(this.subscription.getKey('auth'))))
                    },
                    deviceType: this.getDeviceType(),
                    userAgent: navigator.userAgent
                })
            });
            
            const result = await response.json();
            if (result.success) {
                this.isSubscribed = true;
                console.log('Push notification subscription successful');
                this.showNotificationStatus('success', 'התראות דחיפה הופעלו בהצלחה! 🔔');
                return true;
            } else {
                console.error('Failed to register subscription:', result.error);
                return false;
            }
            
        } catch (error) {
            console.error('Error subscribing to push notifications:', error);
            return false;
        }
    }
    
    async unsubscribe() {
        if (!this.subscription) return true;
        
        try {
            // Unsubscribe from browser
            await this.subscription.unsubscribe();
            
            // Notify server
            await fetch('/api/notifications/unsubscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    customer_id: this.customerId,
                    endpoint: this.subscription.endpoint
                })
            });
            
            this.subscription = null;
            this.isSubscribed = false;
            console.log('Push notification unsubscribed');
            this.showNotificationStatus('info', 'התראות דחיפה הופסקו');
            return true;
            
        } catch (error) {
            console.error('Error unsubscribing:', error);
            return false;
        }
    }
    
    async sendTestNotification() {
        if (!this.customerId) {
            console.error('Customer ID not found');
            return;
        }
        
        try {
            const response = await fetch('/api/notifications/test/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    customer_id: this.customerId
                })
            });
            
            const result = await response.json();
            if (result.success) {
                this.showNotificationStatus('success', 'הודעת בדיקה נשלחה!');
            } else {
                this.showNotificationStatus('error', 'שגיאה בשליחת הודעת בדיקה');
            }
        } catch (error) {
            console.error('Error sending test notification:', error);
        }
    }
    
    urlB64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');
        
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
    
    getDeviceType() {
        const userAgent = navigator.userAgent;
        if (/android/i.test(userAgent)) return 'Android';
        if (/iPad|iPhone|iPod/.test(userAgent)) return 'iOS';
        if (/Windows/i.test(userAgent)) return 'Windows';
        if (/Mac/i.test(userAgent)) return 'Mac';
        if (/Linux/i.test(userAgent)) return 'Linux';
        return 'Unknown';
    }
    
    showNotificationPrompt() {
        if (!this.isSupported || this.isSubscribed || !this.customerId) return;
        
        // Create notification prompt
        const promptHtml = `
            <div id="notification-prompt" class="fixed bottom-4 left-4 right-4 max-w-md mx-auto bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-xl shadow-lg z-50 transition-all duration-300 transform translate-y-full opacity-0">
                <div class="flex items-start gap-3">
                    <div class="flex-shrink-0">
                        <i class="fas fa-bell text-yellow-300 text-xl"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <h4 class="font-bold text-white mb-1">התראות דחיפה 🔔</h4>
                        <p class="text-blue-100 text-sm mb-3">קבל התראות כשהתיקון מוכן לאיסוף או כשנדרש אישור</p>
                        <div class="flex gap-2">
                            <button onclick="bikeNotifications.subscribe()" class="bg-slate-800/70 hover:bg-slate-700 text-white border border-slate-600 px-3 py-1 rounded-lg text-sm font-medium transition-colors">
                                אפשר התראות
                            </button>
                            <button onclick="document.getElementById('notification-prompt').remove()" class="bg-blue-500/20 text-white px-3 py-1 rounded-lg text-sm hover:bg-blue-500/30 transition-colors">
                                לא עכשיו
                            </button>
                        </div>
                    </div>
                    <button onclick="document.getElementById('notification-prompt').remove()" class="flex-shrink-0 text-blue-200 hover:text-white">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        
        // Add to DOM if not exists
        if (!document.getElementById('notification-prompt')) {
            document.body.insertAdjacentHTML('beforeend', promptHtml);
            
            // Animate in
            setTimeout(() => {
                const prompt = document.getElementById('notification-prompt');
                if (prompt) {
                    prompt.classList.remove('translate-y-full', 'opacity-0');
                    prompt.classList.add('translate-y-0', 'opacity-100');
                }
            }, 1000);
        }
    }
    
    showNotificationStatus(type, message) {
        const colors = {
            success: 'from-green-500 to-green-600',
            error: 'from-red-500 to-red-600',
            info: 'from-blue-500 to-blue-600'
        };
        
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            info: 'info-circle'
        };
        
        const statusHtml = `
            <div id="notification-status" class="fixed top-4 right-4 bg-gradient-to-r ${colors[type]} text-white p-4 rounded-xl shadow-lg z-50 max-w-sm transition-all duration-300 transform translate-x-full opacity-0">
                <div class="flex items-center gap-3">
                    <i class="fas fa-${icons[type]} text-xl"></i>
                    <span class="flex-1">${message}</span>
                    <button onclick="document.getElementById('notification-status').remove()" class="text-white/80 hover:text-white">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        
        // Remove existing status
        const existing = document.getElementById('notification-status');
        if (existing) existing.remove();
        
        // Add new status
        document.body.insertAdjacentHTML('beforeend', statusHtml);
        
        // Animate in
        setTimeout(() => {
            const status = document.getElementById('notification-status');
            if (status) {
                status.classList.remove('translate-x-full', 'opacity-0');
                status.classList.add('translate-x-0', 'opacity-100');
            }
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            const status = document.getElementById('notification-status');
            if (status) {
                status.classList.add('translate-x-full', 'opacity-0');
                setTimeout(() => status.remove(), 300);
            }
        }, 5000);
    }
    
    createNotificationPanel() {
        const panelHtml = `
            <div id="notification-panel" class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
                <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fas fa-bell text-blue-400"></i>
                    התראות
                </h3>
                <div class="space-y-4">
                    <div class="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                        <div class="flex items-center gap-3">
                            <i class="fas fa-mobile-alt text-green-400"></i>
                            <div>
                                <div class="text-white font-medium">התראות דחיפה</div>
                                <div class="text-slate-400 text-sm">קבל התראות ישירות למכשיר</div>
                            </div>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" id="push-notifications-toggle" class="sr-only peer" ${this.isSubscribed ? 'checked' : ''}>
                            <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                    </div>
                    
                    <div class="flex gap-2">
                        <button onclick="bikeNotifications.sendTestNotification()" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                            <i class="fas fa-paper-plane mr-2"></i>שלח הודעת בדיקה
                        </button>
                        <button onclick="bikeNotifications.checkSubscriptionStatus()" class="bg-slate-600 hover:bg-slate-500 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                            <i class="fas fa-sync mr-2"></i>בדק סטטוס
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        return panelHtml;
    }
}

// Initialize notifications when DOM is loaded
let bikeNotifications;
document.addEventListener('DOMContentLoaded', () => {
    bikeNotifications = new BikeGarageNotifications();
    
    // Add toggle listener
    document.addEventListener('change', (e) => {
        if (e.target.id === 'push-notifications-toggle') {
            if (e.target.checked) {
                bikeNotifications.subscribe();
            } else {
                bikeNotifications.unsubscribe();
            }
        }
    });
});

// Export for global access
window.bikeNotifications = bikeNotifications;
