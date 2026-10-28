# GitHub rate-limit burner — investigation plan

**Status:** executing — time-sensitive, active production impact.
**Type:** investigation checklist (no code changes implied by the investigation itself;
remediation, once the source is found, may need its own §5a PR).
**Origin:** Gary, 2026-10-28, relayed through the planner session after `SendMessage` to
`planner` failed (same gap already flagged for `planner`→`supervisor`).

---

## 0. Why this is urgent

A steady **~2.2 req/sec sustained GitHub REST-core burn** is draining the shared `garyjob`
(GitHub user ID `1079482`) rate-limit quota. This is not a nuisance — it is **confirmed blocking
three parallel Sophia tracks right now**: `truesight_autopilot` PR #558 merge, `dapp_beta` PR #153
merge, `farm-media-site` PR #1 merge. Whoever picks up any unit below should treat this as
higher priority than routine WIP, not queue behind it.

---

## 1. Pre-flight (§5d — everything already known, captured so no unit re-discovers it)

**Already ruled out** (Sophia's own diagnostic work, Discord `#github-rate-limit-burner`,
channel `1564964855344005211`, guild `923008087315587072`):
- This autopilot box (`sophia-nelanco`, `i-05276b8ae82d6b88c`) itself.
- `nelanco-claude`'s `envoy_trigger.watcher` — polls Telegram/Discord, not GitHub (an early
  mislabel pointing at this was self-corrected in the same thread).
- A stale second checkout.
- Cron/systemd timers on the boxes already checked.

**Structural finding, load-bearing for every unit below:** GitHub meters rate limit **by user,
not by token**. All three of Sophia's PATs (`TRUESIGHT_DAO_AUTOPILOT`, `GITHUB_READ_PAT`,
`GITHUB_TRANSCRIPT_PAT`) authenticate as the same `garyjob` user and **share one 5,000 req/hour
quota**. Worse: `nelanco-claude`'s own `ubuntu` user is **also** `gh auth login`'d as `garyjob` —
so even Envoy's/supervisor's own `gh` CLI calls on this box draw from the identical quota. That
usage is sparse/bursty from direct observation and doesn't match the sustained ~2.2 req/sec
pattern, but it means **the burner could be any process on any host that has ever authenticated
as `garyjob`** — the search space is "every box with that credential," not "every box running
Sophia's code."

**New this session (Envoy, read-only, both AWS accounts enumerated):**

- **Explorya (`440626669078`) has zero EC2 instances** across `us-east-1`, `us-east-2`,
  `us-west-1`, `us-west-2` (not a full global-region sweep, but the account's standard operating
  regions) — **ruled out entirely as a candidate host.**
- **Nelanco (`767697632458`) has 18 running/stopped EC2 instances** (full list below). One
  initially looked anomalous — no `Name` tag — but on inspection it's `i-0f9b50986503f2123`, an
  autoscaling-group-managed `krake_ror` worker (lowercase `name` tag, `aws:autoscaling:groupName
  = krake_ror`, launched by `RunInstances`/`RegisterTargets` via the ASG's fleet, confirmed via
  CloudTrail — not a manually-launched anomaly, not a smoking gun). Krake's data-harvesting stack
  has no known GitHub dependency, but it hasn't been individually SSH-checked — see U2.

| Instance | Name | State | Launched | In the verified-reachable SSH fleet? |
|---|---|---|---|---|
| `i-030c1452b197c920a` | GETDATA_REDIS | running | 2026-01-02 | yes — `getdata_redis` |
| `i-09ecc8ecc91d09206` | seni_redis_2 | **stopped** | 2026-02-03 | no |
| `i-063dc4a3be90bd630` | seni_ror_200250915 | running | 2026-05-28 | yes — `seni_ror` |
| `i-07c76510b231d787f` | krake_data | running | 2025-10-24 | yes — `krake_data` |
| `i-05a041b6956aa7154` | krake_nginx | running | 2025-11-04 | yes — `krake_nginx` |
| `i-09883a010a52509f6` | seni_sk_auto | running | 2026-05-28 | yes — `seni_sk` (IP may have moved, verify) |
| `i-08ebe96afbc649a95` | seni_sql_2026 | running | 2026-01-08 | yes — `seni_sql` |
| `i-05f8770a932b76649` | dao_protocol_nelanco | running | 2026-05-28 | yes — `dao_protocol` |
| `i-0b8c6d989594fb229` | dao-protocol-beta | running | 2026-06-09 | no — new, not in `~/.ssh/config` |
| `i-05276b8ae82d6b88c` | sophia-nelanco | running | 2026-07-15 | yes — `sophia` |
| `i-01e55daf0323d93ab` | seni_sk_backfill_20260824 | running | 2026-08-24 | no |
| `i-0f7b01f6535f1c404` | krake_sk_consolidated | running | 2026-10-05 | partially — several `krake_sk_*` aliases exist, verify which one this is |
| `i-01ad5eca707e4445f` | nelanco-claude-code | running | 2026-10-25 | this box (Envoy) — already in-scope above |
| `i-085d04224ca04e106` | mtproto-proxy | running | 2026-08-03 | no |
| `i-0c935b455bf225dd9` | seni_sk_auto | running | 2026-10-05 | ambiguous — duplicate-looking name to the row above |
| `i-03a6c2f41f0a37b00` | seni_redis_2 | running | 2026-10-09 | ambiguous — duplicate-looking name, and the *other* `seni_redis_2` above is stopped |
| `i-0f9b50986503f2123` | (lowercase `name`=krake_ror, ASG-managed) | running | 2026-10-19 | no — explained above, likely clean |
| `i-0ebddf52cd92d0841` | bionpact_autopilot | running | 2026-08-18 | yes — `bionpact` |

