# EVENTS — cacao event activation playbook

How Agroverse runs a **cacao event activation** (showing up at a conference /
forum with ceremonial cacao + tea, a placard, and provenance QR codes), and
how those events are tracked so any LLM session can pick one up cold.

**Where everything lives:** `TrueSightDAO/go_to_market` repo → `events/`
(cloned locally at `~/Applications/market_research/events/`).

---

## 1. Read this first: the machine index

`events/index.json` is the aggregated, date-sorted index of every event,
embedding each event's full metadata. **An LLM should read it before touching
any event folder.** It is *generated* — never hand-edit it.

- Source of truth = each `events/<slug>/event.json`.
- Regenerate: `python3 events/build_index.py` (self-relative; run from anywhere).

## 2. Folder anatomy

```
events/
  index.json              # generated aggregate (read first)
  build_index.py          # regenerates index.json from the event.json files
  README.md               # short human pointer
  <slug>/                 # one per event, e.g. sftechfestjune26/
    event.json            # per-event source of truth (machine-readable)
    EXECUTION_CHECKLIST.md # phased working surface (check items as done)
    proposal*.md          # plan-of-record
    implementation_roadmap.md
    field_assets.md       # (optional) placard / table-tent / sticker / card copy
```

`<slug>` convention: lowercase event name + month + day, e.g.
`dualtechsummitjune26`, `sftechfestjune26`, `onsenglobalforumjune23`.

## 3. `event.json` schema (schema_version 1)

```jsonc
{
  "schema_version": 1,
  "slug": "sftechfestjune26",
  "name": "SF Tech Fest 2026",
  "status": "planning",          // planning | confirmed | done | cancelled
  "status_note": "one-line where-it-stands summary",
  "date": "2026-06-12",          // ISO; index sorts on this
  "end_date": "2026-06-12",
  "start_time": "11:00",         // or null
  "end_time": "17:00",           // or null
  "timezone": "America/Los_Angeles",
  "venue": "ICC, 525 Los Coches St, Milpitas, CA 95035",
  "city": "Milpitas, CA",
  "host": { "name": "Soniya", "org": "SF Tech Fest" },
  "format": "what we serve and how (flasks/cups/self-serve/basket...)",
  "products": ["Oscar's ceremonial cacao (Bahia)", "Paulo's cacao tea (Pará)"],
  "qr_codes": [
    { "id": "SFTF_CC_2026", "landing": "agl4", "product": "Oscar's ceremonial cacao", "status": "pending" }
  ],
  "owner": "Gary",
  "next_milestone": { "phase": 0, "due": "2026-06-05", "what": "..." },
  "reminders": { "apple_reminder": true, "apple_calendar": "Work", "check_in_date": "2026-05-27" },
  "docs": { "checklist": "EXECUTION_CHECKLIST.md", "proposal": "proposal.md", "roadmap": "implementation_roadmap.md" },
  "links": { "luma": "https://luma.com/..." }
}
```

`build_index.py` adds a `"path": "<slug>"` field to each event in the index.

## 4. Phase convention (the EXECUTION_CHECKLIST.md spine)

Every event checklist follows the same arc — adapt the specifics, keep the shape:

| Phase | What | Owner |
|---|---|---|
| 0 | **Confirm with the host** (date, table/placement, self-serve vs. pour, passes, shoutout) | Gary |
| 1 | **QR codes + placard/labels** (mint codes, design print assets) | Claude |
| 2 | **Dry run** — print a test, scan both QRs, confirm opt-in lands in subscribers tab — **this is a gate; nothing prints until it passes** | Claude |
| 3 | **Print + prep** (print placard, pull cacao, log `[INVENTORY MOVEMENT]`, pack kit) | Gary |
| 4 | **Event day** (setup, midday check, teardown, photos) | Gary |
| 5 | **Immediate post-event** (verify signups, add leads to Hit List) | Claude + Gary |
| 6 | **Follow-up + story** (manager follow-ups, thank-you to host, optional essay) | mixed |

Each checklist ends with a per-phase follow-up table; those follow-ups are
**internal team reminders**, tracked in `agentic_ai_context/OPEN_FOLLOWUPS.md`
— *not* `dao_client check_in_partner` (that tool is for inventory-carrying
retail partners, not event hosts).

## 5. QR naming convention

`PREFIX_<CC|CT>_<YYYY or YYYYMMDD_n>` → an AGL shipment landing page:
- `CC` = ceremonial cacao → **agl4** (Oscar's Farm, Bahia)
- `CT` = cacao tea → **agl8** (Paulo's Farm, Pará)
- Promo/display codes are minted as `SAMPLE` status.
- Codes are generated with the canonical batch tool and published to
  `TrueSightDAO/lineage-assets` (`qrs/<id>.json` + `pngs/<id>.png`). See
  `AGROVERSE_QR_CODE_BATCH_GENERATION.md` and `LINEAGE_ASSETS.md`.
- The scan target carries UTM: `?utm_source=event&utm_medium=qr&utm_campaign=<slug-tag>`.
- The opt-in path rides the existing agl4/agl8 shipment pages (consent
  checkbox → `Agroverse News Letter Subscribers` tab), not a new event page.

## 6. Apple Reminder + Calendar check-in convention

For each event, the Phase 0 **host check-in** is mirrored to the operator's Mac
so it doesn't get lost (created via `osascript`):
- An **Apple Reminder** titled `📞 Confirm <Event> logistics with <Host> (Phase 0)`,
  due on the `check_in_date`, body = the Phase 0 questions + a pointer to the
  checklist file (which holds the ready-to-send draft message).
- A matching **Apple Calendar** event on the **Work** calendar with alerts
  24h-before and at-start.
- Record this in the event's `event.json` `reminders` block.

Reminders app's AppleScript bridge is slow — wrap writes in
`with timeout of 540 seconds`, and run reads/updates as separate calls.

## 7. Adding a new event (checklist)

1. `mkdir events/<slug>/`; write `EXECUTION_CHECKLIST.md` (copy the phase spine), `proposal.md`, `implementation_roadmap.md`.
2. Write `events/<slug>/event.json` (schema above).
3. `python3 events/build_index.py` → regenerates `index.json`.
4. (If Phase 0 outreach is imminent) create the Apple Reminder + Calendar check-in; set `reminders` in `event.json` and re-run the generator.
5. Commit via PR → merge (per the `~/Applications` git flow).

---

*Created 2026-05-26 by Claude (Anthropic). Sibling docs: `LINEAGE_ASSETS.md`,
`AGROVERSE_QR_CODE_BATCH_GENERATION.md`, `CMO_SETH_GODIN.md`, `OPEN_FOLLOWUPS.md`.*
