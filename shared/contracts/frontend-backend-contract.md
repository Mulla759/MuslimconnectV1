# Frontend-Backend API Contract

This document defines the explicit data contract for the first wired endpoint:
`GET /api/v1/events/upcoming`.

## Consumer Surfaces

The static frontend pages currently model these event properties:
- `frontend/web-dashboard.html` (event feed cards)
- `frontend/web-event-detail.html` (event details)

## Endpoint

- Method: `GET`
- Path: `/api/v1/events/upcoming`
- Query params:
  - `limit` (integer, 1-100, default 10)

## Response Shape

```json
{
  "items": [
    {
      "id": 1,
      "organization_id": 1,
      "organization_name": "Muslim Student Association",
      "organization_verified": true,
      "title": "Annual MSA Gala Night 2026",
      "description": "Community dinner, keynote speakers, and student awards.",
      "location": "University Ballroom, Main Campus",
      "start_datetime": "2026-04-10T19:00:00",
      "end_datetime": "2026-04-10T22:00:00",
      "status": "scheduled"
    }
  ],
  "count": 1
}
```

## Field Semantics

- `organization_verified`: display verified badge when true.
- `start_datetime` / `end_datetime`: ISO-like datetime strings intended for client-side formatting.
- `status`: backend currently excludes `cancelled` from this endpoint.

## Evolution Rules

1. Additive changes are preferred (new optional fields).
2. Breaking changes require:
   - Contract file update
   - Schema update
   - Frontend migration plan
