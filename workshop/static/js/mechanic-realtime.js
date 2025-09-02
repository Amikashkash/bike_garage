/**
 * Mechanic-specific real-time functionality
 * Extends the base real-time client for mechanic users
 */

class MechanicRealtime extends BikeGarageRealtime {
    constructor() {
        super();
        this.currentTaskId = null;
        this.setupMechanicFeatures();
    }
    
    setupMechanicFeatures() {
        // Get current task ID if on task page
        const taskElement = document.querySelector('[data-task-id]');
        if (taskElement) {
            this.currentTaskId = taskElement.dataset.taskId;
        }
        
        // Setup mechanic-specific UI handlers
        this.setupTaskCompletionHandlers();
        this.setupStuckRepairHandlers();
    }
    
    // Override connection callbacks
    onConnectionEstablished() {
        console.log('Mechanic real-time connection established');
        this.updateConnectionIndicator(true);
    }
    
    onConnectionLost() {
        console.log('Mechanic real-time connection lost');
        this.updateConnectionIndicator(false);
    }
    
    // Mechanic-specific message handlers
    handleNewRepairAssignment(data) {
        super.handleNewRepairAssignment(data);
        
        // Show assignment modal if not on dashboard
        if (!window.location.pathname.includes('dashboard')) {
            this.showAssignmentModal(data);
        }
        
        // Update assignment counter
        this.updateAssignmentCounter();
    }
    
    handleStuckRepairResolved(data) {
        super.handleStuckRepairResolved(data);
        
        // If this is current task, enable form
        if (this.currentTaskId && data.repair_id == this.currentTaskId) {
            this.enableTaskForm();
            this.showManagerResponse(data.manager_response);
        }
    }
    
