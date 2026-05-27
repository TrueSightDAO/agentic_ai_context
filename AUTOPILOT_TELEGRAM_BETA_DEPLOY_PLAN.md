# Autopilot Telegram interface + dapp beta/prod split + Tier-2 beta auto-deploy

**Status:** PLANNING — roadmap committed, implementation not started.
**Owner:** Gary Teh (+ AI sessions)
**Created:** 2026-05-26
**Convention:** This is the tracked roadmap required by `OPERATING_INSTRUCTIONS.md` §5 before any implementation code. Keep the **Resume tracker** current as each unit lands. Reference example: `EDGAR_DAO_EXTRACTION_PLAN.md`.

---

## 1. Goal (why this exists)

Get Gary **out of babysitting a Claude/OpenCode CLI**. The end state:

1. Gary talks to a private assistant over **Telegram** while on the move — locked to him alone, with **multiple parallel contexts** (one per topic).
2. The assistant (**`truesight_autopilot`**) implements the change, runs CI, and **lands it on a beta environment** automatically once CI is green.
3. Gary's only touchpoint is **the running beta site** + a Telegram "it's live at &lt;url&gt;" message. He promotes to **prod manually**.

This replaces the current flow (draft PR → Gary reviews code → merges) and the fragile DApp `chat.html` SSE interface.

**Decision already made:** the backbone is `truesight_autopilot`, **not** OpenClaw. OpenClaw (`opencolin/openclaw-nebius`) is itself a coding CLI to drive — adopting it would not remove the babysitting. Autopilot is a persistent service that already has the agentic loop, repo write + `merge_pr()`, DAO identity, Edgar contribution logging, and AWS/Gmail monitoring. See conversation 2026-05-26.

---

## 2. Decisions locked

