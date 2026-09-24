# Sophia → temporarily run on Onaya's Claude (Haiku 4.5) token

**Status:** root-caused, plan drafted, not yet triggered.
**Owner:** Gary Teh · **Drafted by:** Claude Anthropic (Envoy/planner), 2026-09-24.
**Requested by:** Gary Teh: *"I wonder if we could swap Sophia for the time being to use
Claude's token currently being used by Onaya? Since that Claude token is underutilized right
now"* → *"And then once swapped update the Doc."*

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**
> §5c always-stop gate: this swap requires a **live production restart of Sophia's autopilot
> service** — the DAO's primary governor-facing chat surface.

---

## 1. Pre-flight (§5d completeness)

### 1.1 Onaya (Bionpact) is already live on Claude — confirmed, not assumed

`ssh bionpact` → `/opt/bionpact_autopilot/.env` (values redacted, keys confirmed present):
```
LLM_PROVIDER=litellm
LITELLM_MODEL=anthropic/claude-haiku-4-5
ANTHROPIC_API_KEY=sk-a...   (set)
```
This contradicts `PROJECT_INDEX.md`'s Bionpact row and `WORKSPACE_CONTEXT.md`, which both still
describe Onaya as running "Python, FastAPI, DeepSeek (same stack as truesight_autopilot)" — that
is **stale**; she's been moved to Claude Haiku 4.5 via litellm at some point without those docs
being updated. Also confirmed: `ANTHROPIC_API_KEY` has **zero entries** in
`credentials/API_CREDENTIALS_DOCUMENTATION.md` — this credential has never been documented at
all. Both gaps get closed in PR3 below.

### 1.2 Sophia's own code already supports this exact swap

`truesight_autopilot/app/config.py:498-516`:
```python
# LLM — DeepSeek default; Claude/others selectable via LLM_PROVIDER=litellm
# + LITELLM_MODEL. Claude was dropped for cost (2025) but the litellm path
# is provider-agnostic; set ANTHROPIC_API_KEY to re-enable it as an option.
llm_provider: str = os.getenv("LLM_PROVIDER", "deepseek")
...
anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
...
litellm_model: str = os.getenv("LITELLM_MODEL", "deepseek/deepseek-flash")
```
The swap is mechanically just: set `LLM_PROVIDER=litellm`, `LITELLM_MODEL=anthropic/claude-haiku-4-5`,
`ANTHROPIC_API_KEY=<Onaya's key>` in Sophia's live `.env`, then restart. No code change needed —
this is a config-only PR (or possibly no PR at all if done purely via the live `.env`, see §2).

### 1.3 The volume mismatch — the actual risk

Bionpact/Onaya is deliberately described (`agents/bionpact.json`, `PROJECT_INDEX.md`) as a
**"locked-down, private sibling instance... for the Ops team (Gary Teh + Elizabeth Wong)"** —
low, human-paced traffic. Sophia is the DAO's main public autopilot; earlier this session her
overnight load was measured at **~84.7M tokens/night**. Pointing Sophia's dramatically higher
volume at the same `ANTHROPIC_API_KEY` risks:
- Exhausting that key's rate limit / spend cap fast, which would also degrade or break Onaya's
  own service (shared key = shared limit).
- A surprise bill on whichever Anthropic account/workspace this key bills to — "underutilized"
  is a snapshot of Onaya's traffic alone, not a statement about what it can absorb from Sophia's
  load.
- **This is explicitly framed as temporary** ("for the time being") — likely tied to the
  DeepSeek-V4.1-Flash price increase surfaced earlier this session. Scope this as a bounded,
  monitored trial, not a permanent cutover, and keep the DeepSeek config recoverable (§2 rollback).

### 1.4 The restart must go through Sophia's own `deploy_autopilot()` — not a raw SSH restart

`truesight_autopilot/app/tools/ssh_tools.py:38-50` (`_SELF_RESTART_RE`) **explicitly blocks**
`systemctl restart/stop/kill/reload ... truesight-autopilot` (and `pkill`/`kill` on
`uvicorn`/`app.main`) over SSH, with the comment: *"Block raw self-restart of the autopilot: it
bypasses deploy_autopilot's idle-drain guard and bricks in-flight turns."* Confirmed live this
session: attempting a direct credential/config read on Sophia's box from this seat was itself
denied by the permission classifier ("Credential Exploration") — this swap cannot be done by
Envoy SSHing in and hand-editing + restarting.

The sanctioned path is Sophia's own `deploy_autopilot()` tool
(`truesight_autopilot/app/tools/deploy.py:660`), which she calls from within her own Telegram-
triggered turn. It has a documented idle-drain guard (`_other_threads_busy`) and a known
self-severance bug when a turn calls it on itself (`OPEN_FOLLOWUPS.md`, thread 27138, 2026-09-14)
— the verified mitigation there is a **detached `systemd-run --on-active=60`** invocation of the
same sanctioned deploy path, run past the calling turn's own boundary. PR2 below should use that
same verified mitigation, not a naive inline call.

