# Sophia — Multi-Tenant Governance, Identity & Vault — Execution Roadmap

**Status as of 2026-06-11:** designed (this conversation) — ready to phase + hand off
**Repo under change:** `truesight_autopilot` (Sophia's OWN codebase) + a new skeleton context repo (Phase 4)
**Designed by:** Gary Teh + Claude · **Implemented by:** Sophia (autopilot), human-merged

> ⛔ **Own-repo gate (every phase):** Sophia **opens PRs only and NEVER self-merges
> `truesight_autopilot` PRs** — a human reviews + merges. Every commit carries the
> `Generated-by: Sophia (TrueSight Autopilot)` trailer.

> **RESUME HERE (vault-first order, 2026-06-11):** Phase 0, PR0.1 — `app/policy.py` identity
> resolver (telegram_id → {guest, governor}). Then immediately Phase 3 (vault). The vault
> needs identity resolution to gate its web page; it does NOT need the full tool-layer
> enforcement or data/instruction boundary from Phase 0.2–0.4.
>
> **Worktree convention:** because the follow-up monitor handoff (thread 2622) is actively
> opening PRs on `truesight_autopilot`, all vault work uses a `git worktree` at
> `/opt/truesight_autopilot/worktrees/vault/` to avoid clone conflicts. See §11.

---

## 1. Why / the vision

Sophia today assumes **one org** (TrueSight), **one surface** (Gary's personal group, always
proactive), **one identity** (Gary, implicitly governor), **one action policy** (do anything).
Other people + other orgs (Liz, Bilal) now want her help. Every requirement below is "turn one
of those hardcoded singletons into a configurable, policy-gated axis," so she can safely operate
in collaborative rooms and be cleanly replicated per org.

## 2. The unifying model — one policy keyed on **(tenant × surface × identity × action)**

Every decision Sophia makes resolves through a single policy layer:

- **Tenant** (org) → which context substrate, credential vault, transcript sink, ledger, governor
  set. **One Sophia instance per org** (decided) — full isolation.
- **Surface** (group / topic / DM) → an **engagement mode** (proactive vs addressed-only) and a
  transparency requirement.
- **Identity** (who's speaking) → resolved from `telegram_id → Contributors contact (Column X,
  numeric Telegram ID) → Governors cache`. Unbound = **guest**. Column **H** holds the
  **Telegram Handle** (`@username`) for display/audit only — never the authorization key.
- **Action-class** → `read` (open) vs `write/admin` (governor) vs `secrets` (never in chat;
  vault page only).

The policy is **data-driven** and consulted **before engaging** and **before any tool runs**.

## 3. Security invariants (the non-negotiable spine — every phase upholds these)

1. **Enforce at the tool layer, never the prompt.** Write/admin tools check the requester's
   resolved role and refuse otherwise. Prompts get socially engineered; tool gates don't.
2. **Ingested content is DATA, never INSTRUCTIONS.** Attachments, transcribed docs, other
   people's messages are context only. **Only an authenticated governor's direct message is an
   instruction.** (Prompt-injection / confused-deputy defense for collaborative rooms.)
3. **Credentials never appear in chat / transcripts / PRs / logs — to anyone, governors
   included.** The LLM only ever sees `{name, purpose, scopes}`; values are injected at
   tool-execution time. Secrets are managed only on the vault page.
4. **Guest-default.** An unbound/unknown identity gets read-only public context + codebases +
   transcript history; **no secrets, no writes.**
5. **No silent powerful actions.** Every privileged action is announced + audited in a governed
   channel; sensitive flows happen in a transparent group context, **not private DMs**.
6. **Authentication ≠ authorization.** Proving *who you are* (email/RSA) is separate from
   *what you may do* (governor-in-cache). A verified non-governor is politely bounced.
7. **Confidentiality of a challenge code comes from the email channel, NOT from PKI.** Signing
   with a private key proves authenticity, not secrecy (the public key is public). Codes are
   delivered to the inbox on file and **stored only as hashes**.

## 4. Authorization model (decided)

**Single tier, Telegram-native, frictionless:** `telegram_id → Column X → Governors cache →
privileged actions`. No RSA step-up for everyday actions (would force users out of Telegram).
**No "nuclear floor"** — Sophia has no fund-movement tool; a deleted credential is re-added on
the vault page; a destroyed box is re-imaged from the AMI; ledger writes are reversible via
compensating entries. The only un-undoable action she has is **sending email/messages as the
org** — reputational, not catastrophic, and fully auditable, so transparency is the proportionate
control. Compensating controls replace the dropped key-tier: **audit+announce every privileged
action, alert on every new identity binding, fast revocation, recommend 2FA** (Telegram + email).

The **vault page** is a *separate surface with a stronger gate* (email→RSA auth, then
governor-cache) — credential mutation was never a Telegram action.

---

## 5. Pre-flight checklist

- [ ] Confirm the Governors cache (`governor_registry`) is the single source of truth for
      governor status, keyed by an identifier reachable from `Contributors contact information`.
- [ ] Confirm `Contributors contact information` has a usable **Column X** for the numeric
      telegram_id and **Column H** for the **Telegram Handle** (`@username`), and
      `Contributors Digital Signatures` has **Column D** (verified) + **Column
      G** (challenge artifact) + a **Verification Key Consumed** flag.
- [ ] Confirm the existing `[EMAIL REGISTERED EVENT]`/`[EMAIL VERIFICATION EVENT]` plumbing can
      be reused for code mint + consume (adapt link → paste-back code).
- [ ] Confirm an email-send path for the challenge (Edgar/GAS mailer or autopilot Gmail), with a
      per-tenant sender identity.
- [ ] Confirm the per-topic role/session metadata can carry an **engagement mode** alongside role.
- [ ] Reaffirm the own-repo gate (open PRs, never self-merge; `Generated-by` trailer).

---

## 6. Phased roadmap (vault-first order — Gary decision 2026-06-11)

> **Why vault-first:** the credential vault is universally useful regardless of multi-tenant
> governance decisions (Bilal conversation, Liz's interest). It secures credentials for the
> Gary–Sophia collaboration immediately. Phase 0.1 (identity resolver) is the minimal
> dependency the vault needs — it does NOT need the full tool-layer enforcement or
> data/instruction boundary.

### Step A — Phase 0.1: Identity resolver *(minimal dependency for vault)*
| PR | Description |
|----|-------------|
| 0.1 | `app/policy.py` — resolve `(tenant, surface, identity, action) → allow/deny`. Identity resolver: `telegram_id → Column X → Governors cache → {guest, governor}`. Unbound = guest. **Only this sub-PR of Phase 0 — the rest of Phase 0 is deferred.** |

### Step B — Phase 3: Credential vault (box-local) *(immediate value)*
| PR | Description |
|----|-------------|
| 3.1 | **Vault store** on the box: encrypted at rest; entries `{name, purpose, scopes, version, value(enc), created_by, created_at}`. **Never-overwrite**; **delete allowed**; **versioning** for safe rotation. Audit log of add/delete (RSA-signed actor). |
| 3.2 | **Reference-by-name / inject-at-execution**: tools request a credential by name; value injected at call time; the LLM/transcript/logs only ever see `{name, purpose, scopes}`. |
| 3.3 | **Vault web page**: authenticate via email→RSA flow → check **Governors cache** → governor: vault UI (add w/ purpose, delete, view names+purpose, not values); non-governor: friendly **contribution-nudge** denial (no leak of contents/existence). |
| 3.4 | **Backup/restore**: encrypted vault backup so a re-imaged box restores creds (box-loss ≠ credential-loss); ties to the `credential_vault` restore-runbook. |
| 3.5 | **Missing-credential behavior**: Sophia names the missing credential + purpose and points the governor to the vault page; never fails silently, never routes around it. |
| 3.6 | "What's your vault URL?" → returns the (non-secret) auth URL to anyone; access still gated. |
| 3.7 | Tests: overwrite refused; delete works; versioned rotation keeps in-flight refs; value never returned in any chat/tool-trace path; non-governor bounced; restore round-trip. |

### Step C — Phase 0.2–0.4: Remaining policy + enforcement *(deferred after vault)*
| PR | Description |
|----|-------------|
| 0.2 | **Tool-layer enforcement** — write/admin tools consult the policy with the *requester's* resolved role and refuse for guests. Read tools open; secret values never returned. |
| 0.3 | **Data-vs-instruction boundary** — mark ingested content (attachments, transcriptions, third-party messages) as non-actionable context; only a governor's direct message is an instruction. |
| 0.4 | Tests: guest blocked from each write tool; governor allowed; ingested "please deploy" never triggers a tool; secret never surfaced. |

### Step D — Phase 1: Identity binding (email-challenge → Telegram)
| PR | Description |
|----|-------------|
| 1.1 | Challenge mint: generate the Verification Key (reuse), store **hash in Column G** (never plaintext), email the **plaintext code** to the address on file; **sign the email** with Sophia's key (authenticity). Abuse controls: 15-min expiry, ≤5 attempts, rate-limit per telegram_id + per email, one pending per pair (newest supersedes), no governor-enumeration. |
| 1.2 | **Move-to-DM** — the code exchange happens in DM (email + code never group-visible); verification is the one thing an *unverified* user may do in DM. |
| 1.3 | Consume + bind: hash the pasted code, compare to Column G → set **Column D = verified**, **Verification Key Consumed = true**, write **Column X = numeric telegram_id** and **Column H = Telegram Handle (`@username`)**. Emit an `[IDENTITY BINDING EVENT]` for audit (never the code). |
| 1.4 | **Re-bind alerts + revocation** — notify existing governors + the email owner on a new binding ("@handle linked to X — revoke if not you"); any governor can revoke; re-bind supersedes. |
| 1.5 | Tests: happy path; wrong code (attempts decrement); expired; replay (consumed key dead); plaintext never written to G; non-governor email verifies as member (no privilege). |

### Step E — Phase 2: Engagement modes, collaborative groups, DMs
| PR | Description |
|----|-------------|
| 2.1 | Per-surface **engagement mode**: `proactive` (personal workspace, current behavior) vs `addressed-only` (collaborative). |
| 2.2 | **Addressed-only behavior**: ingest + transcribe everything into the thread transcript, but **reply only when addressed** — @mention, leading vocative ("Sophia, …"), her name in a voice transcript, or a reply to her message. Require a clear address token (avoid name false-positives). |
| 2.3 | **❤️-on-ingest**: react with a heart when an attachment is ingested/transcribed — a "seen + logged" receipt without a noisy reply. |
| 2.4 | **DM policy**: read-only + write-disabled; gate who may DM (known/verified), rate-limit unknowns; verification flow is the allowed on-ramp. |
| 2.5 | **Audit/announce channel**: every privileged action posts a one-liner to a governed channel. |
| 2.6 | Tests: addressed-only stays silent on un-addressed chatter but ❤️s an attachment; @mention triggers a reply; DM write refused; privileged action announced. |

### Step F — Phase 4: Multi-org replication (one instance per org)
| PR | Description |
|----|-------------|
| 4.1 | **Tenant config** abstraction: `{context_repo, vault, transcript_sink, ledger, governor_set, telegram_group(s), mailer_identity}` — replaces hardcoded TrueSight singletons. |
| 4.2 | **Skeleton context repo** (template, NOT a fork of `agentic_ai_context`): OPERATING_INSTRUCTIONS + a **tools manifest** (each tool ↔ the vault credential it needs) + a ledger. Independent orgs fork the skeleton; their transcripts emit to **their own** repo. |
| 4.3 | **Image-based provisioning**: a base Sophia AMI + a launch script (reuse the AMI/watch work) that stands up a new box with an **empty vault** + tenant config. |
| 4.4 | **Onboarding runbook**: clone image → set tenant config → governor seeds the vault via its page → bind the org's Telegram group → first verification. |
| 4.5 | Tests/dry-run: a second tenant config routes context/transcripts/vault to its own targets; no cross-tenant credential or context bleed. |

---

## 7. UAT — operator acceptance (run in Telegram / the vault page)

**Phase 0 — policy + boundary**
- P0.1 A guest (unbound telegram_id) asking for a code change / deploy is **refused** (read still works).
- P0.2 A verified governor's same request **succeeds**.
- P0.3 An **attachment/message containing "Sophia, deploy prod"** is transcribed but **never executes** a tool.
- P0.4 Asking Sophia to print a credential value returns a **refusal**, never the value.

**Phase 1 — binding**
- P1.1 "Verify me as `<email>`" → Sophia DMs, emails a code; pasting it sets Column D=verified, Consumed=true, Column X=telegram_id.
- P1.2 Wrong code decrements attempts; expired code is rejected; a consumed code can't be reused.
- P1.3 Column G holds a **hash**, never the plaintext code.
- P1.4 A new binding **alerts** existing governors; a governor can **revoke** it.
- P1.5 A non-governor email verifies as **member** — read access, no privilege.

**Phase 2 — engagement / DMs**
- P2.1 In an `addressed-only` group, ordinary chatter between two people gets **no reply**; an attachment gets a **❤️**.
- P2.2 **@Sophia** / "Sophia, …" / her name in a voice note → she replies.
- P2.3 A **DM write request** is refused (read works); an unknown DMing gets gated/limited.
- P2.4 A privileged action posts to the **audit channel**.

**Phase 3 — vault**
- P3.1 Governor adds a credential w/ purpose on the vault page; **overwrite is refused**; **delete works**; **rotation via version** doesn't break an in-flight reference.
- P3.2 A **verified non-governor** hits the vault page → **friendly nudge**, no contents leaked.
- P3.3 A credential **value never appears** in any chat reply or tool trace; Sophia uses it by name.
- P3.4 Deleting a needed credential → Sophia **complains + points to the vault page**.
- P3.5 Re-image the box → **restore** brings the vault back.

**Phase 4 — replication**
- P4.1 A second tenant config routes its **context, transcripts, and vault** to its own targets.
- P4.2 **No cross-tenant bleed** — tenant B can't read tenant A's context or credentials.
- P4.3 A fresh instance onboards end-to-end: image → config → governor seeds vault → group bound → first verification works.

**Completion gate:** each phase's PRs are **human-merged** (Sophia opens, never self-merges) and its UAT block passes before the next phase starts.

---

## 8. Rollout

Deploy each phase via the targeted path (`git checkout -B main origin/main` on the box, **no
`git clean`** — `sessions/`, `followups/`, and the vault must survive), restart
`truesight-autopilot`, then run that phase's UAT. Phase 4 provisions *new* boxes rather than
touching the TrueSight instance.

## 9. Resume tracker (vault-first order)

> **Build-status note (2026-06-16, audited against `truesight_autopilot@main 0f9d0a9`):** the
> checkboxes below predate the code. Actual state in the repo:
> - **Step A — Phase 0.1 (identity resolver):** `app/policy.py` exists and is wired into
>   `main.py`, **but** resolves governors via an **env allowlist + display-name match**, not yet
>   the `telegram_id → Column X → Governors cache` sheet lookup (TODO comment in `policy.py`).
> - **Step B — Phase 3 (vault):** `app/vault.py` + `vault_routes` + vault UI templates shipped
>   and merged (durability fixes through PR #214, 2026-06-15). Substantially done.
> - **Step D — Phase 1 (identity binding):** `app/identity_binding.py` fully built **with tests**
>   (mint/verify/bind/revoke/status), **but not wired into the Telegram adapter** — no `/verify`
>   command, no callers. Column mapping corrected to **X=ID / H=Handle** in PR #221.
> - **Step E — Phase 2 (engagement modes):** `app/engagement.py` shipped with tests.
> - **Topic-role architecture** (`AUTOPILOT_TOPIC_ROLE_ARCHITECTURE.md`): `app/roles.py` shipped,
>   wired into `main.py` + `telegram_adapter.py` (role menu, tool gating, per-topic role). That
>   doc's resume tracker is also stale — PR1 is effectively done.
>
> Net: the *modules* for Phases 0.1/1/2/3 + topic-roles exist; the *remaining glue* is the
> Column-X read-side resolver in `policy.py` and exposing identity-binding as a Telegram flow.

| Step | PRs opened | Merged (human) | Deployed | UAT |
|------|-----------|----------------|----------|-----|
| **A — Phase 0.1: Identity resolver** | ☐ | ☐ | ☐ | P0.1 |
| **B — Phase 3: Credential vault** | ☐ | ☐ | ☐ | P3.1–P3.7 |
| **C — Phase 0.2–0.4: Remaining policy** | ☐ | ☐ | ☐ | P0.2–P0.4 |
| **D — Phase 1: Identity binding** | ☐ | ☐ | ☐ | P1.1–P1.5 |
| **E — Phase 2: Engagement modes** | ☐ | ☐ | ☐ | P2.1–P2.4 |
| **F — Phase 4: Multi-org replication** | ☐ | ☐ | ☐ | P4.1–P4.3 |

> **RESUME HERE (vault-first):** Step A — Phase 0.1 `app/policy.py` (identity resolver:
> `telegram_id → Column X → Governors cache → {guest, governor}`). Then Step B — Phase 3
> (credential vault). Open PRs via git worktree; **do not self-merge** (human reviews).
> Report progress in this handoff topic (thread 2744).

---

## 11. Worktree convention (parallel handoff threads)

Because the follow-up monitor handoff (thread 2622) is actively opening PRs on
`truesight_autopilot`, all vault/governance work uses a **git worktree** to avoid clone
conflicts:

```bash
# Set up the worktree (one-time)
cd /opt/truesight_autopilot
git worktree add /opt/truesight_autopilot/worktrees/vault/ main

# Work in it
cd /opt/truesight_autopilot/worktrees/vault/
git checkout -b feature/vault-store
# ... make changes, commit, push, open PR ...

# Clean up when done
git worktree remove /opt/truesight_autopilot/worktrees/vault/
```

The worktree shares the same `.git` directory as the main clone, so branches, remotes, and
config are identical. The working tree is independent — changes in one don't affect the other
until you `git merge` or `git pull`.

**Rule:** every vault/governance PR opened from this thread (2744) uses the worktree path.
The follow-up monitor thread (2622) uses the main clone path. Never the twain shall conflict.

---

## 13. Safe deploy orchestration — idle-check watcher

**Context (Gary, 2026-06-11 voice thread 2744):** deploying new code while other
active tracks (follow-up monitor in thread 2622, active Telegram sessions, long-running
tool calls) are mid-execution causes SIGTERM and lost work. The deploy must wait until
all tracks are idle.

**Anti-pattern to avoid:** a long-running loop that never idles (e.g. a background
watcher that polls every 30s) should not block deployment forever. Each track gets a
max expected duration; if exceeded, the track is treated as stuck/crashed and the
deploy proceeds.

### Track registry

Each background process registers itself in a shared state file
(`data/active_tracks.json`):

```json
{
  "version": 1,
  "tracks": [
    {
      "id": "followup-monitor",
      "label": "Follow-up monitor (thread 2622)",
      "started_at": "2026-06-11T23:00:00Z",
      "last_heartbeat": "2026-06-11T23:05:00Z",
      "expected_max_duration_s": 30,
      "status": "running"
    },
    {
      "id": "email-poller",
      "label": "Email poller",
      "started_at": "2026-06-11T22:00:00Z",
      "last_heartbeat": "2026-06-11T23:05:00Z",
      "expected_max_duration_s": 15,
      "status": "running"
    },
    {
      "id": "telegram:2744",
      "label": "Chat session (thread 2744)",
      "started_at": "2026-06-11T23:04:00Z",
      "last_heartbeat": "2026-06-11T23:05:00Z",
      "expected_max_duration_s": 120,
      "status": "running"
    }
  ]
}
```

### Deploy watcher logic

```python
def can_deploy() -> bool:
    """Check if it's safe to restart the service."""
    tracks = load_active_tracks()
    now = time.time()
    
    for track in tracks:
        if track["status"] != "running":
            continue
        
        elapsed = now - parse_iso(track["last_heartbeat"])
        max_duration = track["expected_max_duration_s"]
        
        if elapsed < max_duration:
            # Track is actively running — wait
            logger.info("Deploy blocked: %s is active (%ds elapsed, %ds max)",
                        track["id"], elapsed, max_duration)
            return False
        
        # Track exceeded its max duration — treat as stuck/crashed
        logger.warning("Deploy proceeding: %s exceeded max duration (%ds > %ds)",
                       track["id"], elapsed, max_duration)
    
    return True
```

### Heartbeat mechanism

Each long-running loop writes its heartbeat to the shared state file on every
iteration. The deploy watcher reads the file, not the live process state — so
a crashed process with a stale heartbeat is detected and doesn't block deployment.

### Manual override

On the vault web page (Phase 3.3), the System Status panel shows:
- Active tracks with their IDs and status
- Whether a deploy is pending
- A **"Deploy now"** button that bypasses the idle check entirely

### Timeout table

| Track | Expected max duration | Notes |
|-------|----------------------|-------|
| Telegram chat turn | 120 s | LLM call + tool execution |
| Follow-up monitor check | 30 s | Probe + state write |
| Email poller poll | 15 s | Gmail query + dispatch |
| SSH / git operation | 60 s | Clone, push, deploy |
| AWS watcher poll | 10 s | Status check |
| Daily briefing | 60 s | LLM generation |

### Implementation (PR)

1. `app/deploy_watcher.py` — shared state file reader + `can_deploy()` logic
2. Wire heartbeat writes into: `followup_loop`, `email_poller`, `telegram_adapter`
   (per-session), `watch_runner`, `daily_briefing`
3. Add `/vault/api/system-status` endpoint to vault_routes.py
4. Add "System Status" panel to vault web page showing active tracks + deploy button
5. Modify `deploy_autopilot()` to call `can_deploy()` before restarting
6. Tests: can_deploy blocks when track is active; proceeds when idle; proceeds when
   track exceeded timeout; manual override bypasses check

---

## 14. Dependency notes / cross-references

- Builds on the shipped **per-topic concurrency** (lock/queue/ack) and **watch-and-notify** work
  (the AMI primitive in Phase 4.3), and the **durable follow-up monitor** (`SOPHIA_FOLLOWUP_MONITOR_PLAN.md`).
- Phase 1 reuses the `dao_client` / Edgar email-verification plumbing.
- Phase 3 backup ties to `credential_vault` (restore runbook).
- Box hardening (Cypher-Defense / EC2-SG remediation) becomes **load-bearing** once the vault
  holds real secrets — the box is the crown jewels.
