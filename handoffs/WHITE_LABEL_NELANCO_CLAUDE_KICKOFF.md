# White-label Phase 2 → `nelanco-claude` — kickoff

**Runner:** the `nelanco-claude` interactive box (`claude.truesight.me`, `100.57.50.48`) — **not Sophia**.
**Registered:** `handoffs/HANDOFF_MANIFEST.md`, 2026-07-15.
**Plan of record:** `plans/WHITE_LABEL_IMPLEMENTATION_PLAN.md` (on `main`).

---

## 1. Gary — unblock the box first (Gate D)

Per `plans/NELANCO_CLAUDE_CODE_BOX_PLAN.md`, **Gate D is the open blocker and only Gary can clear
it** — it needs an interactive login to his Claude account:

```bash
ssh nelanco-claude
tmux new -s claude          # so the session survives a dropped connection
claude                      # log in to the Pro/Max/Team account
/remote-control             # then drive it from the phone
```

Gate C is done: 47 repos in `/opt/claude_workspace`, 64 secret files laid down, fleet SSH working,
git identity `Claude Anthropic` with a working HTTPS PAT helper. **The box can push and open PRs
today** — it just needs a logged-in session.

Until Gate D is done, this handoff is registered but nothing will pick it up.

---

## 2. Paste this into the box as the first message

> Read `agentic_ai_context/plans/WHITE_LABEL_IMPLEMENTATION_PLAN.md` on `main` — start at §2.0, then
> read the **START HERE** block. Execute **PR2 only** (B3 + B4 + B5), then stop and report.
>
> Ground rules that are already settled — do not re-derive them:
> - The label is **2" W × 4" H portrait**. Confirmed by Gary, flipped in `agroverse_shop_beta#183`.
> - B1/B2/B14 are **fixed** (`#184`). The funnel works end-to-end; the suite is **34/34 green**.
> - B3/B4/B5 root causes are in the register with file + line. Read them, don't rediscover them.
>
> Work in **`agroverse_shop_beta`** (never `_prod` — §3f). Use a **git worktree**. Write tests that
> **fail first** (§9), and drive the real handlers — page-load assertions are why these bugs shipped
> (§10). Report the DAO contribution as **`Claude Anthropic`** when PR2 merges, then tick the resume
> tracker.

---

## 3. What PR2 is

| Bug | What breaks | Where |
|---|---|---|
| **B3** 🟠 money | Quote shipping at qty 200, change to 1,000 → total updates, **rates don't re-fetch**, old selection stays, button stays enabled → **checkout at 1/5 the real shipping**. | `white-label.js:369` binds qty `change` → `updateOrderTotal` only; `calculateShipping` derives weight from qty (`:396`) but is bound solely to address blur / state change (`:378–381`). Nothing invalidates `selectedShippingRateId`. |
| **B4** 🟠 | Gallery **never sorts**; "newest first" is a no-op. | Upload signs via legacy `client.sign()` (`:320`), which per `dao-client/src/payload.ts:21` does **no Timestamp injection**. Backend reads `Timestamp` (`dao.py:369`) → `created_at: ""` on every design → `localeCompare` always 0. The order path (`:451`) correctly uses `submitEvent()` — **two signers in one file**. |
| **B5** 🟡 | Shipping failures are **silent** — nothing renders, button stays disabled, no reason given. | `catch (e) {}` — empty, `:435`. |

**Watch out on B3:** re-quoting on every qty change also collides with **Q2** — 500 bars ≈ 76 lb and
1,000 ≈ 151 lb are both over the **USPS 70 lb** single-parcel limit, so the higher tiers may return
no rates at all. If that surfaces, **stop and report** rather than inventing a multi-parcel scheme;
that's a Gary decision.

---

## 4. How to verify (this is the part that matters)

The pre-existing `tests/white-label-uat.spec.ts` **passed while the funnel was completely dead**,
because it only asserts on a loaded page. Both showstoppers lived in interaction handlers. Two specs
now exist that do it properly — follow their shape:

- `tests/white-label-label-spec.spec.ts` — spec-drift guard + validator driven by a **real file drop**
- `tests/white-label-auth-receipt.spec.ts` — registration + receipt driven by **real clicks**

```bash
cd /opt/claude_workspace/agroverse_shop_beta   # or wherever the box clones it
python3 -m http.server 8000 &
npx playwright test tests/white-label-*.spec.ts --project=chromium --reporter=list
# expect 34/34 before you change anything
```

Prove your new tests fail against the **unfixed** tree first, then pass. Both prior units did this
(D0: 5/7 → 7/7; PR1: 5/8 → 8/8) — it's the only evidence that a test tests anything.

---

## 5. Decisions that are Gary's, not the box's

Do not resolve these unilaterally; **stop and ask**:

- **Q1** — `agroverse-designs` is a **public** repo (`"visibility": "public"`). The sha256(email)
  foldering is obfuscation, not confidentiality: anyone with a customer's email can hash it and
  enumerate. It holds **unreleased corporate branding**. Making it private breaks the "no server
  proxy" design decision.
- **Q2** — the USPS 70 lb limit vs. the 500/1,000-bar options (above).
- **Q5** — no **600×1200 portrait** artwork template exists anywhere. **Blocks PR4.**
- Two canonical-doc corrections are logged in `CONTEXT_UPDATES.md` awaiting an explicit §3 ask:
  `PROJECT_INDEX.md:75` still says `(4″×2″ PNG)`; `WORKSPACE_CONTEXT.md:131`'s *"Sticker Mule 4x2in"*
  line needs a note that it's **QR-code label stock**, since reusing it as an artwork spec is the
  likely origin of the whole rotated-spec bug.
- **`AGROVERSE_WHITE_LABEL_SUPPLY_CHAIN.md` does not exist**, though
  `agroverse_shop/docs/WHITE_LABEL_SUPPLY_CHAIN_HANDOFF.md` points at it. The Liz pilot, routing,
  and school pricing it references are unrecorded — which is why the label spec had to be recovered
  by measuring pixels off a JPEG. Someone should write it.
