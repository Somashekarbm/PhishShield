async function register() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();
    document.getElementById('register-message').innerText = data.message || 'User registered!';
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    document.getElementById('login-message').innerText = data.message || 'Login successful!';

    if (response.ok) {
        localStorage.setItem('token', data.token);
        document.getElementById('classify').style.display = 'block';
        document.getElementById('user-actions').style.display = 'block';
        checkAdmin();
    }
}

async function classify() {
    const url = document.getElementById('url').value;
    const modelId = document.getElementById('model-id').value;
    const token = localStorage.getItem('token');

    const response = await fetch('/api/classify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ url, model_id: modelId })
    });

    const data = await response.json();
    document.getElementById('classify-message').innerText = JSON.stringify(data);
}

async function logout() {
    const token = localStorage.getItem('token');

    const response = await fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        localStorage.removeItem('token');
        document.getElementById('classify').style.display = 'none';
        document.getElementById('user-actions').style.display = 'none';
        document.getElementById('admin').style.display = 'none';
        document.getElementById('login-message').innerText = 'Logged out successfully!';
    }
}

async function requestDataDeletion() {
    const token = localStorage.getItem('token');

    const response = await fetch('/api/user/data-deletion', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    document.getElementById('user-message').innerText = data.message || 'Data deletion requested!';

    if (response.ok) {
        localStorage.removeItem('token');
        document.getElementById('classify').style.display = 'none';
        document.getElementById('user-actions').style.display = 'none';
        document.getElementById('admin').style.display = 'none';
    }
}

async function listUsers() {
    const token = localStorage.getItem('token');

    const response = await fetch('/api/admin/users', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    if (response.ok) {
        let usersList = document.getElementById('users-list');
        usersList.innerHTML = '';
        data.users.forEach(user => {
            usersList.innerHTML += `<p>User ID: ${user.userId}, Username: ${user.username}, Email: ${user.email}</p>`;
        });
    } else {
        document.getElementById('admin-message').innerText = data.message;
    }
}

async function deleteUser() {
    const userId = document.getElementById('delete-user-id').value;
    const token = localStorage.getItem('token');

    const response = await fetch(`/api/admin/user/${userId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    document.getElementById('admin-message').innerText = data.message || 'User deleted!';
}

async function checkAdmin() {
    const token = localStorage.getItem('token');

    const response = await fetch('/api/admin/users', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        document.getElementById('admin').style.display = 'block';
    }
}
