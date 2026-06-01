// ============ API HELPER ============
const API_BASE = '/finance/api';

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error Response:', errorText);
            throw new Error(`API call failed: ${response.status}`);
        }
        
        return response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

function ensureConfirmationModal() {
    let modalEl = document.getElementById('actionConfirmModal');
    if (modalEl) return modalEl;

    modalEl = document.createElement('div');
    modalEl.className = 'modal fade';
    modalEl.id = 'actionConfirmModal';
    modalEl.tabIndex = -1;
    modalEl.setAttribute('aria-hidden', 'true');
    modalEl.innerHTML = `
        <div class="modal-dialog modal-dialog-centered modal-sm">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="actionConfirmTitle">Please confirm</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p class="mb-0" id="actionConfirmMessage"></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-confirm-cancel>Cancel</button>
                    <button type="button" class="btn btn-danger" data-confirm-ok>Confirm</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modalEl);
    return modalEl;
}

async function confirmAction(message, options = {}) {
    const {
        title = 'Please confirm',
        confirmText = 'Confirm',
        confirmButtonClass = 'btn-danger'
    } = options;

    if (!window.bootstrap?.Modal) {
        return window.confirm(message);
    }

    const modalEl = ensureConfirmationModal();
    const titleEl = modalEl.querySelector('#actionConfirmTitle');
    const messageEl = modalEl.querySelector('#actionConfirmMessage');
    const cancelButton = modalEl.querySelector('[data-confirm-cancel]');
    const confirmButton = modalEl.querySelector('[data-confirm-ok]');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

    titleEl.textContent = title;
    messageEl.textContent = message;
    confirmButton.textContent = confirmText;
    confirmButton.className = `btn ${confirmButtonClass}`;

    return new Promise(resolve => {
        let settled = false;

        const cleanup = confirmed => {
            if (settled) return;
            settled = true;
            confirmButton.removeEventListener('click', onConfirm);
            cancelButton.removeEventListener('click', onCancel);
            modalEl.removeEventListener('hidden.bs.modal', onHidden);
            resolve(confirmed);
        };

        const onConfirm = () => {
            cleanup(true);
            modal.hide();
        };

        const onCancel = () => {
            cleanup(false);
            modal.hide();
        };

        const onHidden = () => cleanup(false);

        confirmButton.addEventListener('click', onConfirm);
        cancelButton.addEventListener('click', onCancel);
        modalEl.addEventListener('hidden.bs.modal', onHidden, { once: true });
        modal.show();
    });
}

function showBudgetPopup(budgetAlert) {
    if (!budgetAlert) return;

    let popupEl = document.getElementById('budgetAlertPopup');
    if (!popupEl) {
        popupEl = document.createElement('div');
        popupEl.id = 'budgetAlertPopup';
        popupEl.setAttribute('role', 'alert');
        popupEl.setAttribute('aria-live', 'assertive');
        popupEl.innerHTML = `
            <div class="budget-alert-icon">
                <span class="material-symbols-outlined">notifications_active</span>
            </div>
            <div class="budget-alert-copy">
                <strong></strong>
                <span></span>
            </div>
            <button type="button" aria-label="Close budget alert">
                <span class="material-symbols-outlined">close</span>
            </button>
        `;
        document.body.appendChild(popupEl);

        popupEl.querySelector('button').addEventListener('click', () => {
            popupEl.classList.remove('show');
        });
    }

    popupEl.className = budgetAlert.level === 'over_budget' ? 'budget-alert-popup danger' : 'budget-alert-popup warning';
    popupEl.querySelector('strong').textContent = budgetAlert.title || 'Budget alert';
    popupEl.querySelector('.budget-alert-copy span').textContent = budgetAlert.message;

    window.requestAnimationFrame(() => popupEl.classList.add('show'));
    window.clearTimeout(window.budgetAlertPopupTimer);
    window.budgetAlertPopupTimer = window.setTimeout(() => {
        popupEl.classList.remove('show');
    }, 6500);
}

async function enableBudgetNotifications() {
    if (!('Notification' in window)) {
        alert('This browser does not support pop-up notifications.');
        return false;
    }

    if (Notification.permission === 'granted') {
        alert('Budget alerts are already enabled.');
        return true;
    }

    if (Notification.permission === 'denied') {
        alert('Notifications are blocked in your browser settings.');
        return false;
    }

    const permission = await Notification.requestPermission();
    alert(permission === 'granted' ? 'Budget alerts enabled!' : 'Budget alerts were not enabled.');
    return permission === 'granted';
}

function showBrowserBudgetNotification(budgetAlert) {
    if (!budgetAlert || !('Notification' in window) || Notification.permission !== 'granted') {
        return false;
    }

    const notification = new Notification(budgetAlert.title || 'Budget alert', {
        body: budgetAlert.message,
        tag: `budget-${budgetAlert.category}-${budgetAlert.level}`,
        requireInteraction: budgetAlert.level === 'over_budget'
    });

    notification.onclick = () => {
        window.focus();
        window.location.href = '/finance/budget';
        notification.close();
    };

    return true;
}

function handleBudgetAlert(budgetAlert) {
    if (!budgetAlert) return;
    showBrowserBudgetNotification(budgetAlert);
    showBudgetPopup(budgetAlert);
}

function closeModal(modalId) {
    const modalEl = document.getElementById(modalId);
    if (!modalEl || !window.bootstrap?.Modal) return;
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) {
        modal.hide();
    }
}

// ============ USER REFRESH ============
async function refreshUserData() {
    const confirmed = await confirmAction('Are you sure you want to refresh your data?', {
        title: 'Refresh data',
        confirmText: 'Refresh',
        confirmButtonClass: 'btn-warning'
    });
    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch('/finance/api/user/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error || 'Failed to refresh user data');
        }

        await response.json();
        alert('User data refreshed successfully!');
        location.reload();
    } catch (error) {
        console.error('Error refreshing user data:', error);
        alert('Error refreshing data: ' + error.message);
    }
}

// ============ SALARY FUNCTIONS ============
async function updateSalary() {
    const salaryInput = document.getElementById('salary-amount');
    if (!salaryInput) {
        console.error('Salary input not found');
        alert('Form not found. Please refresh the page.');
        return;
    }
    
    const salary = parseFloat(salaryInput.value);
    
    if (isNaN(salary) || salary < 0) {
        alert('Please enter a valid salary amount');
        return;
    }
    
    console.log('Updating salary to:', salary);
    
    try {
        const response = await fetch(`/finance/api/user/salary?salary=${salary}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }
        
        const result = await response.json();
        console.log('Salary updated:', result);
        alert('Salary updated successfully!');
        
        // Close modal
        const modalEl = document.getElementById('salaryModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
        }
        
        // Reload page
        location.reload();
        
    } catch (error) {
        console.error('Error updating salary:', error);
        alert('Error updating salary: ' + error.message);
    }
}