    // Mechanic-specific UI methods
    showAssignmentModal(data) {
        const modalHtml = `
            <div id="assignment-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div class="bg-slate-800/95 backdrop-blur-sm border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
                    <div class="text-center mb-4">
                        <div class="bg-blue-500/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-tools text-blue-400 text-2xl"></i>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-2">תיקון חדש הוקצה!</h3>
                    </div>
                    
                    <div class="space-y-3 mb-6">
                        <div class="bg-slate-700/30 border border-slate-600 p-3 rounded-lg">
                            <div class="text-sm text-slate-400">אופניים</div>
                            <div class="font-semibold text-white">${data.bike_info}</div>
                        </div>
                        <div class="bg-slate-700/30 border border-slate-600 p-3 rounded-lg">
                            <div class="text-sm text-slate-400">לקוח</div>
                            <div class="font-semibold text-white">${data.customer_name}</div>
                        </div>
                        <div class="bg-slate-700/30 border border-slate-600 p-3 rounded-lg">
                            <div class="text-sm text-slate-400">תיאור התקלה</div>
                            <div class="font-semibold text-white">${data.problem_description}</div>
                        </div>
                    </div>
                    
                    <div class="flex gap-3">
                        <button onclick="window.location.href='/repair/${data.repair_id}/'" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                            התחל עבודה
                        </button>
                        <button onclick="document.getElementById('assignment-modal').remove()" class="flex-1 bg-slate-600/50 hover:bg-slate-600 border border-slate-500 text-slate-300 hover:text-white py-2 px-4 rounded-lg font-medium transition-colors">
                            סגור
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Auto-remove after 30 seconds
        setTimeout(() => {
            const modal = document.getElementById('assignment-modal');
            if (modal) modal.remove();
        }, 30000);
    }
    
    updateAssignmentCounter() {
        const counter = document.querySelector('#assignment-counter');
        if (counter) {
            const currentCount = parseInt(counter.textContent) || 0;
            counter.textContent = currentCount + 1;
            counter.classList.add('animate-pulse');
            setTimeout(() => counter.classList.remove('animate-pulse'), 1000);
        }
    }
    
    updateConnectionIndicator(connected) {
        const indicator = document.querySelector('#connection-indicator');
        if (indicator) {
            if (connected) {
                indicator.classList.remove('bg-red-500');
                indicator.classList.add('bg-green-500');
                indicator.title = 'מחובר לעדכונים מקוונים';
            } else {
                indicator.classList.remove('bg-green-500');
                indicator.classList.add('bg-red-500');
                indicator.title = 'לא מחובר לעדכונים מקוונים';
            }
        }
    }
    
    enableTaskForm() {
        const form = document.querySelector('#task-completion-form');
        if (form) {
            // Enable all form inputs
            const inputs = form.querySelectorAll('input, button, select, textarea');
            inputs.forEach(input => {
                input.disabled = false;
            });
            
            // Remove stuck indicators
            const stuckIndicators = document.querySelectorAll('.stuck-indicator');
            stuckIndicators.forEach(indicator => indicator.remove());
        }
    }
    
    showManagerResponse(response) {
        if (!response) return;
        
        const responseHtml = `
            <div id="manager-response" class="bg-green-50 border-l-4 border-green-400 p-4 mb-4 rounded">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-user-tie text-green-400"></i>
                    </div>
                    <div class="mr-3">
                        <h4 class="text-sm font-medium text-green-800">תגובת המנהל:</h4>
                        <p class="text-sm text-green-700 mt-1">${response}</p>
                    </div>
                </div>
            </div>
        `;
        
        const form = document.querySelector('#task-completion-form');
        if (form) {
            form.insertAdjacentHTML('afterbegin', responseHtml);
        }
    }
    
    setupTaskCompletionHandlers() {
        // Handle task completion form
        document.addEventListener('submit', (e) => {
            if (e.target.id === 'task-completion-form') {
                e.preventDefault();
                this.handleTaskCompletion(e.target);
            }
        });
        
        // Handle individual item completion
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('complete-item-btn')) {
                const itemId = e.target.dataset.itemId;
                this.completeRepairItem(itemId);
            }
        });
    }
    
    setupStuckRepairHandlers() {
        // Handle stuck repair reporting
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('report-stuck-btn')) {
                this.showStuckModal();
            }
        });
    }
    
    handleTaskCompletion(form) {
        const formData = new FormData(form);
        const completedItems = formData.getAll('completed_items');
        
        // Send real-time update about task progress
        this.send({
            type: 'task_progress_update',
            repair_id: this.currentTaskId,
            completed_items: completedItems,
            notes: formData.get('notes') || ''
        });
        
        // Submit form normally
        form.submit();
    }
    
    completeRepairItem(itemId) {
        // Send real-time notification about item completion
        this.send({
            type: 'complete_repair_item',
            item_id: itemId,
            repair_id: this.currentTaskId
        });
        
        // Update UI immediately
        const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
        if (itemElement) {
            itemElement.classList.add('completed');
            const checkbox = itemElement.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.checked = true;
        }
    }
    
    showStuckModal() {
        const modalHtml = `
            <div id="stuck-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                <div class="bg-slate-800/95 backdrop-blur-sm border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
                    <div class="text-center mb-4">
                        <div class="bg-orange-500/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-exclamation-triangle text-orange-400 text-2xl"></i>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-2">דיווח על בעיה</h3>
                        <p class="text-slate-300">תאר את הבעיה שמונעת המשך התיקון</p>
                    </div>
                    
                    <form id="stuck-report-form" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-2">סיבת החסימה</label>
                            <textarea name="stuck_reason" rows="4" class="w-full bg-slate-700/30 border border-slate-600 text-white rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 placeholder-slate-400" placeholder="תאר את הבעיה..." required></textarea>
                        </div>
                        
                        <div class="flex gap-3">
                            <button type="submit" class="flex-1 bg-orange-600 hover:bg-orange-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                                שלח דיווח
                            </button>
                            <button type="button" onclick="document.getElementById('stuck-modal').remove()" class="flex-1 bg-slate-600/50 hover:bg-slate-600 border border-slate-500 text-slate-300 hover:text-white py-2 px-4 rounded-lg font-medium transition-colors">
                                ביטול
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Handle form submission
        document.getElementById('stuck-report-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            this.reportStuckRepair(formData.get('stuck_reason'));
            document.getElementById('stuck-modal').remove();
        });
    }
    
    reportStuckRepair(reason) {
        // Send real-time notification about stuck repair
        this.send({
            type: 'mark_stuck',
            repair_id: this.currentTaskId,
            reason: reason
        });
        
        // Update UI to show stuck state
        this.showStuckState(reason);
        
        // Also send to server via AJAX
        fetch(`/mechanic/repair/${this.currentTaskId}/stuck/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ reason: reason })
        });
    }
    
    showStuckState(reason) {
        const stuckHtml = `
            <div class="stuck-indicator bg-orange-50 border-l-4 border-orange-400 p-4 mb-4 rounded">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-exclamation-triangle text-orange-400"></i>
                    </div>
                    <div class="mr-3">
                        <h4 class="text-sm font-medium text-orange-800">תיקון תקוע - ממתין לתגובת מנהל</h4>
                        <p class="text-sm text-orange-700 mt-1">${reason}</p>
                    </div>
                </div>
            </div>
        `;
        
        const form = document.querySelector('#task-completion-form');
        if (form) {
            form.insertAdjacentHTML('afterbegin', stuckHtml);
            
            // Disable form
            const inputs = form.querySelectorAll('input, button, select, textarea');
            inputs.forEach(input => {
                input.disabled = true;
            });
        }
    }
}

// Initialize mechanic real-time client if user is mechanic
document.addEventListener('DOMContentLoaded', () => {
    const userType = document.querySelector('[data-user-type]')?.dataset.userType;
    if (userType === 'mechanic') {
        window.bikeRealtime = new MechanicRealtime();
    }
});