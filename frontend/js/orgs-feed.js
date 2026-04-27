const API_URL = 'http://127.0.0.1:8000/api/v1/organizations';

const CATEGORY_LABELS = {
  msa: 'MSA Chapter',
  cultural: 'Cultural',
  academic: 'Academic',
  sports: 'Sports & Fitness',
  service: 'Community Service',
  professional: 'Professional',
  dawah: 'Dawah',
  general: 'General'
};

const CATEGORY_COLORS = {
  msa: '#4A6C58',
  cultural: '#D4AF37',
  academic: '#2563EB',
  sports: '#059669',
  service: '#7C3AED',
  professional: '#DC2626',
  dawah: '#0284C7',
  general: '#6B7280'
};

function getInitial(name) {
  return name.charAt(0).toUpperCase();
}

function buildOrgCard(org) {
  const color = CATEGORY_COLORS[org.category] || '#4A6C58';
  const categoryLabel = CATEGORY_LABELS[org.category] || org.category;
  const verifiedBadge = org.verified ? `
    <svg class="verified-badge" viewBox="0 0 20 20">
      <path d="M10 0l2.4 3.3L16.2 2l.5 4.1 4 1-2.5 3.2L20 14l-3.8 1.5-.5 4.1-3.8-1.7L10 20l-2.4-2.1-3.8 1.7-.5-4.1L-.5 14l1.8-3.7L-1.2 7l4-1L3.3 2l3.8 1.3L10 0z" fill="#3B82F6"/>
      <path d="M7 10l2 2 4-4" stroke="#fff" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>` : '';

  return `
    <div class="org-card" data-category="${org.category}" data-name="${org.name.toLowerCase()}">
      <div class="card-cover" style="background: linear-gradient(135deg, ${color}, ${color}dd);">
        <div class="card-avatar" style="background: linear-gradient(135deg, ${color}cc, ${color}); display:flex; align-items:center; justify-content:center;">
          <span style="color: white; font-size: 1.5rem; font-weight: 700;">${getInitial(org.name)}</span>
        </div>
      </div>
      <div class="card-body">
        <div class="card-name-row">
          <span class="card-name">${org.name}</span>
          ${verifiedBadge}
        </div>
        <span class="category-pill cat-${org.category}">${categoryLabel}</span>
        <p class="card-bio">${org.bio || ''}</p>
        <div class="card-stats">${org.followers} followers &middot; ${org.event_count} events</div>
        <div class="card-actions">
          <button class="btn-follow">Follow</button>
          <button class="btn-view">View</button>
        </div>
      </div>
    </div>
  `;
}

function initFilters() {
  const searchInput = document.getElementById('searchInput');
  const filterPills = document.querySelectorAll('.filter-pill');
  const noResults = document.getElementById('noResults');
  let activeFilter = 'all';

  function applyFilters() {
    const query = searchInput.value.toLowerCase().trim();
    const orgCards = document.querySelectorAll('.org-card');
    let visibleCount = 0;

    orgCards.forEach(card => {
      const category = card.dataset.category;
      const name = card.dataset.name || '';
      const matchesFilter = activeFilter === 'all' || category === activeFilter;
      const matchesSearch = !query || name.includes(query);

      if (matchesFilter && matchesSearch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    if (noResults) noResults.style.display = visibleCount === 0 ? 'block' : 'none';
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

  // Follow toggle
  document.querySelectorAll('.btn-follow').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('following');
      btn.textContent = btn.classList.contains('following') ? 'Following' : 'Follow';
    });
  });
}

async function loadOrgs() {
  const grid = document.getElementById('orgsGrid');
  try {
    const res = await fetch(API_URL);
    const data = await res.json();
    if (data.items.length === 0) {
      grid.innerHTML = '<p>No organizations found.</p>';
      return;
    }
    grid.innerHTML = data.items.map(buildOrgCard).join('') + `
      <div class="no-results" id="noResults" style="display:none;">
        <p>No organizations found matching your search.</p>
      </div>
    `;
    initFilters();
  } catch (err) {
    grid.innerHTML = '<p>Could not load organizations. Make sure the backend is running.</p>';
  }
}

loadOrgs();

