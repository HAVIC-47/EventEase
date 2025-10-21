// Dark mode toggle with animation
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggle-mode');
    const body = document.body;
    
    // Check if dark mode was previously enabled
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
        toggleButton.textContent = '☀️';
    }
    
    toggleButton.addEventListener('click', function() {
        // Add rotation animation class
        toggleButton.classList.add('rotating');
        
        // Toggle dark mode after a short delay to sync with animation
        setTimeout(() => {
            body.classList.toggle('dark-mode');
            
            if (body.classList.contains('dark-mode')) {
                toggleButton.textContent = '☀️';
                localStorage.setItem('darkMode', 'enabled');
            } else {
                toggleButton.textContent = '🌙';
                localStorage.removeItem('darkMode');
            }
        }, 300);
        
        // Remove animation class after animation completes
        setTimeout(() => {
            toggleButton.classList.remove('rotating');
        }, 600);
    });
    
    // Search functionality
    const searchBar = document.querySelector('.search-bar');
    if (searchBar) {
        searchBar.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const searchTerm = e.target.value.trim();
                if (searchTerm) {
                    // Redirect to events page with search query
                    window.location.href = `/events/?search=${encodeURIComponent(searchTerm)}`;
                }
            }
        });
    }
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Load notification count
    loadNotificationCount();
    
    // Refresh notification count every 30 seconds
    setInterval(loadNotificationCount, 30000);
});

// Notification functions
function loadNotificationCount() {
    const notificationCountElement = document.getElementById('notification-count');
    if (!notificationCountElement) return;
    
    fetch('/core/notification-count/')
        .then(response => response.json())
        .then(data => {
            const count = data.count || 0;
            if (count > 0) {
                notificationCountElement.textContent = count > 99 ? '99+' : count;
                notificationCountElement.style.display = 'flex';
            } else {
                notificationCountElement.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error loading notification count:', error);
        });
}

// Form validation for auth forms
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('input[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            field.style.borderColor = '#40B5AD';
        }
    });
    
    return isValid;
}
