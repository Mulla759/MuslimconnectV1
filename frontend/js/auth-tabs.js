document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.auth-tab');
  const forms = document.querySelectorAll('.auth-form');

  function switchTab(tabName) {
    tabs.forEach(t => t.classList.toggle('auth-tab--active', t.dataset.tab === tabName));
    forms.forEach(f => f.classList.toggle('active', f.id === tabName + '-form'));
  }

  tabs.forEach(tab => tab.addEventListener('click', () => switchTab(tab.dataset.tab)));

  if (window.location.hash === '#signup') switchTab('signup');

  document.querySelectorAll('form').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    window.location.href = 'web-dashboard.html';
  }));
});
