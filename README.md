# MuslimConnect Monorepo

MuslimConnect is a campus-community platform for Muslim students to discover organizations, view upcoming events, and stay aligned on prayer/community life in one place.

This repository contains:
- A static frontend prototype in `frontend/`
- A FastAPI backend scaffold in `backend/`
- Shared frontend/backend API contracts in `shared/contracts/`

## Tech Stack

### Frontend
- HTML/CSS/JavaScript
- Multi-page static prototype

### Backend
- Python 3.12+
- FastAPI + Uvicorn
- SQLite
- Pytest + Ruff

## Prerequisites

- Python 3.12+
- Git

## Quick Start

```bash
git clone https://github.com/Mulla759/MuslimconnectV1.git
cd MuslimconnectV1
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
cp .env.example .env
python3 scripts/dev.py
```

That single `python3 scripts/dev.py` command starts both services from the repo root:
- Frontend static server
- Backend API server with reload enabled

When startup succeeds, the launcher prints the exact URLs to use:
- Frontend landing page: `http://127.0.0.1:5500/web-landing.html`
- Frontend dashboard: `http://127.0.0.1:5500/web-dashboard.html`
- Backend health: `http://127.0.0.1:8000/api/v1/health`
- Backend events: `http://127.0.0.1:8000/api/v1/events/upcoming`
- Backend docs: `http://127.0.0.1:8000/docs`

Stop both servers with `Ctrl+C`.

## One-Command Dev Workflow

The canonical local workflow is:

```bash
python3 scripts/dev.py
```

The launcher:
- Starts the frontend and backend together
- Uses `.venv/bin/python` automatically when that virtual environment exists
- Keeps logs in one terminal
- Exits with a clear error if a chosen port is already in use
- Does not auto-pick random ports unless you explicitly change them

This is the workflow to share with contributors who need frontend and backend running together for backend testing.

## Choosing Hosts and Ports

The defaults are:
- Backend: `127.0.0.1:8000`
- Frontend: `127.0.0.1:5500`

If those ports are not available on a contributor machine, keep the same one-command workflow and change the values once in `.env`:

```bash
APP_HOST=127.0.0.1
APP_PORT=8000
FRONTEND_HOST=127.0.0.1
FRONTEND_PORT=5500
```

You can also override them directly at launch time:

```bash
python3 scripts/dev.py --frontend-port 5600 --backend-port 8100
```

If someone needs the servers accessible from other devices on the same network, bind to all interfaces explicitly:

```bash
python3 scripts/dev.py --frontend-host 0.0.0.0 --backend-host 0.0.0.0
```

Then use that machine's local IP address instead of `127.0.0.1` when testing from another device.

## Backend Testing While Frontend Is Running

The frontend is still a static prototype, so it does not yet call the live API directly. Running both servers together is still useful because it gives contributors a single local session for:
- Visual frontend review
- Manual backend endpoint testing
- Swagger inspection at `/docs`
- Contract verification against `shared/contracts/`

Useful backend checks while the dev launcher is running:

```bash
curl http://127.0.0.1:8000/api/v1/health
curl "http://127.0.0.1:8000/api/v1/events/upcoming?limit=5"
```

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
