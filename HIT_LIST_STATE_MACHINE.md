# Hit List state machine — states, transitions, and what each one means

_Last updated 2026-05-03 by Claude (Anthropic)._

The "Hit List" tab in
[spreadsheet 1eiqZr3LW-…](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit?gid=0#gid=0)
holds every retail-prospect row the DAO is tracking. The **Status**
column drives a 13-state machine. This doc enumerates every state and
every transition so humans (and future LLMs) can reason about a row at
a glance.

## TL;DR

A row's life cycle:

```
(blank) → Research → AI: Enrich with contact → AI: Email found → AI: Warm up prospect → AI: Prospect replied → Manager Follow-up
```

with branches off `Research` for rejection (`AI: No fit signal`),
fast-tracking to warm-up (`AI: Warm up prospect` directly when the
Email column is already populated), and from Enrich for manual triage
(`AI: Contact Form found` / `AI: Enrich — manual`).

**Three states are LEGACY** — no automation writes them any more:

- **`AI: Photo rejected`** — renamed to `AI: No fit signal` on 2026-05-03 (PR #104) since the photo+Grok pipeline that originally produced it is retired. Existing rows in this state are still re-evaluated by the rescue path; once they cycle through, they end up either at `AI: Enrich with contact` (positive signal found) or migrated to `AI: No fit signal` (still no signal). The `scripts/rename_legacy_photo_rejected_status.py` one-off bulk-renames whatever's left.
- **`AI: Photo needs review`** — photo+Grok rubric was ambiguous. No replacement; manual triage only.
- **`AI: Shortlisted`** — photo+Grok said "looks like a fit." Operator-managed.

## Flow chart

```mermaid
stateDiagram-v2
    [*] --> Blank: row added by\ndiscover_apothecaries
    Blank --> Research: appended\nwith Status=Research

    Research --> Warmup: Hosts Circles=Yes\nAND Email present
    Research --> Enrich: Hosts Circles=Yes\nAND no Email
    Research --> NoFitSignal: site crawled OK\nAND zero keywords

    NoFitSignal --> Enrich: rescue: Hosts Circles=Yes\non re-crawl
    PhotoRejected --> Enrich: legacy: rescue path\nstill accepts old name

    Shortlisted --> Enrich: human-shortlisted-to-enrich\n(operator)
    AIShortlisted --> Enrich: shortlisted-to-enrich\n(legacy)

    Enrich --> EmailFound: enrich found email
    Enrich --> ContactForm: enrich found contact form\nbut no email
    Enrich --> EnrichManual: enrich found neither\n(no website / fetch failed)

    EmailFound --> Warmup: email-to-warmup\n(promote)

    Warmup --> Replied: Gmail reply detected\nfor sent warm-up

    Replied --> ManagerFollowup: operator routes\nfor follow-up

    ContactForm --> ManagerFollowup: operator follow-up
    EnrichManual --> ManagerFollowup: operator follow-up

    ManagerFollowup --> [*]: manual close
    Warmup --> [*]: no reply,\nstays as Warmup

    PhotoRejected: AI: Photo rejected\n(LEGACY — renamed 2026-05-03)
    PhotoNeedsReview: AI: Photo needs review\n(LEGACY — no automation reaches this)
    AIShortlisted: AI: Shortlisted\n(LEGACY — photo+Grok pipeline retired)

    Research: Research
    Enrich: AI: Enrich with contact
    EmailFound: AI: Email found
    ContactForm: AI: Contact Form found
    EnrichManual: AI: Enrich — manual
    Warmup: AI: Warm up prospect
    Replied: AI: Prospect replied
    ManagerFollowup: Manager Follow-up
    NoFitSignal: AI: No fit signal
    Shortlisted: Shortlisted (human)
```

## State definitions

| State | Meaning | Who reads it (consumer scripts) | Who writes it (writer scripts) |
|---|---|---|---|
| _(blank / new)_ | Just added; not yet evaluated. | `detect_circle_hosting_retailers.py` (only when Status==Research; blank rows ignored). | `discover_apothecaries_la_hit_list.py` (sets `Research` immediately, so blank is transient). |
| **Research** | Awaiting site-crawl qualification. Has at least Shop Name + Address. | `detect_circle_hosting_retailers.py` cron at :50. | `discover_apothecaries_la_hit_list.py` (Nearby Search appends new rows). |
| **AI: No fit signal** | Site crawled successfully and found **no** qualifying keywords (cacao ceremony / women's circle / sound bath / etc.). Recoverable: a re-crawl that later finds keywords promotes back to Enrich (rescue path, default-on). Renamed from legacy `AI: Photo rejected` on 2026-05-03 (PR #104) since the photo+Grok pipeline that originally produced the legacy name is retired. | `detect_circle_hosting_retailers.py` rescue path (reads both new + legacy names). | `detect_circle_hosting_retailers.py` (when crawl returns OK + zero matches). |
| ~~AI: Photo rejected~~ _(LEGACY)_ | Old name for the same condition as `AI: No fit signal` — renamed 2026-05-03 (PR #104). Rescue path still reads this name for back-compat. Operator can run `scripts/rename_legacy_photo_rejected_status.py` to bulk-migrate any remaining rows. | `detect_circle_hosting_retailers.py` rescue path. | _(legacy_; nothing new produces this name). |
| **AI: Enrich with contact** | Qualified. Needs Place Details lookup + email harvesting. | `hit_list_enrich_contact.py` cron at :35. | `detect_circle_hosting_retailers.py` (Hosts Circles=Yes + no email yet); `hit_list_promote_status.py` (`shortlisted-to-enrich`, `human-shortlisted-to-enrich`). |
| **AI: Email found** | Email harvested. Awaiting promotion to warm-up. | `hit_list_promote_status.py` (`email-to-warmup`). | `hit_list_enrich_contact.py` (when website crawl + Grok pick produced an email). |
| **AI: Contact Form found** | Only a contact form URL surfaced; no email. **Terminal automation state** — manual follow-up only. Never auto-promoted to warm-up. | None (operator). | `hit_list_enrich_contact.py`. |
| **AI: Enrich — manual** | Enrich couldn't find a website *or* a place_id (or both). Operator triage required. | None (operator). | `hit_list_enrich_contact.py`. |
| **AI: Warm up prospect** | Ready for warm-up Gmail draft. Email present. | `suggest_warmup_prospect_drafts.py` cron (creates drafts; doesn't change status). | `detect_circle_hosting_retailers.py` (Hosts Circles=Yes + email already present, fast-track); `hit_list_promote_status.py` (`email-to-warmup`). |
| **AI: Prospect replied** | Gmail detected an inbound reply to our warm-up. Operator should triage. | None directly (operator); `backfill_warmup_reply_remarks.py` for audit logging. | `backfill_warmup_reply_remarks.py` / `backfill_all_warmup_replies.py` when reply detected. |
| **Manager Follow-up** | Operator-claimed row needing follow-up Gmail draft. | `suggest_manager_followup_drafts.py` cron (creates drafts). | Operator (manual) or downstream operator process. |
| **Shortlisted** _(human)_ | Human-confirmed fit during manual triage. | `hit_list_promote_status.py` (`human-shortlisted-to-enrich`). | Operator (manual). |
| ~~AI: Shortlisted~~ _(LEGACY)_ | Old: photo+Grok rubric said "looks like a fit." | `hit_list_promote_status.py` (`shortlisted-to-enrich`) still consumes; nothing produces. | _(legacy_; `hit_list_research_photo_review.py` cron retired in PR #101). |
| ~~AI: Photo needs review~~ _(LEGACY)_ | Old: photo+Grok ambiguous, manual triage required. | None (operator). | _(legacy_; same retired cron). |

## Transitions

### From `(blank / new)`
| → State | Trigger | Condition |
|---|---|---|
| `Research` | `discover_apothecaries_la_hit_list.py` (manual `workflow_dispatch`) | Nearby Search returned a new place_id; row appended. |

### From `Research`
| → State | Trigger | Condition |
|---|---|---|
| `AI: Warm up prospect` | `detect_circle_hosting_retailers.py` (cron `:50 * * * *`) | Hosts Circles=Yes (positive site signal) **AND** Email column already populated. Fast-tracks past Enrich since email is the only thing Enrich would have produced. |
| `AI: Enrich with contact` | `detect_circle_hosting_retailers.py` (cron `:50`) | Hosts Circles=Yes **AND** Email column empty. |
| `AI: No fit signal` | `detect_circle_hosting_retailers.py` (cron `:50`) | Site crawled OK + zero keyword matches. Default ON; pass `--no-reject-no-signal` to opt out. Renamed from legacy `AI: Photo rejected` on 2026-05-03. |

### From `AI: No fit signal` _(or legacy `AI: Photo rejected`)_
| → State | Trigger | Condition |
|---|---|---|
| `AI: Enrich with contact` | `detect_circle_hosting_retailers.py` (cron `:50`, default-on rescue) | Re-crawl found qualifying keywords (signal appeared after the original rejection — e.g. site updated). Rescue path reads BOTH the new name and the legacy `AI: Photo rejected` for back-compat. |

### From `Shortlisted` (human) / `AI: Shortlisted` (legacy)
| → State | Trigger | Condition |
|---|---|---|
| `AI: Enrich with contact` | `hit_list_promote_status.py` (manual or scheduled) | Has Website OR place_id in Notes (so Enrich has something to work with). Pass `--skip-contact-guardrail` to bypass. |

### From `AI: Enrich with contact`
| → State | Trigger | Condition |
|---|---|---|
| `AI: Email found` | `hit_list_enrich_contact.py` (cron `:35 * * * *`) | Place Details lookup + website crawl + Grok email pick produced a confirmed email. |
| `AI: Contact Form found` | `hit_list_enrich_contact.py` (cron `:35`) | No email surfaced, but a contact form URL did. **Terminal** — manual follow-up only. |
| `AI: Enrich — manual` | `hit_list_enrich_contact.py` (cron `:35`) | No website, no place_id, or all crawls failed. Manual triage. |

### From `AI: Email found`
| → State | Trigger | Condition |
|---|---|---|
| `AI: Warm up prospect` | `hit_list_promote_status.py email-to-warmup` (cron `:20 * * * *`) | Email column non-empty + has reasonable structure. Lower default `--limit` than the other promotion modes since this triggers actual outbound drafts downstream. |

### From `AI: Warm up prospect`
| → State | Trigger | Condition |
|---|---|---|
| `AI: Prospect replied` | `backfill_warmup_reply_remarks.py` / `backfill_all_warmup_replies.py` (manual / scheduled) | Gmail detected an inbound reply from the prospect's address to our warm-up thread. |
| _(stays)_ | `suggest_warmup_prospect_drafts.py` (cron) | Creates Gmail draft, but **does not change status** until the prospect replies. Drafts are reviewed/sent manually. |

### From `AI: Prospect replied`
| → State | Trigger | Condition |
|---|---|---|
| `Manager Follow-up` | Operator (manual) | Operator routes the reply for follow-up Gmail drafting. |

### Manual triage states
`AI: Contact Form found`, `AI: Enrich — manual`, `AI: Photo needs review` (legacy) — these are operator endpoints. Cron does not move them anywhere; operator decides whether to find an email manually, switch to a different shop, or close the row.

## Cron schedule that drives the machine

| Cron | Workflow | What it does | Reads | Writes |
|---|---|---|---|---|
| `:00 * * * *` | _(disabled — was photo review)_ | Retired in PR #101. Workflow kept as `workflow_dispatch` for manual debugging only. | — | — |
| `:20 * * * *` | `hit_list_promote_status.py` | `shortlisted-to-enrich` + `email-to-warmup` promotions. | `AI: Shortlisted`, `Shortlisted`, `AI: Email found` | `AI: Enrich with contact`, `AI: Warm up prospect` |
| `:20 * * * *` | `field_agent_location_places_pull.py` | Pulls Place Details for new field-agent-logged locations. | other sheet (Recent Field Agent Location) | appends new `Research` rows to Hit List |
| `:35 * * * *` | `hit_list_enrich_contact.py` | Enrich queue + fill-gap sweep. | `AI: Enrich with contact` (queue) + any row with field gaps | `AI: Email found` / `AI: Contact Form found` / `AI: Enrich — manual` |
| `:50 * * * *` | `detect_circle_hosting_retailers.py` | Site crawl, Hosts Circles writeback, Research promotion + rescue + reject. | `Research`, `AI: No fit signal`, legacy `AI: Photo rejected` | `AI: Warm up prospect` / `AI: Enrich with contact` / `AI: No fit signal` |
| Manual | `discover_apothecaries_la_hit_list.py` | Nearby Search across centroids → appends new `Research` rows. | — | new rows with Status=`Research` |
| Manual | `suggest_warmup_prospect_drafts.py` | Creates Gmail drafts for `AI: Warm up prospect` rows with Email. | `AI: Warm up prospect` | _none_ (drafts only) |
| Manual | `suggest_manager_followup_drafts.py` | Creates Gmail follow-up drafts. | `Manager Follow-up` | _none_ (drafts only) |

## Anti-patterns / common gotchas

- **A row stuck in `Research` with no Website**: `detect_circle_hosting_retailers.py` skips rows without a Website, so they never get qualified. Operator should backfill Website manually (or run a discovery script that finds it).
- **A row in `AI: Email found` with empty Email**: `email-to-warmup` skips it. Either the email got cleared by accident (recoverable: edit Email cell, next cron picks it up) or Enrich set the wrong status (rare).
- **A row in `AI: Warm up prospect` for weeks with no draft**: `suggest_warmup_prospect_drafts.py` is manual-trigger-only. Operator should run it explicitly.
- **A row in `AI: Photo needs review` from old data**: legacy state. No automation will move it. Manually re-set to `Research` to re-qualify under the new pipeline.
- **The Hosts Circles column (col AW)** is the canonical "did we crawl this site for cacao-ceremony keywords yet" signal. Empty = not crawled. `Yes (...)` = positive. `Not detected` = crawled, no keywords. The state machine relies on this column being honest.

## See also

- [`PLACES_API_CACHING.md`](./PLACES_API_CACHING.md) — how Place Details caching works, including the `place_id` lookup that Enrich does.
- [`PARTNER_OUTREACH_PROTOCOL.md`](./PARTNER_OUTREACH_PROTOCOL.md) — manual partner-outreach playbook (orthogonal to the cron pipeline).
- [`HIT_LIST_CONTACT_ENRICHMENT.md`](./HIT_LIST_CONTACT_ENRICHMENT.md) — deeper dive on the Enrich step.
- `market_research/scripts/hit_list_promote_status.py --help` — modes for the promotion cron.
- `market_research/scripts/detect_circle_hosting_retailers.py --help` — qualification cron.
