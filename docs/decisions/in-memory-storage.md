# In-Memory Storage Architecture for Task Tracker 

## Context

The Task Tracker  is a monolithic FastAPI application designed for learning purposes. It needs to store and retrieve task data (title, description, status, priority, assignee, timestamps). The project prioritizes clarity and fast iteration over enterprise-style architecture patterns. Early design decisions needed to address how to persist task state across requests.

## Decision

Use a module-level in-memory dictionary (`_tasks` in `app/storage.py`) as the exclusive data store instead of introducing a datasase. Task data is loaded and modified entirely in Python memory, with no disk I/O or external persistence layer.

## Alternatives Considered

**1. SQLite with ORM (e.g., SQLAlchemy)**
- Would provide ACID semantics and proper schema enforcement
- Rejected because it adds significant boilerplate (ORM models, migrations, session management) that obscures the core learning objective and slows iteration. The project explicitly avoids "enterprise-style architecture" and ORM abstractions.

**2. PostgreSQL or cloud-hosted database**
- Would provide production-ready persistence, scalability, and multi-process safety
- Rejected for similar reasons: introduces operational complexity (database provisioning, connection pooling, network latency) unsuitable for a learning codebase. Adds deployment dependencies that conflict with the goal of simplicity.

**3. File-based persistence (JSON or CSV)**
- Would offer persistence without a database, using simple serialization to disk
- Rejected because it introduces thread-safety issues in the in-memory dictionary (readers/writers conflict) without solving the core learning need. Provides false confidence in data durability for a project that is explicitly ephemeral.

## Trade-offs

**What the decision gives:**
- Minimal code complexity; task operations are straightforward dictionary lookups and mutations
- Fast development and testing; no setup/teardown of database fixtures beyond clearing the dict
- Direct access to in-memory task objects for inspection and debugging
- Immediate feedback during development (no database lag or connection issues)

**What the decision gives up:**
- Data durability: all tasks are lost when the application stops
- Concurrency safety: no locking or transaction isolation if multiple processes/threads access `_tasks` simultaneously (the in-memory dict is not thread-safe for concurrent mutations)
- Queryability: filtering by status/priority must be done in-memory loops (see `get_all_tasks()` in `storage.py`), not via a query language
- Scalability: memory usage grows unbounded; no archival or pagination strategy
- Multi-instance deployments: each container has its own task set; tasks created on one instance are invisible to others

## Consequences

1. **Test isolation works easily**: The `_reset_storage()` fixture in `conftest.py` can clear all tasks before/after each test by reassigning the dictionary.

2. **Deployment limitations**: The application cannot be deployed as a multi-instance service (e.g., behind a load balancer in Kubernetes). The Dockerfile builds a valid container, but each instance would be independent.

3. **Stateless API is a misnomer**: The API is stateful (it accumulates tasks in memory) but not externally stateful. Clients cannot distinguish between a restart that lost data and a restart that preserved it.

4. **No validation layer between API and storage**: `app/models.py` validates input at the handler level (Pydantic), but there is no schema enforcer in storage; mutations happen on plain dictionaries.

5. **Business logic isolation is clean**: State machine transitions (in `business_rules.py`) are independent of storage, so they could be tested and reused if storage changes later.

## Open Questions

1. **When should persistence be added?** Is the learning objective fully met with in-memory storage, or does the project need to demonstrate how to migrate to a real database without breaking tests?

2. **How should concurrent requests be handled?** If the development server receives simultaneous PATCH requests to the same task, the in-memory dictionary may corrupt. Should this be documented as a limitation, or protected with locks?

3. **What is the intended scope of "learning"?** Is the goal to learn FastAPI/Pydantic/REST design, or also data persistence patterns? If the latter, when does the in-memory assumption become a barrier?

4. **Should data retention be explicit?** Currently, tasks disappear silently on restart. Should a migration path exist (e.g., import/export endpoints, or environment-driven toggle to use a real database)?
