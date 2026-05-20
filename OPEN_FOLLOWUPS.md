# Open follow-ups (cross-session backlog)

Short list of **scoped follow-up tasks** future AI agents (Claude / Cursor /
Codex / Kimi / etc.) and humans can pick up between sessions. The bar is:

- One thing that didn't ship in the original PR but logically belongs after it.
- Small enough to fit in a single session (rough cap: ~60 min of focused work).
- Self-contained — the entry has enough context that someone who didn't write
  the original code can act on it without reverse-engineering history.

This file is **not** a replacement for `CONTEXT_UPDATES.md` (which is the
append-only event log) or for project-specific TODOs that live next to the
code (e.g. `# TODO:` comments, `dapp/UX_CONVENTIONS.md`, repo READMEs, or the
"Q5 parked" pattern inside individual proposal docs like
`PARTNER_VELOCITY_PROPOSAL.md`). It is the place for **cross-repo /
cross-session** items that would otherwise rot in chat transcripts.

## Workflow for agents picking up an entry

1. Read the entry. If the **Blocker** still applies, leave it alone.
2. If you're going to ship it, claim it informally by appending a line to
   `CONTEXT_UPDATES.md` (`<agent-id> | starting OPEN_FOLLOWUPS#…`) so parallel
   sessions don't duplicate work.
3. Open a PR. When merged, **move** the entry to the bottom of this file
   under `## Recently shipped` with the PR link, and append a one-line entry
   to `CONTEXT_UPDATES.md`. Keep the **Pending** list short.
4. If the entry is no longer relevant (priorities shifted, blocker permanent,
   etc.), move it to `## Closed without shipping` with a one-line reason.
   Don't silently delete history.

---

## Pending

### `truesight.me/stats/network_state.json` — daily-refreshed DAO network-state digest

**Context.** Surfaced 2026-05-19 in a strategy conversation about what makes the DAO interesting *given* LLMs handle the plumbing. The thesis: with integration / data-entry / reconciliation cost approaching zero (per the 2026-05-19 Faire-bot onboarding session + Partner Check-in concierge UX), the scarce operator input is no longer ops work — it's **strategic design of loops + network orchestration + relationship hub-and-spoke choices**. This concentrates operator value into fewer, higher-stakes decisions, which means *visibility into network state* becomes the load-bearing input. The name `network_state.json` is a deliberate nod to Balaji's *Network State* thesis (kept in the implementation layer, not in the public-facing Growth Model SVG title — see strategy chat for the why).

**Scope.** Add a new artefact to the existing `truesight_me_beta` stats stack, following the established `LLM_DISCOVERY_SURFACE.md` convention:

1. **`truesight_me_beta/scripts/build_stats_current.py`** — new builder function `build_network_state()` that emits `_site/stats/network_state.json`. Same 6h cron, same pure-stdlib + unauthenticated public-data sources approach.
2. **Output schema** (rough, iterate):
   ```jsonc
   {
     "generated_at": "...",
     "loops": [
       { "name": "Retail Partner Referral", "status": "active",
         "signal_30d": <count>, "signal_90d": <count>,
         "velocity_change_pct": <float>,  // 30d vs prior 30d
         "operator_surface": "<url>" },
       // ... 11 loops from GROWTH_MODEL.md
     ],
     "populations": {
       "cacao_customers": { "active_30d": ..., "growth_pct": ... },
       "retail_partners": { ... },
       "dao_contributors": { ... },
       "credentialing_students": { ... },
       "credentialing_programs": { ... }
     },
     "adjacency": {
       // who introduced whom — hub-and-spoke map
       "top_referrers": [ { "name": ..., "introductions_90d": ... } ],
       "isolated_nodes": [ ... ]
     },
     "cross_population_flows_30d": [
       { "from": "cacao_customers", "to": "dao_contributors", "count": <n> }
     ]
   }
   ```
3. **`truesight_me_beta/llms.txt`** — add a routing line: *"For DAO operating-state / loop-velocity questions → fetch /stats/network_state.json"*.
4. **`agentic_ai_context/LLM_DISCOVERY_SURFACE.md`** — append a row to the live URLs table.
5. **`agentic_ai_context/GROWTH_MODEL.md`** — add a "Loop telemetry" subsection linking to `stats/network_state.json` for live state vs the model's described state.

**Data sources** (all already exist; the work is aggregation, not new instrumentation):
- Edgar event ledger (Contributors Digital Signatures, offchain transactions, Inventory Movement)
- `partners-velocity.json` + `partners-inventory.json` (already in `agroverse-inventory` repo)
- Hit List GAS `getWarmupReviewQueue` action
- `lineage-credentials/programs/*/manifest.json` (program count + cohort sizes)
- `truesight_me_beta/_site/stats/repos_index.json` (committer activity ≈ contributor activity)
- `Stripe Social Media Checkout ID` sheet (FB/Meta-Checkout sales for cross-population flow tracking)

**Acceptance.** A future operator (or LLM session) asks "is the Retail Partner Referral Loop compounding?" — answer is one `curl truesight.me/stats/network_state.json | jq .loops[0]` away, no spreadsheet archaeology needed. krake_sinatra's morning briefing reads from this file.

