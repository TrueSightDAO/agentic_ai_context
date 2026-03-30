# Purchase agreement PDFs (Agroverse wholesale / import)

Use this document when generating **customer purchase agreements** as PDFs so you do not need to rediscover layout rules, file locations, or canonical farm URLs each time.

---

## Where outputs live

- **Folder:** `market_research/purchase_agreements/`
- **Generator (example — 3rd Eye Cafe):** `market_research/purchase_agreements/generate_purchase_agreement_3rd_eye_cafe.py`
- **Output (example):** `purchase_agreement_3rd_eye_cafe_20260325.pdf` (date in filename can be updated when regenerating)

**Run:**

```bash
python3 /path/to/market_research/purchase_agreements/generate_purchase_agreement_3rd_eye_cafe.py
```

Requires **Python 3** and **reportlab** (and **Pillow** if the optional logo path is used).

---

## Style and technical conventions (ReportLab)

Follow the same patterns as these existing generators in `market_research/`:

- `generate_expo_west_schedule_pdf.py` — `SimpleDocTemplate`, letter size, margins ~0.5–0.75″, tables with colored header row
- `retail_price_list/generate_earth_commons_price_list.py` — Agroverse logo from `retail_price_list/`, header green **`#2d5a27`**, light row backgrounds

**Critical:** In ReportLab `Table` cells, use **`Paragraph`** objects for any markup (`<b>`, `<br/>`, `<a href="...">`, entities). Plain strings **do not** interpret HTML and will render badly.

**Lists:** Use `ListFlowable` / `ListItem` for bullets (see the 3rd Eye script).

**Money / line-item table:** Use two columns — **Line item** (left) and **Amount (USD)** (right-aligned). Separate **product** from **forwarder/brokerage** with a thick `LINEBELOW` under the product row plus a merged **section banner row** (`SPAN`) for the forwarder name (e.g. Sea Coast Logistics).

**Deposit display:** Show **quoted logistics subtotal**, **product + logistics subtotal (50/50 base)**, **50% due on signing**, **50% due on arrival**, then estimated **MPF / bond / duties** and an **estimated total excluding duties/exams** as appropriate.

**Signatures (no awkward page breaks):** Wrap the entire **Buyer** signature stack (note + title + signature line + name/title/date) in **`KeepTogether`** so ReportLab does not split it across pages.

**Per-page buyer initials:** Use `doc.build(story, onFirstPage=fn, onLaterPages=fn)` to draw a small footer on **every** page, e.g. `Buyer (Customer Name) initials: __________` and `Page N`. This is optional legally but helps show the buyer saw every page (reduces “missing or replaced page” disputes). Pair with a one-line instruction above the signature block that the buyer should initial each footer. For binding US deals, counsel may still prefer page initials + full signature; electronic signing tools often capture intent differently.

---

## Canonical farm URLs (agroverse.shop)

When the contract references a farm, **link to the public farm page** (and keep the URL as a constant at the top of the script):

| Farm | Canonical URL |
|------|----------------|
| **Oscar’s farm (Bahia)** | [https://agroverse.shop/farms/oscar-bahia/index.html](https://agroverse.shop/farms/oscar-bahia/index.html) |

Add rows here when new farm profile URLs exist. Product pages on `agroverse.shop` are not a substitute for the farm journey page when the agreement should cite **origin / story / traceability**.

---

## Business defaults often reused

- **U.S. FDA Importer of Record / CBP importer (when quoted in agreements):** TrueTech Inc.; EIN 88-3411514; CBP importer number 88-341151400 — **confirm with the user** before each new agreement in case entities change.
- **Warehouse (Brazil) example used in scripts:** R. Cel. Paiva, 46 - Centro, Ilhéus - BA, 45653-310, Brazil.
- **Freight:** Quotes are typically broken into line items (inland, airport, air, terminal, handling, delivery, clearance, FDA, etc.). Tabulate **each line with a dollar amount**; carry broker disclaimers (exams, duties, bond, MPF min/max) in prose under the table or in footnotes.

**Payment rails** and account numbers change by deal — always take them from the user or finance; do not assume from memory.

---

## Creating a *new* agreement from scratch

1. **Copy** the closest existing `generate_purchase_agreement_*.py` in `purchase_agreements/`.
2. **Rename** the file and `OUTPUT_PATH` to the customer and date.
3. **Edit constants** at the top: weights, price/lb, broker line amounts, dates, hold end date, parties’ addresses, forwarder name, `FARM_CANONICAL_URL` (or add a new farm row to the table above).
4. **Recompute** derived totals (or keep them computed from constants so one source of truth drives the money table).
5. **Run** the script and open the PDF to verify links, table boundaries, and payment rows.

For supply-chain and freighting **context** (Brazil → US, inventory locations), see **`SUPPLY_CHAIN_AND_FREIGHTING.md`** in this repo.

---

## Related index entries

- **`PROJECT_INDEX.md`** — `market_research` row references purchase agreements.
- **`WORKSPACE_CONTEXT.md`** §4 — `agroverse_shop` ↔ `market_research` (points here for PDF purchase agreements).

When you add a new pattern or default, update **this file** and append a line to **`CONTEXT_UPDATES.md`**.
