# Contributing to MuslimConnect

This repository is structured as a frontend prototype plus a production-ready backend scaffold.
Use this guide so contributions stay predictable and reviewable.

## 1. Onboarding

1. Fork the repository.
2. Clone your fork.
3. Create and activate a Python virtual environment.
4. Install backend dependencies.
5. Copy `.env.example` to `.env` and adjust values if needed.
6. Run backend tests and lint checks before opening a PR.

## 2. Local Setup Commands

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env

# quality gates
ruff check backend/app backend/tests
pytest backend
```

## 3. Branching Strategy

1. Keep `main` always releasable.
2. Branch from `main` using descriptive names:
   - `feature/<short-topic>`
   - `fix/<short-topic>`
   - `chore/<short-topic>`
3. Prefer small, focused PRs over large batch changes.

## 4. Pull Request Process

1. Rebase your branch onto latest `main`.
2. Run local quality checks (`ruff`, `pytest`) before opening a PR.
3. Open a PR with:
   - Scope summary
   - Implementation notes
   - Test evidence
   - Any migration or env changes
4. Address review comments with follow-up commits.
5. Merge only when required checks pass.

## 5. Code Style Expectations

- Python style is enforced by `ruff`.
- Use explicit, descriptive names:
  - Files: `<domain>_<layer>.py` when possible (example: `events_controller.py`)
  - Functions: verb-first for actions (`list_upcoming_events`, `fetch_upcoming_events`)
  - Models: noun-based (`EventSummary`, `UpcomingEventsResponse`)
- Keep modules small and layered:
  - `routes` for HTTP boundaries
  - `controllers` for response shaping
  - `services` for business logic
  - `repositories/models` for persistence/domain concerns
- Add concise module docstrings at file top.
- Add tests for new behavior and regressions.

## 6. Contracts and Compatibility

Frontend/backend payload expectations are documented in:
- `shared/contracts/frontend-backend-contract.md`
- `shared/contracts/upcoming-events-response.schema.json`

When changing API shape, update both contract files in the same PR.

## 7. Commit Guidance

Use clear, imperative commit messages:
- `feat: add event creation endpoint scaffold`
- `fix: handle cancelled events in upcoming query`
- `docs: update API contract for dashboard feed`
