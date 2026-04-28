# Retailer Technical Onboarding — ledger + website + inventory pipeline

**Status:** Compiled 2026-04-28 from the end-to-end onboarding of The Way Home Shop (Portland, OR — first onboarded 2026-04-28).
**Audience:** AI assistants (Claude / Cursor / Codex / Kimi) and human operators handling the **post-"Partnered"** technical work.
**Sibling docs:**
- **`RETAILER_ONBOARDING_PLAYBOOK.md`** — the **field-visit / sales** flow that ends at `Status = Partnered`. This doc picks up there.
- **`PARTNER_VELOCITY_PROPOSAL.md`** — the velocity JSON consumers (Restock Recommender, etc.).
- **`AGROVERSE_PRICE_LIST_AND_ASSETS.md`** — pricing terms (Consignment 5 / Wholesale-bought 10).
- **`tokenomics/SCHEMA.md`** — canonical column definitions for every Main Ledger tab referenced below.

---

## 1. What this doc is

The **technical onboarding sequence** that lights up a new retail partner across the ecosystem **after** the field-visit work has produced a verbal/written "yes" on consignment (or wholesale-bought) and the operator has the partner's contact + address + opening order details.

When done correctly:

- The partner appears in `partners-inventory.json` (daily sync) and `partners-velocity.json` (weekly sync).
- The DApp Restock Recommender dropdown auto-includes them.
- A public partner page renders at `https://agroverse.shop/partners/<slug>/` with the "When you visit" section auto-rendering once inventory is on the ledger.
- The cacao-journeys page auto-includes them in the geographic path.
- The wholesale page lists them in the U.S. stockists directory.
- The first opening-order bags appear in the partner's venue inventory.

If any join key drifts (see §6 *Recurring failure modes*) the partner is silently dropped from the JSONs — fix immediately.

---

## 2. Inputs you need before starting

