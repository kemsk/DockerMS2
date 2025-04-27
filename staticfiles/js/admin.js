let users = [
    { name: "Pepito, Rem Well", id: "1001", email: "remwell@example.com", username: "remwell", role: "Admin" },
    { name: "Dela Cruz, Juan", id: "1002", email: "juan@example.com", username: "juandelacruz", role: "Encoder" }
];

let violations = [];

let students = [
    { name: "Mary Kate Saguin", id: "20220025024" },
    { name: "Kim Flores", id: "20220025025" },
    { name: "Glenn Michael Deguit", id: "20220025026" }
];

// ========== GENERAL FUNCTIONS ==========
// Real-time Clock
function updateDateTime() {
    const date = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    const currentDateElement = document.getElementById('current-date');
    const currentTimeElement = document.getElementById('current-time');
    
    if (currentDateElement) {
        currentDateElement.innerText = date.toLocaleDateString('en-US', options);
    }
    
    if (currentTimeElement) {
        currentTimeElement.innerText = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
}

// When the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Set up real-time clock update
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Initialize any components
    const addViolationForm = document.getElementById('add-violation-form');
    if (addViolationForm) {
        addViolationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Submit via AJAX or form submit
            this.submit();
        });
    }
    
    // User management form
    const manageUsersForm = document.getElementById('manage-users-form');
    if (manageUsersForm) {
        manageUsersForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Submit via AJAX or form submit
            this.submit();
        });
    }
    
    // Initialize AJAX for marking violations as claimed/resolved
    const claimBtns = document.querySelectorAll('.claim-btn');
    if (claimBtns) {
        claimBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const violationId = this.getAttribute('data-id');
                updateViolationStatus(violationId, 'claimed');
            });
        });
    }
    
    // User subsection toggle
    const viewActiveUsersBtn = document.getElementById('view-active-users-btn');
    const createNewUserBtn = document.getElementById('create-new-user-btn');
    
    if (viewActiveUsersBtn && createNewUserBtn) {
        viewActiveUsersBtn.addEventListener('click', () => showUserSubSection('view-active-users-btn'));
        createNewUserBtn.addEventListener('click', () => showUserSubSection('create-new-user-btn'));
    }
});

// ========== USER MANAGEMENT SECTION ==========
function showUserSubSection(buttonId) {
    const activeUsersSection = document.getElementById('active-users-section');
    const createUserSection = document.getElementById('create-user-section');
    
    document.querySelectorAll('#view-active-users-btn, #create-new-user-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (buttonId === 'view-active-users-btn') {
        activeUsersSection.style.display = 'block';
        createUserSection.style.display = 'none';
        document.getElementById(buttonId).classList.add('active');
    } else {
        activeUsersSection.style.display = 'none';
        createUserSection.style.display = 'block';
        document.getElementById(buttonId).classList.add('active');
    }
}

// ========== AJAX FUNCTIONS ==========
function updateViolationStatus(violationId, status) {
    // Get the CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch('/evs/update_violation_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            violation_id: violationId,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page or update the UI
            window.location.reload();
        } else {
            alert('Error updating violation status: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the violation status.');
    });
}

// Function to filter violations table
function filterViolations() {
    const filterStatus = document.getElementById('filter-by-status').value;
    const searchTerm = document.getElementById('search-student').value.toLowerCase();
    const rows = document.querySelectorAll('#violations-table-body tr');
    
    rows.forEach(row => {
        const studentName = row.cells[0].textContent.toLowerCase();
        const status = row.cells[5].textContent.toLowerCase();
        
        const matchesStatus = filterStatus === '' || status === filterStatus;
        const matchesSearch = searchTerm === '' || studentName.includes(searchTerm);
        
        if (matchesStatus && matchesSearch) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Set up event listeners for filtering
if (document.getElementById('filter-by-status')) {
    document.getElementById('filter-by-status').addEventListener('change', filterViolations);
}

if (document.getElementById('search-student')) {
    document.getElementById('search-student').addEventListener('input', filterViolations);
}
