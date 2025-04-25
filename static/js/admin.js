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

// ========== VIOLATIONS SECTION ==========
function displayViolations() {
    const tableBody = document.querySelector('#violations-table-body');
    tableBody.innerHTML = '';
    violations.forEach(violation => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${violation.name}</td>
            <td>${violation.studentId}</td>
            <td>${violation.ticket}</td>
            <td>${violation.type}</td>
            <td>${violation.date}</td>
            <td class="status-${violation.status.toLowerCase()}">${violation.status}</td>
        `;
        tableBody.appendChild(row);
    });
}

// ========== USERS SECTION ==========
function displayUsers() {
    const tableBody = document.querySelector('#users-table tbody');
    tableBody.innerHTML = '';

    if (users.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No users found.</td></tr>';
        return;
    }

    users.forEach((user, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.name}</td>
            <td>${user.id}</td>
            <td>${user.email}</td>
            <td>${user.username}</td>
            <td>
                <button class="btn btn-sm btn-warning">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteUser(${index})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function deleteUser(index) {
    if (confirm("Are you sure you want to delete this user?")) {
        users.splice(index, 1);
        displayUsers();
    }
}

// Handle create user form
document.getElementById('manage-users-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('employee-name').value;
    const id = document.getElementById('employee-id').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    users.push({ name, id, email, username, role: "Encoder" });
    displayUsers();

    document.getElementById('manage-users-form').reset();
    showUserSubSection('view-active-users-btn');
});

// ========== BUTTON TOGGLE BETWEEN ACTIVE USERS AND CREATE FORM ==========
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

document.getElementById('view-active-users-btn').addEventListener('click', () => showUserSubSection('view-active-users-btn'));
document.getElementById('create-new-user-btn').addEventListener('click', () => showUserSubSection('create-new-user-btn'));

// ========== ADD VIOLATION SECTION ==========
document.getElementById('add-violation-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const studentIdOrName = document.getElementById('student-id').value;
    const violationTypes = Array.from(document.querySelectorAll('input[name="violation"]:checked')).map(input => input.value).join(', ');
    const ticketNumber = document.getElementById('ticket-number').value;
    const reportedBy = document.getElementById('reported-by').value;
    const photoProof = document.getElementById('photo-proof').files[0];

    const student = students.find(student => student.id === studentIdOrName || student.name.toLowerCase() === studentIdOrName.toLowerCase());

    if (!student) {
        alert('Student not found.');
        return;
    }

    const newViolation = {
        name: student.name,
        studentId: student.id,
        ticket: ticketNumber,
        type: violationTypes,
        date: new Date().toLocaleString(),
        status: "Pending",
        photoProof: photoProof ? photoProof.name : "No Photo"
    };

    violations.push(newViolation);
    displayViolations();
    document.getElementById('add-violation-form').reset();
    generateTicketNumber();
});

function generateTicketNumber() {
    const prefix = "TICKET-";
    const timestamp = new Date().getTime();
    const ticketNumber = prefix + timestamp;
    document.getElementById('ticket-number').value = ticketNumber;
    return ticketNumber;
}

// ========== GENERAL NAVIGATION ==========
function showSection(section) {
    document.querySelectorAll('.content-section').forEach(content => {
        content.style.display = 'none';
    });

    document.querySelectorAll('.btn').forEach(btn => {
        btn.classList.remove('active');
    });

    section.classList.add('active');
    document.getElementById(section.id + '-content').style.display = 'block';
}

// Top Navigation Buttons
document.getElementById('view-violations').addEventListener('click', function () {
    showSection(this);
});

document.getElementById('add-violation').addEventListener('click', function () {
    showSection(this);
});

document.getElementById('manage-users').addEventListener('click', function () {
    showSection(this);
    displayUsers();
    showUserSubSection('view-active-users-btn'); // Default subview
});

// Real-time Clock
function updateDateTime() {
    const date = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    document.getElementById('current-date').innerText = date.toLocaleDateString('en-US', options);
    document.getElementById('current-time').innerText = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

setInterval(updateDateTime, 1000);

document.addEventListener('DOMContentLoaded', () => {
    displayViolations();
    generateTicketNumber();
    showSection(document.getElementById('view-violations'));
});