# Last-mile carrier — Energy Transport Logistics (SFO OPS)

> **Captured:** 2026-10-13 · **Source:** Telegram screenshot (Black King shipment thread) · **By:** Sophia Truesight
> **Lane:** SFO airport release → **Kirsten's SF warehouse** (US domestic drayage / last-mile) — Phase 7 of `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`.
> **Shipment:** Black King, **AWB 047-3175-3223** (SSA→SFO, TAP 047-3175-3223).

## Vendor record

| Field | Value |
|---|---|
| **Carrier** | **Energy Transport Logistics** — *SFO OPS* |
| **Office phone** | **844-737-7447** |
| **PRO #** | **2001689064** |
| **Booked via** | **Daniel (Seacoast Logistics)** — the forwarder scheduled the carrier |
| **Arranged by** | **Kirsten Ritschel** — called the carrier to arrange the delivery time |

## Context (from the screenshot thread)

- Daniel (Seacoast Logistics) asked for the carrier number and posted the **SFO OPS** contact + **PRO# 2001689064** at ~6:26 PM.
- Kirsten replied *"Will call them now"*, then *"Alright. They've scheduled…"* — i.e. Kirsten phoned Energy Transport Logistics to lock in the drop-off time.

## Notes / open items

- **New vendor** — this carrier did **not** previously appear anywhere in `agentic_ai_context` (searched org-wide for "Energy Transport"). It should be added to the freight-forwarder / last-mile vendor set alongside **Seacoast Logistics** (forwarder) and **Magic Custom Brokers** (customs).
- **Not yet in the checklist.** The Phase-7 slot `- [ ] Delivery SFO → Kirsten's SF warehouse.` should carry this vendor's block; the edit failed this pass on a **latin-1 encoding** error in `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` (needs a re-encode to UTF-8 first). **DONE 2026-10-13:** checklist re-encoded to UTF-8 and the `#### Last-mile carrier` table injected into the Phase-7 slot.
- **PRO# 2001689064** is the carrier's own tracking reference — carry it on the delivery paperwork.
- This leg is under the **cargo-arrival gate**: record the vendor now, but **do not** post the final `[ASSET RECEIPT]` / `[INVENTORY MOVEMENT]` until the cargo physically arrives and the drop-off is confirmed.
