# Pricing SSOT — finalized prices, lot attribution, and where they live

**Status:** proposed 2026-10-24. Governor: Gary Teh. Companion to
`EMAIL_SEND_POLICY.md` §6.2–§6.3 (the pricing gate and the pricing mandate).

> **Why this file exists.** Prices were being re-derived per conversation, and a price that
> exists only in `skus.json` is destroyed on the next regeneration. This is the durable record of
> *what each price is, what it rests on, and where the master copy lives* — so a number agreed
> once is never renegotiated with ourselves.

---

## 0. Where prices live (the one rule)

| Layer | Location | Editable? |
|---|---|---|
| **MASTER** | Spreadsheet `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, tab **`Agroverse SKUs`**, **column C `Price (USD)`** | YES — **only here** |
| Derived | `agroverse-inventory/skus.json` | NO — never |
| Derived | `store-inventory.json`, `partners-inventory.json` | NO — never |
| Stock source | `Currencies` tab; **column M = productId** links a stock row to its SKU | see §5 |

Generator: `go_to_market/scripts/sync_agroverse_store_inventory.py` (reads `Agroverse SKUs` A–I,
and `Currencies` A+M). **A price written anywhere else does not exist.**

---

## 1. Lot attribution — established, and the trap avoided

Bulk nibs in San Francisco come from **two different shipments with a 53% cost gap.** They must
never share one price.

| SF inventory line | Qty | Landed cost | Farm binding |
|---|---|---|---|
| `Cacao Nibs (KG) - Ilheus, Brazil 2024 + 047-3175-3223 - San Francisco` | **80.0 kg** | **$41.69/kg** | Oscar's farm, AGL4 |
| `Cacao Nibs (Kilograms) Santos 20260213 - AGL13 + 047-3175-3223 - San Francisco` | **99.5 kg** | **$27.25/kg** | **unbound — no farm recorded** |

### The Ilhéus ↔ Oscar binding, and how it was established

The retail SKU `8-ounce-organic-cacao-nibs` carries **Shipment `AGL4`, Farm `Oscar`**, and its
stock line is `8 Ounce Package Kraft Pouch - Ilheus, Brazil 2024`. That binds
**Ilhéus 2024 ↔ AGL4 ↔ Oscar's farm**. So calling the $41.69 lot "Oscar's Criollo nibs" is
**supported by the master data**.

### The Santos ↔ Oscar binding does NOT exist

`Santos 20260213` appears **only** as a shipment/date descriptor on the AGL13 nibs and tea lines.
No SKU, no `Currencies` row, and no treasury field binds it to a farm. **Therefore the Santos
2026 lot must not be described to a buyer as Oscar's, or as Criollo, until it is confirmed.**
Describing it as "our 2026 Santos lot" is accurate; anything more is invention.

> This distinction is the whole point of §6.1. The prior draft to Dr. Hughes described the $74
> nibs as "Oscar's farm Criollo" — which is **correct for the Ilhéus 2024 lot** and happens to be
> the lot the $74 price belongs to. The number was right. The risk is that the same narrative gets
> applied to the Santos lot, where it would be false.

---

## 2. Finalized prices

Margin targets: **55% on bulk**, 43.7% floor where landed cost forces it, **50%** on beans.

### 2a. Existing SKU rows — values for `Agroverse SKUs` column C

| Row | SKU (Product ID) | Current C | Set C to | Landed | SF stock | Quotable now? |
|---|---|---|---|---|---|---|
| 8 | `premium-organic-cacao-beans-la-do-sitio` (Paulo beans, AGL8) | `$0.00` | **`$71.00`** | $35.28 | **10 kg** | YES |
| 10 | `oscar-bahia-cacao-tea-1lb` | `$20` | **`$27.50`** | $27.25/kg | 21 kg | YES |
| 5 | `organic-criollo-cacao-beans-oscar-farm` (AGL14) | `$0.00` | **`$71.00`** | ~$28.48 est | **0 kg** | NO — priced, not quotable |
| 6 | `organic-hybrid-cacao-beans-jesus-da-deus` (Vivi, AGL13) | `$0.00` | **`$50.00`** | $24.94 est | **0 kg** | NO — priced, not quotable |
| 7 | `organic-criollo-cacao-nibs-oscar-farm` (AGL4) | `$0.00` | **`$74.00`** | $41.69 | **0 kg as AGL4** | NO — see §3 |

Pricing a SKU whose only stock is overseas is deliberate: it records the decision so it is not
re-derived, while §6.1 still blocks quoting it.

### 2b. Bulk lots with NO SKU row — rows must be created first

**This is the blocking gap.** The 179.5 kg of sellable SF nibs have **no wholesale SKU**. The only
wholesale nibs SKU is `organic-criollo-cacao-nibs-oscar-farm`, which is bound to AGL4 and shows
**0** stock. You cannot write a price into column C for a row that does not exist.

| Proposed new SKU | Qty | Landed | Price | GM |
|---|---|---|---|---|
| `cacao-nibs-santos-2026-agl13` (per kg) | 99.5 kg | $27.25 | **$60.50/kg** | 55.0% |
| `cacao-nibs-ilheus-2024` (per kg) | 80.0 kg | $41.69 | **$74.00/kg** | 43.7% |
| `cacao-tea-santos-2026-agl13` (per kg) | 21.0 kg | $27.25 | **$60.50/kg** | 55.0% |
| `coopercabruca-cacao-butter` (per kg) | 5.0 kg | $34.40 | **$76.50/kg** | 55.0% |

> **The $74 reconciliation.** $74 was the number quoted to Dr. Hughes, and it was withdrawn
> here as "too high for everything". Both are right: **$74/kg is the correct price for the
> Ilhéus 2024 / Oscar lot** (43.7% GM on a $41.69 landed cost) and **wrong for the Santos 2026
> lot**, which needs $60.50. The error was never the number — it was applying one number to two
> lots with a 53% cost spread.

### 2c. Below-cost reference — the counter floor

| | Per kg | Per lb |
|---|---|---|
| Be Sweet's ask ($12/lb) | **$26.46** | $12.00 |
| Santos 2026 landed cost | $27.25 | $12.36 |
| **Their ask vs our cost** | **−$0.79/kg → underwater** | |

The ask is **below landed cost on the cheap lot and 38% below it on the other.** No volume
qualifies it — with no restock, unused stock still sells next quarter at the same price.

---

## 3. What is NOT quotable, and why

| SKU | Reason |
|---|---|
| `organic-criollo-cacao-beans-oscar-farm` (AGL14) | **0 kg in SF.** 108 kg is in Ilhéus (AGL16). Cannot fill 5 kg. |
| `organic-hybrid-cacao-beans-jesus-da-deus` (Vivi) | **Never imported.** Zero kg anywhere. |
| `organic-criollo-cacao-nibs-oscar-farm` (AGL4) | SKU is AGL4-bound with **0** stock, while the physical Oscar nibs sit under the **Ilhéus 2024** line. The SKU ↔ inventory binding is broken; the lot is sellable, the SKU does not represent it. |
| Packaged goods as wholesale | 200 g pouch costs $13.78 ($68.90/kg equiv.) — no wholesale margin survives. **Retail-only.** |

### Retail unchanged
Ceremonial 200 g pouches **$25**, 81% bars **$10**, tea 50 g **$10**, 8 oz nibs **$25**.

---

## 4. Evidence base for margins

- **Landed costs** from `treasury-cache/dao_offchain_treasury.json` `unit_cost_usd` — invoice
  actuals, not the freight planner (which understates by ≈$7/kg: $9.89 modelled vs $16.21–17.07 actual).
- **Freight + duty constant** ≈**$17.07/kg** Ilhéus→SF, derived independently from two product
  pairs (Paulo AGL8 $18.21→$35.28; Coopercabruca butter $17.33→$34.40) and corroborated by
  invoiced actuals on AWB `047-3175-3223`.
- **Market comps (Oct 2026):** bulk cacao nibs $34–56/kg wholesale; ceremonial paste $48.50/kg
  wholesale / $92.60 retail; cacao tea $44–105/kg; specialty beans $30–50/kg.

**Structural conclusion:** at ≈$17/kg freight we cannot compete as a bulk commodity supplier.
Most landed costs sit at or above the wholesale comp ceiling. The defensible position is
premium/specialty — single origin, named farm, QR traceability, third-party heavy-metal panel —
or retail.

---

## 5. Known gaps (blocking execution)

1. **No sheet-write path exists.** There is no `update_google_sheet` tool and no write function in
   `truesight_autopilot` (only `app/identity_binding.py` performs a Sheets update, for an unrelated
   purpose). Writing column C currently requires the Sheets UI or a new tool. **This blocks §2.**
   Options: (a) type the §2a values by hand, or (b) authorise an `update_google_sheet` PR.
2. **Bulk lots have no SKU rows** (§2b). Requires adding rows to the master, not editing cells.
3. **`Currencies` column M is incomplete** — which is why stock reads `0` for SKUs that physically
   exist. A SKU's stock only populates when its currency rows carry a `productId` in column M.
   This is a data-repair task across ~172 currency rows.
4. **AGL8 263.6 kg unlocated.** AGL8 shows 263.6 kg / $15,386 with no `San Francisco` marker, while
   10 kg is marked SF. Under §6.1 that remainder is not quotable. Needs a physical count.
5. **Santos 2026 farm attribution unverified** (§1) — blocks any farm claim on 99.5 kg.

---

## 6. Change log

| Date | Change | Basis |
|---|---|---|
| 2026-10-24 | Initial SSOT. Withdrew the flat $74/kg tier-ladder recommendation. | Gary: no restocking for 2026 → finite stock → hold price, do not discount. |