### 1.5 `.env` vs vault

`DEEPSEEK_API_KEY` already lives in plain `truesight_autopilot/.env` on Sophia's box (per this
box's own `CLAUDE.md` credentials table) — the vault (`vault.json.enc`) is used for a narrower
set of secrets (e.g. Discord bot token, SSH keys), not LLM provider keys. `ANTHROPIC_API_KEY`
joining `.env` alongside `DEEPSEEK_API_KEY` matches the existing convention; no vault migration
needed.

---

## 2. Authorization envelope (§5e)

| Surface | Envelope |
|---|---|
| Sophia's `.env` — add `ANTHROPIC_API_KEY`, flip `LLM_PROVIDER`/`LITELLM_MODEL` | Pre-authorized by this request — but the **restart that makes it live** is the gate below. |
| **Restarting `truesight-autopilot` to pick up the new provider** | **Always-stop gate (§5c: production deploy).** Must run via Sophia's own `deploy_autopilot()` (detached, per §1.4), not a raw restart. Confirm current in-flight-thread count is low before triggering, per standing practice (`sophia_manual_restart_freezes_threads`). |
| **Rollback** | Pre-authorized, standing: revert `.env` to `LLM_PROVIDER=deepseek` / `DEEPSEEK_MODEL=deepseek-flash` (remove or leave `ANTHROPIC_API_KEY` unset in provider selection) and redeploy the same sanctioned way, any time this trial underperforms or the shared key gets rate-limited. |
| Updating `API_CREDENTIALS_DOCUMENTATION.md` / `PROJECT_INDEX.md` / `WORKSPACE_CONTEXT.md` (PR3) | Pre-authorized — docs only. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Set `LLM_PROVIDER=litellm`, `LITELLM_MODEL=anthropic/claude-haiku-4-5`, `ANTHROPIC_API_KEY=<Onaya's key, copied>` in Sophia's live `.env` on the autopilot box. No code change — `.env` edit only, not yet live (service not restarted). Confirm the previous `DEEPSEEK_*` values are still present/commented so rollback is a one-line flip, not a reconstruction. | `truesight_autopilot` (live `.env`, not a git commit — this file is gitignored per standing convention) |
| **PR2** | **Deploy** — trigger Sophia to run her own `deploy_autopilot()` (detached `systemd-run`, per §1.4's verified mitigation) so the new provider takes effect without severing in-flight turns. **Live verification**: confirm via `journalctl`'s request log that a real turn now dispatches through `litellm`/`anthropic` (not `deepseek`), and that Sophia produces a coherent response — not just that the process restarted clean. Watch for rate-limit errors from the shared key over the following ~30–60 min (this is the actual test of "underutilized"). **§2 always-stop gate — needs explicit `go` before triggering.** | `truesight_autopilot` (deploy) |
| **PR3** | Update docs: (a) `API_CREDENTIALS_DOCUMENTATION.md` — add the `ANTHROPIC_API_KEY` entry (currently entirely undocumented) noting it's now shared between Onaya and Sophia (temporary); (b) fix the stale Bionpact stack description in `PROJECT_INDEX.md` §Bionpact row and `WORKSPACE_CONTEXT.md` (both still say "DeepSeek (same stack)"); (c) note in `config.py`'s own comment (`truesight_autopilot/app/config.py:499-500`) that the litellm/Claude path is live again as of this swap, temporarily, superseding "Claude was dropped for cost (2025)." | `agentic_ai_context`, `truesight_autopilot` |
| **RUN/UAT** | Folded into PR2 — see §5. | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (the `.env` edit). Fresh roadmap — nothing started.
>
> No open governor decisions block PR1. PR2's deploy trigger is the standing always-stop gate —
> ask once before triggering, not per-thread.

| Unit | Done | Contribution reported |
|---|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ |
| PR1 (`.env` swap, not yet live) | ☐ | ☐ |
| PR2 (deploy + live verification) | ☐ | ☐ |
| PR3 (doc updates) | ☐ | ☐ |

---

## 5. UAT

| Step | What to expect | Acceptance criterion |
|---|---|---|
| 1 | PR2's `journalctl` check | Request log shows `litellm`/`anthropic` dispatch, not `deepseek` |
| 2 | A real governor message in an active Telegram thread, post-restart | Coherent response; no tool-call regressions vs. DeepSeek-flash behavior |
| 3 | ~30-60 min watch window | No rate-limit / 429 errors from the shared `ANTHROPIC_API_KEY`; Onaya's own responsiveness unaffected |
| 4 | If step 3 fails | Roll back per §2 immediately — this is a monitored trial, not a committed migration |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each completed unit via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first).
