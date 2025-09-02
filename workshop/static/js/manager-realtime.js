/**
 * Manager-specific real-time functionality
 * Extends the base real-time client for manager users
 */

class ManagerRealtime extends BikeGarageRealtime {
    constructor() {
        super();
        this.stuckRepairsCount = 0;
        this.qualityChecksCount = 0;
        this.setupManagerFeatures();
    }
    
    setupManagerFeatures() {
        // Get current counts from DOM
        this.updateCounts();
        
        // Setup manager-specific UI handlers
        this.setupQualityCheckHandlers();
        this.setupStuckRepairHandlers();
        this.createManagerDashboard();
    }
    
    // Override connection callbacks
    onConnectionEstablished() {
        console.log('Manager real-time connection established');
        this.updateConnectionIndicator(true);
        this.refreshManagerStats();
    }
    
    onConnectionLost() {
        console.log('Manager real-time connection lost');
        this.updateConnectionIndicator(false);
    }
    
    // Manager-specific message handlers
    handleMechanicStuckNotification(data) {
        super.handleMechanicStuckNotification(data);
        this.stuckRepairsCount++;
        this.updateStuckCounter();
        this.addToStuckRepairsList(data);
        this.showStuckRepairModal(data);
    }
    
    handleQualityCheckReady(data) {
        super.handleQualityCheckReady(data);
        this.qualityChecksCount++;
        this.updateQualityCounter();
        this.addToQualityChecksList(data);
    }
    
    handleNewRepairCreated(data) {
        super.handleNewRepairCreated(data);
        this.updateNewRepairsCounter();
        this.addToNewRepairsList(data);
        
        // Update specific status counter based on repair status FIRST
        this.updateStatusCounter(data.status, 1); // +1 for new repair
        
        // Show notification about the update
        this.showCounterUpdateNotification(data);
        
        // Refresh the dashboard after a short delay to show the counter update
        this.refreshManagerDashboard();
    }
    
    handleRepairApproved(data) {
        super.handleRepairApproved(data);
        
        // Update counters: -1 from pending approval, +1 to approved waiting
        this.updateStatusCounter('pending_approval', -1);
        this.updateStatusCounter('approved_waiting_for_mechanic', 1);
        
        // Show specific notification for manager
        this.showCounterUpdateNotification({
            bike_info: data.bike_info,
            customer_name: data.customer_name,
            status: 'approved_waiting_for_mechanic'
        });
        
        console.log(`✅ Repair #${data.repair_id} approved by customer - updated counters`);
        
        // Refresh the dashboard to show updated lists
        this.refreshManagerDashboard();
    }
    
    handleRepairPartiallyApproved(data) {
        super.handleRepairPartiallyApproved(data);
        
        // For partial approval, we keep it in pending_approval but show notification
        // The counter doesn't change since it's still awaiting full approval
        
        // Show specific notification for manager
        this.showPartialApprovalNotification(data);
        
        console.log(`⚠️ Repair #${data.repair_id} partially approved by customer (${data.approved_count}/${data.total_count})`);
        
        // Refresh to show updated status in the lists
        this.refreshManagerDashboard();
    }
    
