# Security Review

## Al Findings

| ID | Severity | File / location | Finding | Evidence | Suggested next step | Confidence | Grade | Reason |
|---|---|---|---|---|---|---|---|---|
| SEC-01 | High | app/main.py:47 | All task data and mutation endpoints are unauthenticated. Any client able to reach the API can create, list, modify, or delete tasks. | The route handlers contain no authentication/authorization dependency or ownership check (create: app/main.py:47; list/get: app/main.py:70; update/delete: app/main.py:114). The container listens on all interfaces (Dockerfile:32). Course-scope intent is plausible, but not explicitly documented as an accepted security limitation. | Explicitly document this as local/demo-only, restrict network exposure, or add an authentication/authorization boundary before deployment. | High | TODO | TODO |
| SEC-02 | Medium | app/models.py:29; app/storage.py:37 | `description` and `assignee` have no size limits; tasks accumulate indefinitely and `GET /tasks` returns the entire collection without pagination. This permits memory and response-size exhaustion. | Only `title` is capped at 200 characters (app/models.py:20); `description` and `assignee` are unconstrained (app/models.py:32). Storage is a module-global dictionary and list retrieval materializes all entries (app/storage.py:7, app/storage.py:51). The architecture note records unbounded memory growth (docs/decisions/in-memory-storage.md:37). | Set field-size limits, paginate/cap list results, and enforce request/body limits at the deployment boundary. | High | TODO | TODO |
| SEC-03 | Low | app/main.py:29 | CORS explicitly trusts the opaque `null` origin, broadening browser access beyond the named local development origins. | `allow_origins` includes `"null"` and all methods/headers are enabled (app/main.py:31). Credentials are disabled (app/main.py:39). The frontend uses `http://localhost:8000` (frontend/index.html:444), so this entry is not needed for the visible frontend. | Remove `"null"` unless there is a documented, required opaque-origin client; keep an explicit environment-specific origin allowlist. | High | TODO | TODO |
| SEC-04 | Low | Dockerfile:1; requirements.txt:1; .github/workflows/ci.yml:28 | Dependencies are pinned, but packages are installed without hashes, Docker base images use mutable tags, and CI has no dependency/container vulnerability scan. | Runtime dependencies are version-pinned (requirements.txt:1), but no requirement hashes or image digests are present (Dockerfile:1). CI installs dependencies and runs tests only (.github/workflows/ci.yml:28). | Use a hash-locked dependency workflow, pin base images by digest, and add dependency/container scanning in CI. | High | TODO | TODO |

## My Manual Findings

| Severity | File:Line | Finding | Suggested Fix | Reason |
|---|---|---|---|---|

## Reconciliation

### Agfeement

### Al-only

### You-only

## Top 3 Unfixed Backlog

Rank | Finding | Severity | Owner | Next Step
| 1 | Add authentication, authorization, and task ownership before any real deployment. | Medium if deployed | Backend
Define the expected user model and protect all task mutation/ read endpoints. |
| 2 | Bound request and storage growth for task fields and total task count. | Medium | Backend | Add max lengths for
'description' and 'assignee', then decide whether rate limits or quotas belong at app or proxy level. I | 3 | Upgrade vulnerable/dev-risk dependencies and tighten supply-chain pins. | Medium | Platform | Update
'python-dotenv and pytest', then consider SHA/digest pinning for CI actions and Docker base images. |
