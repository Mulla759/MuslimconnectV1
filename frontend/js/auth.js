const API_BASE = 'http://127.0.0.1:8000/api/v1';

// Handle Sign In
document.getElementById('signin-form').querySelector('form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data));
      window.location.href = 'web-dashboard.html';
    } else {
      alert(data.detail || 'Login failed');
    }
  } catch (err) {
    alert('Could not connect to server');
  }
});

// Handle Sign Up
document.getElementById('signup-form').querySelector('form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const first_name = document.getElementById('first-name').value;
  const last_name = document.getElementById('last-name').value;
  const email = document.getElementById('signup-email').value;
  const password = document.getElementById('signup-password').value;
  const campus = document.getElementById('campus').value;

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ first_name, last_name, email, password, campus })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data));
      window.location.href = 'web-dashboard.html';
    } else {
      alert(data.detail || 'Registration failed');
    }
  } catch (err) {
    alert('Could not connect to server');
  }
});

