# Content Marketing Schedule — canonical reference

> **The forward-looking content calendar for Agroverse / TrueSight DAO.**
> One row per planned post or article, forward-planned to **Aug 2027**.
>
> **Authoritative schema:** `tokenomics/SCHEMA.md` **§5**.
> This file exists so the sheet is discoverable from `agentic_ai_context` — the documented
> first stop for AIs — because the schema lives in a *different* repo and was not findable here.

---

## 1. The sheet

| Field | Value |
|---|---|
| **Spreadsheet ID** | `1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ` |
| **URL** | https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit |
| **Title** | `20250924 - Instagram Content Marketing Schedule` |
| **Owner / custodian SA** | `agroverse_ledger_manager` |
| **Access** | see §5 below — **not** readable via the `read_google_sheet` tool |

### What it is (and is not)

It is the **demand side** of the content pipeline: *what content should exist, and when*.

It is **not** the supply side. The split, per `tokenomics/SCHEMA.md` §5:

| Side | Document | Answers |
|---|---|---|
| **Demand** | **this file** / the sheet | What content should exist, and when |
| **Supply** | `MEDIA_ARCHIVE_PIPELINE.md` | What real media we actually hold |
| **Generation** | `sops/GENERATED_MEDIA_SOP.md` | How to derive assets from that supply |

---

## 2. Live state of the sheet

Verified by reading the sheet directly on **2026-11-10** (not copied from the schema):

| Check | Value |
|---|---|
| Tabs | **9** |
| `Instagram Content Schedule` rows | **315** (incl. header → 314 planned posts) |
| Columns (Instagram tab) | **14** (A–N) |
| `Post Day` span | `20250928` → `20270806` |

If these numbers have drifted substantially, re-verify before trusting the plan.

---

## 3. Tabs

| Tab | gid | Header? | Purpose |
|---|---|---|---|
| `Instagram Content Schedule` | 1682511679 | yes | **Primary** — 314 planned posts, 14 cols (A–N) |
| `Agroverse Blog Content Schedule` | 1735486924 | yes | 16 rows, 16 cols (carries Wix Draft IDs) |
| `TrueSight Blog Content Schedule` | 534758277 | yes | 2 rows, 17 cols (adds `Markdown Source`) |
| `Linkedin Content Schedule` | 480257671 | **no — empty** | Reserved, header never written |
| `Email Newsletter` | 1613728523 | **no — empty** | Reserved, header never written |
| `Feedback on Content` | 497764730 | yes | 18 rows — community feedback on published content |
| `Hashtag suggestions` | 0 | yes | Hashtag database |
| `Sample target profiles` | 1457421718 | yes | Audience research |
| `Configuration` | 814523764 | yes (9 frozen rows) | Status vocabulary + companion URLs |

---

## 4. Column schema — `Instagram Content Schedule` (row 1, frozen: 1 row × 2 cols)

| Col | Name | Type | Notes |
|---|---|---|---|
| A | `primary_key` | String | 8-hex content hash — **stable row identity**. `sync_content_schedule.py` matches on this and never overwrites B |
| B | `status` | Enum | `PLANNED` → `CRAFTING` → `SCHEDULED` (vocabulary in the `Configuration` tab) |
| C | `Week` | String | `Week 61` — a **monotonic counter, not an ISO week** |
| D | `Date Range` | String | `Nov 05-Nov 11, 2026` — display only |
| E | `Theme Focus` | String | Weekly umbrella theme |
| F | `Post Day` | String | **`YYYYMMDD`** e.g. `20261110` — *not* a date type |
| G | `Day of Week` | String | Denormalised from F |
| H | `Post Type` | Enum | `Reel` (~235) · `Carousel` (~79) |
| I | `Theme` | Enum | `Behind-the-Scenes` · `Recipes & Rituals` · `Regenerative Farming` · `Cacao Education` · `Community Impact` |
| J | `Description` | String | Post brief — ⚠️ **largely templated** (112 unique of 314; top 3 templates repeat 51× each) |
| K | `Caption` | String | Draft caption (314/314 populated) |
| L | `Hashtags` | String | Space-separated tag block |
| M | `CTA` | String | Call to action |
| N | `Tool Suggestions` | String | Pre-generation vocabulary — uniformly `CapCut…; Canva…; Instagram Native for scheduling`. Predates `GENERATED_MEDIA_SOP.md`; does not yet name Seedance/Seedream |