    // Manager-specific UI methods
    createManagerDashboard() {
        // Add real-time status panel to manager dashboard
        const dashboard = document.querySelector('#manager-dashboard');
        if (!dashboard) return;
        
        const statusPanelHtml = `
            <div id="realtime-status-panel" class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
                <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fas fa-broadcast-tower text-green-400"></i>
                    סטטוס מקוון
                    <div id="connection-indicator" class="w-3 h-3 rounded-full bg-gray-500"></div>
                </h3>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-red-500/20 border border-red-500/30 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-red-300 text-sm font-medium">תיקונים תקועים</div>
                                <div id="stuck-counter" class="text-2xl font-bold text-red-400">${this.stuckRepairsCount}</div>
                            </div>
                            <i class="fas fa-exclamation-triangle text-red-400 text-2xl"></i>
                        </div>
                    </div>
                    
                    <div class="bg-yellow-500/20 border border-yellow-500/30 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-yellow-300 text-sm font-medium">בדיקות איכות</div>
                                <div id="quality-counter" class="text-2xl font-bold text-yellow-400">${this.qualityChecksCount}</div>
                            </div>
                            <i class="fas fa-clipboard-check text-yellow-400 text-2xl"></i>
                        </div>
                    </div>
                    
                    <div class="bg-blue-500/20 border border-blue-500/30 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-blue-300 text-sm font-medium">תיקונים חדשים</div>
                                <div id="new-repairs-counter" class="text-2xl font-bold text-blue-400">0</div>
                            </div>
                            <i class="fas fa-plus-circle text-blue-400 text-2xl"></i>
                        </div>
                    </div>
                </div>
                
                <div class="mt-4 flex gap-2">
                    <button onclick="managerRealtime.refreshManagerStats()" class="bg-slate-600 hover:bg-slate-500 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                        <i class="fas fa-sync mr-2"></i>רענן נתונים
                    </button>
                    <button onclick="managerRealtime.showStuckRepairsList()" class="bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/30 px-4 py-2 rounded-lg text-sm transition-colors">
                        <i class="fas fa-list mr-2"></i>תיקונים תקועים
                    </button>
                    <button onclick="managerRealtime.showQualityChecksList()" class="bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-400 border border-yellow-500/30 px-4 py-2 rounded-lg text-sm transition-colors">
                        <i class="fas fa-clipboard-list mr-2"></i>בדיקות איכות
                    </button>
                </div>
            </div>
        `;
        
        dashboard.insertAdjacentHTML('afterbegin', statusPanelHtml);
    }
    
    updateConnectionIndicator(connected) {
        const indicator = document.querySelector('#connection-indicator');
        if (indicator) {
            if (connected) {
                indicator.classList.remove('bg-red-500', 'bg-gray-500');
                indicator.classList.add('bg-green-500');
                indicator.title = 'מחובר לעדכונים מקוונים';
            } else {
                indicator.classList.remove('bg-green-500', 'bg-gray-500');
                indicator.classList.add('bg-red-500');
                indicator.title = 'לא מחובר לעדכונים מקוונים';
            }
        }
    }
    
    updateCounts() {
        // Get counts from existing DOM elements
        const stuckElement = document.querySelector('#stuck-counter');
        const qualityElement = document.querySelector('#quality-counter');
        
        if (stuckElement) {
            this.stuckRepairsCount = parseInt(stuckElement.textContent) || 0;
        }
        if (qualityElement) {
            this.qualityChecksCount = parseInt(qualityElement.textContent) || 0;
        }
    }
    
    updateStuckCounter() {
        const counter = document.querySelector('#stuck-counter');
        if (counter) {
            counter.textContent = this.stuckRepairsCount;
            counter.classList.add('animate-pulse');
            setTimeout(() => counter.classList.remove('animate-pulse'), 1000);
        }
    }
    
    updateQualityCounter() {
        const counter = document.querySelector('#quality-counter');
        if (counter) {
            counter.textContent = this.qualityChecksCount;
            counter.classList.add('animate-pulse');
            setTimeout(() => counter.classList.remove('animate-pulse'), 1000);
        }
    }
    
    updateNewRepairsCounter() {
        const counter = document.querySelector('#new-repairs-counter');
        if (counter) {
            const currentCount = parseInt(counter.textContent) || 0;
            counter.textContent = currentCount + 1;
            counter.classList.add('animate-pulse');
            setTimeout(() => counter.classList.remove('animate-pulse'), 1000);
        }
    }
    
