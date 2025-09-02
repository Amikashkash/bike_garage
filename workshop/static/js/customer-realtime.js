/**
 * Customer-specific real-time functionality
 * Extends the base real-time client for customer users
 */

class CustomerRealtime extends BikeGarageRealtime {
    constructor() {
        super();
        this.notificationsCount = 0;
        this.activeRepairs = [];
        this.setupCustomerFeatures();
    }
    
    setupCustomerFeatures() {
        // Get customer data from DOM
        this.getCustomerData();
        
        // Setup customer-specific UI handlers
        this.setupNotificationHandlers();
        this.createCustomerPanel();
        this.loadActiveRepairs();
    }
    
    getCustomerData() {
        const customerElement = document.querySelector('[data-customer-id]');
        if (customerElement) {
            this.customerId = customerElement.dataset.customerId;
        }
    }
    
    // Override connection callbacks
    onConnectionEstablished() {
        console.log('Customer real-time connection established');
        this.updateConnectionStatus(true);
        this.loadNotifications();
    }
    
    onConnectionLost() {
        console.log('Customer real-time connection lost');
        this.updateConnectionStatus(false);
    }
    
    // Customer-specific message handlers
    handleCustomerNotification(data) {
        super.handleCustomerNotification(data);
        this.notificationsCount++;
        this.updateNotificationCounter();
        this.addNotificationToList(data);
        this.showCustomerNotificationModal(data);
    }
    
    handleRepairStatusUpdate(data) {
        super.handleRepairStatusUpdate(data);
        this.updateRepairProgress(data.repair_id, data.status);
        this.showProgressNotification(data);
    }
    
    handleRepairReadyForPickup(data) {
        super.handleRepairReadyForPickup(data);
        this.showReadyForPickupModal(data);
        this.updateRepairToReady(data.repair_id);
    }
    
    // Customer-specific UI methods
    createCustomerPanel() {
        // Add real-time status panel to customer dashboard
        const dashboard = document.querySelector('#customer-dashboard') || document.querySelector('.customer-content');
        if (!dashboard) return;
        
        const panelHtml = `
            <div id="customer-realtime-panel" class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-xl font-bold text-white flex items-center gap-2">
                        <i class="fas fa-bell text-blue-400"></i>
                        עדכונים מקוונים
                    </h3>
                    <div class="flex items-center gap-2">
                        <div id="connection-status" class="w-3 h-3 rounded-full bg-gray-400"></div>
                        <span id="connection-text" class="text-sm text-slate-400">מתחבר...</span>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div class="bg-slate-700/30 border border-slate-600 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-slate-400 text-sm font-medium">התראות חדשות</div>
                                <div id="notifications-counter" class="text-2xl font-bold text-blue-400">${this.notificationsCount}</div>
                            </div>
                            <i class="fas fa-inbox text-blue-400 text-2xl"></i>
                        </div>
                    </div>
                    
                    <div class="bg-slate-700/30 border border-slate-600 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-slate-400 text-sm font-medium">תיקונים פעילים</div>
                                <div id="active-repairs-counter" class="text-2xl font-bold text-purple-400">${this.activeRepairs.length}</div>
                            </div>
                            <i class="fas fa-tools text-purple-400 text-2xl"></i>
                        </div>
                    </div>
                </div>
                
                <div class="flex gap-2 flex-wrap">
                    <button onclick="customerRealtime.showNotificationsList()" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                        <i class="fas fa-list mr-2"></i>כל ההתראות
                    </button>
                    <button onclick="customerRealtime.showRepairsList()" class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                        <i class="fas fa-wrench mr-2"></i>התיקונים שלי
                    </button>
                    <button onclick="customerRealtime.refreshCustomerData()" class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                        <i class="fas fa-sync mr-2"></i>רענן
                    </button>
                </div>
            </div>
        `;
        
        dashboard.insertAdjacentHTML('afterbegin', panelHtml);
    }
    