---

## 5. Access — read this before concluding it is inaccessible

**Custodian SA:** `agroverse_ledger_manager`
**Key on the autopilot box:** `/opt/truesight_autopilot/config/google/agroverse_ledger_manager_gdrive_key.json`

⚠️ **The `read_google_sheet` tool cannot read this sheet.** That SA is *not* in the tool's
`service_account_name` allowlist (`cypher_defense`, `tdg_scoring`, `upc_barcode`,
`edgar_dapp_listener`, `agroverse_qr_code_manager`, `agroverse_market_research`).
This is a known tool gap — see `OPEN_FOLLOWUPS.md`.

A permissions failure there is **not** evidence the sheet is missing or unshared.
Read it over `ssh_run` with the key path above:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
SID = "1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ"
cred = service_account.Credentials.from_service_account_file(
    "/opt/truesight_autopilot/config/google/agroverse_ledger_manager_gdrive_key.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
svc = build("sheets", "v4", credentials=cred, cache_discovery=False)
rows = svc.spreadsheets().values().get(
    spreadsheetId=SID, range="Instagram Content Schedule!A1:N1000").execute().get("values", [])
```

---

## 6. Gotchas that cause real bugs

1. **`Post Day` (F) is a string `YYYYMMDD`, not a date.** Sort/compare as text. A date-typed
   read or a `date()` coercion will misorder or silently null it.
2. **`primary_key` (A) is the identity.** Match on it; never key a sync on row position, and
   never overwrite `status` (B) from the source — B is operator-owned state.
3. **`Week` (C) is a running counter**, not an ISO week number. `Week 61` ≠ ISO week 61.
4. **`Description` (J) is mostly templated** — 112 unique strings across 314 rows, with the top
   three templates each repeating 51×. Do not treat J as a bespoke brief per row.
5. **`Tool Suggestions` (N) is stale vocabulary** from before `GENERATED_MEDIA_SOP.md`. It does
   not mention the current generation tools.
6. **Two tabs are reserved but headerless** (`Email Newsletter`, `Linkedin Content Schedule`).
   They are *empty shells* — see §7.

---

## 7. Known gaps (recorded, not fixed)

- **`Email Newsletter` is an empty shell — no header row.** The newsletter channel therefore has
  **no row in the forward calendar**, even though campaigns are actively sending (e.g. campaign
  `freight_landed`, 44 recipients, 2026-11-10). Until a header is defined, newsletter sends are
  untracked against the content plan. A header mirroring the Instagram tab
  (`primary_key`, `status`, `Post Day`, theme, subject, etc.) would close this.
- **`Linkedin Content Schedule` is likewise headerless. If a task implies this sheet already
  schedules LinkedIn or newsletter content, it does not — only Instagram and the two blogs do.

---

## 8. Related

- `tokenomics/SCHEMA.md` §5 — **authoritative** schema (update it there first, then mirror here)
- `MEDIA_ARCHIVE_PIPELINE.md` — supply side (what media we hold)
- `sops/GENERATED_MEDIA_SOP.md` — generating derivative assets
- `growth/GROWTH_MODEL.md` — Content Marketing as a growth channel
- `PROJECT_INDEX.md` — `market_research` project row
- `sops/AGROVERSE_NEWSLETTER_WORKFLOW.md` — newsletter generate/draft/send/track SOP

---

## Changelog

| Date | Change |
|---|---|
| 2026-11-10 | Created. Sheet was previously findable only via `tokenomics/SCHEMA.md` §5 — 0 hits in `agentic_ai_context` for the ID, title, or "content calendar". Includes live-verified tab list, column schema, access notes (SA not in `read_google_sheet` allowlist), and the headerless `Email Newsletter` / `LinkedIn` gap. |
