# Backend Quick Orientation

This backend is intentionally simple, modular, and easy to extend.

## Request Flow (Current Example)

`GET /api/v1/events/upcoming`

1. `api/routes/events.py` receives the HTTP request.
2. `controllers/events_controller.py` converts service data to response models.
3. `services/event_service.py` applies business rules (such as limit bounds).
4. `repositories/event_repository.py` runs SQL queries.
5. `db/connection.py` manages SQLite connection and bootstrapping.

## File-by-File Purpose

- `app/main.py`: FastAPI app creation, middleware, router wiring, startup DB init.
- `app/config/settings.py`: environment configuration (`.env` support).
- `app/models/event.py`: response model contracts.
- `app/utils/response.py`: shared response envelope helper.
- `tests/test_events_api.py`: API-level tests for endpoint behavior and payload shape.

## Naming Pattern

- `routes/*`: transport layer files (`events.py`, `health.py`)
- `controllers/*_controller.py`: response shaping layer
- `services/*_service.py`: business logic layer
- `repositories/*_repository.py`: data access layer

Use this pattern when adding new domains (`organizations`, `users`, `rsvps`, etc.).