    updateConnectionStatus(connected) {
        const statusIndicator = document.querySelector('#connection-status');
        const statusText = document.querySelector('#connection-text');
        
        if (statusIndicator && statusText) {
            if (connected) {
                statusIndicator.classList.remove('bg-gray-400', 'bg-red-500');
                statusIndicator.classList.add('bg-green-500');
                statusText.textContent = 'מחובר';
                statusText.classList.remove('text-gray-600', 'text-red-600');
                statusText.classList.add('text-green-600');
            } else {
                statusIndicator.classList.remove('bg-gray-400', 'bg-green-500');
                statusIndicator.classList.add('bg-red-500');
                statusText.textContent = 'לא מחובר';
                statusText.classList.remove('text-gray-600', 'text-green-600');
                statusText.classList.add('text-red-600');
            }
        }
    }
    
    updateNotificationCounter() {
        const counter = document.querySelector('#notifications-counter');
        if (counter) {
            counter.textContent = this.notificationsCount;
            counter.classList.add('animate-pulse');
            setTimeout(() => counter.classList.remove('animate-pulse'), 1000);
        }
    }
    
    showCustomerNotificationModal(data) {
        const modalHtml = `
            <div id="customer-notification-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div class="bg-slate-800/95 backdrop-blur-sm border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
                    <div class="text-center mb-4">
                        <div class="bg-blue-500/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-bell text-blue-400 text-2xl"></i>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-2">${data.title}</h3>
                    </div>
                    
                    <div class="bg-slate-700/30 border border-slate-600 p-4 rounded-lg mb-6">
                        <p class="text-slate-300">${data.message}</p>
                    </div>
                    
                    <div class="flex gap-3">
                        ${data.action_url ? `
                            <button onclick="window.location.href='${data.action_url}'" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                                צפה בפרטים
                            </button>
                        ` : ''}
                        <button onclick="customerRealtime.closeNotificationModal('${data.notification_id}')" class="flex-1 bg-slate-600/50 hover:bg-slate-600 border border-slate-500 text-slate-300 hover:text-white py-2 px-4 rounded-lg font-medium transition-colors">
                            סגור
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Auto-close after 15 seconds
        setTimeout(() => {
            const modal = document.getElementById('customer-notification-modal');
            if (modal) modal.remove();
        }, 15000);
    }
    
    showReadyForPickupModal(data) {
        const modalHtml = `
            <div id="ready-pickup-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div class="bg-slate-800/95 backdrop-blur-sm border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
                    <div class="text-center mb-4">
                        <div class="bg-green-500/20 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-check-circle text-green-400 text-3xl"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-green-400 mb-2">🎉 מוכן לאיסוף!</h3>
                        <p class="text-slate-300">התיקון הושלם בהצלחה</p>
                    </div>
                    
                    <div class="bg-green-500/10 border border-green-500/30 p-4 rounded-lg mb-6">
                        <h4 class="font-semibold text-green-300 mb-2">${data.bike_info}</h4>
                        <p class="text-green-200">${data.message}</p>
                    </div>
                    
                    <div class="bg-yellow-500/10 border border-yellow-500/30 p-3 rounded-lg mb-4">
                        <div class="flex items-center gap-2">
                            <i class="fas fa-clock text-yellow-400"></i>
                            <span class="text-sm text-yellow-200">שעות פתיחה: ראשון-חמישי 8:00-18:00</span>
                        </div>
                    </div>
                    
                    <div class="flex gap-3">
                        <button onclick="window.location.href='/customer/repairs/'" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                            צפה בתיקון
                        </button>
                        <button onclick="document.getElementById('ready-pickup-modal').remove()" class="flex-1 bg-slate-600/50 hover:bg-slate-600 border border-slate-500 text-slate-300 hover:text-white py-2 px-4 rounded-lg font-medium transition-colors">
                            סגור
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Play celebration sound
        this.playCelebrationSound();
    }
    
