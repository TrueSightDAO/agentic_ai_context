# FIFO QR Code Selection Rule for Consignment Sales

**Adopted:** 2026-06-17 (thread 6311)
**Applies to:** Any `truesight-dao-report-sales` transaction where the consignment holder sells a bag and does not specify which QR code was sold.

## The Rule

**First In, First Out (FIFO).** When a consignment holder sells a bag of cacao (or any QR-code-tracked product) and does not indicate which specific QR code was sold, default to the **lowest-numbered QR code from the oldest batch** under that holder's management.

### Algorithm

1. Collect all QR codes currently assigned to the consignment holder (manager name matches).
2. Group by batch date (the date embedded in the QR code, e.g. `20260121` in `2024OSCAR_20260121_32`).
3. Sort batches ascending by date (oldest first).
4. Within the oldest batch, sort QR codes ascending by sequence number (the trailing digits).
5. Pick the first QR code in that sorted list.

### Example

Gergana - The Way Home Shop has 10 QR codes on consignment:
- `2024OSCAR_20260121_32`, `_33`, `_34` (batch date: 2026-01-21)
- `2024OSCAR_20260330_23` through `_29` (batch date: 2026-03-30)

Under FIFO, the default pick is **`2024OSCAR_20260121_32`** — the oldest batch, lowest sequence number.

## Rationale

- **Inventory accuracy:** Matches standard inventory accounting (oldest stock moves first).
- **Predictable:** No ambiguity — anyone can reconstruct the same result from the same data.
- **Auditable:** The ledger shows a clear, consistent pattern.
- **Aligns with physical handling:** For perishable/fresh cacao, older stock should sell first.

## When This Rule Does Not Apply

- The consignment holder explicitly states which QR code was sold (their word takes precedence).
- The governor explicitly overrides the rule for a specific transaction.
- The QR code was sold via the Agroverse Shop checkout (the system records the exact code at purchase).

## Related

- `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` — how many bags to ship on consignment
- `AGROVERSE_QR_CODE_BATCH_GENERATION.md` — QR code naming conventions
- `LEDGER_CONVERSION_AND_REPACKAGING.md` — inventory tracking
