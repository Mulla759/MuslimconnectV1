(function() {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        nav.classList.toggle('navbar--scrolled', window.scrollY > 20);
        ticking = false;
      });
      ticking = true;
    }
  });
})();
