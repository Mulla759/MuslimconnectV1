# MuslimConnect Monorepo

MuslimConnect is a campus-community platform for Muslim students to discover organizations, view upcoming events, and stay aligned on prayer/community life in one place.

This repository now contains:
- A locked frontend prototype (`frontend/`) with production UI direction.
- A backend starter architecture (`backend/`) that backend engineers can immediately extend.
- Shared API contracts (`shared/contracts/`) so frontend expectations are explicit.

## Tech Stack

### Frontend
- HTML/CSS/JavaScript (multi-page static prototype)
- Google Fonts + Phosphor icons
- Tailwind CDN on marketing page only (`web-landing.html`)

### Backend Scaffold
- Python 3.12+
- FastAPI + Uvicorn
- SQLite (seeded local DB)
- Pytest + Ruff

## Prerequisites

- Python 3.12+
- `pip`
- Git

## Installation (Monorepo)

```bash
# 1) clone and enter
git clone https://github.com/Mulla759/MuslimconnectV1.git
cd MuslimconnectV1

# 2) create env
python3 -m venv .venv
source .venv/bin/activate

# 3) install backend deps
pip install -r backend/requirements.txt

# 4) configure env vars
cp .env.example .env
```

## Run Locally (Frontend + Backend Together)

Use two terminals from repo root.

### Terminal A: Backend API

```bash
source .venv/bin/activate
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

- Health check: `http://127.0.0.1:8000/api/v1/health`
- Example endpoint: `http://127.0.0.1:8000/api/v1/events/upcoming`

### Terminal B: Frontend Static Pages

```bash
python3 -m http.server 5500 --directory frontend
```

- Landing: `http://127.0.0.1:5500/web-landing.html`
- Dashboard: `http://127.0.0.1:5500/web-dashboard.html`

## Backend Architecture (Scaffold)

The backend is intentionally modular and extensible:

- `routes` define HTTP endpoints.
- `controllers` shape API responses.
- `services` hold business logic.
- `repositories` handle persistence queries.
- `models` define request/response schemas.
- `config` centralizes settings.
- `utils` holds shared helpers.
- `tests` validate API behavior and contract shape.

Backend onboarding details are in `backend/README.md`.

### Example End-to-End Endpoint

`GET /api/v1/events/upcoming`

Flow:
1. Route: `backend/app/api/routes/events.py`
2. Controller: `backend/app/controllers/events_controller.py`
3. Service: `backend/app/services/event_service.py`
4. Repository: `backend/app/repositories/event_repository.py`
5. DB bootstrap/query: `backend/app/db/connection.py`

## Shared Frontend/Backend Contracts

These files define what the frontend expects from the backend:

- `shared/contracts/frontend-backend-contract.md`
- `shared/contracts/upcoming-events-response.schema.json`

If API response shape changes, update these contracts in the same PR.

## Contributing

See `CONTRIBUTING.md` for:
- onboarding and local setup
- branch naming strategy
- PR process
- code style and test expectations

## Repository Structure Map

```text
muslimconnect/
├── backend/
│   ├── app/
│   │   ├── main.py                        # FastAPI app entrypoint
│   │   ├── api/routes/
│   │   │   ├── health.py                  # Liveness endpoint
│   │   │   └── events.py                  # Example upcoming-events endpoint
│   │   ├── config/settings.py             # Env-driven app settings
│   │   ├── controllers/events_controller.py # API response shaping
│   │   ├── services/event_service.py      # Business rules for events
│   │   ├── repositories/event_repository.py # SQL queries for events
│   │   ├── models/event.py                # Response schemas
│   │   ├── db/connection.py               # SQLite init + seed + connection
│   │   └── utils/response.py              # Shared response helper
│   ├── README.md                          # Backend orientation for new devs
│   ├── tests/test_events_api.py           # API tests
│   ├── requirements.txt                   # Backend dependencies
│   ├── pytest.ini                         # Test discovery config
│   └── .ruff.toml                         # Lint configuration
├── db/
│   ├── schema.sql                         # Legacy prototype SQL (kept for reference)
│   ├── database.py                        # Legacy prototype DB helper
│   └── database.db                        # Local SQLite file
├── frontend/
│   ├── web-landing.html                   # Marketing page
│   ├── web-auth.html                      # Auth page
│   ├── web-dashboard.html                 # Feed/dashboard page
│   ├── web-orgs.html                      # Organizations page
│   ├── web-event-detail.html              # Event detail page
│   ├── css/                               # Shared and page-specific styles
│   ├── js/                                # Page interaction scripts
│   └── assets/logo.svg                    # Brand mark
├── repos/                                 # Legacy prototype repository modules
├── shared/contracts/                      # Explicit frontend/backend API contract
├── CONTRIBUTING.md
├── .env.example
├── app.py                                 # Legacy prototype script
└── README.md
```

## Notes for Backend Engineers

- The current frontend is static and does not yet fetch live API data.
- Treat this backend as the initial contract-aligned foundation.
- Add new domains by repeating the same route/controller/service/repository model.