// ============ TRANSACTION FUNCTIONS ============
async function saveTransaction() {
    console.log('saveTransaction called');
    
    const nameInput = document.getElementById('txn-name');
    const amountInput = document.getElementById('txn-amount');
    const typeSelect = document.getElementById('txn-type');
    const categorySelect = document.getElementById('txn-category');
    const dateInput = document.getElementById('txn-date');
    
    if (!nameInput || !amountInput) {
        console.error('Transaction form inputs not found');
        alert('Form inputs not found. Please refresh the page.');
        return;
    }
    
    const name = nameInput.value;
    const amount = parseFloat(amountInput.value);
    const type = typeSelect ? typeSelect.value : 'expense';
    const category = categorySelect ? categorySelect.value : 'other';
    
    // Get current date in correct format
    let date = dateInput ? dateInput.value : '';
    if (!date) {
        const today = new Date();
        date = today.toISOString().split('T')[0];
    }
    
    // Validate date format
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
        const today = new Date();
        date = today.toISOString().split('T')[0];
    }
    
    if (!name || isNaN(amount)) {
        alert('Please fill in Name and Amount');
        return;
    }
    
    const transaction = {
        name: name,
        amount: amount,
        type: type,
        category: category,
        is_subscription: false,
        is_recurring: false,
        date: date
    };
    
    console.log('Saving transaction:', transaction);
    
    try {
        const result = await apiCall('/transactions', { 
            method: 'POST', 
            body: JSON.stringify(transaction) 
        });
        
        console.log('Transaction saved:', result);
        handleBudgetAlert(result.budget_alert);
        if (!result.budget_alert) {
            alert('Transaction saved successfully!');
        }
        
        // Close modal
        const modalEl = document.getElementById('transactionModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
        }
        
        // Clear form
        nameInput.value = '';
        amountInput.value = '';
        if (dateInput) dateInput.value = '';
        
        // Reload page
        setTimeout(() => location.reload(), result.budget_alert ? 1800 : 0);
        
    } catch (error) {
        console.error('Error saving transaction:', error);
        alert('Error saving transaction: ' + error.message);
    }
}

// ============ SUBSCRIPTION FUNCTIONS ============
async function saveSubscription() {
    console.log('saveSubscription called');
    
    const nameInput = document.getElementById('sub-name');
    const amountInput = document.getElementById('sub-amount');
    const categorySelect = document.getElementById('sub-category');
    const nextDateInput = document.getElementById('sub-next-date');
    
    if (!nameInput || !amountInput) {
        console.error('Subscription form inputs not found');
        alert('Form inputs not found. Please refresh the page.');
        return;
    }
    
    const name = nameInput.value;
    const amount = parseFloat(amountInput.value);
    const category = categorySelect ? categorySelect.value : 'entertainment';
    let nextBillingDate = nextDateInput ? nextDateInput.value : null;
    
    if (!name || isNaN(amount)) {
        alert('Please fill in Name and Amount');
        return;
    }
    
    // Set default next billing date if not provided
    if (!nextBillingDate) {
        const today = new Date();
        nextBillingDate = today.toISOString().split('T')[0];
    }
    
    const subscription = {
        name: name,
        amount: amount,
        type: 'expense',
        category: category,
        is_subscription: true,
        is_recurring: true,
        next_billing_date: nextBillingDate,
        date: new Date().toISOString().split('T')[0]
    };
    
    console.log('Saving subscription:', subscription);
    
    try {
        const result = await apiCall('/transactions', { 
            method: 'POST', 
            body: JSON.stringify(subscription) 
        });
        
        console.log('Subscription saved:', result);
        handleBudgetAlert(result.budget_alert);
        if (!result.budget_alert) {
            alert('Subscription saved successfully!');
        }
        
        // Close modal
        const modalEl = document.getElementById('subscriptionModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
        }
        
        // Clear form
        nameInput.value = '';
        amountInput.value = '';
        if (nextDateInput) nextDateInput.value = '';
        
        // Reload page
        setTimeout(() => location.reload(), result.budget_alert ? 1800 : 0);
        
    } catch (error) {
        console.error('Error saving subscription:', error);
        alert('Error saving subscription: ' + error.message);
    }
}

