# Sophia — Vault Hotfix + Ops-Safety — roll-up (handoff to thread 2744)

**Status as of 2026-06-12:** handed to Sophia in the **Governance & Vault** topic (thread 2744)
**Repo:** `truesight_autopilot` (Sophia's OWN codebase) · companion to `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md`

> ⛔ **Own-repo gate:** open PRs only, **NEVER self-merge** — a human reviews + merges.
> `Generated-by: Sophia (TrueSight Autopilot)` trailer on every commit.
> ⚠️ **First, commit the vault.** `app/vault_routes.py` / `app/vault_app.py` are currently
> **UNCOMMITTED on the prod box** — commit them on a branch + PR before anything else. No
> uncommitted code on prod.

> **RESUME HERE:** Fix #1 (the vault 500) — it's a one-line-per-call bug blocking the whole page.

This rolls up everything found while debugging the vault + tonight's two self-brick incidents
(2026-06-12). Do these in order.

## Fix #1 — Vault 500 (blocking) 🔴
`https://sophia.truesight.me/vault/` returns **500**. Traceback:
```
app/vault_routes.py:108, in vault_page → TemplateResponse(...)
TypeError: unhashable type: 'dict'
```
Cause: old-style `TemplateResponse("vault.html", {"request": request, ...})`. The installed
Starlette wants the **new signature** — `request` FIRST:
```python
return templates.TemplateResponse(request, "vault.html", {...context without request...})
```
So the context dict was being passed where the template *name* goes → jinja2 used a dict as a
cache key → "unhashable type: dict". **Fix every `TemplateResponse(...)` call in `vault_routes.py`**
(login page too, not just `/vault/`). **UAT:** `/vault/` and `/vault/login` → 200, render.

## Fix #2 — Discoverability 🔴
The Sophia root landing page (`/`, "Sophia — TrueSight DAO Oracle") links only to
`oracle.truesight.me` and `truesight.me` — **nothing to the vault.** Add a clear nav link/button
from `/` to `/vault/`, so a governor who opens `sophia.truesight.me` can actually reach the vault.

## Requirement #3 — Live thread-status panel (Gary) 🟡
On the (governor-gated) vault page, render a **UI on top of `/vault/api/system-status`**:
- the **active threads** and what each is doing right now (from `_live_progress` — current tool,
  round, elapsed, instruction), and the **queue depth** per thread;
- a prominent **"Safe to redeploy?"** indicator — **green only when all threads are idle**, red
  when any thread has an in-flight turn.
This is the operator's window into "what is Sophia doing right now" and "is it safe to restart her."

## Requirement #4 — Idle-drain before self-redeploy (Gary) 🟡
Tonight Sophia **SIGKILL-restarted herself mid-turn**, severing in-flight turns and wedging the
Telegram adapter (3 threads went unresponsive). Before any self restart/redeploy:
- (a) check **no thread has an active turn** (`_active_streams` / `_live_progress` / per-thread
  locks — the SAME idle signal as #3's indicator);
- (b) if busy → **defer**, or **drain** (stop accepting new turns, let in-flight ones finish);
- (c) restart with a **graceful SIGTERM + drain window — NEVER SIGKILL**.

## Guardrail #5 — Prod runs merged `main` only 🟡
Tonight the prod box was running `autopilot/followup-store` (an **open, unmerged** PR) — which is
how broken/unreviewed code reached prod. **Never self-deploy a worktree/feature branch to the prod
box.** Dev happens in the worktrees; the prod box only ever runs **merged `main`**, deployed after
a human merge. (Pairs with #4: deploy = merge → drain → graceful restart.)

## UAT (operator)
| # | Check |
|---|-------|
| V1 | `https://sophia.truesight.me/vault/` and `/vault/login` → **200, render** (not 500). |
| V2 | A link to the vault is reachable from `https://sophia.truesight.me/`. |
| V3 | The vault shows the live **thread-status panel** (active threads + current activity + queue depth) and a **"Safe to redeploy?"** indicator (red when any thread busy, green when all idle). |
| V4 | A self-redeploy **while a thread is mid-turn is deferred until idle** (graceful SIGTERM+drain, no mid-turn kill). |
| V5 | The vault code (`vault_routes.py`/`vault_app.py`) is **committed + merged to main**; prod runs `main`. |

**Completion gate:** PRs human-merged (Sophia opens, never self-merges); V1–V5 pass.

> **RESUME HERE:** commit the uncommitted vault code → Fix #1 (TemplateResponse) → #2 → #3 → #4/#5.
> Report progress in thread 2744.
