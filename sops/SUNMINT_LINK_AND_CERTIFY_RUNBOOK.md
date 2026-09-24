# Runbook — SunMint: link a cacao QR to a tree, then issue its certificate

**Owner:** Sophia Truesight (autopilot). **Governor:** Gary.
**Origin:** thread 35189, 2026-09-24 — *"how do future LLMs and Sophia know how to
replicate this process of linking when prompted?"*
**Companions (read these too):**
- `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` — the event/CLI/dapp contract (authoritative on *the mechanism*).
- `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` — the certificate rules (authoritative on *the cert*).

This runbook is the **ordered end-to-end when-prompted procedure**. It does not restate
the plan or the SOP; it sequences them and pins the operational gotchas discovered live.

---

## 0. One-line summary

**census → de-dup (REQUIRED) → link → verify → render from the canonical template →
acceptance gate → deliver.**

---

## 1. Census — whose QRs, and which ones?

When asked to link "a person's tree" / "their earliest codes":

1. Resolve the person's **QR owner email** in the Agroverse QR sheet (use the
   `agroverse-qr-code-manager` service account).
2. Pull **all** their rows — sweep **every column** for the name/email, not just the
   owner column (a code can hide under a manager or a different string).
3. Sort by mint date (the `YYYYMMDD` segment of the qr_id). Group by batch when one
   owner has several orders — "earliest overall" vs "earliest of the documented
   purchase" can differ; **show the governor both and let them pick.**
4. Prefer a **matched pair** (one per origin/SKU) when linking two.

Record the two candidate ids before doing anything else.

---

## 2. De-dup the target SunMint row(s) — **REQUIRED before linking**

**Why (live bug).** The GAS handler's **LINK path matches SunMint rows
first-match-only** (`sunmint` handler `process_tree_planting_link.js`, the LINK branch —
it sets the row index and `break`s). If a tree has **duplicate rows**, the link flips
only the **first**; the twin stays `NEW` → the tree silently "comes back" as plantable.
(The **REJECT** path already fixed this — *"No break: invalidate EVERY row"* — LINK never
got the same fix.)

**Do:**
1. **Back up** the `SunMint Tree Planting` tab to a timestamped JSON first.
2. Find twin rows: **identical on the identity columns** (col A `Telegram Update ID`,
   col D `Telegram Message ID`, species, plot, photo).
3. Delete twins **bottom-up** (descending row index) so indices stay valid.
4. Keep the **canonical** row (for an already-linked tree that is the `LINKED`/first row;
   for a new tree it is the first `NEW`).
5. Re-verify: every target tree is now a **singleton**.

> Never blanket-dedupe the whole sheet — twins are sheet-wide and include `INVALID`
> status rows. Scope strictly to the trees you are about to link.

---

## 3. Link — `[TREE PLANTING LINK EVENT]`

See `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` for the full contract. Operational essentials:

- **Canonical CLI:** `truesight_dao_client/modules/link_tree_planting.py`
  (`--qr-code`, `--sunmint-submission-message-id`). The dapp page
  `link_tree_planting.html` signs the same event.
- **Who may sign:** the handler gates on **governor OR sentinel** (not governor-only).
  **Sophia Truesight is a sentinel** (`Is Sentinel = TRUE`, col W of the Main Ledger
  `Contributors contact information` tab) → her signature is accepted. A non-governor,
  non-sentinel signer is *logged then skipped*.
- **Delivery:** Edgar verifies the signature, appends the event to **Telegram Chat Logs**,
  and the post-verify dispatch fires the GAS processor
  (`?action=processTreePlantingLinksFromTelegramChatLogs` via
  `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_LINK`). Processing is **not instant** — allow a
  minute and re-read before concluding it failed.
- **Ledger effect (`-1 Cacao Tree To Be Planted`):** a QR on a **managed** ledger in
  `TPL_MAIN_LEDGER_LEDGER_URLS` books its fulfillment pair to the **main DAO ledger**.
  Verify the QR's ledger *before* firing — the wrong-ledger case is the documented revert.
- **Gate:** this is a **money-adjacent** event (**always-stop**; needs explicit governor go).
- **Route to the governor even when pre-authorized?** No — a governor's standing "go" on
  the plan authorizes the link; submit it directly and report the ledger row.

**Pairing note:** the link encodes **QR ↔ tree** only. The **awardee's name lives in the
cert config**, not the link — so a mis-pairing is cheap to fix at the cert step
(re-render), but **get the QR↔tree pairing right** because the link is the durable record.

---

## 4. Verify the link (end-to-end, don't trust the submit response)

- **QR status** → `ASSIGNED_TO_TREE` (lat/lon + tree photo copied onto the QR record).
- **SunMint row** → `LINKED`.
- **Tree Planting Link** tracking tab → a `LINKED / OK` row, signed by you.
- **Ledger** → the `-1 Cacao Tree To Be Planted` pair, on the **main** ledger.

If the QR is still `SOLD` / no tracking row, it is almost always an **ingestion race** —
re-read before re-submitting (do **not** re-fire; that risks a double-link).

---

## 5. Render the certificate(s)

Follow `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` in full. The two operational traps:

1. **Render from the CANONICAL template path only** — `agentic_ai_context/templates/sunmint_certificate/render_sunmint_certificate.py`.
   **Never** a `/tmp` working copy: on 2026-09-24 a cert was rendered from a stale
   untracked `/tmp` snapshot (pre-#1352, 403 lines) with **no overlay logic**, and the
   Agroverse centre logo was silently thresholded away. Resolve the template via
   `read_repo_file` / raw URL, and optionally assert its `md5` against `main` first.
2. **The `2023SA…` (Santa Anna) QR family fails pyzbar at native size** — decode at 2–3×
   first. The canonical template now retries on upscale automatically.

**Config** (`example.config.json` is a template): set `qr_id`, `ledger_ref` (the tree's
canonical id — SunMint col D), `awardee`, `date_display`, `photo_url`, `with_photo`,
`variants`. The **signature mark** (`--mark`) is private
(`signature_assets/sophia_truesight/sophia_truesight_signature_mark.png`) and is **never
committed with the template**.

---

## 6. Acceptance gate (do not skip)

Per SOP §4, on the **rendered output**:
- The cert's QR **decodes** and its payload **exactly equals** the registry PNG's payload —
  in **both** the in-place PNG **and** the exported PDF (note: the PDF decodes at its
  native 300 dpi; downsampling below that can fail in *any* tool and is not a defect).
- No overlap/clipping of text, photo, signature, or QR.

---

## 7. Deliver

Post the PNG(s) + PDF(s) into the thread (personal + institutional per the request), with
the QR id + tree id in the caption. Record the issue.

---

## 8. Related open bugs (do not silently work around)

- **LINK path first-match-only** — the de-dup in §2 is the workaround; the real fix
  (port the REJECT path's all-rows loop into LINK) is filed in `OPEN_FOLLOWUPS.md`.
- **`sync_tree_links.py` status-clobber** — `build_qr_patch` inherits `status: "MINTED"`
  and clobbers `SOLD`. Filed in `OPEN_FOLLOWUPS.md`.
- **`merge_preserve_events` drops top-level fields** — never hand-edit a manifest; re-seed.
  Filed in `OPEN_FOLLOWUPS.md`.
