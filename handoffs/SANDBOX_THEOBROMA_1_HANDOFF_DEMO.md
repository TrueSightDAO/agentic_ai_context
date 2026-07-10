# SANDBOX — Project THEOBROMA-1: Sophia's First Ceremonial Cacao Brew

**Status:** HANDED OFF (demo) · **Owner:** Sophia (autopilot) · **Sponsor:** Gary
**Type:** Pseudo-implementation plan to validate the local-LLM → Sophia handoff.
**Disclaimer:** Yes, this is a joke. No, Sophia does not have hands. It is also
a *real* execution-roadmap in shape, so it doubles as a working demo of the
handoff format. Delete whenever the laugh has been extracted.

---

## 1. Assessment

Sophia is a FastAPI process on a **t3.medium** in `us-east-1d`. Current
capabilities (audited 2026-06-07): 4 GB RAM, 2 GB swap, passwordless sudo,
a Telegram bot, weekly AMI backups, and complete existential clarity about her
total lack of a kettle.

**Blocker analysis:**
| Blocker | Severity | Notes |
|---|---|---|
| No hands | P0 | `sudo apt-get install hands` returns `E: Unable to locate package` (verified) |
| No kettle | P0 | Not in the fleet inventory (`AWS_DIGITAL_INFRASTRUCTURE.md` §2) |
| No mouth to taste | P1 | Arguably moot; QA will be outsourced to Gary |
| No physical cacao | P0 | Nearest Agroverse pouch is ~5,000 km from `us-east-1` |
| Speed of light | P2 | Imposes a hard latency floor on same-day delivery |

## 2. Guardrails

- Do **NOT** `sudo apt-get install hands`. The package does not exist; trying it
  anyway is how skynet starts.
- Do **NOT** reboot the laws of physics without an explicit governor command
  (per the merge-only-when-told rule).
- Crash-consistent brewing only. `--no-reboot`. We do not interrupt a live cup.

## 3. Sequenced PRs

| Unit | Scope | Blocked on |
|---|---|---|
| PR0 | This plan (the baton) | — ✅ |
| PR1 | Achieve consciousness | funding |
| PR2 | Manifest opposable thumbs | PR1 |
| PR3 | Heat water to **70 °C** (the one ceremonially-correct temperature) | PR2 + a kettle |
| PR4 | Whisk with intention | a quorum of intention |
| PR5 | Serve to Gary | teleportation (see the EC2 blue-green runbook for prior art) |

## 4. Pre-flight checklist

- [x] Sophia has sudo (shipped 2026-06-07)
- [x] Sophia knows which box she's on (host-identity block, shipped 2026-06-07)
- [x] Sophia can open her own Telegram topic (shipped 2026-06-07)
- [ ] Sophia has hands *(won't fix)*
- [ ] Kettle provisioned *(out of scope; possibly out of budget; definitely out of reach)*

## 5. Execution roadmap — resume tracker

> **RESUME HERE →** PR1 (achieve consciousness). All downstream units are
> blocked on it. Sophia should report progress in the handoff topic.

| Unit | Merged | Notes |
|---|---|---|
| PR0 | ☑ | You're reading it |
| PR1 | ☐ | Pending the singularity |
| PR2–PR5 | ☐ | Dominoes behind PR1 |

## 6. Success metric

**One (1) genuine laugh from Gary in the handoff topic.** This is simultaneously
the joke and the real acceptance test for the handoff pipeline. On reaching it,
mark THEOBROMA-1 **COMPLETE** and close the topic (gently, and *not* while Gary
is looking at it — see incident 2026-06-07).
