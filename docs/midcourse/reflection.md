# Reflection

I used Cursor’s coding agent as a pair-programmer for this Module assessment: exploring the existing FastAPI layout, drafting the comments and activity designs against `AGENTS.md` constraints, implementing storage/models/routes/tests, and integrating the Kanban UI in `frontend/index.html`. I kept ownership by choosing the two scoped features myself (comments + activity), rejecting persistence/auth/pagination suggestions, and verifying with the existing pytest style before trusting the UI.

AI helped most when extending the in-memory storage consistently: cascading comment deletes, maintaining `comment_count`, and emitting `status_changed` details with `from`/`to` without rewriting the whole task API. That saved time versus hand-wiring every edge case.

AI slowed me down when early suggestions drifted toward SQLite or nested comment payloads that would break the current monolithic in-memory design and existing tests. Reviewing those outputs against the repo forced an explicit mini-ADR and stronger prompts, which was valuable but cost an extra planning loop.

The clearest place my review changed the result was the frontend: I rejected showing comments during create, required edit-modal-only comment UX, and insisted the global activity panel refresh after drag-and-drop status changes so the board and feed stay consistent. Those edits came from running the app mentally against acceptance criteria, not from accepting the first generated UI sketch.

Overall, the useful pattern was small loops—backend, tests, frontend, verify—rather than one large generated patch.