| Decision | Value | Notes |
|---|---|---|
| Backbone | `truesight_autopilot` | OpenClaw rejected (it's a CLI to babysit). |
| Interface | **Telegram** | Not Slack. Single-user lockdown is trivial; no workspace overhead; topics = contexts. |
| Telegram bot | **New dedicated bot** | Do NOT reuse the existing ledger bot — see §6 foot-gun. |
| Beta subdomain | **`beta.dapp.truesight.me`** | Confirmed 2026-05-26. Matches the `beta.` convention (`beta.truesight.me`, `beta.agroverse.shop`). |
| dapp repo shape | `dapp` (prod) → eventually `dapp_prod`; new **`dapp_beta`** | Beta-first sequencing; prod rename is deferred cosmetic cleanup. |
| Backend chat endpoint | **`/chat-blocking`** | Avoids the SSE fragility that breaks `chat.html` on mobile. |
| Multi-context | Telegram **forum topics** → `X-Session-Id` | Reuses autopilot's existing session model (`/sessions`, `/sessions/new`). |
| Identity | Reuse **Telegram-user → DAO-contributor** mapping | Ties systems at identity layer, not bot layer. |
| Beta gate | **Tier 1 → Tier 2** | Start one-tap "ship to beta?"; graduate per-repo to auto-merge-on-green-CI as trust builds. |
| Prod gate | **Always manual** | Promotion to `*_prod` forks is never automated. |

---

## 3. Pre-flight checklist (confirm BEFORE coding)

Operator-gated — Gary or a human must resolve these; an AI session cannot self-serve them:

- [ ] **DNS** — who manages `truesight.me` DNS (Namecheap per `agroverse_shop` creds?). Add `CNAME beta.dapp.truesight.me → truesightdao.github.io`.
- [ ] **BotFather** — create a dedicated bot (e.g. `@truesight_autopilot_bot`); capture the token. Decide storage: `truesight_autopilot/.env` (`TELEGRAM_AUTOPILOT_BOT_TOKEN`).
- [ ] **Gary's Telegram user_id** — the single allowlisted numeric ID (get from `@userinfobot` or the webhook payload).
- [ ] **GitHub org auth** — confirm `gh` can create repos under `TrueSightDAO` (for `dapp_beta`).
- [ ] **Adapter host** — same EC2 (`100.52.234.163`) as a second systemd unit, or a separate process? (Recommend: second systemd unit on the same box; it already runs the FastAPI service.)
- [ ] **Backend identity** — confirm whether autopilot calls `/chat-blocking` with Gary's governor key or a dedicated service identity. Check `truesight_autopilot/.env` (`EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY`).
- [ ] **Prod safety state** — verify `disable_governor_check` is **false** and `DRY_RUN` is intentional in the EC2 `.env`.

Decisions already locked (no action): subdomain name, separate bot, Telegram over Slack, autopilot backbone.

---

## 4. Track A — dapp beta/prod split

Goal: a safe beta landing zone for autopilot, leaving production untouched.

| Unit | Work | Shippable result |
|---|---|---|
| **A0** | Pre-flight: DNS record for `beta.dapp.truesight.me`; confirm Pages is enabled. | DNS resolves; CNAME ready. |
| **A1** | Create **`dapp_beta`** repo as a copy of `dapp`. Add `CNAME=beta.dapp.truesight.me`. Enable GitHub Pages. **Port dapp's CI** (`.github/workflows/ci.yml` — Node unit + Playwright) so "green CI" is meaningful. | `beta.dapp.truesight.me` serves the dapp; CI runs on push. |
| **A2** | Wire autopilot: add `dapp_beta` to `allowed_repos` (`app/config.py`) and to the **beta-merge allowlist** (§5/B5). `dapp` (prod) stays manual-promote. | Autopilot may open/merge PRs on `dapp_beta` only. |
| **A3** *(deferred)* | Stand up the prod side **matching the verified org convention: prod is a FORK of the beta base** (confirmed 2026-05-27 — `truesight_me_prod` forks `truesight_me_beta`; `agroverse_shop_prod` forks `agroverse_shop_beta`; the `_beta` repos are non-forks). Keep `dapp_beta` as the non-fork base (already correct); make the prod repo a **fork of `dapp_beta`** and promote beta→prod via `gh repo sync`. Incumbent `dapp` is the live prod (non-fork) on `dapp.truesight.me`; decide between (a) leave `dapp` as prod and `gh repo sync --source dapp_beta` (they share history) or (b) introduce `dapp_prod` as a true fork and migrate the prod CNAME. Either way: clean up the **91 `TrueSightDAO/dapp` refs**, **re-verify the Pages custom domain**, and **preserve each repo's CNAME** (NO `gh repo sync --force` — §6). **Do NOT make the beta repo a fork** — forks disable Actions by default (breaks the green-CI gate) and `gh repo sync` would flow the wrong way. | Convention-consistent fork-based prod; CNAME-safe promotion. |

**Do A3 last**, after the beta flow is proven. A1–A2 are additive and zero-risk to the live site.

---

## 5. Track B — autopilot Telegram interface + beta-deploy gate

Goal: the private, reliable, multi-context Telegram front-end that lands work on beta.

| Unit | Work | Shippable result |
|---|---|---|
| **B1** | Telegram adapter (new bot) → autopilot **`/chat-blocking`**. **Single-user allowlist**: respond only to Gary's `user_id`; silently drop all others. New systemd unit on EC2. | Gary (only) can chat with autopilot over Telegram; reliable (no SSE). |
| **B2** | **Topic ↔ session** mapping: enable forum topics in a private group; map `message_thread_id` → `X-Session-Id`. Reuse `/sessions`, `/sessions/new`, `/session`. | Each topic is an independent persistent context. |
| **B3** | **Identity reuse**: resolve Telegram `user_id` → DAO contributor → governor public key (from the existing mapping) for the backend call, instead of a hardcoded key. | Lockdown keyed off DAO identity; future-proof if other governors are added later. |
| **B4** | **File/photo passthrough** for tools that need it (`qr_scanner`, `upload_file_to_github`, `/chat/upload`). | Can send a photo/file from the phone into a chat. |
| **B5** | **Beta-deploy gate — Tier 1**: agent prepares + runs CI; posts "Ready — ship to beta?" with an inline button. On tap, call existing `github_client.merge_pr()` **into beta repos only**, **after CI is green**. Then **verify** (Pages build succeeded + URL returns 200) and **report the beta URL** in Telegram. | One-tap ship-to-beta; Gary's touchpoint is the beta URL. |
| **B6** | **Graduate to Tier 2** per-repo: auto-merge-on-green-CI (no tap). Add auto-rollback on red and **escalate-to-Telegram-when-uncertain**. Prod promotion remains a manual command. | Fully hands-off to beta for trusted repos. |

---

## 6. Risks & foot-guns (read before each unit)

1. **CNAME divergence (prior incident).** `dapp_beta` CNAME = `beta.dapp.truesight.me`; `dapp_prod` CNAME = `dapp.truesight.me`. Promotion must **never** `gh repo sync --force` — it overwrites prod's CNAME with beta's and kills the production domain (this broke `truesight.me` before). Exclude CNAME from any sync, or promote via a PR that doesn't touch it. (See `feedback_truesight_me_cname_divergence`.)
2. **Telegram single-webhook constraint.** A bot has exactly one update consumer. The existing ledger bot's webhook already points at GAS (`tokenomics/.../webhooks/telegram_webhook_listener.gs`) and drives critical ledger ingestion + TDG scoring. **Use a separate bot** for autopilot — do not repoint the ledger bot.
3. **Agent-brain quality is the real Tier-2 gate.** Draft-PR review is forgiving; auto-merge-on-green is not. A weak loop will get stuck or ship subtly-wrong-but-CI-green changes. Mitigations: CI-must-pass, auto-rollback on red, mandatory escalation when uncertain — and likely a brain upgrade (see §7). Do not enable Tier 2 on a repo until the loop has earned it.
4. **`disable_governor_check`.** Must be `false` in prod `.env`, or the RSA gate is bypassed.
5. **Rename churn.** 91 files reference `TrueSightDAO/dapp`. GitHub redirects keep things working, but update references deliberately in A3; renaming the prod repo can disturb the Pages custom-domain binding (re-save it).

---

## 7. Out of scope / parallel tracks

- **Brain upgrade** (`fix_agent.py` / `llm_client.py`): a stronger model/harness inside the loop. Parallel track — strongly recommended before broad Tier 2, but not blocking B1–B5. See `docs/LLM_PROVIDER_ROADMAP.md` in `truesight_autopilot`.
- **Edgar (Rails) & tokenomics GAS auto-deploy**: these have **no Pages auto-deploy** (`sentiment_importer` uses manual `./deploy.sh`; GAS needs `clasp deploy`). Hands-off-to-beta is a later phase for these; static/Pages repos (dapp, agroverse_shop, truesight_me, capoeira) come first.
- **Slack**: explicitly rejected for personal use.

---

## 8. Resume tracker

**RESUME HERE → Track A COMPLETE (2026-05-27). Both domains live and convention-matched.** `dapp_beta` (non-fork base) → beta.dapp.truesight.me; `dapp_prod` (fork of dapp_beta) → dapp.truesight.me (HTTP 200); old `dapp` archived. DNS in Route53 (EXPLORYA, zone `Z0032474227N6EQ3Z4QU`). Promote beta→prod via `gh repo sync` (never `--force`). **Next real work = B4–B6** (file/photo passthrough; beta-deploy gate Tier-1→Tier-2 auto-merge into `dapp_beta`). B1–B3 + web browsing shipped 2026-05-26. Track C (public Q&A) **shelved** — §9. *(Cosmetic follow-up: ~remaining incidental `TrueSightDAO/dapp` doc mentions still resolve via the archived repo; sweep opportunistically.)*

| Unit | PR | Merged | Deployed | Contribution reported |
|---|---|---|---|---|
| Roadmap (this file) | agentic_ai_context#205 | ✅ | n/a | ✅ |
| (extra) Web browsing — Tavily | truesight_autopilot#43 | ✅ | ✅ | ✅ |
| A0 DNS record (Route53, EXPLORYA) | (route53 change C0171027E43KCV4QPIY6) | ✅ | ✅ resolves + serves 200 | ☐ |
| A1 create `dapp_beta` + CNAME + Pages + CI | (gh repo create + push 2026-05-27) | ✅ | ✅ (Pages enabled, cname set) | ☐ |
| A2 autopilot beta allowlist | truesight_autopilot#50 | ✅ | ✅ | ☐ |
| A3 prod-side fork: `dapp_prod` (fork of dapp_beta) → dapp.truesight.me; old dapp archived; autopilot allowlist | truesight_autopilot#53 (+gh fork/Pages/Route53) | ✅ | ✅ serves 200 | ☐ |
| B1 Telegram adapter + single-user lock | truesight_autopilot#44 | ✅ | ✅ | ☐ |
| B2 topic↔session (in #44) | truesight_autopilot#44 | ✅ | ✅ | ☐ |
| B3 identity reuse (in #44) | truesight_autopilot#44 | ✅ | ✅ | ☐ |
| B4 file/photo passthrough | — | ☐ | ☐ | ☐ |
| B5 beta gate Tier 1 (one-tap ship) | — | ☐ | ☐ | ☐ |
| B6 beta gate Tier 2 (auto-on-green) | — | ☐ | ☐ | ☐ |

Per `OPERATING_INSTRUCTIONS.md` §5 + the DAO contribution convention: after each unit merges, report the contribution before starting the next, and tick both boxes here.

---

## 9. Track C — public non-sensitive Q&A tier — SHELVED (2026-05-26)

**Decision (Gary, 2026-05-26): shelved, do not build.** Rationale: it mostly burns LLM tokens for random non-ops users (Tom/Dick/Harry) who don't need it, and the DAO already has public-facing surfaces (oracle.truesight.me + truesight.me `llms.txt`/`stats`) for anyone who genuinely wants DAO facts. `@truesight_autopilot_bot` stays private to Gary. Revisit only if there's a concrete ops need for public access. Original design notes kept below for that case.

Idea (Gary, 2026-05-26): let **anyone** ask the bot non-sensitive questions about TrueSight DAO, while keeping the powerful capabilities owner-only.

**Why this is not just "remove the allowlist":** the autopilot chat agent has dangerous tools (`open_fix_pr`, `merge_pr`, `deploy_autopilot`, `submit_contribution`, `upload_file_to_github`, `read_local_file`/`list_directory` over the server FS) and its system prompt + `agentic_ai_context` grounding contain internal/operational detail. A public tier therefore needs its own walls:

- **Restricted tool set** — read-only, public-safe only (e.g. `web_search`, read of *public* repos/whitepaper); none of the mutating/infra/FS tools.
- **Public-only grounding** — answer from the existing public surface (truesight.me `llms.txt` + `stats/*.json`, whitepaper, `ecosystem_change_logs/advisory/BASE.md`), NOT internal `agentic_ai_context`.
- **Rate limiting + abuse/prompt-injection hardening.**
- **Tiering:** owner (Gary's ID) → full autopilot; everyone else → restricted public path.

**Shape decision needed before planning:** (a) same bot `@truesight_autopilot_bot` with a public tier vs a **separate public bot**; (b) or skip a new bot entirely and put public Q&A on the **existing** oracle/`truesight.me` surface. Recommendation leans: keep `@truesight_autopilot_bot` private to Gary; do public Q&A as a separate, restricted surface reusing the public knowledge layer.
