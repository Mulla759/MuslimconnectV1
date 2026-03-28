document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const filterPills = document.querySelectorAll('.filter-pill');
  const orgCards = document.querySelectorAll('.org-card');
  const noResults = document.getElementById('noResults');

  let activeFilter = 'all';

  function applyFilters() {
    const query = searchInput.value.toLowerCase().trim();
    let visibleCount = 0;

    orgCards.forEach(card => {
      const category = card.dataset.category;
      const name = card.dataset.name?.toLowerCase() || '';

      const matchesFilter = activeFilter === 'all' || category === activeFilter;
      const matchesSearch = !query || name.includes(query);

      if (matchesFilter && matchesSearch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    noResults.classList.toggle('visible', visibleCount === 0);
  }

  filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeFilter = pill.dataset.filter;
      applyFilters();
    });
  });

  searchInput.addEventListener('input', applyFilters);

  // Follow toggle for org cards
  document.querySelectorAll('.btn-follow').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('following');
      btn.textContent = btn.classList.contains('following') ? 'Following' : 'Follow';
    });
  });
});