| Input | Source | Required? |
|---|---|---|
| Partner display name | Operator (e.g. "The Way Home Shop") | Yes |
| Slug (`partner_id`) | Derive from display name (lowercase, hyphenated, no special chars) | Yes — canonical key |
| Contact name | Operator (e.g. "Gergana") | Yes |
| Contact email | Operator (e.g. info@thewayhomeshop.com) | Yes |
| Full street address | Operator (e.g. "8437 SE Stark Street, Portland, OR 97216") | Yes |
| Partner type | `Consignment` (default) or `Wholesale` | Yes — see `AGROVERSE_PRICE_LIST_AND_ASSETS.md` |
| Latitude / longitude | Geocode the address (Nominatim works) | Yes — for `partners-data.js` |
| Public website | Operator | Recommended |
| Mission / about blurb | Pull from website (3 sentences) or operator | Yes — for partner page |
| Hero image URL | From their site (`og:image` or homepage banner) | Recommended |
| Logo image URL | Their favicon / brand mark | Recommended |
| Opening-order QR codes | Operator (list of serialized codes from the source manager's stock) | Yes for first shipment |
| Source manager name | Whoever holds the stock being shipped (typically `Kirsten Ritschel`) | Yes |
| Inventory item / Currency string | Full Currency name from the Main Ledger `Currencies` tab — must match the QR codes' Currency on `Agroverse QR codes` col **I** | Yes |

---

## 3. The end-to-end sequence

Steps in dependency order. Skip any step at your peril — the chain breaks silently.

### 3.1 Submit `[CONTRIBUTOR ADD EVENT]` for the retailer contact

**Tool:** `dao_client` — `truesight_dao_client.edgar_client.EdgarClient.submit("CONTRIBUTOR ADD EVENT", ...)`

**CRITICAL — naming convention:**

The `Contributor Name` MUST be formatted as **`<First Name> - <Store Name>`** (e.g. `Gergana - The Way Home Shop`). This is the canonical format Edgar will produce anyway; pre-formatting prevents the auto-rename that has historically broken downstream joins. See **`feedback_contributor_naming_for_retail_partners.md`** in agent memory.

Attributes:

- `Contributor Name`: `<First> - <Store>`
- `Contributor Email`: `info@<store>.com` (or whatever the operator provides)
- `Initial Digital Signature`: `(none — store-manager contact, no key needed)` — retail contacts don't need their own RSA key; movements are signed by the operator (Gary, governor) on their behalf.
- `Submitted At`: ISO 8601 UTC
- `Submission Source`: `dao_client/edgar_client` (or whatever invoked it)

**Verify:** After submission, the row should land at the next blank row of `Contributors contact information` within ~30 seconds. Confirm via gspread that `data[-1][0] == "<First> - <Store>"`.

### 3.2 Set Mailing Address on the Contributors row (col U)

**Why:** `[CONTRIBUTOR ADD EVENT]` only writes Name + Email. Mailing Address (col **U**) needs to be set separately so the Restock Recommender's `?action=get_partner_address` lookup works.

**Tool:** Direct gspread write (no Edgar event covers col U).

**Cells:**
- Col **U** (1-indexed = 21): full street address (e.g. `8437 SE Stark Street, Portland, OR 97216`)
- Col **T** (1-indexed = 20): `FALSE` (or leave blank). **Do NOT set TRUE.** Col T = "Is Store Manager" is reserved for **online-fulfillment** managers (Gary + Kirsten) — i.e. people who can ship `agroverse.shop` orders from their physical inventory. A retail partner like Gergana holds consigned stock at her shop but does NOT fulfill online orders, so her bags must NOT count toward `Agroverse SKUs!I` (online-fulfillable totals). `partners-inventory.json` venue totals do **not** depend on col T — only on `Agroverse Partners.E` matching the ledger location string.

### 3.3 Append row to `Agroverse Partners`

**Tool:** Direct gspread write (no Edgar event covers this sheet).

**Sheet:** Main Ledger → `Agroverse Partners` (gid=1983902109).

**Columns** (per `tokenomics/SCHEMA.md` corrected 2026-04-28):

| Col | Value |
|---|---|
| A `partner_id` | slug (e.g. `the-way-home-shop`) |
| B `partner_name` | display name (e.g. `The Way Home Shop`) |
| C `partner_page_url` | `https://agroverse.shop/partners/<slug>` |
| D `status` | `active` |
| E `contributor_contact_id` | **MUST match Contributors!A exactly** — `<First> - <Store>` |
| F `location` | free-text city, state (e.g. `Portland, Oregon`) — drives cacao-journeys filter |
| G `notes` | optional onboarding notes |
| H `last_synced_at` | ISO 8601 UTC of when you wrote the row (the sync script overwrites later) |
| I `partner type` | `Consignment` or `Wholesale` (validated against `States!Z`; literal sheet header has a space) |

### 3.4 Build the website partner page

**Repo:** `agroverse_shop` (use a worktree per the parallel-sessions memory).

**Step-by-step:**

1. Clone `partners/lumin-earth-apothecary/index.html` (or any other thematically-similar partner page) as the template.
2. Find-replace slug + display name + address + email + phone + website + lat/lon + Google Maps query string + owner name.
3. Replace the about blurb with the partner's actual mission (pull from their site or operator-supplied).
4. Remove the Lumin-specific `partner-gallery` block — no photos yet for a fresh partner. (Add it later when shelf photos arrive; see `DOWNLOADS_MEDIA_TO_AGROVERSE.md` for the ingest workflow.)
5. Remove the Lumin-specific `Agroverse Cacao on the Shelves` block — same reason.
6. Update meta description / og:description / twitter:description so they match the actual mission (don't carry over Lumin's "mother-daughter-owned herbal sanctuary" boilerplate).

**Asset paths to reserve (operator uploads later if not staged now):**
- `assets/partners/headers/<slug>-header.jpeg` (resize to ≤ 1600 px longest side, JPEG q72-80, keep < 1 MB)
- `assets/partners/logos/<slug>-logo.<ext>` — `.png` if transparent, `.jpg` if photo. **Verify the page's `<img src>` matches the actual file extension** — this has bitten us before.

### 3.5 Update partner-discovery surfaces (same agroverse_shop PR)

| File | Change |
|---|---|
| `js/partners-data.js` | Append entry: `{ name, slug, lat, lon, location, description }`. The `description` should be 1-2 sentences; this populates partner-navigation cards and the journey path. |
| `partner_locations.json` | Append `{<slug>: {name, location}}`. Used by the Restock Recommender's address loader. |
| `wholesale/index.html` | Insert `<li>` in the U.S. stockists list, alphabetical placement. |
| `partners/index.html` | Insert a `<a class="partner-card">` in the hub grid, alphabetical. Logo path must match the actual file extension. |
| `cacao-journeys/pacific-west-coast-path/index.html` | Auto-includes if `location` contains `Washington / Oregon / California / Arizona`. **If your hero image is `.jpeg` not `.jpg`**, add the slug to the `imageExt` conditional at the bottom of the page (search for `'hacker-dojo' \|\| stop.slug ===`). |

### 3.6 Add hero + logo photos to the partner page

**Tool:** `sips` for resize / format conversion.

**Sources:**
- Header: their site's `og:image` or homepage banner (1200×630-ish landscape).
- Logo: their favicon, apple-touch-icon, or brand mark on the homepage. WordPress sites typically have `wp-content/uploads/.../favicon-*.png` or `cropped-*.png`.

**Anti-bot note:** thewayhomeshop.com (and other WordPress sites) reject some User-Agent strings. If `curl` returns 403, try a current-Safari UA (`Version/17.4 Safari/605.1.15`) — that's worked on multiple WordPress sites in this workspace.

### 3.7 Submit `[INVENTORY MOVEMENT]` events for the opening order

**Tool:** `dao_client` — `python3 -m truesight_dao_client.modules.report_inventory_movement`

For each QR code in the opening order, run:

```
python3 -m truesight_dao_client.modules.report_inventory_movement \
  --manager-name "<Source manager name, e.g. Kirsten Ritschel>" \
  --recipient-name "<First> - <Store>" \
  --inventory-item "<Full Currency string from Agroverse QR codes col I>" \
  --qr-code "<2024OSCAR_20260330_23>" \
  --quantity 1
```

Looping over 5–10 codes is mechanical. Each event produces one bag at the recipient.

**Authorization note:** the `--manager-name` is the *source* (sender) — typically Kirsten — not the dao_client signer. Edgar accepts the event because the dao_client signer (Gary) is a Governor; if a non-Governor were signing, the events would be rejected as `unauthorized` unless their digital signature matched the manager-name on Contributors.

### 3.8 Verify the JSONs pick the partner up

The async pipeline:

1. `[INVENTORY MOVEMENT]` events → `Inventory Movement` tab → status `NEW`.
2. GAS `process_movement_telegram_logs.gs` runs (next trigger) → applies movements to ledgers → status `PROCESSED`.
3. Daily 06:15 UTC: `publish-agroverse-inventory-snapshot.yml` reads `offchain asset location` → emits `partners-inventory.json`.
4. Weekly Mon 06:45 UTC: `publish-partners-velocity.yml` → emits `partners-velocity.json` with the new partner_name + location + partner_type.
5. Within ~24h of #3, the partner page's "When you visit" section (driven by `js/partner-catalog-snippets.js`) renders.
6. Within ~7 days of #4, the Restock Recommender dropdown shows the new partner.

If you don't want to wait, **run both syncs locally** with `--execute` and commit the resulting JSONs to `agroverse-inventory` directly (PR + merge).

---

## 4. Verification checklist

After completing §3, validate end-to-end:

- [ ] `Contributors contact information` row exists; col A is `<First> - <Store>`; col T is `FALSE` (or blank — **not TRUE**, which is reserved for online-fulfillment managers); col U has the address.
- [ ] `Agroverse Partners` row exists; col E exactly matches Contributors col A.
- [ ] `partners-inventory.json` (run `sync_agroverse_store_inventory.py --execute` if you don't want to wait) contains the partner under their slug, with at least one item.
- [ ] `partners-velocity.json` contains the partner with `partner_name`, `location`, `partner_type` (run `sync_partners_velocity.py --execute`).
- [ ] Visit `https://agroverse.shop/partners/<slug>/` — page renders; logo + hero load (no broken images); "When you visit" section appears below the about/gallery once the inventory JSON is fresh.
- [ ] Visit `https://agroverse.shop/partners/` — partner card visible.
- [ ] Visit `https://agroverse.shop/wholesale/` — partner appears in the U.S. stockists list.
- [ ] Visit `https://dapp.truesight.me/restock_recommender.html` — partner appears in the dropdown with `<name> · <location>`.
- [ ] If applicable: `https://agroverse.shop/cacao-journeys/pacific-west-coast-path/` — partner appears in the geographic path.

---

## 5. Reference numbers — what each step costs in time

Roughly observed from the 2026-04-28 Way Home Shop onboarding (1 hour total):

| Phase | Time |
|---|---|
| Phase 1 — ledger work (3.1–3.3) | ~10 min |
| Phase 2 — website (3.4–3.5, 3 PRs) | ~20 min |
| Phase 3 — photos (3.6) | ~5 min |
| Phase 4 — inventory movements (3.7) | ~5 min for 10 codes |
| Phase 5 — verification + JSON regen | ~10 min |
| Buffer for join-fix issues / template-clone leftovers | ~10 min |

Well-scoped onboardings should land in 30-45 min once the inputs in §2 are gathered.

---

## 6. Recurring failure modes

The 2026-04-28 onboarding hit two failure modes that are worth memorizing:

### 6a. Edgar auto-renames the contributor (and silently breaks the join)

**Symptom:** A few minutes / hours after submitting `[CONTRIBUTOR ADD EVENT]`, the Contributors row's name has changed from `Gergana` to `Gergana - The Way Home Shop`. `partners-inventory.json` silently excludes the partner because `Agroverse Partners!E` no longer matches.

**Root cause:** Edgar has a deduplication / naming-policy layer that renames retail-contributor rows to disambiguate against future name collisions.

**Mitigation:** Pre-format the `Contributor Name` as `<First> - <Store>` from the start so the rename is a no-op. Set `Agroverse Partners!E` to the same combined string. See `feedback_contributor_naming_for_retail_partners.md` in agent memory.

**Detection:** If `partners-inventory.json` doesn't contain the partner 24h after the daily sync ran, immediately check (1) `Contributors col A` exact format, (2) `Agroverse Partners col E` exact match against col A. Do **not** also flip col T to `TRUE` to "fix" it — col T has different semantics (online-fulfillment), and toggling it inflates the `Agroverse SKUs!I` online-fulfillable totals incorrectly.

### 6b. Template-cloned page references files that don't exist

**Symptom:** Logo / hero image broken on the live partner page.

**Root cause:** Cloning Lumin Earth's index.html → all asset references retain the original slug (`lumin-earth-apothecary-logo.jpg`), or get find-replaced to a slug + extension that doesn't match the actually-uploaded file (e.g. `<slug>-logo.jpg` when the file is `.png`).

**Mitigation:** After committing the partner page AND uploading photos, `curl -I` the asset URLs to confirm `200 OK`. Any 404 is a slug or extension mismatch.

### 6c. Partner page's `cacao-journeys` image extension

**Symptom:** Partner appears in the cacao-journeys path but with a broken image.

**Root cause:** `cacao-journeys/pacific-west-coast-path/index.html` defaults to `.jpg` for stop images and only switches to `.jpeg` for slugs in a hardcoded list.

**Mitigation:** If your header is `.jpeg`, add the slug to the conditional at the bottom of the file. (Or rename the file to `.jpg`.)

---

## 7. What can be scripted vs what needs AI inference

A `dao_client onboard_retail_partner` CLI could collapse most of §3 into a single command. Tracking this as `OPEN_FOLLOWUPS.md` work; for now, here's the breakdown:

| Step | Scriptable? | Notes |
|---|---|---|
| 3.1 `[CONTRIBUTOR ADD EVENT]` | Fully | New `dao_client` module wraps `EdgarClient.submit("CONTRIBUTOR ADD EVENT", …)`. |
| 3.2 col U | Fully | gspread direct write — script needs editor scope. Col T should NOT be set for retail partners (online-fulfillment-only). |
| 3.3 `Agroverse Partners` row | Fully | gspread append. |
| 3.4 partner page from template | Partial | Template clone + sed-style replacements are fully scriptable. **About-blurb** (§2) requires either operator-supplied text or LLM extraction from the partner's website (Grok API works). |
| 3.5 partners-data.js / partner_locations.json / wholesale / hub | Fully | All four are alphabetical-insert operations. **Lat/lon** geocoding via Nominatim (free, no key) given the address. |
| 3.6 hero + logo photos | Mostly | `og:image` / favicon URLs are usually scrapable; `sips` resizes. **Choosing** a good hero (vs e.g. a flyer) is judgment — easier to have the operator pre-stage images. |
| 3.7 `[INVENTORY MOVEMENT]` loop | Fully | Already covered by `report_inventory_movement.py` — script just loops. |
| 3.8 wait + verify | Fully | Run both syncs with `--execute` immediately after §3.7 and validate the JSONs. |

**AI inference needed (if the operator doesn't supply):**
- About-blurb / mission paragraph (LLM extracts from the partner's website).
- Hero photo selection (LLM looks at homepage `<img>` set, picks the most "shop interior / storefront / mission-aligned" one).
- Partner-specific copy ("`carries Agroverse cacao at <location>`" — nice to have but mechanical).

If the operator provides about-blurb + hero URL + logo URL up front, the entire onboarding becomes a single CLI command with no AI inference required. See `OPEN_FOLLOWUPS.md` for the script-build follow-up.

---

## 8. Worked example — The Way Home Shop (2026-04-28)

| Field | Value |
|---|---|
| Slug | `the-way-home-shop` |
| Display name | `The Way Home Shop` |
| Contact | `Gergana - The Way Home Shop` (combined, per §3.1) |
| Email | `info@thewayhomeshop.com` |
| Address | `8437 SE Stark Street, Portland, OR 97216` |
| Lat / lon | `45.5189 / -122.5765` (approx Mt. Tabor / Montavilla) |
| Partner type | `Consignment` |
| Source manager | `Kirsten Ritschel` |
| Inventory item | `Ceremonial Cacao Kraft Pouch - Alibaba:269035810001023771 + 8 Ounce Package Kraft Pouch CP340992735BR \| Kirsten 20260121` |
| Opening QR codes | `2024OSCAR_20260330_23..29` (7) + `2024OSCAR_20260121_32..34` (3) = 10 bags |

**Pull requests (in order):**

| Repo | PR | What |
|---|---|---|
| `agroverse_shop_beta` | #82 | Partner page + partners-data.js + partner_locations.json + wholesale stockists |
| `agroverse_shop_beta` | #83 | Hero + logo |
| `agroverse_shop_beta` | #84 | Hub card + cacao-journeys jpeg fix |
| `agroverse_shop_beta` | #85 | One-line logo extension fix |
| `agroverse-inventory` | #5 → #7 | partners-velocity.json + partners-inventory.json refreshes (#7 was the join-fix) |
| Plus | dao_client | 1 `[CONTRIBUTOR ADD EVENT]` + 10 `[INVENTORY MOVEMENT]` events |

**Time:** ~1 hour, including ~10 minutes recovering from the §6a Edgar auto-rename + col T clear.

---

## 9. Index of files this playbook touches

**Main Ledger sheet (`1GE7PUq-…`):**
- `Contributors contact information` (cols A, D, T, U)
- `Agroverse Partners` (cols A–I)

**Repos:**
- `agroverse_shop_beta` — partner page (`partners/<slug>/`), `js/partners-data.js`, `partner_locations.json`, `wholesale/index.html`, `partners/index.html`, `cacao-journeys/pacific-west-coast-path/index.html`
- `agroverse-inventory` — `partners-inventory.json`, `partners-velocity.json` (regenerated by the syncs)
- `go_to_market` (market_research) — `scripts/sync_agroverse_store_inventory.py`, `scripts/sync_partners_velocity.py` (run if you don't want to wait for the cron)
- `dao_client` — `report_inventory_movement.py`, `edgar_client.py` (for `[CONTRIBUTOR ADD EVENT]`)
- `dapp` — `restock_recommender.html` (auto-includes via JSON; no edit needed)

**Sister docs:**
- `RETAILER_ONBOARDING_PLAYBOOK.md` — field-visit / sales side that ends at "Partnered".
- `PARTNER_VELOCITY_PROPOSAL.md` — JSON design.
- `AGROVERSE_PRICE_LIST_AND_ASSETS.md` — pricing terms.
- `tokenomics/SCHEMA.md` — sheet column definitions.
