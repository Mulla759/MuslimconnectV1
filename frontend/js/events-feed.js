const API_URL = 'http://127.0.0.1:8000/api/v1/events/upcoming';

function formatDate(datetimeStr) {
  const date = new Date(datetimeStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) +
    ' · ' + date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

function buildEventCard(event) {
  return `
    <article class="event-card" onclick="window.location.href='web-event-detail.html'">
      <div class="event-flyer">
        <div class="event-flyer-bg flyer-gradient-1">
          <div class="flyer-content">
            <div class="flyer-org-badge">${event.organization_name}</div>
            <div class="flyer-title">${event.title}</div>
            <div class="flyer-date-info">${formatDate(event.start_datetime)}</div>
          </div>
          <svg class="flyer-decoration" viewBox="0 0 40 40" fill="white">
            <path d="M20 2L23.5 14H36L25.75 22L29.25 34L20 26L10.75 34L14.25 22L4 14H16.5L20 2Z"/>
          </svg>
        </div>
        <div class="event-date-badge">${formatDate(event.start_datetime)}</div>
      </div>
      <div class="event-card-content">
        <div class="event-org-row">
          <div class="event-org-avatar" style="background: var(--green-500);">
            ${event.organization_name.charAt(0)}
          </div>
          <span class="event-org-name">${event.organization_name}</span>
          ${event.organization_verified ? `
            <span class="verified-badge">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                <circle cx="12" cy="12" r="11" fill="none" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </span>` : ''}
        </div>
        <h3 class="event-title">${event.title}</h3>
        <div class="event-location">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          ${event.location}
        </div>
        <div class="event-actions">
          <button class="action-btn save-btn" aria-label="Save event" onclick="event.stopPropagation();">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
            </svg>
          </button>
          <div class="action-spacer"></div>
          <button class="rsvp-btn" onclick="event.stopPropagation();">RSVP</button>
        </div>
      </div>
    </article>
  `;
}

async function loadEvents() {
  const feed = document.getElementById('events-feed');
  try {
    const res = await fetch(API_URL);
    const data = await res.json();
    if (data.items.length === 0) {
      feed.innerHTML = '<p>No upcoming events.</p>';
      return;
    }
    feed.innerHTML = data.items.map(buildEventCard).join('');
  } catch (err) {
    feed.innerHTML = '<p>Could not load events. Make sure the backend is running.</p>';
  }
}

loadEvents();