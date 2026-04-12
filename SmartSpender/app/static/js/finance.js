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

// ============ USER REFRESH ============
async function refreshUserData() {
    const confirmed = confirm('Are you sure you want to refresh your data?');
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
        alert('Transaction saved successfully!');
        
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
        location.reload();
        
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
        alert('Subscription saved successfully!');
        
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
        location.reload();
        
    } catch (error) {
        console.error('Error saving subscription:', error);
        alert('Error saving subscription: ' + error.message);
    }
}

// ============ DELETE FUNCTIONS ============
async function deleteTransaction(id) {
    if (!confirm('Are you sure you want to delete this?')) return;
    
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

// ============ BUDGET FUNCTIONS ============
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

// ============ MODAL CONTROLS ============
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
console.log('Finance.js loaded successfully');
console.log('Functions available:', {
    updateSalary: typeof updateSalary,
    saveTransaction: typeof saveTransaction,
    saveSubscription: typeof saveSubscription,
    deleteTransaction: typeof deleteTransaction,
    saveBudget: typeof saveBudget,
    showTransactionModal: typeof showTransactionModal,
    showSubscriptionModal: typeof showSubscriptionModal,
    showSalaryModal: typeof showSalaryModal,
    showBudgetModal: typeof showBudgetModal,
    refreshUserData: typeof refreshUserData
});
