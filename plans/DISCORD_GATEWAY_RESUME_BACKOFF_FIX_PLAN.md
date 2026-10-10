# Discord gateway RESUME + backoff-reset fix (truesight_autopilot)

**Date:** 2026-10-10 · **Author:** Envoy (planner session, `nelanco-claude`) · trigger: governor
("I noticed that in discord Sophia often hangs and doesn't reply. I wonder if it is because the
discord connection she is hanging on to times out or because of something else").

**Auto-start: yes** — single, narrowly-scoped, self-contained bug fix in one file; no UAT surface
beyond the automated test added in PR0 itself; low risk of staleness between writing and trigger.

---

## 0. Root cause (confirmed against live logs, 2026-10-10)

`journalctl -u truesight-autopilot-discord.service` on the autopilot box shows the Discord
gateway disconnecting every 1–3 hours with one of:

```
Discord gateway closed; reconnecting in Ns
Discord gateway error: no close frame received or sent; reconnecting in Ns
```

"no close frame received or sent" is the `websockets` library's message for an abnormal
closure (the TCP connection went silent — a NAT/load-balancer/Discord-infra idle timeout —
without a proper WS close handshake). This is the "connection she's hanging onto times out"
the governor suspected.

Two compounding bugs in `app/discord_adapter.py` turn a normal, recoverable reconnect into a
silent dropped-message window:

1. **No gateway session RESUME.** `_gateway_loop`/`_gateway_once` always send a fresh
   `IDENTIFY` (op 2) on reconnect — never `RESUME` (op 6). Discord only replays events that
   happened while disconnected to a **resumed** session (same `session_id` + last `seq`); a
   fresh `IDENTIFY` gets nothing. So any governor message sent during the ~5–65s reconnect
   window is **silently and permanently lost** — no error, no retry, it just never arrives.
   This is the actual "hangs and doesn't reply" symptom.
2. **Backoff never resets on success.** `backoff = min(backoff * 2, 60.0)` runs every loop
   iteration regardless of how long the prior connection lasted — it only ever climbs for the
   life of the process. Log evidence from one process run (started 2026-10-10 05:53:52 UTC):
   first disconnect `reconnecting in 5s` → next `10s` → `20s` → `40s` → `60s`, then **every
   subsequent disconnect for the rest of that process's ~9-hour life waited the full 60s**,
   even though each connection in between lasted 25–150 minutes (clearly healthy, not a
   crash loop). The longer Sophia's Discord adapter runs without a redeploy, the longer each
   dead window gets, and the longer the message-loss risk window from bug #1.

Fixing #1 is the actual message-loss fix; fixing #2 shortens how often it needs to fire at all
and is also what makes resetting correctly safe (see §2.2 — a naive "reset every READY" risks a
reconnect-storm/rate-limit if a connection flaps immediately after READY; gating the reset on a
minimum connected duration avoids that).

---

## 1. Pre-flight (§5d completeness — everything PR0 needs is below; no cross-repo read required)

**File to change:** `truesight_autopilot/app/discord_adapter.py`

**Current code (lines 1547–1627 of the version read 2026-10-10, i.e. the gateway section —
quoted in full so PR0 needs no further discovery):**

```python
# ── Gateway ─────────────────────────────────────────────────────────────


def _gateway_url() -> str:
    data = _api("GET", "/gateway/bot")
    if not data or not data.get("url"):
        raise RuntimeError("could not fetch gateway URL from Discord")
    return data["url"] + _GATEWAY_QUERY


async def _heartbeat(ws, interval: float, seq_getter: Callable[[], int | None]) -> None:
    while True:
        await asyncio.sleep(interval)
        await ws.send(json.dumps({"op": 1, "d": seq_getter()}))


async def _gateway_once(
    url: str,
    allowed: set[str],
    public_key: str | None,
    guild_id: str,
    bot_id: str,
    dispatch: Callable[[dict[str, Any]], None],
    dispatch_reaction: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    import websockets

    async with websockets.connect(url, max_size=2**22) as ws:
        hello = json.loads(await ws.recv())
        interval = hello["d"]["heartbeat_interval"] / 1000.0
        seq: dict[str, int | None] = {"n": None}
        hb = asyncio.create_task(_heartbeat(ws, interval, lambda: seq["n"]))
        await ws.send(
            json.dumps(
                {
                    "op": 2,
                    "d": {
                        "token": get_token(),
                        "intents": GATEWAY_INTENTS,
                        "properties": {"os": "linux", "browser": "truesight-sophia"},
                    },
                }
            )
        )
        logger.info("Discord gateway READY handshake sent (guild=%s)", guild_id)
        try:
            async for raw in ws:
                event = json.loads(raw)
                if event.get("s") is not None:
                    seq["n"] = event["s"]
                etype = event.get("t")
                if etype == "MESSAGE_CREATE":
                    dispatch(event["d"])
                elif etype == "MESSAGE_REACTION_ADD" and dispatch_reaction is not None:
                    dispatch_reaction(event["d"])
        finally:
            hb.cancel()


async def _gateway_loop(
    allowed: set[str],
    public_key: str | None,
    guild_id: str,
    bot_id: str,
    dispatch: Callable[[dict[str, Any]], None],
    dispatch_reaction: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    backoff = 5.0
    while True:
        try:
            url = _gateway_url()
            await _gateway_once(
                url, allowed, public_key, guild_id, bot_id, dispatch, dispatch_reaction
            )
            logger.warning("Discord gateway closed; reconnecting in %.0fs", backoff)
        except Exception as exc:  # noqa: BLE001 -- reconnect on any failure
            logger.warning(
                "Discord gateway error: %s; reconnecting in %.0fs", exc, backoff
            )
        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, 60.0)
```

**Discord gateway facts this fix depends on (so PR0 doesn't need to look them up):**

- `HELLO` (op 10) carries `heartbeat_interval` — unchanged, still read the same way.
- `READY` (dispatch `t == "READY"`) payload (`event["d"]`) carries `session_id` (string) and,
  when present, `resume_gateway_url` (string, a dedicated endpoint recommended for the next
  reconnect — falls back to the normal `/gateway/bot` URL when absent).
- `RESUME` is op 6, payload `{"token": <bot token>, "session_id": <from READY>, "seq": <last
  seen "s">}`. Send it **instead of** `IDENTIFY` (op 2) when a prior `session_id` + `seq` are
  available.
- `RESUMED` (dispatch `t == "RESUMED"`) confirms a resume succeeded — no payload handling
  needed beyond logging.
- `INVALID_SESSION` (op 9) payload `d` is a bool: `true` = may still try to resume shortly,
  `false` = must discard the session and send a fresh `IDENTIFY`.
- Close codes **4007** (invalid seq) and **4009** (session timed out) also mean the session is
  not resumable — covered defensively via `ws.close_code` after the loop exits, in addition to
  the `op == 9` handling (Discord may signal either or both).
- `websockets.connect(...)` exposes `ws.close_code` (int or `None`) once the connection has
  closed; `None` means an abnormal closure with no close frame (exactly the "no close frame
  received or sent" case from the logs) — treated as resumable by default, per Discord's own
  reconnect guidance.

**Existing module-level pieces already in the file, unchanged by this fix:** `_GATEWAY_QUERY`,
`GATEWAY_INTENTS`, `get_token()`, `logger`. `_FATAL_CLOSE_CODES` (4004/4010/4011/4012/4013/4014)
is pre-existing dead code (defined, never referenced) — **out of scope for this PR**, do not
touch it.

**Dependency:** `websockets` package — already a dependency (imported in the current code);
no new dependency.

---

## 2. Sequenced plan — ONE PR (§5a: fits in a single turn, single file)

### PR0 — RESUME support + backoff reset-on-stable-connection

**Scope:** `truesight_autopilot/app/discord_adapter.py` only, replacing exactly the four
functions quoted in §1 (`_gateway_url` is unchanged and can be left alone; only
`_heartbeat`/`_gateway_once`/`_gateway_loop` change) — plus unit tests.

**2.1 — `_gateway_once` gains a `session: dict[str, Any]` parameter** (a plain dict the caller
owns and passes by reference across reconnects, persisting `session_id` / `seq` / `resume_url`):

- Connect to `session.get("resume_url") or url` (prefer the dedicated resume endpoint once we
  have one from a prior `READY`).
- Seed `seq["n"]` from `session.get("seq")` instead of always starting at `None`, so the
  heartbeat sends the right seq immediately even before the first new event arrives post-resume.
- After the `HELLO`, decide `IDENTIFY` vs `RESUME`: if `session.get("session_id")` and
  `session.get("seq") is not None`, send op 6 `RESUME` with that session_id/seq; otherwise send
  the existing op 2 `IDENTIFY` payload unchanged.
- In the dispatch loop: handle `op == 9` (`INVALID_SESSION`) — log it, and if `event.get("d")`
  is falsy, clear `session_id`/`seq`/`resume_url` from `session` (forces a fresh IDENTIFY next
  attempt), then `return` (let the outer loop reconnect). Handle `etype == "READY"` — store
  `session["session_id"]` and, if present, `session["resume_url"] = resume_gateway_url +
  _GATEWAY_QUERY`. Handle `etype == "RESUMED"` — just log it (session already up to date).
  Existing `MESSAGE_CREATE`/`MESSAGE_REACTION_ADD` handling is unchanged, just re-ordered under
  the new `etype` branches.
- After the `async for` loop (still inside the `async with`, right after the heartbeat-cancel
  `finally`): if `ws.close_code` is in `{4007, 4009}`, clear the same three session keys (belt
  and suspenders alongside the op-9 handling, since Discord may close directly on those codes
  without a preceding op 9).

**2.2 — `_gateway_loop` tracks connection duration and only resets backoff after a stable
connection** (this is the fix for bug #2 — see §0 for why "reset on every READY" is unsafe):

- Own the persistent `session: dict[str, Any] = {}` (created once, outside the `while True`,
  passed into every `_gateway_once` call) instead of `_gateway_once` creating fresh state each
  time.
- Record `connected_at = time.time()` immediately before each `_gateway_once` call.
- After `_gateway_once` returns or raises (existing try/except structure unchanged), add: `if
  time.time() - connected_at >= 60.0: backoff = 5.0` — i.e. only forgive the backoff when the
  connection that just ended had been up for at least 60 seconds. A connection that fails fast
  (bad token, repeated invalid-session, DNS failure) still gets the full exponential climb to
  60s, so this cannot create a reconnect storm or trip Discord's IDENTIFY rate limit — it only
  fixes the case the logs show: long-lived, healthy connections that eventually hit one idle
  timeout and then get needlessly penalized with a stale, climbed-up backoff for every
  disconnect thereafter.
- `time` is already imported at module level (used elsewhere in the file, e.g.
  `_binding_cache`) — no new import needed there. `websockets` stays a function-local import in
  `_gateway_once` (unchanged pattern); no need to import it in `_gateway_loop` since the close-
  code check lives inside `_gateway_once`, not the loop.

**2.3 — Tests** (new file `tests/test_discord_gateway_resume.py`, mirroring the existing
`tests/test_discord_adapter.py` conventions already in the repo):

- `_gateway_once` sends `IDENTIFY` when `session` is empty, and `RESUME` when `session` has
  `session_id` + `seq` populated (assert on the JSON sent to a fake/mock websocket).
- A `READY` event populates `session["session_id"]` (and `resume_url` when
  `resume_gateway_url` is present in the payload).
- An `INVALID_SESSION` (op 9) event with `d: false` clears `session`; with `d: true` leaves it
  intact.
- `_gateway_loop`'s backoff: simulate one `_gateway_once` call that raises after < 60s elapsed
  (backoff should climb, not reset) and one that raises after >= 60s elapsed (backoff should
  reset to 5.0 after that call) — this can mock `time.time()` or use a short real sleep with a
  lowered threshold constant injected for the test, whichever matches the existing test file's
  style for this module (check `tests/test_discord_adapter.py` for the established
  mocking pattern before choosing — this is a trivial in-repo read, not a cross-repo one, so it
  does not violate §5d).

**Self-cert:**

> ✅ Pre-flight Completeness: no execution unit requires reading a file/state not already
> captured in the pre-flight.

---

## 3. Resume tracker

**RESUME HERE → PR0** (the only unit in this plan).

| Unit | Advance | PR opened | Merged (human) | Deployed |
|------|---------|-----------|-----------------|----------|
| PR0 — Discord gateway RESUME + backoff reset | _(auto)_ | ☑ [#529](https://github.com/TrueSightDAO/truesight_autopilot/pull/529) | ☑ `1ca1dcc` (squash-merged 2026-10-10) | ☐ `gate:` always-stop (prod deploy / service restart) |

Both gates above are standing §5c always-stop rules (merge to `truesight_autopilot`'s default
branch; redeploying/restarting the live Discord adapter) — they apply regardless of
`Auto-start`, which only skips the *initial* wait before starting PR0 itself.

## 4. UAT

**UAT: n/a (covered by automated tests in PR0 §2.3)** — this is a backend connection-handling
fix with no human-facing surface. Operational verification after deploy: tail
`journalctl -u truesight-autopilot-discord.service -f` through the next natural gateway
disconnect and confirm a `Discord gateway RESUME sent` (or `RESUMED`) log line appears instead
of a cold `IDENTIFY`, and that the backoff value in subsequent `reconnecting in Ns` lines resets
to 5s after a long-lived connection rather than staying pinned at 60s.

## 5. Contribution reporting

After PR0 merges and deploys, report the DAO contribution per
`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md` crediting **"Sophia Truesight"** (the implementing
agent) — see `OPERATING_INSTRUCTIONS.md` §5b.
