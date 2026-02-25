# Agents.md

## Project Overview

A producer-consumer architecture built with **FastAPI** and **Loguru** for structured logging. The producer generates tasks and the consumer processes them. The application supports multiple deployment environments (development, QA, production) via Docker.

---

## Architecture

| Layer | Responsibility |
|---|---|
| **Repository** | All database operations (queries, inserts, updates, deletes) |
| **Service** | All business logic and orchestration |
| **Router/API** | Request/response handling only — no logic or DB calls |

---

## Code Style

### Layering Rules
- **Repository layer** — the only place DB operations are allowed. No business logic here.
- **Service layer** — the only place business logic lives. No direct DB calls; delegate to repository.
- **Router layer** — thin layer. Only calls service methods and returns responses.

### Repository Conventions
Every repository function must:
1. Use the designated **decorator** (e.g. `@connect_db` or equivalent).
2. Accept **`session`** as the **last parameter**.

```python
# ✅ Correct
@connect_db
async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    ...

# ❌ Wrong — missing decorator, session not last
async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    ...
```

---

## Commands

### After Every Code Generation
Always validate syntax immediately after writing or modifying code:

```bash
uv run ruff check .
```

Fix all reported issues before considering the task complete. Do not skip this step.

---

## Checklist for Every Code Change

- [ ] Logic is in the correct layer (DB → repository, logic → service)
- [ ] Repository functions have the decorator and `session` as the last param
- [ ] `uv run ruff check .` passes with no errors
- [ ] No direct DB calls outside the repository layer
