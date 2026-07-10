# Repackaging Settlement — SOP

**Event:** `[REPACKAGING SETTLEMENT EVENT]`
**Purpose:** Finalize a repackaging batch — deplete inputs from inventory, add outputs, set Currencies metadata, and make products visible on agroverse.shop.
**Prerequisite:** A `[REPACKAGING BATCH EVENT]` must already be processed (composition JSON published, Currency rows created).

---

## Flow

```
CLI → sign → Edgar → Telegram → dispatch → GAS → Sheets → store-inventory.json → agroverse.shop
```

---

## 1. Gather information

You need four things before running the command:

### (a) Composition URL
The batch composition JSON. Format: `https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/<request_id>.json`

### (b) Holder name
Who physically holds the inventory (e.g. `"Kirsten Ritschel"`).

### (c) Farm info
Farm name, state, country, year, landing page URL, ledger URL. Extract from the repackaging batch or the AGL shipment page.

### (d) SKU mapping (CRITICAL)
Must match actual SKU IDs from the **`Agroverse SKUs`** tab on the Main Ledger (`spreadsheet ID 1GE7PUq-...`, tab `Agroverse SKUs`, column A).

**How to find the right SKU:**

1. Check the existing SKU list:
   ```python
   # spreadsheet: 1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU
   # tab: Agroverse SKUs
   # column A = SKU Product ID, column B = human-readable name
   ```

2. Match by:
   - **Product type** (bar vs pouch vs tea vs nibs)
   - **Farm** (Oscar's Farm, Fazenda Santa Ana, La do Sitio, etc.)
   - **Weight** (50g, 200g, 1lb)
   - **Year** (2024, 2023)

3. **Concrete examples from the current SKU catalog:**

| Product | SKU ID |
|---------|--------|
| 81% Chocolate Bar 50g — Oscar's Farm, Bahia | `organic-81-dark-chocolate-bar-50g-oscar-bahia-2024` |
| 81% Chocolate Bar 50g — Fazenda Santa Ana, Bahia | `organic-81-dark-chocolate-bar-50g-fazenda-santa-ana-bahia-2023` |
| Ceremonial Cacao 200g — Oscar's Farm | `oscar-bahia-ceremonial-cacao-200g` |
| Ceremonial Cacao 200g — Fazenda Santa Ana | `ceremonial-cacao-fazenda-santa-ana-2023-200g` |
| Ceremonial Cacao 200g — La do Sitio Farm | `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g` |
| Cacao Tea 1lb — Oscar's Farm | `oscar-bahia-cacao-tea-1lb` |
| 8oz Cacao Nibs — Amazon Rainforest | `8-ounce-organic-cacao-nibs` |
| Organic Criollo Beans — Oscar's Farm | `organic-criollo-cacao-beans-oscar-farm` |

4. **Match each output** from the composition JSON to an SKU ID using substring matching on the output label. The `--sku-mapping` flag accepts a JSON object mapping substring → SKU ID. First match wins.

---

## 2. Run the settlement

```bash
cd ~/Applications/dao_client

python3 -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/<request_id>.json" \
    --holder-name "<Name>" \
    --farm-name "<Farm>" \
    --state "<State>" \
    --country "<Country>" \
    --year "<YYYY>" \
    --landing-page "<URL>" \
    --ledger-url "<URL>" \
    --sku-mapping '{"<substring>": "<sku-id>", ...}'
```

Use `--dry-run` first to verify the signed payload.

---

## 3. Verification checklist

After submitting (HTTP 200), verify within 1-2 minutes:

- [ ] Telegram Chat Logs shows `[REPACKAGING SETTLEMENT EVENT]` entry
- [ ] `offchain transactions` has 6 new rows (date = today): depletions (-7 nibs, -3 pouches, -15 labels, -15 boxes) and additions (+3 ceremonial, +15 bars)
- [ ] `offchain asset location` quantities updated (formulas recompute from `offchain transactions`)
- [ ] `Currencies` col C = TRUE, cols E-J populated, col M = correct SKU IDs
- [ ] `store-inventory.json` regenerated (run `sync_agroverse_store_inventory.py --execute` if needed)
- [ ] `agroverse.shop/#products` shows the new bars/cacao in stock (GitHub CDN may take ~5 min)

---

## 4. Common failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `offchain asset location` still shows -1 or 0 | Column D in `offchain transactions` is a string, not a number | Ensure values are numeric (not `"3.00000000"`) |
| Inventory shows 0 on website | Wrong SKU IDs in Currencies col M | Re-read `Agroverse SKUs` tab and fix mapping |
| Website stale | GitHub CDN cache (max 5 min) | Wait, or check `raw.githubusercontent.com/.../8ac3abc/store-inventory.json` |
| Edgar rejects submission | Missing required fields | `--composition-url` and `--holder-name` are required |
| GAS handler doesn't fire | `DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP` not set | Provision env var on Edgar box |

---

## 5. Idempotency

The event is safe to re-submit. The GAS handler:
- Skips depletion if `offchain asset location` amount is already 0
- Skips output addition if row already exists (same currency + holder)
- Skips Currencies metadata if column is already populated

A duplicate submission produces a Telegram log entry but no duplicate sheet writes.