    showProgressNotification(data) {
        // Show a less intrusive progress notification
        this.showNotification('info', 'עדכון תיקון', data.message, {
            duration: 7000,
            actionUrl: `/customer/repair/${data.repair_id}/`
        });
    }
    
    closeNotificationModal(notificationId) {
        // Mark notification as read
        this.markNotificationRead(notificationId);
        
        // Remove modal
        document.getElementById('customer-notification-modal')?.remove();
    }
    
    updateRepairProgress(repairId, status) {
        const repairElement = document.querySelector(`[data-repair-id="${repairId}"]`);
        if (!repairElement) return;
        
        // Update status display
        const statusElement = repairElement.querySelector('.repair-status');
        if (statusElement) {
            statusElement.textContent = this.getStatusDisplay(status);
            statusElement.className = `repair-status status-${status}`;
        }
        
        // Update progress bar if exists
        const progressBar = repairElement.querySelector('.progress-bar');
        if (progressBar) {
            const progress = this.getStatusProgress(status);
            progressBar.style.width = `${progress}%`;
        }
        
        // Add visual highlight
        repairElement.classList.add('border-blue-300', 'bg-blue-50/20');
        setTimeout(() => {
            repairElement.classList.remove('border-blue-300', 'bg-blue-50/20');
        }, 3000);
    }
    
    updateRepairToReady(repairId) {
        const repairElement = document.querySelector(`[data-repair-id="${repairId}"]`);
        if (!repairElement) return;
        
        // Add ready styling
        repairElement.classList.add('border-green-400', 'bg-green-50');
        
        // Add ready badge
        const badgeHtml = `
            <div class="ready-badge absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full shadow-lg">
                <i class="fas fa-check mr-1"></i>מוכן!
            </div>
        `;
        
        if (repairElement.style.position !== 'relative') {
            repairElement.style.position = 'relative';
        }
        repairElement.insertAdjacentHTML('beforeend', badgeHtml);
    }
    
    addNotificationToList(notification) {
        const listContainer = document.querySelector('#notifications-list');
        if (!listContainer) return;
        
        const itemHtml = `
            <div class="notification-item bg-slate-700/30 border border-slate-600 rounded-lg p-4 mb-3" data-notification-id="${notification.notification_id}">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h4 class="font-semibold text-white">${notification.title}</h4>
                        <p class="text-sm text-slate-300 mt-1">${notification.message}</p>
                        <span class="text-xs text-slate-400 mt-2 block">${new Date().toLocaleString('he-IL')}</span>
                    </div>
                    <div class="flex gap-2">
                        ${notification.action_url ? `
                            <button onclick="window.location.href='${notification.action_url}'" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-xs transition-colors">
                                פרטים
                            </button>
                        ` : ''}
                        <button onclick="customerRealtime.markNotificationRead('${notification.notification_id}')" class="bg-gray-300 hover:bg-gray-400 text-gray-700 px-3 py-1 rounded text-xs transition-colors">
                            סמן כנקרא
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        listContainer.insertAdjacentHTML('afterbegin', itemHtml);
    }
    
    setupNotificationHandlers() {
        // Handle notification actions
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('mark-read-btn')) {
                const notificationId = e.target.dataset.notificationId;
                this.markNotificationRead(notificationId);
            }
        });
    }
    
    loadActiveRepairs() {
        // Load active repairs count from server
        fetch('/api/customer/active-repairs/')
            .then(response => response.json())
            .then(data => {
                this.activeRepairs = data.repairs || [];
                this.updateActiveRepairsCounter();
            })
            .catch(error => console.error('Error loading active repairs:', error));
    }
    
    updateActiveRepairsCounter() {
        const counter = document.querySelector('#active-repairs-counter');
        if (counter) {
            counter.textContent = this.activeRepairs.length;
        }
    }
    
    loadNotifications() {
        // Load unread notifications count from server
        fetch('/api/customer/notifications/')
            .then(response => response.json())
            .then(data => {
                this.notificationsCount = data.unread_count || 0;
                this.updateNotificationCounter();
            })
            .catch(error => console.error('Error loading notifications:', error));
    }
    
    showNotificationsList() {
        // Toggle or create notifications list
        const existing = document.querySelector('#notifications-panel');
        if (existing) {
            existing.remove();
            return;
        }
        
        const panelHtml = `
            <div id="notifications-panel" class="fixed right-4 top-20 w-96 bg-slate-800/95 backdrop-blur-sm border border-slate-700 rounded-xl shadow-xl z-40 max-h-96 overflow-y-auto">
                <div class="p-4 border-b border-slate-600">
                    <div class="flex items-center justify-between">
                        <h3 class="font-bold text-white">התראות</h3>
                        <button onclick="document.getElementById('notifications-panel').remove()" class="text-slate-400 hover:text-white">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div id="notifications-list" class="p-4">
                    <div class="text-center text-gray-500 py-4">
                        טוען התראות...
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', panelHtml);
        
        // Load notifications
        this.loadNotificationsList();
    }
    
