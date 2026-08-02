# Release Evidence

## Baseline
- Branch: final-project
- Date: 2026-08-02
- Local app run command: `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- `/health` result: `200` with body `{"status":"ok","timestamp":"2026-08-02T07:21:05.324632+00:00"}`
- Frontend check: opened `frontend/index.html` in the browser and confirmed the Kanban board with the `New Task` button and board columns is visible.
- Test command: `source venv/bin/activate && python -m pytest -q`
- Test result: `19 passed in 0.08s`

## CI evidence
- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: GitHub Actions workflow is configured for `push` and `pull_request`, and the command `pytest -v --tb=short` is the verification step.
- Test command used by CI: `pytest -v --tb=short`
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.

## Docker evidence
- Build command: `docker build -t task-tracker-backend:final .`
- Run command: `docker run --rm -d -p 8000:8000 --name task-tracker-final task-tracker-backend:final`
- `/health` check: `200` with body `{"status":"ok","timestamp":"2026-08-02T07:21:17.641693+00:00"}`
- Non-root check, if implemented: the image creates and switches to a non-root user `app` in the final container stage.
- No-baked-secrets check: no `.env` file or secret values are copied into the image; only the application source and Python environment are layered into the container.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The app can be run locally with `uvicorn app.main:app --reload` | Repository runtime and direct `GET /health` verification | Confirmed | Updated README to use the exact verified command form with host and port |
| The app stores data in SQLite | Source inspection of `app/storage.py` and runtime behavior | Not confirmed / incorrect | README now states the code uses an in-memory dictionary, which matches the current implementation |
| Docker image serves `/health` on port 8000 | Direct `docker build` and `docker run` verification | Confirmed | No functional code change required; captured in release evidence |
| CI runs pytest for repository changes | `.github/workflows/ci.yml` and test command | Confirmed | Kept the existing workflow and verified the command path |
