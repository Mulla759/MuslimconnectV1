class ShareManager {
  constructor() {
    this.tooltip = document.getElementById('shareTooltip');
    this.btn = document.getElementById('shareBtn');
    this.visible = false;
    this.btn?.addEventListener('click', (e) => {
      if (e.target.closest('.share-tooltip')) return;
      this.visible = !this.visible;
      this.tooltip.classList.toggle('visible', this.visible);
    });
    document.addEventListener('click', (e) => {
      if (!this.btn?.contains(e.target)) {
        this.visible = false;
        this.tooltip?.classList.remove('visible');
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => new ShareManager());