    showRepairsList() {
        // Navigate to repairs page or show modal
        window.location.href = '/customer/repairs/';
    }
    
    loadNotificationsList() {
        fetch('/api/customer/notifications/list/')
            .then(response => response.json())
            .then(data => {
                const listContainer = document.querySelector('#notifications-list');
                if (!listContainer) return;
                
                listContainer.innerHTML = '';
                
                if (data.notifications && data.notifications.length > 0) {
                    data.notifications.forEach(notification => {
                        this.addNotificationToList(notification);
                    });
                } else {
                    listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">אין התראות חדשות</div>';
                }
            })
            .catch(error => {
                console.error('Error loading notifications list:', error);
                const listContainer = document.querySelector('#notifications-list');
                if (listContainer) {
                    listContainer.innerHTML = '<div class="text-center text-red-500 py-4">שגיאה בטעינת התראות</div>';
                }
            });
    }
    
    refreshCustomerData() {
        this.loadActiveRepairs();
        this.loadNotifications();
        this.showNotification('success', 'רענון הושלם', 'הנתונים עודכנו בהצלחה', { duration: 3000 });
    }
    
    getStatusDisplay(status) {
        const statusMap = {
            'reported': 'דווח',
            'diagnosed': 'מאובחן',
            'approved': 'אושר',
            'in_progress': 'בביצוע',
            'awaiting_quality_check': 'בדיקת איכות',
            'quality_approved': 'מוכן לאיסוף',
            'completed': 'הושלם',
            'delivered': 'נמסר'
        };
        
        return statusMap[status] || status;
    }
    
    getStatusProgress(status) {
        const progressMap = {
            'reported': 10,
            'diagnosed': 25,
            'approved': 40,
            'in_progress': 60,
            'awaiting_quality_check': 80,
            'quality_approved': 95,
            'completed': 100,
            'delivered': 100
        };
        
        return progressMap[status] || 0;
    }
    
    playCelebrationSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Play a cheerful ascending melody
            const melody = [523, 659, 784, 1047]; // C, E, G, C
            
            melody.forEach((frequency, index) => {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.value = frequency;
                oscillator.type = 'sine';
                
                const startTime = audioContext.currentTime + (index * 0.2);
                const endTime = startTime + 0.3;
                
                gainNode.gain.setValueAtTime(0.1, startTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, endTime);
                
                oscillator.start(startTime);
                oscillator.stop(endTime);
            });
        } catch (error) {
            console.log('Audio context not available');
        }
    }
}

// Initialize customer real-time client if user is customer
document.addEventListener('DOMContentLoaded', () => {
    const userType = document.querySelector('[data-user-type]')?.dataset.userType;
    if (userType === 'customer') {
        window.bikeRealtime = new CustomerRealtime();
        window.customerRealtime = window.bikeRealtime;
    }
});