    showStuckRepairModal(data) {
        const modalHtml = `
            <div id="stuck-repair-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-xl p-6 max-w-lg w-full shadow-2xl">
                    <div class="text-center mb-4">
                        <div class="bg-red-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-exclamation-triangle text-red-600 text-2xl"></i>
                        </div>
                        <h3 class="text-xl font-bold text-gray-800 mb-2">מכונאי תקוע!</h3>
                    </div>
                    
                    <div class="space-y-3 mb-6">
                        <div class="bg-gray-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">מכונאי</div>
                            <div class="font-semibold">${data.mechanic_name}</div>
                        </div>
                        <div class="bg-gray-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">אופניים</div>
                            <div class="font-semibold">${data.bike_info}</div>
                        </div>
                        <div class="bg-gray-50 p-3 rounded-lg">
                            <div class="text-sm text-gray-600">לקוח</div>
                            <div class="font-semibold">${data.customer_name}</div>
                        </div>
                        <div class="bg-red-50 p-3 rounded-lg border border-red-200">
                            <div class="text-sm text-red-600 font-medium">סיבת החסימה</div>
                            <div class="text-red-800">${data.reason}</div>
                        </div>
                    </div>
                    
                    <div class="flex gap-3">
                        <button onclick="managerRealtime.handleStuckRepair(${data.repair_id})" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                            טפל בתיקון
                        </button>
                        <button onclick="document.getElementById('stuck-repair-modal').remove()" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors">
                            סגור
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Auto-remove after 60 seconds
        setTimeout(() => {
            const modal = document.getElementById('stuck-repair-modal');
            if (modal) modal.remove();
        }, 60000);
    }
    
    handleStuckRepair(repairId) {
        // Close modal
        document.getElementById('stuck-repair-modal')?.remove();
        
        // Navigate to stuck repair management
        window.location.href = `/manager/stuck-repair/${repairId}/`;
    }
    
    addToStuckRepairsList(data) {
        const listContainer = document.querySelector('#stuck-repairs-list');
        if (!listContainer) return;
        
        const itemHtml = `
            <div class="stuck-repair-item bg-red-50 border border-red-200 rounded-lg p-4 mb-3" data-repair-id="${data.repair_id}">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h4 class="font-semibold text-red-800">${data.bike_info}</h4>
                        <p class="text-sm text-red-600">מכונאי: ${data.mechanic_name}</p>
                        <p class="text-sm text-red-600">לקוח: ${data.customer_name}</p>
                        <p class="text-xs text-red-500 mt-1">${data.reason}</p>
                    </div>
                    <button onclick="managerRealtime.handleStuckRepair(${data.repair_id})" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors">
                        טפל
                    </button>
                </div>
            </div>
        `;
        
        listContainer.insertAdjacentHTML('afterbegin', itemHtml);
    }
    
    addToQualityChecksList(data) {
        const listContainer = document.querySelector('#quality-checks-list');
        if (!listContainer) return;
        
        const itemHtml = `
            <div class="quality-check-item bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-3" data-repair-id="${data.repair_id}">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h4 class="font-semibold text-yellow-800">${data.bike_info}</h4>
                        <p class="text-sm text-yellow-600">מכונאי: ${data.mechanic_name}</p>
                        <p class="text-sm text-yellow-600">לקוח: ${data.customer_name}</p>
                    </div>
                    <button onclick="window.location.href='/manager/quality-check/${data.repair_id}/'" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition-colors">
                        בדוק איכות
                    </button>
                </div>
            </div>
        `;
        
        listContainer.insertAdjacentHTML('afterbegin', itemHtml);
    }
    
    addToNewRepairsList(data) {
        const listContainer = document.querySelector('#new-repairs-list');
        if (!listContainer) return;
        
        const itemHtml = `
            <div class="new-repair-item bg-blue-50 border border-blue-200 rounded-lg p-4 mb-3" data-repair-id="${data.repair_id}">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h4 class="font-semibold text-blue-800">${data.bike_info}</h4>
                        <p class="text-sm text-blue-600">לקוח: ${data.customer_name}</p>
                        <p class="text-xs text-blue-500 mt-1">${data.problem_description}</p>
                    </div>
                    <button onclick="window.location.href='/manager/assign/${data.repair_id}/'" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors">
                        הקצה מכונאי
                    </button>
                </div>
            </div>
        `;
        
        listContainer.insertAdjacentHTML('afterbegin', itemHtml);
    }
    
    setupQualityCheckHandlers() {
        // Handle quality check approval
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('approve-quality-btn')) {
                const repairId = e.target.dataset.repairId;
                this.approveQualityCheck(repairId);
            }
        });
    }
    
    setupStuckRepairHandlers() {
        // Handle stuck repair resolution
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('resolve-stuck-btn')) {
                const repairId = e.target.dataset.repairId;
                this.showResolveStuckModal(repairId);
            }
        });
    }
    
    approveQualityCheck(repairId) {
        // Send real-time update
        this.send({
            type: 'approve_quality',
            repair_id: repairId
        });
        
        // Update local counter
        this.qualityChecksCount--;
        this.updateQualityCounter();
        
        // Remove from list
        const item = document.querySelector(`[data-repair-id="${repairId}"].quality-check-item`);
        if (item) item.remove();
    }
    
    showResolveStuckModal(repairId) {
        const modalHtml = `
            <div id="resolve-stuck-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl">
                    <div class="text-center mb-4">
                        <div class="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-check-circle text-green-600 text-2xl"></i>
                        </div>
                        <h3 class="text-xl font-bold text-gray-800 mb-2">פתירת תיקון תקוע</h3>
                        <p class="text-gray-600">הוסף הנחיות למכונאי</p>
                    </div>
                    
                    <form id="resolve-stuck-form" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">הנחיות למכונאי</label>
                            <textarea name="manager_response" rows="4" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="הוסף הנחיות או פתרון..." required></textarea>
                        </div>
                        
                        <div class="flex gap-3">
                            <button type="submit" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                                שחרר תיקון
                            </button>
                            <button type="button" onclick="document.getElementById('resolve-stuck-modal').remove()" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors">
                                ביטול
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Handle form submission
        document.getElementById('resolve-stuck-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            this.resolveStuckRepair(repairId, formData.get('manager_response'));
            document.getElementById('resolve-stuck-modal').remove();
        });
    }
    
    resolveStuckRepair(repairId, response) {
        // Send real-time update
        this.send({
            type: 'resolve_stuck_repair',
            repair_id: repairId,
            manager_response: response
        });
        
        // Update local counter
        this.stuckRepairsCount--;
        this.updateStuckCounter();
        
        // Remove from list
        const item = document.querySelector(`[data-repair-id="${repairId}"].stuck-repair-item`);
        if (item) item.remove();
        
        // Also send to server via AJAX
        fetch(`/manager/resolve-stuck/${repairId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ manager_response: response })
        });
    }
    
    refreshManagerStats() {
        // Refresh stats from server
        fetch('/api/manager/stats/')
            .then(response => response.json())
            .then(data => {
                this.stuckRepairsCount = data.stuck_repairs || 0;
                this.qualityChecksCount = data.quality_checks || 0;
                this.updateStuckCounter();
                this.updateQualityCounter();
            })
            .catch(error => console.error('Error refreshing stats:', error));
    }
    
    showStuckRepairsList() {
        // Toggle or create stuck repairs list
        const existing = document.querySelector('#stuck-repairs-panel');
        if (existing) {
            existing.remove();
            return;
        }
        
        const panelHtml = `
            <div id="stuck-repairs-panel" class="fixed right-4 top-20 w-96 bg-white border border-gray-200 rounded-xl shadow-xl z-40 max-h-96 overflow-y-auto">
                <div class="p-4 border-b border-gray-200">
                    <div class="flex items-center justify-between">
                        <h3 class="font-bold text-gray-800">תיקונים תקועים</h3>
                        <button onclick="document.getElementById('stuck-repairs-panel').remove()" class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div id="stuck-repairs-list" class="p-4">
                    <!-- Items will be populated by real-time updates -->
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', panelHtml);
    }
    
    showQualityChecksList() {
        // Toggle or create quality checks list
        const existing = document.querySelector('#quality-checks-panel');
        if (existing) {
            existing.remove();
            return;
        }
        
        const panelHtml = `
            <div id="quality-checks-panel" class="fixed right-4 top-20 w-96 bg-white border border-gray-200 rounded-xl shadow-xl z-40 max-h-96 overflow-y-auto">
                <div class="p-4 border-b border-gray-200">
                    <div class="flex items-center justify-between">
                        <h3 class="font-bold text-gray-800">בדיקות איכות</h3>
                        <button onclick="document.getElementById('quality-checks-panel').remove()" class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div id="quality-checks-list" class="p-4">
                    <!-- Items will be populated by real-time updates -->
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', panelHtml);
    }
    
    // Override the base refreshRepairsList method for manager dashboard
    refreshRepairsList() {
        this.refreshManagerDashboard();
    }
    
    updateStatusCounter(status, increment) {
        // Update specific dashboard section counters based on repair status
        let sectionId;
        
        switch(status) {
            case 'pending_diagnosis':
                sectionId = '#pending-diagnosis-count';
                break;
            case 'pending_approval':
                sectionId = '#pending-approval-count';
                break;
            case 'approved_waiting_for_mechanic':
                sectionId = '#approved-waiting-count';
                break;
            case 'in_progress':
                sectionId = '#in-progress-count';
                break;
            case 'awaiting_quality_check':
                sectionId = '#quality-check-count';
                break;
            case 'ready_for_collection':
                sectionId = '#ready-collection-count';
                break;
            default:
                console.log('Unknown status for counter update:', status);
                return;
        }
        
        // Find counter element and update
        const counter = document.querySelector(sectionId);
        if (counter) {
            const currentCount = parseInt(counter.textContent) || 0;
            const newCount = Math.max(0, currentCount + increment);
            counter.textContent = newCount;
            
            // Add animation
            counter.classList.add('animate-pulse');
            setTimeout(() => counter.classList.remove('animate-pulse'), 1000);
            
            console.log(`Updated ${status} counter: ${currentCount} -> ${newCount}`);
        }
    }
    
    showCounterUpdateNotification(data) {
        // Show a brief notification about the counter update
        const statusText = this.getStatusDisplayText(data.status);
        console.log(`📊 Counter updated: ${statusText} +1 (${data.bike_info})`);
        
        // Create a temporary notification element
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 transform transition-all duration-300';
        notification.innerHTML = `
            <div class="flex items-center gap-2">
                <i class="fas fa-plus-circle"></i>
                <span>עדכון: ${statusText} +1</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('translate-x-0'), 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    showPartialApprovalNotification(data) {
        // Show a specific notification for partial approvals
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-yellow-600 text-white px-4 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300';
        notification.innerHTML = `
            <div class="flex items-center gap-2">
                <i class="fas fa-exclamation-triangle"></i>
                <div class="flex-1">
                    <div class="font-medium">אישור חלקי</div>
                    <div class="text-sm">${data.customer_name}: ${data.approved_count}/${data.total_count} פעולות</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('translate-x-0'), 10);
        
        // Remove after 4 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }
    
    getStatusDisplayText(status) {
        const statusMap = {
            'pending_diagnosis': 'ממתין לאבחון',
            'pending_approval': 'ממתין לאישור',
            'approved_waiting_for_mechanic': 'ממתין למכונאי',
            'in_progress': 'בעבודה',
            'awaiting_quality_check': 'בדיקת איכות',
            'ready_for_collection': 'מוכן לאיסוף'
        };
        return statusMap[status] || status;
    }
    
    refreshManagerDashboard() {
        // For now, just use a simple page reload to avoid script injection issues
        // TODO: Implement proper section-wise updates without script conflicts
        console.log('Refreshing manager dashboard via reload...');
        setTimeout(() => {
            try {
                window.location.reload();
            } catch (error) {
                console.error('Error during dashboard reload:', error);
            }
        }, 500);
    }
}

// Initialize manager real-time client if user is manager
document.addEventListener('DOMContentLoaded', () => {
    const userType = document.querySelector('[data-user-type]')?.dataset.userType;
    if (userType === 'manager') {
        window.bikeRealtime = new ManagerRealtime();
        window.managerRealtime = window.bikeRealtime;
    }
});