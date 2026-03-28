class ToggleManager {
  constructor() {
    document.addEventListener('DOMContentLoaded', () => {
      this.initFollowToggles();
      this.initSaveToggles();
      this.initRsvpToggles();
    });
  }

  initFollowToggles() {
    document.querySelectorAll('.follow-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        btn.classList.toggle('following');
        btn.textContent = btn.classList.contains('following') ? 'Following' : 'Follow';
      });
    });
  }

  initSaveToggles() {
    document.querySelectorAll('.save-btn, .media-badge--save').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        btn.classList.toggle('saved');
        const svg = btn.querySelector('svg');
        if (svg) {
          svg.setAttribute('fill', btn.classList.contains('saved') ? 'currentColor' : 'none');
        }
      });
    });
  }

  initRsvpToggles() {
    const btns = [document.getElementById('rsvpBtn')].filter(Boolean);
    if (!btns.length) return;
    let rsvpd = false;
    btns.forEach(btn => btn.addEventListener('click', () => {
      rsvpd = !rsvpd;
      btns.forEach(b => {
        const textEl = b.querySelector('.rsvp-text');
        b.classList.toggle('rsvpd', rsvpd);
        if (textEl) textEl.textContent = rsvpd ? 'Cancel RSVP' : "RSVP \u2014 I'm Going";
        b.classList.remove('animate');
        void b.offsetWidth;
        b.classList.add('animate');
      });
    }));
  }
}

new ToggleManager();
