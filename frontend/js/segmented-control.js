class SegmentedControl {
  constructor(el) {
    this.el = el;
    this.buttons = el.querySelectorAll('.seg-btn');
    this.buttons.forEach(btn => {
      btn.addEventListener('click', () => this.activate(btn));
    });
  }
  activate(btn) {
    this.buttons.forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    if (btn.dataset.tab === 'following') {
      this.el.classList.add('tab-following');
    } else {
      this.el.classList.remove('tab-following');
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.segmented-control').forEach(el => new SegmentedControl(el));
});