// Delete function for both transactions and subscriptions 
async function deleteTransaction(id) {
    const confirmed = await confirmAction('Are you sure you want to delete this transaction?', {
        title: 'Delete transaction',
        confirmText: 'Delete'
    });
    if (!confirmed) return;
    
    console.log('Deleting transaction:', id);
    
    try {
        await apiCall(`/transactions/${id}`, { method: 'DELETE' });
        alert('Deleted successfully!');
        location.reload();
    } catch (error) {
        console.error('Error deleting:', error);
        alert('Error deleting: ' + error.message);
    }
}

// Al budget functions 
async function saveBudget() {
    console.log('saveBudget called');
    
    const categorySelect = document.getElementById('budget-category');
    const limitInput = document.getElementById('budget-limit');
    
    if (!categorySelect || !limitInput) {
        console.error('Budget form inputs not found');
        alert('Form inputs not found. Please refresh the page.');
        return;
    }
    
    const category = categorySelect.value;
    const monthlyLimit = parseFloat(limitInput.value);
    const monthYear = new Date().toISOString().slice(0, 7);
    
    if (!category || isNaN(monthlyLimit)) {
        alert('Please fill in all fields');
        return;
    }
    
    const budget = {
        category: category,
        monthly_limit: monthlyLimit,
        month_year: monthYear
    };
    
    console.log('Saving budget:', budget);
    
    try {
        const result = await apiCall('/budgets', { 
            method: 'POST', 
            body: JSON.stringify(budget) 
        });
        
        console.log('Budget saved:', result);
        alert('Budget saved successfully!');
        
        // Close modal
        const modalEl = document.getElementById('budgetModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
        }
        
        limitInput.value = '';
        location.reload();
        
    } catch (error) {
        console.error('Error saving budget:', error);
        alert('Error saving budget: ' + error.message);
    }
}

async function deleteBudget(id) {
    const confirmed = await confirmAction('Are you sure you want to delete this budget?', {
        title: 'Delete budget',
        confirmText: 'Delete'
    });
    if (!confirmed) return;

    try {
        await apiCall(`/budgets/${id}`, { method: 'DELETE' });
        alert('Budget deleted successfully!');
        location.reload();
    } catch (error) {
        console.error('Error deleting budget:', error);
        alert('Error deleting budget: ' + error.message);
    }
}

// Bootstrap modal functions. This is needed because we want to ensure the modals are properly initialized 
// before trying to show them, especially if the user has a slow connection 
// or if there are any issues with loading Bootstrap's JavaScript
function showTransactionModal() {
    console.log('showTransactionModal called');
    const modalEl = document.getElementById('transactionModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    } else {
        console.error('Transaction modal element not found');
        alert('Modal not found. Please refresh the page.');
    }
}

function showSubscriptionModal() {
    console.log('showSubscriptionModal called');
    const modalEl = document.getElementById('subscriptionModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    } else {
        console.error('Subscription modal element not found');
        alert('Modal not found. Please refresh the page.');
    }
}

function showSalaryModal() {
    console.log('showSalaryModal called');
    const modalEl = document.getElementById('salaryModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    } else {
        console.error('Salary modal element not found');
        alert('Modal not found. Please refresh the page.');
    }
}

function showBudgetModal() {
    console.log('showBudgetModal called');
    const modalEl = document.getElementById('budgetModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    } else {
        console.error('Budget modal element not found');
        alert('Modal not found. Please refresh the page.');
    }
}

// Log that script loaded
window.enableBudgetNotifications = enableBudgetNotifications;
window.handleBudgetAlert = handleBudgetAlert;
window.closeModal = closeModal;

console.log('Finance.js loaded successfully');
console.log('Functions available:', {
    updateSalary: typeof updateSalary,
    saveTransaction: typeof saveTransaction,
    saveSubscription: typeof saveSubscription,
    deleteTransaction: typeof deleteTransaction,
    saveBudget: typeof saveBudget,
    deleteBudget: typeof deleteBudget,
    showTransactionModal: typeof showTransactionModal,
    showSubscriptionModal: typeof showSubscriptionModal,
    showSalaryModal: typeof showSalaryModal,
    showBudgetModal: typeof showBudgetModal,
    refreshUserData: typeof refreshUserData,
    enableBudgetNotifications: typeof enableBudgetNotifications
});
