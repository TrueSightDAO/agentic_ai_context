# Sophia GitHub Rate-Limit Governor — bounded outbound concurrency

**Status:** Plan-of-record. Created 2026-09-05 by DeepSeek Local (Gary's request).
**Repo:** `TrueSightDAO/truesight_autopilot` (Sophia's own codebase — opens PRs, human merges).
**Convention:** OPERATING_INSTRUCTIONS.md §5 / §5a / §5c / §5d / §5e.

> ## ▶ RESUME HERE: PR1

## Context

Sophia's write PAT (`TRUESIGHT_DAO_AUTOPILOT`, fine-grained, 5,000 req/h core) has been
exhausting to `403` under sustained load (observed 2026-09-02/05: `Retry-After` backoffs of
587s and 1,360s froze startup + turns; same entries re-read ~8×). This session already landed
three mitigations: **read-only PAT split** (`GITHUB_READ_PAT`, #396), **read-cache** (#395), and
**incremental deploy-ledger feed** (#408). This plan closes the remaining gap: **nothing bounds
Sophia's *concurrent* outbound GitHub calls**, so when multiple Telegram threads run turns in
parallel, their reads/writes burst the shared PAT together.

**Thread-concurrency is already shipped** (`SOPHIA_THREAD_CONCURRENCY_PLAN.md`, PR0–PR3, 2026-06):
- Tool bodies run off the event loop: `_run_tool` → `asyncio.to_thread(_run_tool_sync, …)` (`app/main.py:2484`).
- Per-topic serialization: adapter `_thread_dispatch_locks` (`app/telegram_adapter.py:65–76`) + `_ack_queued_if_busy` (`:131`); brain session locks (`app/main.py:152`).
- Cross-topic concurrency: adapter `ThreadPoolExecutor(max_workers=10)` (`app/telegram_adapter.py:2661`).

So the event loop is already non-blocking; what's missing is a **global bound** so the now-parallel
threads don't stampede GitHub, plus **proactive rate-limit awareness** so she throttles before 403,
plus **thread-safety** on the shared caches that are now touched from worker threads.

## Pre-flight (captured state — no execution unit re-discovers this)

- **Read tools** — `app/tools/github_tools.py`: `_github_headers()` (`:41`, prefers `github_read_pat`), `read_repo_file()` (`:51`), `search_codebase()` (`:117`); in-memory cache `_read_cache` + `_cache_get`/`_cache_set` + `_GITHUB_READ_CACHE_TTL/_MAX` (module top, `:26–40`) — **plain dict, NOT thread-safe** (accessed from `asyncio.to_thread` workers).
- **Deploy ledger** — `app/deploy_ledger.py`: `_headers()` (`:60`), `_read_dir()` (`:91`), `_read_file()` (`:103`), `_put_file()` (`:125`), `_delete_file()` (`:154`); all plain sync `httpx` with `timeout=15.0`.
- **Write client** — `app/github_client.py`: `GitHubClient` uses PyGithub (sync) + lazy `.user`; reads/writes both go through it.
- **Adapter** — `app/telegram_adapter.py`: `_thread_dispatch_locks: dict[str, threading.Lock]` (`:65`) — **grows unbounded** (one lock per (chat,thread), never evicted).
- **No existing global GitHub semaphore** anywhere (`grep Semaphore|BoundedSemaphore|max_workers` finds only the adapter's pool and an oracle IP limiter at `app/main.py:523`).
- **Rate-limit awareness: none** — 403 surfaces only as PyGithub `GithubRetry` "Setting next backoff to NNNs" (`app/github_client.py`), i.e. blind + stalls.

## Sequenced plan (one PR per turn, §5a)

| # | PR | Scope | Files | Gate |
|---|-----|-------|-------|------|
| 1 | **Bounded GitHub concurrency + thread-safe cache** | Add a module-level `threading.BoundedSemaphore` (default 4, env `GITHUB_MAX_CONCURRENCY`) guarding the GitHub calls in `github_tools.py` (read_repo_file, search_codebase) and `deploy_ledger.py` (`_read_dir/_read_file/_put_file/_delete_file`); make `_read_cache` access lock-protected. | `app/tools/github_tools.py`, `app/deploy_ledger.py` | own-repo |
| 2 | **Proactive rate-limit awareness** | On GitHub responses, read `X-RateLimit-Remaining`/`Reset`; log a `WARNING` when remaining < 200, and when < 50 sleep `reset−now` (capped 60s) before the call instead of firing blind into 403. Apply in `_github_headers` callers + `GitHubClient` read path. | `app/tools/github_tools.py`, `app/github_client.py` | own-repo |
| 3 | **Bound the lock registry + shared-state audit** | Evict idle `_thread_dispatch_locks` entries (cap ~500, clear on access older than TTL); audit remaining thread-touched dicts (`_oracle_rate_limit`, `_read_cache`) for races. | `app/telegram_adapter.py` | own-repo |

**Deploy:** after PR1–PR3 merge, human runs the standard box redeploy (`git fetch && git reset --hard origin/main && sudo systemctl restart truesight-autopilot truesight-autopilot-telegram`). §5c always-stop — Sophia does NOT self-deploy.

## Resume tracker

| Unit | PR opened | Merged (human) | Deployed | Contribution reported |
|------|-----------|----------------|----------|----------------------|
| PR1 — bounded concurrency + thread-safe cache | ☐ | ☐ | ☐ | ☐ |
| PR2 — rate-limit awareness | ☐ | ☐ | ☐ | ☐ |
| PR3 — lock-registry bound + audit | ☐ | ☐ | ☐ | ☐ |

## UAT

**UAT: n/a** — backend/library change; covered by automated tests (`python -m py_compile`, plus a
unit test asserting the semaphore is held during a mocked GitHub read and that `_read_cache`
stays consistent under concurrent access). Deploy is human-gated per §5c.

## Authorization envelope (§5e)

- **Pre-authorized (autonomous):** `truesight_autopilot` code changes — Sophia opens PRs, runs local tests; no deploy, no merge-to-main.
- **Gated (human):** merge to `main` (own-repo §5c) and the box redeploy/restart (§5c prod deploy).

> ✅ Pre-flight Completeness: no execution unit requires reading a file/state not already captured
> in the pre-flight.
