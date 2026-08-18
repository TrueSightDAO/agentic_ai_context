# Bionpact — locked-down, private Sophia instance for the Ops team

**Status:** Plan-of-record. Repos created (Unit 0 done); code + infra units not yet started.
**Created:** 2026-08-18 | **Owner:** Gary Teh | **Author:** Claude Code (nelanco-claude box)
**Convention:** Follows `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5d / §5e.

> ## ▶ RESUME HERE: Unit 1 (this doc's own commit) → Unit 2

## Context

Sophia (`truesight_autopilot`) is fully public: her transcript and context repo
(`truesight_autopilot_transcript`, `agentic_ai_context`) are both public GitHub repos. Gary has
stood up an Ops team and wants Elizabeth "Liz" Wong (a community member) to have chat access to a
Sophia-like assistant, but privately — no public transcript, minimal credential exposure given
Liz's trust level differs from Gary's as governor.

Agreed shape (built up over conversation, 2026-08-18):
- **New persona, self-named on first boot.** EC2 tag/box name: **`bionpact_autopilot`**.
- **Own EC2 box**, separate from Sophia's, in the **Nelanco** AWS account (`767697632458`).
- **Telegram-only interface** — a new bot, a chat with just Gary + Liz. No public-facing HTTP
  surface at all (unlike Sophia, who serves `sophia.truesight.me`).
- **Read:** all public `TrueSightDAO` GitHub repos, public Edgar GET endpoints (events-catalog,
  ping, qr-code-check).
- **Write:** only to three new private repos under `TrueSightDAO` (all created, private, seeded
  with an initial commit on `main`):
  - **`bionpact_agentic_ai_context`** — her private context/notes repo (PR-edited; mirrors the
    public `agentic_ai_context`'s role, but private).
  - **`bionpact_autopilot_transcription`** — her private raw conversation transcript log
    (API-only, machine-appended; mirrors `truesight_autopilot_transcript`'s role, but private).
  - **`bionpact_attachments`** — private, API-only blob store for Telegram photo/PDF attachments
    Gary or Liz upload (mirrors the public `store_interaction_attachments`'s role, but private).
    Never cloned or branch-edited — single-file Contents-API writes only.
- **No Edgar writes** (no DAO signing identity) — she can't submit contributions even if asked.
- **No AWS keys, no fleet SSH, no Gmail, no vault** — locked down by default, expand later only
  if Gary asks.

## Pre-flight findings (§5d completeness — captured so no unit needs to re-discover live)

- **Reads are already ungated.** `read_repo_file` / `search_codebase`
  (`truesight_autopilot/app/tools/github_tools.py:23-70`) hit
  `api.github.com/repos/TrueSightDAO/<repo>/...` with no `allowed_repos` check — any public repo,
  out of the box, no code change needed.
- **Branch/PR writes are gated by `settings.allowed_repos`**, checked in `create_repo`
  (github_tools.py:157), `merge_pr` (:277), `mark_pr_ready` (:305), and `git_tools.py`'s push/PR
  path. Setting `allowed_repos = ["bionpact_agentic_ai_context", "bionpact_autopilot_transcription",
  "bionpact_attachments"]` on the new instance's own config confines those write paths to just
  these three repos.
- **`upload_file_to_github` (Contents-API single-file writes) has NO code-level repo gate today**
  (`truesight_autopilot/app/tools/upload_file_to_github.py` — confirmed no `allowed_repos` /
  `api_only_repos` check in the function). It's bounded only by what the GitHub PAT presented can
  actually write to. For Bionpact, the fine-grained write-PAT (Unit 4) is therefore the *real*
  security boundary for attachment/transcript uploads, not just a backstop — Unit 2 will add an
  `allowed_repos` check to this tool too, for defense-in-depth (also benefits Sophia's own
  instance).
- **Edgar's only write path** is `POST /dao/submit_contribution`
  (`app/tools/dao_identity.py:68,80`, `app/tools/dao_submission.py`), gated by
  `edgar.is_configured()` → requires `EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY` all set
  (`app/edgar_logger.py:32-35`). Omit all three → every Edgar write attempt returns a clean error;
  she has no key to sign with even if asked. Public GETs are untouched.
- **GOVERNOR role is instance-local.** `TELEGRAM_ALLOWED_USER_IDS` (env, parsed in
  `app/policy.py:87-102`) plus `GOVERNOR_NAMES` resolve role per-instance (`policy.py:175-238`) —
  setting Gary's + Liz's numeric Telegram IDs on the *new* instance's own `.env` makes them
  GOVERNOR there, fully independent of Sophia's own governor list.
- **AWS / Gmail / SSH / Vault all degrade gracefully when unconfigured** — confirmed no crash risk:
  `aws_monitor.py:46-94` returns an empty account list and skips polling; `gmail_tools.py:80-85`
  returns an error dict; `ssh_tools.py:213-224` returns an error dict; `vault_tools.py:35-81`
  returns "not initialized". Simply omitting `AWS_*`, `GMAIL_*`, and never running the SSH-key /
  vault-init steps is sufficient — no code change needed for these.
- **Blocker — repo names are hardcoded, not configurable.** `"truesight_autopilot_transcript"` is a
  literal in `app/config.py:123` (the `api_only_repos` list); `"agentic_ai_context"` is a literal
  tuple entry in `app/context.py:343` (`_CONTEXT_SYNC_REPOS`) and a literal path segment in
  `app/context.py:425` (`get_context_file`); `"store_interaction_attachments"` is likewise a plain
  list entry (`config.py:131`). All three names are also woven into the LLM's own system prompt at
  `app/context.py:205-210` (the "REPO CLASSES" block that tells the agent which repos are which
  class). **A new instance cannot correctly target the `bionpact_*` repos without a small code
  change first (Unit 2).**
- **Telegram adapter needs no inbound exposure.** `app/telegram_adapter.py` long-polls Telegram
  outbound; a plain group/DM works fine, forum topics are optional (`thread_id` is `None`-safe,
  confirmed in adapter code). So, unlike Sophia's box, **this instance needs no nginx, no certbot,
  no public DNS, no inbound HTTP port at all** — SSH only.
- **Systemd units** (`truesight_autopilot/systemd/*.service`): brain =
  `truesight-autopilot.service` (`uvicorn app.main:app --port 8001 --workers 1` — workers MUST stay
  1, in-process session state); adapter = `truesight-autopilot-telegram.service`. Watchdog (MTProto
  user-session) and vault (credential store) are both skippable for this instance.
- **GitHub PAT split needed.** `_github_headers()` (`github_tools.py:13-19`) only attaches auth
  `if settings.github_pat:` — reads work unauthenticated too (rate-limited, 60/hr). A **single**
  fine-grained PAT scoped to "Only select repositories" = the 3 new private repos (Contents:RW +
  PRs:RW) is right for writes, but fine-grained PATs scoped that narrowly do **not** extend read
  access to other (even public) repos once presented — so reads need either no PAT at all (accept
  the unauthenticated rate limit) or a second, broader **read-only** token. Unit 2 adds a second
  settings field (`github_read_pat`) for this.
- **EC2 provisioning — two conflicting historical parameter sets found; use the newer, verified
  one.** `truesight_autopilot/scripts/launch_ec2.sh` hardcodes `sg-e98f788e` / `subnet-44257d33` /
  key `garyjob_aws` — but the script's own comment flags these as **stale** (Sophia's live box
  actually runs in Explorya today, not Nelanco). The **current Claude Code box** in this same
  Nelanco account was provisioned 2026-07-14 against verified-live values captured in
  `agentic_ai_context/plans/NELANCO_CLAUDE_CODE_BOX_PLAN.md` §5: VPC `vpc-d59748af`, subnet
  `subnet-de8102b9` (us-east-1a), SG `launch-wizard-1` (`sg-003e8016026715f25`), key pair
  `GETDATA_IO_PAIR_20201122`, Ubuntu 22.04 encrypted 30GB gp3. **Use these**, with a pre-flight
  `aws ec2 describe-*` re-verification before launch (values may have drifted since 2026-07-14).

## Sequenced plan (one unit per turn, §5a)

| # | Unit | Type | Status |
|---|------|------|--------|
| 0 | Create `bionpact_agentic_ai_context`, `bionpact_autopilot_transcription`, `bionpact_attachments` — all private, seeded with initial commit on `main` | GitHub (low-risk, reversible) | ✅ done 2026-08-18 |
| 1 | Commit this roadmap to `agentic_ai_context/plans/BIONPACT_AUTOPILOT_PLAN.md` | Docs | in progress (this PR) |
| 2 | Code PR to `truesight_autopilot` (shared repo): add `settings.transcript_repo` (default `"truesight_autopilot_transcript"`), `settings.context_repo_name` (default `"agentic_ai_context"`), `settings.attachments_repo` (default `"store_interaction_attachments"`), `settings.github_read_pat` (default `""`); replace the hardcoded spots (config.py:123,131; context.py:343,425,205-210) to use them; add an `allowed_repos` check to `upload_file_to_github`. Defaults preserve Sophia's exact current behavior — zero behavior change for her. Tests confirming defaults unchanged. | Code (PR + tests, reviewed/merged) | ☐ not started — must merge before Unit 5 |
| 3 | Provision EC2 box `bionpact_autopilot` in Nelanco (verified VPC/subnet/SG/keypair/AMI above); SSH-only, no EIP/DNS/nginx/certbot | AWS infra — **gate** (§5c: irreversible/outward-facing) | ☐ not started |
| 4 | Credentials: Gary creates Telegram bot via BotFather, adds Gary+Liz to a chat with it, gets both numeric Telegram IDs; decides reuse-vs-mint DeepSeek key (defaulting to reuse); creates the fine-grained write-PAT scoped to the 3 new private repos (Contents:RW + PRs:RW) | Human-assisted | ☐ not started |
| 5 | Deploy `truesight_autopilot` (post-Unit-2) onto the new box: fresh `.env` (new `JWT_SECRET`, bot token, `TELEGRAM_ALLOWED_USER_IDS`, `GOVERNOR_NAMES="Gary Teh,Elizabeth Wong"`, `DEEPSEEK_API_KEY`, split GitHub PATs, `TRANSCRIPT_REPO=bionpact_autopilot_transcription`, `CONTEXT_REPO_NAME` left default for reads / also clone `bionpact_agentic_ai_context` for her private notes, `ATTACHMENTS_REPO=bionpact_attachments`, `ALLOWED_REPOS=["bionpact_agentic_ai_context","bionpact_autopilot_transcription","bionpact_attachments"]`; all `AWS_*`/`GMAIL_*`/`EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY` omitted); install only 2 systemd units (brain + telegram adapter) | Deploy | ☐ not started — **report to Gary as soon as this lands** (explicitly requested) |
| 6 | Update `agentic_ai_context` (`PROJECT_INDEX.md` and/or `WORKSPACE_CONTEXT.md`) to record the three new private repos and the new EC2 instance, so Sophia and other LLMs reading the canonical docs know they exist (Gary explicitly authorized this edit) | Docs (direct edit, explicitly authorized) | ☐ not started |

**Resume tracker — Continue from the first row that isn't done.**

## UAT

1. Gary and Liz message the new bot in Telegram → both resolve as GOVERNOR (not GUEST).
2. Ask her to read a file from a public TrueSightDAO repo (e.g. `agentic_ai_context`) → succeeds.
3. Ask her to open a PR against `agentic_ai_context` (not hers) → refused (`allowed_repos` gate).
4. Ask her to open a PR / append a note to `bionpact_agentic_ai_context` → succeeds.
5. Send her a photo/PDF via Telegram → it lands in `bionpact_attachments`, not anywhere else.
6. Ask her to submit a DAO contribution via Edgar → cleanly errors ("Edgar not configured"), no
   crash, no signature possible.
7. Confirm the conversation gets appended to `bionpact_autopilot_transcription` (private, not the
   public transcript repo).
8. She states her own name in the first exchange.

## Open items flagged, not blocking

- DeepSeek key: reuse Sophia's vs. mint separate — defaulting to reuse, easy to split later.
- Fine-grained PAT support on the `TrueSightDAO` org — verifying in Unit 4, not assumed.
