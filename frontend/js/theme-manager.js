document.addEventListener('DOMContentLoaded', () => {
  document.documentElement.dataset.theme = 'light';
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = '#F9F8F3';
});