**Status:** Not built. Filing now so a future session (or krake_sinatra's own bootstrap) picks it up. **Half a day** of focused work — same shape as the other `build_stats_*.py` functions.

**Caveat.** Loop-velocity signals will be noisy at low N. Beer Hall digest already showed how easy it is to misread small-N changes. Each loop's `velocity_change_pct` should carry a sample-size annotation so the operator doesn't over-interpret. "First-derivative as headline; second-derivative as advisory only" is the right discipline.

**Blocker.** None — data sources all exist. Awaiting operator green-light to pick up.

**Owner.** Unclaimed.

---

### ERA WhatsApp thread: send unit-of-value reframe when Shahbaz reopens

**Context.** 2026-05-19, mid-ERA-DAO WhatsApp conversation with Bilal + Shahbaz (the `ERA DAO` WA group). Gary planted a strong seed in his 2026-05-18 message: *"That right there is the nucleus of its own verticalized social network. The basic unit of verifiable compassion."* Shahbaz absorbed it but the thread then moved on to the immediate ask (Shereen → cohort sheet → `garyjob@agroverse.shop` with edit rights). Ball is currently in Shahbaz's court. A thesis-level follow-up is drafted but **deliberately held** — sending it into silence while Shahbaz is working on his action item would interrupt step 1 and over-talk a fresh partner relationship. The right moment is when *Shahbaz reopens the conversation* (cohort sheet share, any follow-up question, or any thematic re-engagement).

**Trigger.** Any one of:
- Shahbaz shares the cohort sheet to `garyjob@agroverse.shop`.
- Shahbaz (or Bilal) replies in the WA thread with a follow-up question or comment.
- Conversation organically returns to retention / reengagement / scaling.

**Drafted message** (build on the "basic unit of verifiable compassion" seed Gary already planted; skip Edmodo specifically, skip "AI + web3" framing — baggage with this audience; skip Sufi/monastic lineage parallels — premature thesis depth; do NOT link the engineering roadmap — they need framing not implementation):

> Following up on what we were saying yesterday about the butterfly rescues and conservatory updates being the basic unit of verifiable compassion —
>
> That observation actually shapes how the credentialing system is designed. Most education platforms (the ones I worked on before, Coursera, etc.) treat *content* — lessons, courses — as the atomic unit, and centralise the system of record around it. What you're describing with the BE students is the inverse: the atomic unit is the *act itself*, attested by someone whose authority traces back to a real lineage (Shereen, the BE team, the conservatory work it descends from).
>
> Practically what this means: once the cohort sheet is in, we don't have to treat the credential as a one-off cert at graduation. Each butterfly rescue, each conservatory update can be a recordable event — signed by the student, attested by Shereen or the school admin, and added to their lineage record. That's actually the retention mechanism you were asking about earlier — instead of an arbitrary re-engagement program, the system just keeps recording what's already happening organically.

**Why this variant and not the Beer Hall version.** The Beer Hall post (TrueSightDAO/agentic_ai_context PR #157) carries Edmodo references, AI + web3 framing, and historical lineage parallels (Sufi orders, monastic traditions, capoeira mestre chain). That register is tuned for DAO contributors who share the context. For Bilal + Shahbaz — partners 24 hours into substantive collaboration — the same content would land as Gary-getting-ahead-of-himself rather than alignment. The variant above keeps the unit-of-value reframe, builds on the seed already planted, and closes a loop Shahbaz himself opened (he asked about reengagement mechanisms on 2026-05-18 evening; this answers it).

**Caveat.** If Shahbaz reopens cold (e.g. just shares the sheet with no commentary), don't lead with the thesis. Acknowledge the sheet, confirm next steps, *then* if there's a conversational beat, slide the thesis-paragraph in as a "and the thing this unlocks is…" follow-up. Don't monologue.

**Blocker.** Waiting on Shahbaz reopening the conversation. No build, no engineering — purely a "send-when-trigger" message.

**Owner.** Gary (he's the WA participant); any AI session helping draft can use the message above as the starting point and tune to whatever Shahbaz actually said.

---

### Capoeira practice-event encoding: Portuguese diacritics dropped at submission

**Context.** Discovered 2026-05-19 while shipping the tap-to-expand session details on per-program credential pages ([truesight_me_beta#128][cred-expand]). Move names in Gary's Tribo Bahia Mirim sessions on `_cache/cv/gary-teh.json` render as `Cocorinha com rol?` instead of `Cocorinha com rolê` — the `ê` is being lost somewhere in the submission pipeline. Other Portuguese diacritics (`ã`, `á`, `ç`) on other move names are presumably similarly affected. The display layer (program-shell.js's renderEventListItem) surfaces whatever the cache has; the bug is upstream.

**Scope.** Trace where the encoding hiccup happens:

1. **Source.** `capoeira/data/moves.json` — confirm the canonical move list carries the correct UTF-8 (it should; this is the seed data).
2. **Practice page.** `capoeira/assets/js/practice-event-submit.js::buildPracticeEventText()` and the signing path. Likely culprit if the payload is stringified through a code path that doesn't preserve UTF-8.
3. **Edgar (`sentiment_importer`).** The `[PRACTICE EVENT]` handler in `dao_controller.rb` and whatever lands the event into Telegram Chat Logs. If Edgar logs through a system that downgrades to Latin-1 anywhere, the diacritic dies there.
4. **GAS scanner.** The Apps Script that picks the event up from Telegram Chat Logs and persists it to lineage-credentials.
5. **lineage-engine build.** `build_cv_cache.py` reads the persisted event and writes the cache JSON. If the input file has the encoding hiccup, the cache will too.

**Acceptance.** A new practice session submitted today with `rolê` in a move name shows up on `truesight.me/programs/tribomirim/credentials/#pk-wR9zU8JMnEz1` (under the expanded session row) as `rolê`, not `rol?`. Confirm in at least one round-trip.

**Cost.** ~1-2 hours including reproduction + fix at the right pipeline layer.

**Blocker.** None. Cleanest path is to submit one fresh test session from the practice page with deliberately-diacritic-heavy move names, then inspect each pipeline stage's stored copy to find where the `ê` becomes `?`.

**Owner.** Unclaimed.

[cred-expand]: https://github.com/TrueSightDAO/truesight_me_beta/pull/128

---

### Credentialing: WhatsApp self-claim flow (deferred — held for demand signal)

**Context.** Surfaced 2026-05-19 in the ERA DAO WhatsApp thread with Bilal + Shahbaz. Butterfly Effect students (and capoeira-Tribomirimbahia students) identify primarily by WhatsApp number, not email. The existing `dapp.truesight.me/create_signature.html` email-based identity flow has no equivalent for these populations. A WhatsApp self-claim flow would let students assert "this pk-hash is me" against an issued credential at `truesight.me/credentials/#<slug>`.

**Scope.** Full design lives at `CREDENTIALING_PLATFORM.md` §13 — flow diagram, alternatives considered, 2026 Meta cost model (user-initiated reply is free, business-initiated push is billed), six-item Meta paperwork prerequisite list (legal entity → business verification → DAO-owned WA-eligible phone number → app + token + webhook), four-piece engineering scope (~2–3 days focused work behind ~1 week of Meta business verification), privacy invariants (`wa_phone_hash = sha256(cc + national)`, never raw number).

**Defer-flip criteria.** This is held — NOT a queue item — until *any one* of:
1. A student in any active program asks how to prove the credential is theirs.
2. A second program beyond BE + capoeira lands with WhatsApp-native participants (i.e. the pattern repeats and self-claim becomes infrastructure rather than feature).
3. BE / IVY acquisition by TDF closes with a contractual requirement for student-side attestation.
4. A receiving platform (employer, school, ceremony org, partner shop) starts checking credentials and asks for a "verified by holder" signal beyond the QR.

Until then the issued-credential surface (cert PDF + QR + public `/credentials/#<slug>`) is the demo. Don't pre-build the auth on speculation.

**Blocker.** No demand signal yet (2026-05-19). Building now would mean ~1 week of Meta business verification + a legal-entity decision on which WABA front to use — both real costs against zero current need.

**Owner.** Unclaimed. Next session that sees a defer-flip criterion fire should pick this up.

---

### Partner Check-in: paste-image-as-attachment (v0.2 attachment support)

**Context.** Operator request 2026-05-12: when filing a Partner Check-in (e.g. for the Matheus / AGL7 freight in flight), be able to **paste an image directly into the Notes field** and have it automatically uploaded as an attachment that the check-in history later renders inline. Use cases: container photos, customs paperwork, retail stencil photos on cacao bags, screenshots of vendor replies. The pattern exists already in adjacent surfaces (`[ASSET RECEIPT EVENT]` uses `--attachment`, `Stores Visits Field Reports` carries `github_raw_url`/`github_blob_url`); this just hasn't been extended to Partner Check-in yet.

**Scope.** Five-component build, each well-trodden:

1. **`dapp/partner_check_in.html`** — add a `paste` event handler on the Notes textarea. When clipboard contains an image blob, POST it to Edgar's `upload_file_to_github` tool, get back the `https://raw.githubusercontent.com/...` URL, and either (a) append it to the Notes text as a markdown image link, or (b) store it as a separate hidden field that ships in the submission payload. Recommend (b) — keeps Notes clean and the attachment a first-class field.
2. **Edgar payload** for `[PARTNER CHECK-IN EVENT]` — add an `Attachment URL: <raw_url>` line, same shape `[ASSET RECEIPT EVENT]` already uses.
3. **`tokenomics/google_app_scripts/find_nearby_stores/process_partner_check_in_telegram_logs.gs`** — extract the URL from the Telegram payload, write it to a new column on the Partner Check-ins tab.
4. **`Partner Check-ins` tab on Main Ledger** — add column O `Attachment URL` (one-time sheet edit + scanner update).
5. **`Shipping Planner` `get_partner_check_ins` action** — include the new column in returned rows. **Partner Check-in history UI** on `partner_check_in.html` — render the URL as a clickable thumbnail (image) or link (PDF) inline with each history entry.

**Acceptance.** Paste an image while filing a check-in for Matheus → submit → reopen the Partner Check-in form with `?partner_id=black-king-ilheus` → the just-filed entry shows the thumbnail in the Check-in History block.

**Caveats.**
- v0.2 limit: one attachment per check-in (matches every other Edgar event). Multi-attachment is a separate v0.3 ask.
- The auto-checkin-on-send (`runProcessSentPartnerPokes`) won't have attachments — the new column will be blank for `Submitted By = "Partner Poke Scheduler v0.1"` rows. No special handling needed.
- The DApp paste handler needs to be careful about clipboards that contain BOTH an image AND text (some screenshot tools do this). Prefer the image; ignore the text — let the operator type Notes themselves.

**Blocker.** None. Edgar's `upload_file_to_github` exists. `Stores Visits Field Reports` already proves the end-to-end pattern. Build is ~2-3 focused hours across the 5 components.

**Owner.** Unclaimed.

---

### Beer Hall daily digest: include Partner Check-ins section

**Context.** Operator request 2026-05-12: the daily Beer Hall digest currently summarizes commits, PRs, and ecosystem activity. Partner Check-ins are core supply-chain operations — they should appear in the digest too. Without this, the WhatsApp Beer Hall community can't see Gary's offline outreach activity (the same observability gap that motivated the original Partner Check-in build, but now applied to the broader community surface, not just LLM advisors).

**Scope.**

- Identify the script that generates the Beer Hall daily digest (`agentic_ai_context/OPENCLAW_WHATSAPP.md` documents the pipeline; the actual generator is in `content_schedule` or a related repo per the doc).
- Add a new data source: read the **Partner Check-ins** tab on Main Ledger via gspread (the credentials already exist for the advisory pipeline), filter to entries from the last 24 hours.
- Render a new digest section: "Partner Check-ins (last 24h): N entries", with a per-entry line `<partner_name> · <method> · <stock_status if relevant> · <notes excerpt>`. Match the existing Beer Hall digest's voice and density.
- Skip empty days — don't render the section if no check-ins happened in the window.

**Acceptance.** Tomorrow's Beer Hall digest includes a `### Partner Check-ins (last 24h)` section listing any entries Gary filed today. If no entries, the section is omitted.

**Blocker.** Beer Hall pipeline's LLM provider (Anthropic last week, possibly switched after the credit-zero incident on 2026-05-11) needs a working credit balance. Verify before building.

**Owner.** Unclaimed.

---

### Trees in Pipeline: finer-grained inventory tag for hybrid Operator partners

**Context.** Kiki's Cocoa is `partner_type=Operator` because she's a SF warehouse hub for some shipments AND handles online fulfillment to end consumers. Her **sales_monthly** is correct (only counts QR Code Sales, never restocks). But her **inventory_units** mixes bulk-warehouse stock (NOT yet financed → should NOT count toward Trees in Pipeline) with retail-ready stock (IS in pipeline → should count). The current filter (`market_research#122` deny-list of Freight Provider + Supplier) keeps Kiki's full inventory total, which slightly over-counts Trees in Pipeline.

**Scope.** Two paths to evaluate:

1. **Per-row inventory_type-based filter.** The Currencies sheet column distinguishes `Cacao Bean (Bulk)` vs `Cacao Mass (Retail Ready)` etc. Trees in Pipeline could sum only `Retail Ready`-format inventory. **Cleanest if the tagging is reliable.**
2. **Per-partner role tagging.** Add a sub-flag on `Agroverse Partners` like `inventory_role: bulk | retail | mixed`. For `mixed` partners, derive proportion from sales velocity. **More complex but handles edge cases.**

Pick path 1 if the inventory_type field on `partner_inventory` JSON is already reliable across all Operator-type partners; otherwise path 2.

**Acceptance.** Open `https://truesight.me/index.html`, Trees in Pipeline drops by Kiki's bulk-warehouse stock total. Sanity-check: the new total roughly matches the sum of inventory at strict-retail partners (Consignment + Wholesale) + the retail-ready portion of Operator-partner inventory.

**Blocker.** Need to verify the inventory_type tagging is consistent on the JSON before committing to path 1. Run `sync_sell_through_report.py` once and inspect Kiki's items[] block in the output JSON.

**Owner.** Unclaimed.

---

### Wire the DApp bell's action items into `ADVISORY_SNAPSHOT.md` generation

*(Scope broadened 2026-05-12 from the original "Wire `Partner Check-ins`…" entry, which had just the operator-scheduled cadence in view. The bell now aggregates three signal sources; the advisory should surface all three.)*

**Context.** The DApp notification bell (shipped 2026-05-12, see [`DAPP_NOTIFICATION_BADGE.md`](./DAPP_NOTIFICATION_BADGE.md)) aggregates three signal sources for the operator:

1. **Outbound Review** — drafts in `AI/Warm-up`, `AI/Follow-up`, `AI/Prospect Replied`, `AI/Partner Poke` cohorts (from `getWarmupReviewQueue`)
2. **Partner Check-in follow-ups** — operator-scheduled cadence (from `list_partners_needing_attention`)
3. **Partner Stock attention** — out-of-stock / low-stock / dormant (from velocity + inventory JSONs)

Today these surface only to Gary via the DApp. LLM advisors (Dr Manhattan, Seth Godin, I Ching oracle) reading `ADVISORY_SNAPSHOT.md` are blind to them — so they keep recommending action Gary's already on (e.g. "you should follow up with prospects" while 12 drafts sit in his queue waiting for review). The integration closes that loop: the advisory becomes a **client of the bell substrate**, surfacing the same operator-bottleneck signals to whoever's reading it.

**Voice locked in (Gary picked 2026-05-12).** Contemplative narrative — data woven into prose with explicit advisor guidance, matching the existing north-star framing at the top of the advisory. The integration MUST produce output of this shape, not a tabular Jira-dashboard:

```markdown
## Action items (where operator review or attention is the bottleneck)

_Same signals the DApp bell aggregates — surfaces what's actually
waiting on Gary, not raw queue depth. Refreshed daily._

**Outbound drafts awaiting send (22 total):** 12 warm-ups (avg 4d
old), 3 follow-ups (all ≥7d — these are stalling), 2 prospect replies
(time-sensitive — prospect already engaged), 5 partner pokes (3
partner-addressed, 2 self-reminders for partners without email).

**Partner check-in cadence (3 overdue or due):** Tech Spot (5d
overdue, last via In Person), Beanery (2d overdue, last via Email),
KiKi's Cocoa (due today, last via Phone). Cadence is operator-driven
— Gary picked these dates when filing each check-in.

**Partner stock signals (3 flagged):** Tech Spot is out of stock
(0 days runway). KiKi's Cocoa is running low (2 units, ~3 days).
Mountain Roastery has been dormant 67 days.

When advising on outreach priority, weight inversely by runway:
out-of-stock partners and prospect replies first; warm-ups can sit.
Treat the dormant set as questions about positioning, not just
restocks — they may need a different conversation.
```

The closing advisor-guidance paragraph should be **regenerated each day to fit that day's specific signals**, not stamped from a fixed template. A useful rule of thumb: when the signals concentrate in stock attention, lean on stockout urgency; when they concentrate in dormancy, lean on positioning/zeitgeist; when they concentrate in drafts, lean on prioritisation. Grok or whichever LLM the advisory generator already uses for its prose framing is the right tier for this.

**Scope.**

- Extend the snapshot generator (Python under `market_research/` or wherever `ADVISORY_SNAPSHOT.md` is built today) to call the three bell sources above. The advisory becomes a *client* of the bell substrate — same calls, no reimplementation of severity scoring.
- Add a new "Action items" section at the top of the operator metrics block (before "Operations health"), rendered exactly in the voice above. Use `list_partners_needing_attention` for cadence and `partners-velocity.json` + `partners-inventory.json` for stock — same data, same scoring rules, same naming as `partner_check_in.html`'s `computeAttentionList()` (so the advisory and the DApp page never disagree by drift).
- Resolve partner_id slugs to human names via `Agroverse Partners!E → Contributors contact information!A` — same join pattern `partner_poke_drafts.gs` uses.
- The advisor-guidance closer (last paragraph) should be regenerated daily by the same LLM the advisory already uses for prose framing.

**Blocker.** Build only **after Partner Poke Scheduler v0 has run for a full week of operator-confirmed calibration** (see [`PARTNER_POKE_SCHEDULER_v0.md`](./PARTNER_POKE_SCHEDULER_v0.md)). The week of real runs surfaces which signals actually drive operator action vs which add noise — those calibrations should be reflected in the rendered advisory before it goes to the oracle. Don't build against synthetic data.

**Acceptance.** Open the next refreshed `ADVISORY_SNAPSHOT.md` and confirm: (a) the "Action items" section is present at the top of operator metrics, in the contemplative-narrative voice above; (b) all three signal sources are surfaced (outbound drafts, partner check-in cadence, partner stock); (c) the closing advisor-guidance paragraph reflects that day's actual signal distribution, not boilerplate; (d) re-running the advisory through the I Ching oracle, Dr Manhattan, and Seth Godin visibly references the specific action items instead of recommending generic outreach.

---

### `dao_client onboard_retail_partner` CLI — v1: website + PR automation

**Context.** MVP shipped via [`dao_client#11`][onboard-mvp] on
2026-04-28 — automates the deterministic ledger + inventory steps
(§3.1 / §3.2 / §3.3 / §3.13 / §3.14 of
`RETAILER_TECHNICAL_ONBOARDING.md`) idempotently, with a YAML manifest
input. Dry-run by default. Operator still has to do the website surface
work + photo upload + PR creation manually after running it.

v1 fills in the remaining steps:

- §3.4 Partner page generation (clone `partners/lumin-earth-apothecary/`,
  named-replacement on slug + name + address + lat/lon + about-blurb;
  about-blurb either operator-supplied in manifest or Grok-extracted
  from `website` URL).
- §3.5 Discovery surface updates (`partners-data.js` append,
  `partner_locations.json` append, `wholesale/index.html` and
  `partners/index.html` alphabetical inserts,
  `cacao-journeys/pacific-west-coast-path/index.html` jpeg-extension
  conditional).
- §3.6 Photo download + resize (operator URLs in manifest, or fall back
  to scraping `og:image` / favicon).
- §3.12 + §3.15 Branch + commit + `gh pr create` in `agroverse_shop_beta`
  and `agroverse-inventory`. Push branch only — operator merges manually
  for the first 5–10 onboardings before flipping to auto-merge.
- §3.4 lat/lon geocoding via Nominatim (free, no key) when manifest
  doesn't include them.

**Acceptance criterion.** Next retail-partner onboarding takes ≤ 5
minutes of operator time end-to-end, including PR review + merge.

**Blocker.** None — every required piece exists. MVP must run cleanly
on a real onboarding before v1 layers on the more invasive automation
(template clone, multi-repo PR creation).

**Owner.** Unclaimed.

[onboard-mvp]: https://github.com/TrueSightDAO/dao_client/pull/11

---

### Eyeball-check `partners-velocity.json` numbers after 4 weekly refreshes

**Context.** First version of `sync_partners_velocity.py` shipped via
[go_to_market#80][velocity-pr] and the first JSON snapshot via
[agroverse-inventory#5][velocity-snap]. Refresh cadence is weekly. Per
Gary's §9 Q5 decision in `PARTNER_VELOCITY_PROPOSAL.md` ("wait till
settle"), no downstream consumer should *trust* the numbers until at
least **4 successful weekly refreshes** have run and a manual sanity
check has confirmed the values track operator intuition for 3–5 known
partners (Go Ask Alice, Lumin Earth, Edge & Node, Kiki's Cocoa).

**Outcome.** Either flip the green-light (wire dormant / high-velocity
signals into warm-up generator — see next entry), or file a defect on
the script if the numbers feel wrong.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read the latest committed snapshot.
- `market_research/scripts/sync_partners_velocity.py` — re-run locally if needed.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §9 Q5 (acceptance criterion).

**Blocker / signal to revisit.** Wait for ≥4 entries on the GitHub
Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible
acceptance check: **2026-05-25** (~4 weeks after first snapshot).

**Owner.** Gary (manual sanity check), then any agent for downstream wiring.

[velocity-pr]: https://github.com/TrueSightDAO/go_to_market/pull/80
[velocity-snap]: https://github.com/TrueSightDAO/agroverse-inventory/pull/5

---

### Wire dormant / high-velocity signals into warm-up draft generator

**Context.** Once `partners-velocity.json` numbers are trusted (see
previous entry), the warm-up draft generator
(`market_research/scripts/suggest_warmup_prospect_drafts.py`) and any
sibling check-in flow can read per-partner activity to:

- **Dormant retailer** (`last_sale_date > 90 days ago` and
  `last_restock_date > 90 days ago`) → trigger a check-in email
  instead of a generic warmup, or de-prioritize warmups for them.
- **High-velocity retailer** (per-SKU `*_12m_monthly_avg >
  category_medians[sku].monthly × N`) → flag as a candidate for
  case-study / testimonial / shelf-photo capture for `/wholesale/`.
- **Cold-start / newly-onboarded retailer**
  (`max(sample_size_*) < 3`) → no recommendation; default to
  category baseline.

**Outcome.** Tighter outreach prioritization without manual triage; a
small CSV-style "this week's flags" surface (sheet or Markdown) for
operator review.

**Files.**
- `market_research/scripts/suggest_warmup_prospect_drafts.py` —
  primary integration point.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic.
- `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` — tighten the
  status-transition rules once the signals exist.

**Blocker.** Previous entry (eyeball-check) must complete green.

---

### Rename "Agroverse Partners" sheet → "DAO Partners" + sweep consumers

**Context.** 2026-05-20: the Main Ledger tab `Agroverse Partners`
(`1GE7PUq-...` gid=1983902109) now holds rows whose `partner_type` is
`Operator`, `Supplier`, `Freight Provider`, `Manufacturer`, etc. — i.e.
the whole DAO partner ecosystem, not just retail/wholesale for the
Agroverse cacao brand. The name is now a misnomer; new operator-partner
onboards (Wayne @ UX.APP, 2026-05-20) make it more obviously so.

**Why it didn't ship inline.** A rename has cross-repo blast radius —
every consumer keys off the literal string `"Agroverse Partners"`. Doing
it as part of the Wayne onboarding PR would have ballooned the diff.

**Scope (single PR after the Wayne onboard PR merges).**
1. Rename the sheet tab `Agroverse Partners` → `DAO Partners` (gid is
   stable; gid-keyed consumers are unaffected).
2. Sweep every literal-string consumer. Known callers to grep first:
   - `dao_client/truesight_dao_client/modules/onboard_partner.py` —
     `PARTNERS_SHEET` constant.
   - `market_research/scripts/sync_partners_velocity.py` (if it reads
     the tab by name).
   - GAS handlers under `tokenomics/` that scan the Main Ledger.
   - DApp Partner Check-in scanner (`dapp/partner_check_in.html` →
     GAS handler) — confirm the worksheet name.
   - `agroverse_shop` discovery surfaces (`partner_locations.json`
     generator, if any).
   - `agentic_ai_context/RETAILER_TECHNICAL_ONBOARDING.md`,
     `PARTNER_CHECK_IN_IMPLEMENTATION.md`, and any other docs that
     name the tab.
3. Workspace-wide grep before declaring victory:
   `grep -r '"Agroverse Partners"' ~/Applications` and
   `grep -r "'Agroverse Partners'" ~/Applications`.

**Outcome.** Tab name reflects its actual scope; future operator /
freight / supplier onboards stop reading as "Agroverse cacao business"
by association.

**Files.** Main Ledger spreadsheet
`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, gid `1983902109`, plus
every caller surfaced by the grep sweep.

**Owner.** Unclaimed.

---

### Advisory ops-health v2: burn rate + days-of-cover at SF

**Context.** Ops-health v1 ([TrueSightDAO/go_to_market#77][pr77] +
[follow-up #78][pr78]) ships per-shipper stock from
`treasury-cache/dao_offchain_treasury.json`, cash float from `off chain asset
balance`, and in-transit freight from `Shipment Ledger Listing`. Burn rate /
days-of-cover at SF (Kirsten) was deliberately deferred — the structured
snapshot at `ecosystem_change_logs/ops_health/current.json` already reserves
two `null` slots: **`sales_velocity_30d`** and **`days_of_cover_at_sf`**.

**Outcome.** When v2 lands, the daily oracle / a future
`dapp/supply_health.html` page can flag a SKU with **🟢 ≥4 weeks cover · 🟡
2–4 weeks · 🔴 <2 weeks** at Kirsten — exactly the signal Gary is missing
today (*"Kirsten goes low before Matheus's freight inbound has arrived"*).

**Files / shape.**
- `market_research/scripts/generate_advisory_snapshot.py` →
  `_compute_ops_health(...)` returns the structured dict; add a peer
  `_compute_burn_rate_and_cover(treasury, qr_sales_rows)` that populates the
  two reserved slots and surface a few `🟢/🟡/🔴` lines in
  `_render_ops_health_markdown`.
- `QR Code Sales` window already loaded by `_fetch_sheet_sales_markdown` when
  `--with-sheet-sales` is on — pass the parsed rows through instead of
  re-reading.

**Join key.** Today the join between sales (per Currency string) and stock
(per `inventory_type` × `unit_format`) is brittle because **`inventory_type`
is only populated on ~28% of `dao_offchain_treasury.json` items as of
2026-04-27** (column added 2026-04-26; backfill in progress). Two paths:

1. **Conservative:** join on the raw `Currency` string (works today, exact
   match per batch — granular but noisy).
2. **Cleaner (preferred when ready):** join on `inventory_type` × `unit_format`
   once the backfill is meaningful (~>80% populated). Surface the same flag
   one level higher.

**Blocker / signal to revisit.** Check `inventory_type` sparseness on
`dao_offchain_treasury.json` before starting:

```bash
curl -sL https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/dao_offchain_treasury.json \
  | python3 -c '
import json, sys
d = json.load(sys.stdin)
items = [it for m in d.get("managers", []) for it in m.get("items", [])]
populated = sum(1 for it in items if (it.get("inventory_type") or "").strip())
print(f"{populated}/{len(items)} = {100*populated/len(items):.0f}% populated")
'
```

If <40%, do path (1) only. If >80%, go straight to path (2). In between, ship
path (1) and re-roll-up by `inventory_type` for the markdown summary.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks after v1
shipped, gives the backfill room).

[pr77]: https://github.com/TrueSightDAO/go_to_market/pull/77
[pr78]: https://github.com/TrueSightDAO/go_to_market/pull/78

---

### `two_bahia_bars` newsletter — post-send open / click / reply read-out

**Context.** First Agroverse newsletter to ship with the full pipeline ([buyer
exclusion][n-pr79], [JPG fallback + tighter image margins][n-pr84],
[side-by-side comparison row][n-pr85]) sent 2026-04-27 to **38 recipients**
(2 past-buyers excluded via `--exclude-buyers-of-substring` against
`Agroverse QR codes`). Tracking on by default — opens land in cols H–K and
clicks in L–P on the **`Agroverse News Letter Emails`** tab of the dedicated
newsletter workbook (`1ed3q3SJ8ztGwfWit6Wxz_S72Cn5jKQFkNrHpeOVXP8s`),
filtered by `campaign='two_bahia_bars'`.

**Why a follow-up reads the data.** The v5 layout (compact 280px images,
side-by-side comparison row at top) was a deliberate design call. Without a
read-out, the data sits in the sheet and the comparison-row decision can't
be validated for future sends. iOS Mail Privacy Protection inflates opens
in the first hour — the read-out should land **after a 7–10 day soak** so
real engagement (repeat opens, clicks, replies) dominates the noise.

**Outcome.** A short summary covering:
- Open rate (recipients with `open_count > 0`) and median `open_count`.
- Click rate (recipients with `click_count > 0`) and which CTA each clicker
  hit (`last_clicked_url` — Oscar's Farm, Fazenda Santa Ana, or both via the
  comparison row's separate "Check this bar" links).
- Reply rate (search Gmail `to:garyjob@agroverse.shop` against the
  recipient list; count distinct addresses that replied).
- **Did the comparison row's "Check this bar" CTA get clicked at a
  meaningfully different rate than the in-section "Check Oscar's Farm
  2024" / "Check Fazenda Santa Ana 2023" CTAs?** (Same destination URLs,
  different anchor text + position. Real design signal for whether the
  comparison row earns its keep on future two-SKU sends.)

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:two_bahia_bars'`,
   description includes the headline numbers).
2. A DAO contribution submission via **`dao_client`** with the analysis as
   the body and a link to the DApp Remarks row.

**Files / shape.**
- Recipient list keyed off `campaign='two_bahia_bars'` from
  `Agroverse News Letter Emails`.
- Open / click columns already populated by Edgar's
  `/newsletter/open.gif` and `/newsletter/click` endpoints.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<recipient> after:2026-04-27`.
- Sheet write: append to `DApp Remarks` on the Hit List spreadsheet
  (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); see
  `market_research/scripts/hit_list_dapp_remarks_sheet.py` for the helper.

**Owner.** Unclaimed. Earliest sensible: **2026-05-07** (10 days after the
send — opens / clicks have stabilized, replies have had a week to land).

**Optional adjacent work.** While reading the data, also note whether
either of the two excluded buyers (`pamelacotton7@msn.com`,
`toffees_fibrils.0l@icloud.com`) ever asked "why didn't I get the
newsletter about the bars I bought?" — would update the buyer-exclusion
copy in `AGROVERSE_NEWSLETTER_WORKFLOW.md` §4.3a if so.

[n-pr79]: https://github.com/TrueSightDAO/go_to_market/pull/79
[n-pr84]: https://github.com/TrueSightDAO/go_to_market/pull/84
[n-pr85]: https://github.com/TrueSightDAO/go_to_market/pull/85

### Warm-up email A/B read-out — PDF-only vs PDF+packaging-photos cohort comparison

**Context.** [`go_to_market#74`][wp-pr74] (merged 2026-04-27) flipped the
default warm-up email payload from "PDF wholesale catalog only" to "PDF +
2 packaging photos" for every send via the partner-outreach pipeline. The
hypothesis: visual product proof in the first touch lifts open / click /
reply rates over a PDF-only ask. Without a read-out, the change sits as
an untested intuition.

**Why a follow-up reads the data.** The cleanest natural experiment we'll
get — the cutover is sharp (one PR), the population is otherwise
homogeneous (same Hit List rows, same template, same operator), and the
volume on either side of 2026-04-27 should be enough for a directional
signal even if not statistically rigorous. Earliest sensible read:
**2026-05-11** (~2 weeks of post-cutover sends + replies have had time
to land — Gmail reply soak window matches the newsletter read-out
above).

**Outcome.** A short comparison covering, for each cohort:
- **Cohort split.** Read the `Email Agent Follow Up` tab of the Hit List
  workbook (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); split
  rows where status indicates a warm-up was sent into:
  - **Pre-2026-04-27** (PDF only) — sent before the cutover.
  - **On/after 2026-04-27** (PDF + 2 packaging photos) — the new default.
- **Metrics per cohort.** Count, open rate (`Open` column > 0), click
  rate (`Click through` column > 0), reply rate (cross-reference Gmail
  for inbound replies to each `to_email` after `sent_at`).
- **Time-controlled comparison.** Repeat the metrics restricted to the
  **2 weeks immediately before** vs **2 weeks immediately after**
  2026-04-27 to neuter time-of-year / list-quality drift.
- **Verdict.** Did packaging-photo warm-ups beat PDF-only on any of
  open / click / reply by a margin that would survive doubling the
  sample size? If yes — keep the new default. If no — flag whether to
  revert or keep as the cleaner UX call regardless of metrics.

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:warmup_packaging_photos_ab'`,
   description includes headline numbers + PR URL).
2. A DAO contribution submission via **`dao_client`** with the analysis
   as the body and a link back to the DApp Remarks row + PR #74.

**Files / shape.**
- Sheet read: `Email Agent Follow Up` tab on
  `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc` via
  `google_credentials.json` + gspread.
- Status / cohort inference: `market_research/HIT_LIST_CREDENTIALS.md`
  documents the Status column conventions.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<to_email> after:<sent_at>` per recipient.
- DApp Remarks append: `market_research/scripts/hit_list_dapp_remarks_sheet.py`.
- Contribution log: dao_client CLI per
  `agentic_ai_context/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`.
- Label / status convention: `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` §9.7.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks post-cutover).

**Why not `/schedule`.** Tried — remote agent can't access the private
sheet, Gmail OAuth, or Edgar tokens (no MCP connectors connected, no
`google_credentials.json` in cloud sandbox). Belongs on the local
backlog.

[wp-pr74]: https://github.com/TrueSightDAO/go_to_market/pull/74

### Migrate `dapp/stores_nearby.html` Add Store form onto the `[STORE ADD EVENT]` Edgar path

**Context.** The dao_client / Edgar / GAS slice of `[STORE ADD EVENT]`
shipped 2026-04-28 (see *Recently shipped* below). The DApp's
`stores_nearby.html` Add Store form still talks directly to GAS
`add_store` — small GET payload that doesn't have the cross-origin
failure mode the retail field report flow had, so it works, but the
DAO has decided that **all signed Hit List writes go through the same
canonical pattern**: DApp → Edgar → Telegram Chat Logs → async GAS
scanner. This entry is the remaining migration to that posture.

**What's needed.**
- Replace the direct `fetch(GAS, {action: 'add_store', …})` call in
  `dapp/stores_nearby.html` with a signed `[STORE ADD EVENT]` POST to
  Edgar (mirror today's `submitRetailFieldReportToEdgar` shape in
  `dapp/store_interaction_history.html`).
- Drop or repurpose the `add_store` action in
  `clasp_mirrors/1NpHrKJW…/Code.js` once no callers remain. The
  `addNewStore()` helper stays — it's the GAS scanner's own
  dependency.
- Verify the DApp form's "duplicate detected" UX still works
  (today the GAS direct call returned `{success: false, duplicate:
  true, existing_store: …}` synchronously; with the async path the
  duplicate detection lands on **Store Adds** col K
  `existing_store_shop_name`, so the form needs a polling /
  back-channel UX or a "submitted — check Hit List in a minute"
  message).

**Cost estimate:** ~30 min including the form's status / duplicate UX.

**Blocker.** None — purely additive once started. Don't bundle with
unrelated `stores_nearby.html` work.

**Owner.** Unclaimed.

### Deprecate `backfill_hit_list_opening_hours.py` + `backfill_hit_list_google_listing.py` after 2 cron cycles

**Context.** 2026-04-28 the two responsibilities — opening-hours grid (Mon
Open … Sun Close) and `Google listing` column — were folded into the routine
hourly cron at `.github/workflows/hit_list_enrich_contact.yml` (`35 * * * *`)
via [TrueSightDAO/go_to_market#88][pr88]. The enriched
`scripts/hit_list_enrich_contact.py` now also fills empty `Address / City /
State / Latitude / Longitude` from the same Places Details call. The two
standalone backfills still exist as manual one-shots but should no longer
need to be invoked routinely.

**Outcome.** Either delete the two standalone scripts, or shrink them to
thin documented wrappers that call into `hit_list_enrich_contact.py`'s
`apply_place_result_to_row_gaps()` helper for one-shot full-table sweeps.

**Files.**
- `market_research/scripts/backfill_hit_list_opening_hours.py`
- `market_research/scripts/backfill_hit_list_google_listing.py`
- `market_research/scripts/hit_list_enrich_contact.py` (already imports both
  via `bl` / `dl` for `resolve_place_id` + `append_place_id_to_notes` —
  if either backfill is deleted, inline the helpers it depends on or move
  them into a shared module).

**Verification before deleting.** On the Hit List, confirm:

1. New rows landing in the past 2 weeks have non-empty `Address`, `City`,
   `State`, `Latitude`, `Longitude`, `Monday Open`, `Google listing` (where
   Places returns those fields) within ~24h of arrival.
2. The `cron`-scheduled action's last 24 runs each show `filled>0` or a
   clean `skipped` count (i.e. the cron is closing gaps, not silently
   no-op'ing).

**Blocker / signal to revisit.** Earliest sensible: **2026-05-12** (~2
weeks of cron cycles after #88 lands).

**Owner.** Unclaimed.

[pr88]: https://github.com/TrueSightDAO/go_to_market/pull/88

---

### Validate the circle-hosting → cacao-velocity hypothesis after 4 partners-velocity refreshes

**Context.** 2026-04-28 observation: two recent / candidate retail partners
mention **women's circles** prominently — [The Way Home Shop in SE
Portland][way-home] (just onboarded) and Lumin Earth (existing partner).
Ceremonial cacao genuinely lives in that ecosystem (women's circles, sound
baths, breathwork, new-moon gatherings), so "hosts circles" is plausibly
a leading indicator of cacao sell-through.

The cheap detection step shipped immediately as
`market_research/scripts/detect_circle_hosting_retailers.py`
(see [go_to_market#XX][circle-pr] when filed) — it crawls each Hit List
retailer's `Website` for high-precision keywords (women's circle, moon
circle, cacao ceremony, sound bath, breathwork, sister/sacred circle,
ecstatic dance) and writes **Yes / Not detected** to a new
**Hosts Circles** Hit List column. *That* part is data-only; this entry
covers the deferred *correlation* check.

**Outcome.** Once `partners-velocity.json` has ≥4 weekly refreshes, cross-
reference per-SKU velocity against the **Hosts Circles** flag for
already-onboarded partners. Two questions:

1. Do circle-hosting partners outsell non-circle peers per-SKU at
   statistically meaningful margins? If yes, **green-light**:
   - Add `Hosts Circles=Yes` as a positive signal on the warm-up draft
     generator (next to the dormant / high-velocity logic in the existing
     entry above).
   - Open a separate research entry on whether to build a **circle
     facilitator** outreach motion (different ICP than retailers — direct
     to circle-leaders who buy in bulk for their gatherings).
2. If the correlation is weak or negative, rule it out and close.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read latest snapshot.
- Hit List **Hosts Circles** column (col after `Google listing`) — read.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic + sample-size guards.

**Blocker / signal to revisit.** Same as the **Eyeball-check
`partners-velocity.json`** entry above — wait for ≥4 entries on the
GitHub Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible:
**2026-05-25**. Combine with that entry's manual sanity check so
both reads happen in one sitting.

**Owner.** Unclaimed.

[way-home]: https://thewayhomeshop.com/
[circle-pr]: https://github.com/TrueSightDAO/go_to_market/pulls?q=is%3Apr+circle+hosting

---

### Fix `addNewStore()` GAS — `setValues`-dimension mismatch on tail-end step

**Context.** `[STORE ADD EVENT]` end-to-end test 2026-04-28 (see *Recently
shipped*) added 3 referrals for Psychic Sister (Clary Sage / Casa de Ritual
/ La Sirena Botanica) — all three landed on Hit List rows 526–528 with the
correct shop name / status / city / state / shop type / Notes / Sales
Process Notes / Status Updated By / Status Updated Date / Store Key.

But every single submission also recorded `status: error` on the **Store
Adds** dedup log with this error message:

```
The number of rows in the data does not match the number of rows in the
range. The data has 1 but the range has 526.
```

That's an Apps Script `setValues(values)` dimensional error from inside
`addNewStore()` (likely the trailing `logDappSubmission_(...)` call or a
sales-notes write). It throws **after** the new Hit List row has been
fully written (since the row is correct), so the data is fine — but the
exception escapes addNewStore's try/catch boundary and lands in the new
GAS scanner's error handler.

**Symptoms.**
- Hit List rows land correctly (operator-visible).
- Store Adds dedup log says `error` with this message (audit-trail-misleading).
- A re-fired Telegram Chat Logs row would NOT re-add (idempotent on
  Telegram Update ID), so no double-row risk.

**Fix targets.**
1. **Root cause** in `clasp_mirrors/1NpHrKJW…/Code.js` `addNewStore()` /
   `logDappSubmission_()`. The `526` figure is "all data rows on the Hit
   List sheet"; somewhere a `range.setValues(arr)` is being called with
   `arr.length === 1` against a range covering all data rows. Likely
   pattern: `sheet.getDataRange().setValues([row])` instead of
   `sheet.appendRow(row)` / `sheet.getRange(targetRow, 1, 1, n).setValues([row])`.
2. **Defensive workaround** in
   `google_app_scripts/find_nearby_stores/process_store_adds_telegram_logs.gs`:
   when `addNewStore` throws, fall back to a Hit List lookup by
   `store_key` (the same key `createStoreKey_` builds). If found,
   record `status: added_with_warning` + the exception text in
   `error_message` instead of `status: error`. That way the audit log
   correctly reports the row was added even when addNewStore's tail
   step fails.

**Cost.** ~20 min for (1) once the offending line is found; ~10 min
for (2). Both are independent — do (2) first if you want clean audit
trails fast; do (1) if you want addNewStore stable for the existing
DApp form callers.

**Owner.** Unclaimed.

---

### Extend iching_oracle advisory with QiMenDunJia overlay

**Context.** Today (2026-05-09) we agreed the I-Ching cast and a QMDJ chart
are complementary lenses on the same moment T — I-Ching tells you the
quality of the moment (via random selection from coin throws), QMDJ tells
you the spatial / strategic structure of that same moment (deterministic
from the timestamp). Pairing them on the same T gives the DAO advisor two
classical frameworks reading the same instant: I-Ching as the narrative /
transformational layer, QMDJ as the spatial / strategic overlay. Honest
disclaimer: combining them is a *modern synthesis*, not a traditional
practice; the UI and the GAS prompt should both flag this.

**Spec.** Full design lives in [`ICHING_QMDJ_EXTENSION.md`][qmdj-spec].
Summary:

- **Library.** `lunar-javascript` (6tail family). Drops in cleanly to the
  static-site / `gas/` stack. Don't reimplement.
- **Client.** After coin throw at moment T: also compute the QMDJ chart
  from T (Ju, Six Yi, Three Wonders, Heaven/Earth Plates, Doors, Stars,
  Spirits) and POST alongside the hexagram + changing lines.
- **GAS.** Extend `oracle_advisory_bridge.gs`:
  - `extractDraw_` += `qmdj_chart` field.
  - `staticContext` += new `QMDJ_FRAMEWORK_REFERENCE.md` (cached — what
    the doors/stars/spirits/wonders mean, what counts as auspicious).
  - `dynamicContext` += per-call QMDJ chart block for moment T.
  - `ORACLE_PROMPT_HEADER` adds two new output sections (QMDJ
    configuration of this moment, Combined frame) and extends section 7
    (decisive action) to use QMDJ's directional / timing signal when one
    is present, otherwise to honestly say the chart doesn't surface a
    strong directional read.
- **Caching.** The new framework reference is static across calls and
  belongs in the cached system block — keeps marginal token cost
  reasonable.
- **UI.** Render QMDJ as a *collapsible* "Extended Reading: QiMenDunJia"
  section below the I-Ching reading, not above it. I-Ching narrative
  stays the primary surface.

**Implementation order.** Three independently testable PRs (not one):

1. **Smoke-test lunar-javascript locally**, then wire chart casting +
   9-palace render into the client. No GAS changes yet.
2. **Land `QMDJ_FRAMEWORK_REFERENCE.md`** in `agentic_ai_context` and
   extend `oracle_advisory_bridge.gs` to fetch + include it.
3. **Refine `ORACLE_PROMPT_HEADER`** sections after seeing live output;
   tune the "no clear signal" fallback language so the LLM doesn't
   fabricate directional advice.

**Cost.** Probably 60-90 min per PR. Total ~3-4 hours of focused work
across the three.

**Risks worth re-reading from the spec before starting.** Information
overload, two-oracles-stapled-together coherence, naive
auto-interpretation, modern-synthesis disclaimer. All addressed in the
spec; don't skip the "Risks / things to be careful about" section.

**Owner.** Unclaimed.

[qmdj-spec]: ./ICHING_QMDJ_EXTENSION.md

---

### krake_browser engine implementation (post-scaffold)

**Context.** Three repos scaffolded 2026-05-20:

- [KrakeIO/krake_browser](https://github.com/KrakeIO/krake_browser) — engine (Sinatra + Playwright/CDP), currently README + ARCHITECTURE + DSL only
- [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) — generic public recipes (WhatsApp send_message, LinkedIn connect_request, Instagram login, FDA facility_search) + JSON Schema
- [TrueSightDAO/tdg_recipes](https://github.com/TrueSightDAO/tdg_recipes) — DAO-specific recipes (partner_followups/check_in, edgar/submit_contribution)

All three are **PRIVATE** — flip to PUBLIC only after the engine works end-to-end and we have a recorded demo.

Vision: persistent local Chromium that human + LLM share. LLM drives recipes via CDP; pauses with `human_intervention` for 2FA, approvals, anti-bot, judgment calls. Direct evolution of the Krake.io DSL (2014) — `solve_captcha` generalized into `human_intervention` with a prompt + ack channel + screenshot.

See `~/Applications/krake_browser/{README,ARCHITECTURE,DSL}.md` for the design (or the same files on the public repo once it's flipped public).

**Scope (engine MVP).** Implement against ARCHITECTURE.md:

1. `bin/krake_browser_launch` — Chromium launcher with `--user-data-dir=$HOME/.krake_browser/profile --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1`.
2. Sinatra app that attaches to running Chromium via CDP (`playwright-ruby-client` is the natural choice given krake_sinatra's stack).
3. Recipe loader: reads JSON from a configurable `--recipes-dir` (default: local clones of both recipe repos).
4. Recipe executor: walks `actions[]`, dispatches each action via Playwright, suspends on `human_intervention`.
5. MCP server tools: `run_recipe(name, vars)`, `list_recipes()`, `ack_intervention(token, action, payload?)`.
6. MCP events: `intervention_required` (prompt + screenshot + token), `recipe_progress`.
7. Localhost-only binding + token auth on the MCP port. Engine refuses to start if `0.0.0.0` detected anywhere.
8. Reference CLI client: minimal Ruby script connecting to MCP, invoking one recipe, printing intervention prompts to stdout and reading ack from stdin (for testing without a full chat UI).

**Validation criterion.** Run `whatsapp/send_message` against Gary's logged-in WhatsApp Web from any MCP client — recipe pauses for approval of the drafted message, human types Continue, message sends.

**Scope addendum (Gary 2026-05-20).** Items 9–10 land alongside the MVP. **Items 11–13 are engine v0.2** — defer until items 1–10 validate end-to-end (run `whatsapp/send_message` against live WhatsApp Web with one human approval). v0.2 turns the engine from "runs strict recipes" into "self-healing browser concierge" and is where the project becomes meaningfully differentiated; trying to ship it in the MVP will stall the WhatsApp demo. The v0.2 items also compound — guideposts (item 11) need the teach-loop (item 12) to repair drift, and passive observation (item 13) is strictly better than narration so ship 13 as part of 12 if it's not much more work.

9. **Bundle krake_recipes with engine install.** The TDG engine instance should come with platform recipes (Instagram, LinkedIn, WhatsApp, Facebook, FDA) pre-available, not require a separate clone step. Implement as a postinstall clone + scheduled `git pull` of [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) into `~/.krake_browser/recipes/krake_recipes/`. Recipes for living sites drift on their own cadence; pull beats pin.
10. **Wrapper-recipe DSL extension for tdg_recipes.** Add three new fields to the recipe schema so a TDG recipe can be a thin layer over a platform recipe:
    - `uses` — path to the platform recipe (e.g. `instagram/dm_send`)
    - `why` — one-paragraph DAO context the LLM reads before deciding to invoke (e.g. "partner check-ins for stores whose primary channel is IG, not WhatsApp — confirm last touch in Hit List first")
    - `vars` — DAO-specific variable defaults that get merged into the platform recipe's variable substitution
    
    Primary use case Gary identified: **partner check-ins** (the load-bearing operational flow) across WA / IG / LinkedIn / FB depending on partner's primary channel. The `why` field becomes the LLM's decision input.

11. **Guidepost model — intent + hint + expected_state alongside strict selectors.** Each action in the DSL gains three optional fields that turn it from a rigid click-here-then-click-there contract into a guidepost the LLM can re-ground at runtime:
    - `intent` — what this step is trying to accomplish ("Open connect-with-note modal")
    - `hint` — natural-language locator advice for the LLM if the strict selector fails ("Click 'Connect'; if hidden, it's under the 'More' button")
    - `expected_state` — observable post-condition the executor checks before moving on ("Textarea for personal note is visible")
    
    Execution order: try `dom_query` / `xpath` first (fast, deterministic, no LLM call). If it returns nothing or `expected_state` doesn't match, escalate to LLM-grounded discovery using `intent` + `hint` (Browser Use / Stagehand semantics — feed the LLM a trimmed accessibility tree, ask for the right element). Strict and flexible coexist in the same recipe; you only pay the LLM cost when the cheap path breaks.

12. **Teach-by-narration loop — continuous DOM repair via human-AI symbiosis.** The mechanism that makes selector drift self-healing instead of silently breaking recipes. Three new MCP tools beyond the MVP set:
    - `read_page_state()` → current URL + serialized DOM (or trimmed accessibility tree) + screenshot. Gives the LLM eyes onto the current tab.
    - `narrate_action(text)` → operator types what they just did manually ("I just clicked the new Connect button, it's now under the three-dot menu"). LLM keeps it as context.
    - `propose_recipe_update(name, patch)` → LLM emits a JSON patch against the recipe and opens it as a PR to krake_recipes or tdg_recipes. Gary reviews + merges; the next scheduled `git pull` makes the fix canonical.

    End-to-end loop: strict selector fails → engine fires `human_intervention` with "I lost the connect button" → Gary does the step manually → narrates → LLM reads page state → drafts a PR with the new selector → Gary merges → next run works. This is the differentiator vs. every other browser-automation tool (which break silently on DOM change). Without this loop, krake_browser is just another Stagehand clone; with it, it's a tool that gets *more reliable over time* through use.

**Blockers.** None. PAT for KrakeIO push lives in `~/Applications/truesight_autopilot/.env` as `KRAKEIO_LLM_PLAYGROUND_PAT`. Use it via `GH_TOKEN=$(grep ^KRAKEIO_LLM_PLAYGROUND_PAT= ~/Applications/truesight_autopilot/.env | cut -d= -f2-)`.

**After engine works.** (a) Flip the 3 repos to PUBLIC, (b) record 30s screencap of the WhatsApp demo, (c) write blog post on `garyjob/blog` (HN explicitly skipped as launch venue — Gary called it "kinda lame"; risk of flop > upside, garyjob/blog has zero downside and can cross-post later if organic traction appears).

**Owner.** Unclaimed.

---

## Recently shipped

### `/aum` dedicated page + per-ledger click-through on `/treasury` — 2026-05-20

Mirrors the `/treasury` pattern shipped earlier same day. New `/aum`
page reads `treasury-cache/dao_offchain_treasury.json` and renders
two sections — **Assets by ledger** first (each managed ledger
expanded to show currencies it holds), then **Per currency** (each
currency expanded to its per-ledger split). Both `/aum` and
`/treasury` per-ledger rows are now click-throughs to the source
Google Sheet, via a new `ledger_urls` dict in the GAS
`treasury_breakdown` payload. Landing-page AUM card flipped from
inline `<details>` to `View breakdown →` link; the dead
`wireStatBreakdowns` / `fetchTreasuryCacheOnce` / `renderUsdTreasuryBreakdown` /
`renderAumBreakdown` machinery (~85 lines) was removed from
`index.html`.

GAS also picked up a small `&refresh=1` escape hatch on the
`treasury_breakdown` endpoint for warming the cache after schema
changes without waiting for the cron.

PRs:
- TrueSightDAO/tokenomics#304 (squash `2640d1e`, GAS deploy `@10`)
- TrueSightDAO/truesight_me_beta#134 (squash `26947f7`, prod cherry-pick `25a6a9e`)

### `dao_client onboard_retail_partner` MVP — 2026-04-28

Manifest-driven CLI that automates the deterministic ledger + inventory
steps from `RETAILER_TECHNICAL_ONBOARDING.md` §3:

- Step 1 `[CONTRIBUTOR ADD EVENT]` (with name pre-formatted as
  `<First> - <Store>` to dodge Edgar's auto-rename).
- Step 2 `Contributors!U` (Mailing Address). Explicitly does **not**
  toggle col T — that flag is reserved for online-fulfillment managers
  (Gary + Kirsten only).
- Step 3 `Agroverse Partners` row append.
- Step 13 `[INVENTORY MOVEMENT]` loop for opening-order QR codes.
- Step 14 subprocess `sync_agroverse_store_inventory.py` and
  `sync_partners_velocity.py` so JSON snapshots refresh.

Idempotent at every step. `--dry-run` is the default. Worked-example
manifest in `examples/onboarding/the-way-home-shop.yaml` replays the
2026-04-28 onboarding as a no-op.

Steps still operator-manual in MVP: partner page, discovery surfaces,
photo download, PR creation (steps 4 / 5–10 / 11 / 12 / 15). Script
prints copy-paste instructions at the end. v1 covers those — see the
remaining Pending entry above.

PR: https://github.com/TrueSightDAO/dao_client/pull/11

---

### `[STORE ADD EVENT]` canonical pattern (additive slice) — 2026-04-28

Signed Hit List adds now route through the same Edgar pattern as retail
field reports: dao_client / DApp signs `[STORE ADD EVENT]` → Edgar
`/dao/submit_contribution` → Telegram Chat Logs → `WebhookTriggerWorker`
fires `processStoreAddsFromTelegramChatLogs` GAS scanner → `addNewStore`
on Hit List + audit row on **Store Adds** dedup log
(`1qbZZhf-…`, gid 1208101506; col B `telegram_update_id` is the dedup
key). Verified end-to-end: 3 Psychic Sister referrals (Clary Sage,
Casa de Ritual, La Sirena Botanica) added as Research rows on Hit List
rows 526–528 with referral provenance in Notes + Sales Process Notes;
scanner replay = 0/0/0/0 (perfectly idempotent).

Two follow-ups split out into Pending above:
1. Migrate `dapp/stores_nearby.html` Add Store form off the legacy
   direct GAS GET onto the same Edgar path.
2. Fix the pre-existing `addNewStore()` GAS `setValues` dimensional
   bug so audit logs say `added` instead of `error` even though the
   actual Hit List rows write correctly.

PRs:
- TrueSightDAO/dao_client#9 — `add_hit_list_store.py` module.
- TrueSightDAO/sentiment_importer#1042 — Edgar `[STORE ADD EVENT]` branch.
- TrueSightDAO/tokenomics#250 — `processStoreAddsFromTelegramChatLogs`
  GAS scanner + Store Adds tab schema.

---

## tribomirimbahia Phase 1B — music library tagging

**Context:** Phase 1A done 2026-05-10 (TrueSightDAO/tribomirimbahia#2) — 39 Bico
Duro per-move clips published. Phase 1B is the next sequential step before the
Phase 2 site can do session generation.

**Scope:** Build `tribomirimbahia/data/music_library.json` per spec §5 + §3:

- 12 capoeira tracks (Gary curates the YouTube URLs).
- Per track: `id`, `title`, `youtube_url`, `duration_seconds`, `bpm` (estimate
  via `librosa` or DeepSeek tap), `tempo_category` (Slow/Medium/Fast),
  `style_notes` (berimbau-heavy, drums-focused, etc.).
- Suggested mix: 3–4 slow berimbau (Foundation/warm-up), 4–5 medium drum-heavy
  (Defense/Attacks), 2–3 fast energetic (Aerials/Floreios).

**Hand-off:** Per `AGENT_BRIEF.md` matrix — BPM detection + tagging is DeepSeek
territory (numeric, no cultural nuance). Gary spot-checks the tempo arc since
it affects practice feel.

**Blocker:** Gary needs to curate the 12 YouTube URLs first.

## tribomirimbahia Phase 2 — capoeira.agroverse.shop site build

**Context:** Phase 1A produced `tribomirimbahia/data/moves.json` (39 moves with
YouTube URLs); spec PDF + AGENT_BRIEF.md describe the static-site requirements.

**Scope:** Greenfield build of `~/Applications/capoeira/` (currently empty)
following the AGENT_BRIEF.md "Phase 2 — Core Site Build" section. Mirror
agroverse_shop conventions (no frameworks, static HTML/CSS/vanilla JS).
Mandatory: `agentic_ai_context/DAPP_PAGE_CONVENTIONS.md` for every page.

**Hand-off:** Claude drafts pages; Gary reviews landing copy + Bahia tone before
flipping DNS. The 4 open questions in AGENT_BRIEF.md "Open questions before
Phase 2" need Gary's answers first (deploy target, Stripe account, Bico Duro
consent, fundraising goal).

**Blocker:** Open questions in AGENT_BRIEF.md not yet answered.

## capoeira: curriculum-based session structure

**Context:** Practice tool at `capoeira.agroverse.shop/practice.html`. Phase 1A
shipped (39 moves), data calibrated for 45-min single-theme sessions in
TrueSightDAO/capoeira#7. But Bico Duro's actual teaching (per his spoken
curriculum in cqKMvYbB1Kw — "primeira coisa: ginga; segunda coisa mais
importante: defesa; terceira coisa: ataque") is NOT single-theme; it's
Foundation → Defense → Attacks progression every session.

**Scope:** Add an alternative session-generation mode that composes:
1 Ginga warm-up (Foundation) + 2 Defense moves + 2-3 Attack moves +
optional Flow cool-down (Giro). This un-skips the Foundation and Flow
themes (currently filtered out because they have <4 moves each) and aligns
the practice tool with how Bico Duro actually teaches.

**Where to edit:** `assets/js/session-generator.js` — add a `pickCurriculumSession()`
alongside the existing single-theme path. Add a UI toggle on `practice.html`
("Single-theme drill" vs "Curriculum session"). Default to curriculum once
implemented.

**Blocker:** None — calibrated data + working single-theme algorithm both
shipped TrueSightDAO/capoeira#7.

## capoeira: session-generator algorithm variety

**Context:** Same Phase 1A practice tool. Current `pickMoves()` is greedy on
weighted score; with identical difficulty bias, sessions 1 and 4 in the headless
simulation were byte-identical (same 6 Beginner Attack moves in the same order).

**Scope:** Add randomized tie-breaking — group candidates by `_weight` bucket,
shuffle within bucket, then pick. Or sample with weighted probability rather
than sort+head. Keeps the difficulty bias intent but diversifies outputs.

**Where to edit:** `assets/js/session-generator.js` `pickMoves()` greedy loop.

**Blocker:** None.

## Closed without shipping

_(empty — move entries here with a one-line reason when they're no longer
relevant)_