**Not yet done, and the actual next steps (in order of likely decisiveness, per Gary):**
1. GitHub's own Security Log (`github.com/settings/security-log`) for user `1079482` — may give
   per-call IP attribution, or may only show PAT-usage/auth events on a personal (non-Enterprise)
   account. **Only Gary can view it** (his account).
2. Systematically check **every** Nelanco instance above — not just the ones already in the SSH
   fleet — for `gh auth status` / stored PATs matching `garyjob` or one of the three token names.
3. `ss -tnp` sampled against GitHub's IP range (`140.82.0.0/16`) on candidate hosts, to catch an
   in-process retry loop making real calls without going through the `autopilot.github` logging
   layer already checked and cleared.

✅ **Pre-flight Completeness:** every host, account, and ruled-out cause above is captured here;
no unit below should need to re-run the EC2 enumeration or re-derive the shared-quota finding.

---

## 2. Investigation units

These are independent diagnostic threads, not a strict code-PR sequence — U2 and U3 can run in
parallel with each other and don't block on U1, but **U1 is the single most likely to be
decisive and should be asked for immediately, not queued.**

| Unit | Owner | Scope |
|---|---|---|
| **U1 — gate: human (Gary only)** | Gary | Check `github.com/settings/security-log` for user `1079482`. Report back whether it gives per-call IP/source attribution for API usage, or only coarse PAT-creation/auth events. If it names an IP, cross-reference against the instance table above immediately — this could close the investigation in one step. |
| **U2** | Sophia or Envoy | For every instance in the pre-flight table **not already confirmed clean**, check (where reachable): `gh auth status`, `cat ~/.config/gh/hosts.yml` (or equivalent), `grep -r` for the three PAT variable names in any `.env`/config on that box. Prioritize the ones flagged "no"/"ambiguous" in the reachability column — those are the real unknowns. Resolve the two apparent `seni_sk_auto` / `seni_redis_2` naming duplicates while there (confirm whether they're genuinely two live instances or a stale/duplicate pair). |
| **U3** | Sophia or Envoy | On every reachable host from the table (prioritize ones already SSH-verified, since that's zero marginal cost), sample `ss -tnp \| grep -E ':443\b' ` filtered to GitHub's IP range (`140.82.0.0/16`, also check `140.82.112.0/20` etc. — get the current authoritative range via `https://api.github.com/meta` rather than hardcoding) over a short window (e.g. 30-60s, a few samples) to catch an in-process loop making real HTTPS calls to GitHub without hitting the already-checked `autopilot.github` Python logging layer (i.e. a non-Python process, or a Python process not going through that logger). |
| **U4 — gate: human** | Gary | Once a source is identified: decide remediation. If it's a stale/forgotten credential on a box, rotating the shared `garyjob` PAT is the clean fix but **affects every legitimate consumer simultaneously** (Sophia's three PATs, Envoy's own `gh auth`, supervisor) — coordinate the rotation, don't just revoke blind. If it's a live misbehaving process, killing it may be immediate and lower-risk than rotation. This decision needs Gary either way. |

**UAT:** n/a — this is an investigation, not a human-facing feature. The "acceptance criterion"
is simply: the ~2.2 req/sec sustained burn stops and the three blocked PR merges succeed.

---

## 3. Resume tracker

**RESUME HERE → U1 (ask Gary now) and U2/U3 (dispatch in parallel, don't wait on U1).**

| Unit | Status | Notes |
|---|---|---|
| U1 — Gary checks Security Log | ☐ | Most likely decisive; ask immediately |
| U2 — per-instance credential check | ☐ | Prioritize the "no"/"ambiguous" rows in the pre-flight table |
| U3 — `ss -tnp` sampling vs 140.82.0.0/16 | ☐ | Prioritize already-reachable hosts first |
| U4 — remediation decision | ☐ (blocked on U1/U2/U3 finding a source) | gate: human |

---

## 4. Authorization envelope (§5e)

- **Pre-authorized, read-only, both AWS accounts and the SSH fleet:** EC2 enumeration (done, this
  doc), `gh auth status`/config checks, `ss -tnp` sampling — all read-only, no state changes.
- **Gated:** anything that rotates/revokes the shared `garyjob` PAT, kills a live process on a
  production host, or otherwise changes state on any candidate box — U4, human only. Finding the
  source is not gated; acting on it is.
