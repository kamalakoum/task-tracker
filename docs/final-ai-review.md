# Final AI Review and Ownership Evidence

## Three AI usage rules

1. **Never paste secrets or sensitive data into AI tools.** I do not share credentials, tokens, `.env` values, or real customer/personal data with an AI assistant.
2. **Always verify before accepting.** I treat AI output as a draft and confirm material claims with a command (`pytest`, `curl /health`, `docker run`), a source read, or a manual UI check before recording or merging anything.
3. **Record and grade AI contributions.** I keep evidence of what AI suggested, label each finding as useful, noisy, or wrong, and document what I accepted, rejected, or corrected (see the review tables below and [`docs/ai-playbook.md`](ai-playbook.md)).

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| “The README should describe the app as SQLite-backed.” | Wrong | The repo source shows the current storage is an in-memory dictionary, so the suggestion contradicts the actual implementation. | Rejected and corrected in the README to match the real code path. |
| “CI can be simplified with a generic Python version and loose dependency install.” | Noise | The existing workflow is already explicit and functional for the course scope. | Kept the existing CI workflow and verified the command path rather than rewriting it. |
| “Docker should be changed to include a database or auth layer for the final project.” | Wrong | That would add new product scope and violate the no-new-features rule from the brief. | Rejected; the container remains a simple runtime wrapper around the existing app. |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| API is unauthenticated. | `app/main.py` contains task CRUD routes without any auth dependency. | Valid | This is a real security posture issue for any network-visible deployment. | Document as local/demo scope and avoid claiming production auth. |
| CORS allows an opaque `null` origin. | `app/main.py` includes `"null"` in `allow_origins`. | Valid | The frontend does not need that origin for the visible local flow. | Keep the allowlist explicit and remove the unnecessary origin. |
| Unbounded memory growth risk from in-memory task storage. | `app/storage.py` uses a module-level dictionary and returns all tasks. | Valid | The course-scoped architecture is simple, but the storage pattern is not production-safe. | Add future documentation or guardrails, but do not expand scope in this final project. |

## Manual check
A manual runtime check was performed by starting the app locally with `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`, then sending `GET /health` and confirming a `200` response. I also verified that the container image responds on `http://127.0.0.1:8000/health` after running `docker build` and `docker run`.

## Rejected or corrected AI output
One AI suggestion recommended describing the repo as SQLite-backed. I rejected that because the current source of truth in `app/storage.py` is an in-memory dictionary, so the documentation would have been false and would have misled future maintainers. I corrected the README to reflect the actual implementation and the verified run commands.

## Ownership statement
I am comfortable submitting this repository because the final work stayed bounded to documentation, release evidence, and repository readiness. Every command I recorded was run in the workspace, the baseline tests were re-verified, and the Docker health check was exercised directly. I can explain each file and decision in this final result because the evidence comes from the actual code, runtime commands, and current repo state rather than from a blind acceptance of AI-generated output.
