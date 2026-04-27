const API_BASE = 'http://127.0.0.1:8000/api/v1';

function formatDate(datetimeStr) {
  const date = new Date(datetimeStr);
  return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
}

function formatTime(datetimeStr) {
  const date = new Date(datetimeStr);
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

function getEventIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function loadEventDetail() {
  const eventId = getEventIdFromURL();
  if (!eventId) return;

  try {
    const res = await fetch(`${API_BASE}/events/${eventId}`);
    if (!res.ok) return;
    const event = await res.json();

    // Update title
    document.title = `${event.title} — MuslimConnect`;

    // Update flyer date badge
    const dateBadge = document.querySelector('.date-badge');
    if (dateBadge) dateBadge.textContent = `${formatDate(event.start_datetime)} · ${formatTime(event.start_datetime)}`;

    // Update event title
    const titleEl = document.querySelector('.event-title');
    if (titleEl) titleEl.textContent = event.title;

    // Update org name
    const orgNameEls = document.querySelectorAll('.org-name, .org-card-name');
    orgNameEls.forEach(el => {
      if (!el.querySelector('span')) el.textContent = event.organization_name;
    });

    // Update org avatars
    const orgAvatars = document.querySelectorAll('.org-avatar, .org-card-avatar');
    orgAvatars.forEach(el => el.textContent = event.organization_name.charAt(0));

    // Update description
    const descEl = document.querySelector('.event-description');
    if (descEl) descEl.innerHTML = `<p>${event.description || 'No description available.'}</p>`;

    // Update date detail
    const detailValues = document.querySelectorAll('.detail-value');
    if (detailValues[0]) detailValues[0].textContent = formatDate(event.start_datetime);
    if (detailValues[1]) detailValues[1].textContent = `${formatTime(event.start_datetime)}${event.end_datetime ? ' – ' + formatTime(event.end_datetime) : ''}`;
    if (detailValues[2]) detailValues[2].textContent = event.location;

    // Update map address
    const mapAddress = document.querySelector('.map-address');
    if (mapAddress) mapAddress.innerHTML = `<strong>${event.location}</strong>`;

  } catch (err) {
    console.error('Could not load event detail:', err);
  }
}

loadEventDetail();