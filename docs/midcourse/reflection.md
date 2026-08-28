# Reflection

I used Cursor’s coding agent as a pair-programmer for this Module assessment: exploring the existing FastAPI layout, drafting the comments and activity designs against `AGENTS.md` constraints, implementing storage/models/routes/tests, and integrating the Kanban UI in `frontend/index.html`. I kept ownership by choosing the two scoped features myself (comments + activity), rejecting persistence/auth/pagination suggestions, and verifying with the existing pytest style before trusting the UI.

AI helped most when extending the in-memory storage consistently: cascading comment deletes, maintaining `comment_count`, and emitting `status_changed` details with `from`/`to` without rewriting the whole task API. That saved time versus hand-wiring every edge case.

AI slowed me down when early suggestions drifted toward SQLite or nested comment payloads that would break the current monolithic in-memory design and existing tests. Reviewing those outputs against the repo forced an explicit mini-ADR and stronger prompts, which was valuable but cost an extra planning loop.

The clearest place my review changed the result was the frontend: I rejected showing comments during create, required edit-modal-only comment UX, and insisted the global activity panel refresh after drag-and-drop status changes so the board and feed stay consistent. Those edits came from running the app mentally against acceptance criteria, not from accepting the first generated UI sketch.

Overall, the useful pattern was small loops—backend, tests, frontend, verify—rather than one large generated patch. Practically, that looked like short iterations: add a storage helper, update a test, run the test suite, and then tweak the UI to match the API contract. I found that keeping the tests as the contract reduced cognitive load when accepting suggestions from the agent.

Concretely, I adopted three small engineering practices during the work: (1) preserve existing public API shapes unless a change is necessary, (2) add minimal, well-scoped tests to protect behavior before refactors, and (3) prefer explicit data in activity entries so the frontend can render without extra calls. Those decisions kept the implementation simple and the test suite fast.

For collaboration, documenting the mini-ADR was crucial. It captured why persistence and nested payloads were deferred, what the migration path to a database would look like, and what contract changes would be required. That note reduced repeated debates and will help future contributors pick up the thread.

Next steps I would take if continuing: extract a storage adapter interface to allow swapping an in-memory store for a persistent one, add end-to-end UI tests for drag-and-drop and activity updates, and expand the activity payload schema for richer metadata (user, timestamp, preview). Those changes are intentionally incremental so they can be validated by tests and reviewed without broad surface-area changes.

Using an AI pair-programmer sped up routine refactors and suggested alternatives I otherwise might not have considered, while human judgment kept the design aligned with the project constraints and tests.
