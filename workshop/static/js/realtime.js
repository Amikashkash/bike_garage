/**
 * Real-time WebSocket Client for Bike Garage
 * Handles WebSocket connections and real-time notifications
 */

class BikeGarageRealtime {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.userType = null;
        this.userId = null;
        this.heartbeatInterval = null;
        
        this.init();
    }
    
    init() {
        // Get user info from DOM or session
        this.getUserInfo();
        
        // Connect if we have user type
        if (this.userType) {
            this.connect();
        }
        
        // Handle page visibility changes
        this.handleVisibilityChange();
        
        // Handle page unload
        this.handlePageUnload();
    }
    
    getUserInfo() {
        // Try to get user type and ID from data attributes
        const userInfoElement = document.querySelector('[data-user-type]');
        if (userInfoElement) {
            this.userType = userInfoElement.dataset.userType;
            this.userId = userInfoElement.dataset.userId;
            console.log(`Real-time client initialized for ${this.userType} (ID: ${this.userId})`);
            return;
        }
        
        // Try session storage
        this.userType = sessionStorage.getItem('user_type') || localStorage.getItem('user_type');
        this.userId = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');
        
        // Try to detect from URL or page content
        if (!this.userType) {
            this.detectUserType();
        }
    }
    
    detectUserType() {
        const path = window.location.pathname;
        if (path.includes('/customer/')) {
            this.userType = 'customer';
        } else if (path.includes('/mechanic/')) {
            this.userType = 'mechanic';
        } else if (path.includes('/manager/')) {
            this.userType = 'manager';
        }
    }
    
    connect() {
        if (!this.userType) {
            console.error('Cannot connect: User type not determined');
            return;
        }
        
        try {
            // Determine WebSocket protocol - force wss for production
            const isProduction = window.location.hostname.includes('onrender.com') || window.location.protocol === 'https:';
            const protocol = isProduction ? 'wss:' : 'ws:';
            const host = window.location.host;
            const wsUrl = `${protocol}//${host}/ws/workshop/${this.userType}/`;
            
            console.log(`Connecting to WebSocket: ${wsUrl}`);
            console.log(`Production mode: ${isProduction}, Protocol: ${protocol}`);
            
            // Add authentication headers if available
            this.socket = new WebSocket(wsUrl);
            
            this.setupEventListeners();
            
        } catch (error) {
            console.error('WebSocket connection error:', error);
            this.scheduleReconnect();
        }
    }
    
    setupEventListeners() {
        this.socket.onopen = (event) => {
            console.log('WebSocket connected');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.startHeartbeat();
            this.onConnectionEstablished();
        };
        
        this.socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };
        
        this.socket.onclose = (event) => {
            console.log('WebSocket disconnected:', event.code, event.reason);
            this.isConnected = false;
            this.stopHeartbeat();
            this.onConnectionLost();
            
            if (event.code !== 1000) { // Not a normal closure
                this.scheduleReconnect();
            }
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.onConnectionError();
        };
    }
    
    handleMessage(data) {
        console.log('Received real-time message:', data);
        
        const { type } = data;
        
        // Handle different message types
        switch (type) {
            case 'connection_established':
                this.handleConnectionEstablished(data);
                break;
            case 'pong':
                this.handlePong(data);
                break;
            case 'repair_status_update':
                this.handleRepairStatusUpdate(data);
                break;
            case 'new_repair_assignment':
                this.handleNewRepairAssignment(data);
                break;
            case 'mechanic_stuck_notification':
                this.handleMechanicStuckNotification(data);
                break;
            case 'customer_notification':
                this.handleCustomerNotification(data);
                break;
            case 'quality_check_ready':
                this.handleQualityCheckReady(data);
                break;
            case 'repair_ready_for_pickup':
                this.handleRepairReadyForPickup(data);
                break;
            case 'stuck_repair_resolved':
                this.handleStuckRepairResolved(data);
                break;
            case 'new_repair_created':
                this.handleNewRepairCreated(data);
                break;
            default:
                console.log('Unhandled message type:', type);
        }
    }
    
    // Message handlers
    handleConnectionEstablished(data) {
        this.showConnectionStatus('success', data.message);
    }
    
    handlePong(data) {
        // Heartbeat response - connection is alive
    }
    
    handleRepairStatusUpdate(data) {
        this.showNotification('info', 'עדכון תיקון', data.message);
        this.updateRepairStatus(data.repair_id, data.status);
        this.playNotificationSound();
    }
    
    handleNewRepairAssignment(data) {
        this.showNotification('success', 'תיקון חדש הוקצה', data.message);
        this.refreshRepairsList();
        this.playNotificationSound('assignment');
    }
    
    handleMechanicStuckNotification(data) {
        this.showNotification('warning', 'מכונאי תקוע', data.message);
        this.highlightStuckRepair(data.repair_id);
        this.playNotificationSound('alert');
    }
    
    handleCustomerNotification(data) {
        this.showNotification('info', data.title, data.message);
        this.addToNotificationsList(data);
        this.playNotificationSound();
    }
    
    handleQualityCheckReady(data) {
        this.showNotification('info', 'בדיקת איכות נדרשת', data.message);
        this.highlightQualityCheck(data.repair_id);
        this.playNotificationSound('quality');
    }
    
    handleRepairReadyForPickup(data) {
        this.showNotification('success', 'מוכן לאיסוף!', data.message);
        this.highlightReadyForPickup(data.repair_id);
        this.playNotificationSound('ready');
    }
    
    handleStuckRepairResolved(data) {
        this.showNotification('success', 'תיקון שוחרר', data.message);
        this.clearStuckHighlight(data.repair_id);
        this.playNotificationSound();
    }
    
    handleNewRepairCreated(data) {
        this.showNotification('info', 'תיקון חדש נוצר', data.message);
        this.refreshRepairsList();
        this.playNotificationSound();
    }
    
    // Utility methods
    send(data) {
        if (this.isConnected && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        } else {
            console.error('Cannot send message: WebSocket not connected');
        }
    }
    
    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            this.send({
                type: 'ping',
                timestamp: Date.now()
            });
        }, 30000); // Every 30 seconds
    }
    
    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }
    
    scheduleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached');
            this.showConnectionStatus('error', 'החיבור המקוון נותק - רענן את הדף');
        }
    }
    
    disconnect() {
        if (this.socket) {
            this.socket.close(1000, 'User disconnected');
        }
        this.stopHeartbeat();
    }
    
    // UI update methods
    showNotification(type, title, message, options = {}) {
        const colors = {
            success: 'from-green-500 to-green-600',
            error: 'from-red-500 to-red-600', 
            warning: 'from-yellow-500 to-orange-500',
            info: 'from-blue-500 to-blue-600'
        };
        
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        
        const notificationId = 'realtime-notification-' + Date.now();
        const duration = options.duration || 5000;
        
        const notificationHtml = `
            <div id="${notificationId}" class="fixed top-4 right-4 bg-gradient-to-r ${colors[type]} text-white p-4 rounded-xl shadow-lg z-50 max-w-sm transition-all duration-300 transform translate-x-full opacity-0">
                <div class="flex items-start gap-3">
                    <i class="fas fa-${icons[type]} text-xl flex-shrink-0 mt-0.5"></i>
                    <div class="flex-1 min-w-0">
                        <h4 class="font-bold text-white mb-1">${title}</h4>
                        <p class="text-white/90 text-sm">${message}</p>
                        ${options.actionUrl ? `
                            <button onclick="window.location.href='${options.actionUrl}'" class="mt-2 bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-lg text-sm transition-colors">
                                צפה בפרטים
                            </button>
                        ` : ''}
                    </div>
                    <button onclick="document.getElementById('${notificationId}').remove()" class="text-white/80 hover:text-white flex-shrink-0">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', notificationHtml);
        
        // Animate in
        setTimeout(() => {
            const notification = document.getElementById(notificationId);
            if (notification) {
                notification.classList.remove('translate-x-full', 'opacity-0');
                notification.classList.add('translate-x-0', 'opacity-100');
            }
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            const notification = document.getElementById(notificationId);
            if (notification) {
                notification.classList.add('translate-x-full', 'opacity-0');
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }
    
    showConnectionStatus(type, message) {
        const statusId = 'connection-status';
        const existingStatus = document.getElementById(statusId);
        if (existingStatus) existingStatus.remove();
        
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500'
        };
        
        const statusHtml = `
            <div id="${statusId}" class="fixed bottom-4 left-4 ${colors[type]} text-white px-4 py-2 rounded-lg text-sm z-50 transition-all duration-300 transform translate-y-full opacity-0">
                <div class="flex items-center gap-2">
                    <i class="fas fa-wifi"></i>
                    <span>${message}</span>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', statusHtml);
        
        // Animate in
        setTimeout(() => {
            const status = document.getElementById(statusId);
            if (status) {
                status.classList.remove('translate-y-full', 'opacity-0');
                status.classList.add('translate-y-0', 'opacity-100');
            }
        }, 100);
        
        // Auto remove for success/info
        if (type !== 'error') {
            setTimeout(() => {
                const status = document.getElementById(statusId);
                if (status) {
                    status.classList.add('translate-y-full', 'opacity-0');
                    setTimeout(() => status.remove(), 300);
                }
            }, 3000);
        }
    }
    
    playNotificationSound(soundType = 'default') {
        // Create different sounds for different types of notifications
        const frequencies = {
            default: [800, 600],
            assignment: [900, 700],
            alert: [1000, 500],
            quality: [700, 800],
            ready: [600, 800, 1000]
        };
        
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const frequencies_list = frequencies[soundType] || frequencies.default;
            
            frequencies_list.forEach((freq, index) => {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.value = freq;
                oscillator.type = 'sine';
                
                const startTime = audioContext.currentTime + (index * 0.2);
                const endTime = startTime + 0.15;
                
                gainNode.gain.setValueAtTime(0.1, startTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, endTime);
                
                oscillator.start(startTime);
                oscillator.stop(endTime);
            });
        } catch (error) {
            console.log('Audio context not available');
        }
    }
    
    // DOM manipulation methods
    updateRepairStatus(repairId, status) {
        const repairElements = document.querySelectorAll(`[data-repair-id="${repairId}"]`);
        repairElements.forEach(element => {
            const statusElement = element.querySelector('.repair-status');
            if (statusElement) {
                statusElement.textContent = status;
                statusElement.className = `repair-status status-${status}`;
            }
        });
    }
    
    refreshRepairsList() {
        // Trigger a refresh of the repairs list if on a relevant page
        const refreshButton = document.querySelector('[data-refresh-repairs]');
        if (refreshButton) {
            refreshButton.click();
        } else {
            // Fallback: reload the page if no refresh mechanism available
            if (window.location.pathname.includes('dashboard') || 
                window.location.pathname.includes('repairs')) {
                setTimeout(() => window.location.reload(), 1000);
            }
        }
    }
    
    highlightStuckRepair(repairId) {
        const repairElement = document.querySelector(`[data-repair-id="${repairId}"]`);
        if (repairElement) {
            repairElement.classList.add('border-red-500', 'bg-red-50/20');
            repairElement.setAttribute('data-stuck', 'true');
        }
    }
    
    clearStuckHighlight(repairId) {
        const repairElement = document.querySelector(`[data-repair-id="${repairId}"]`);
        if (repairElement) {
            repairElement.classList.remove('border-red-500', 'bg-red-50/20');
            repairElement.removeAttribute('data-stuck');
        }
    }
    
    highlightQualityCheck(repairId) {
        const repairElement = document.querySelector(`[data-repair-id="${repairId}"]`);
        if (repairElement) {
            repairElement.classList.add('border-yellow-500', 'bg-yellow-50/20');
            repairElement.setAttribute('data-quality-check', 'true');
        }
    }
    
    highlightReadyForPickup(repairId) {
        const repairElement = document.querySelector(`[data-repair-id="${repairId}"]`);
        if (repairElement) {
            repairElement.classList.add('border-green-500', 'bg-green-50/20');
            repairElement.setAttribute('data-ready', 'true');
        }
    }
    
    addToNotificationsList(notification) {
        // Add to notifications list if exists
        const notificationsList = document.querySelector('#notifications-list');
        if (notificationsList) {
            const notificationHtml = `
                <div class="notification-item p-3 border-b border-gray-200" data-notification-id="${notification.notification_id}">
                    <h4 class="font-semibold">${notification.title}</h4>
                    <p class="text-gray-600">${notification.message}</p>
                    <span class="text-xs text-gray-400">${new Date().toLocaleString('he-IL')}</span>
                </div>
            `;
            notificationsList.insertAdjacentHTML('afterbegin', notificationHtml);
        }
    }
    
    // Event handlers
    handleVisibilityChange() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Page is hidden - can reduce frequency of heartbeat
                this.stopHeartbeat();
            } else {
                // Page is visible again - resume heartbeat
                if (this.isConnected) {
                    this.startHeartbeat();
                }
            }
        });
    }
    
    handlePageUnload() {
        window.addEventListener('beforeunload', () => {
            this.disconnect();
        });
    }
    
    // Connection event callbacks (override these in specific implementations)
    onConnectionEstablished() {
        // Override in specific user type implementations
    }
    
    onConnectionLost() {
        // Override in specific user type implementations
    }
    
    onConnectionError() {
        // Override in specific user type implementations
    }
    
    // Public API methods
    markNotificationRead(notificationId) {
        this.send({
            type: 'mark_notification_read',
            notification_id: notificationId
        });
    }
    
    getConnectionStatus() {
        return {
            connected: this.isConnected,
            userType: this.userType,
            userId: this.userId,
            reconnectAttempts: this.reconnectAttempts
        };
    }
}

// Initialize real-time client when DOM is loaded
let bikeRealtime;
document.addEventListener('DOMContentLoaded', () => {
    bikeRealtime = new BikeGarageRealtime();
});

// Export for global access
window.bikeRealtime = bikeRealtime;