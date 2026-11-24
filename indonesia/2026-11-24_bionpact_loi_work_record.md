# BionPact Indonesia LOI — work record (v1 to v8)

**Prepared by:** Sophia Truesight (autopilot) · **For:** Gary Teh, Director, BionPact Pte Ltd
**Date:** 2026-11-24 · **Status:** signature-ready, **NOT SENT**

Purpose: record what the Letter of Intent went through — the directives, what changed in each version and why, and how compliance was verified — so the final state can be audited without replaying the chat transcript.

**The letter itself is intentionally not stored here.** The final PDF carries a signature and describes a market-entry strategy; the artifact remains on the autopilot box at `/tmp/loi/BionPact_LOI_v8_final.pdf`. Ask Gary for a copy.

---

## 1. Research gates — verified before drafting

Four claims were checked to source rather than asserted. Two of the checks corrected earlier errors, including one of our own.

| Gate | Finding | Why it mattered |
|---|---|---|
| 30–40 t/ha "cocoa" yield | **Not cocoa.** These are oil palm FFB figures (Global Yield Gap Atlas 18.2–41.6 t; MPOB 22–24 t potential). Actual cocoa: BPS national **715 kg/ha**, Central Sulawesi 705, BMP trials >1,000 | An anomaly that would otherwise have been treated as a typo was root-caused to the wrong crop |
| Rp 9bn / 3,000 ha | **Cannot be project cost** — Rp 3m/ha does not cover ~1,000 seedlings/hectare plus clearing plus labour, and is *below one year* of operating cost for an established farm (Fahmid 2018: ~Rp 11.95m/ha/season). Reconciled as a **seedling + wage-subsidy fiscal line** | Prevented a budget figure entering the document under a false definition |
| PP 57/2016 | An **amendment to PP 71/2014** — both citations required; still in force; ≥30% KHG and ≥3 m peat protection | ⚠️ **Self-correction:** earlier work stated BRG sits under PP 57/2016. It does not — BRG is **Perpres 1/2016**, mandate lapsed **30 Dec 2024** |
| POJK 40/POJK.03/2019 | Kol 1–5 day-bands; NPL from Kol 3; **PPAP 5/15/50/100% calculated after deducting collateral** | The precise capital-efficiency mechanism had previously only been asserted |

---

## 2. Directive log — what each directive changed

Eight full drafts. Each was a rebuild rather than a patch, because every directive changed the document's register or argument, not just its wording.

| Directive | Change |
|---|---|
| 8a — tone, addressee, signatory | v2 read as an internal memo. Cause identified: **defensive apparatus built for the wrong reader** — an opening that pre-emptively disclaimed a land grab nobody had raised. Rebuilt as a warm collegial introduction. Addressee became "To Whomever It May Concern"; signatory Gary Teh, **Director, BionPact Pte Ltd** |
| 10 — value proposition, entity name, drop peat/fire | **Yield-improvement framing removed as overreach** — no direct control over farming productivity. Reframed around verified origin + quality matched to a premium-paying buyer; the "invisible care, therefore unrewarded" argument. All peat, wildfire, FOLU, Forest City, mangrove, restoration and superseded regulatory content deleted |
| (Gary, direct) — commercial role | Added §6: **procure cocoa on behalf of buyers → proceeds finance new trees → land regenerates**, plus **native species agroforestry** alongside cocoa (placed in three locations so it survives section-level reading) |
| (Gary, direct) — date | Date of issue set to **25 November 2026** (UTC was still 24 Nov; Singapore and Jakarta already on the 25th) |
| (Gary, direct) — scope correction | The letter never *said* "we operate in Indonesia" — the overclaim was **grammatical**: five unqualified present-tense procurement claims inside a letter about Indonesia. All scoped to the Amazon; Indonesia now stated plainly as **where we do not yet operate** |
| (Gary, direct) — signature | Signature inserted above the signatory block with verified clearance |

---

## 3. Two judgement calls worth preserving

**Financing structure.** Described as *pre-financing / an advance against future delivery*, deliberately not "lending". Financing farmers in Indonesia sits inside an OJK-licensed perimeter (POJK 77/2016 — *pinjaman online* / P2P lending); an unlicensed entity lending to the public is exposed. An advance against delivery keeps it a **trade** transaction rather than a **credit** transaction.

> ⚠️ **Open item: this needs Indonesian counsel review before any farmer signs anything.** If BionPact intends to actually lend, that is a licensing question; if it is an advance against offtake, it is not. The letter currently takes the second position.

**The concession material stays out.** Parigi Moutong, PT ATA/PT AAL, and the IUP→HGU regularisation argument are **not in the letter**. This is a general-capability introduction through a warm contact; naming a distressed concession to an unknown office is the wrong exposure, and would make the document transactional again. Those belong in a separate, specifically-addressed conversation.

---

## 4. Verification method

Every version was checked programmatically against a prohibited-term list rather than by eye. Final state (v8):

- **30 prohibited terms at zero** — TrueSight, DAO, token, blockchain, crypto, TDG, Founder, co-founder, "Pte. Ltd.", gambut, mangrove, Forest City, FOLU, Nusantara, groundwater, rewetting, burning, wildfire, deforestation, restoration, rehabilitation, carbon, biodiversity, PP 71/2014, PP 27/2025, Law 3/2022, Perpres 63/2022, yield, "700 to 800", "1.5 tonnes"
- **Whole-word `peat` and `fire` both 0** — note: a naive substring match falsely flags `peat` inside `repeatedly`; always test whole-word
- **9/9 sections present in order**; **12/12 required elements** including both scope statements, date, UEN, and the three commercial-loop phrases
- **Exactly 1 image**, page 4 only

Two verification traps worth recording:

1. **The signature PNG has zero bottom padding** — its ink runs to the final pixel. A placement that looked correct by bounding box **overlapped the printed name's cap height by 2pt**. Caught by measuring the alpha-channel bbox, not the image rectangle. Final clearance: **4pt**.
2. **Case-sensitive greps produce false "MISSING" results** — `agroforestry` reported absent when `Agroforestry` opened a sentence.

---

## 5. Repo hygiene note

`/tmp/loi/build.py` is a **stale v1-era artifact** that still reads the peat/FOLU draft superseded by directive 10. It is **not** the build path for v4 onward, which were generated directly. Do not use it as a reference for the current document. It should probably be deleted.

---

## 6. Open items

| Item | Status |
|---|---|
| **Contact block** | 🔴 **The one real blocker.** `gary@bionpact.com` bounces (551 5.1.1); no ACRA registered address on file. The letter has a signature but no direct reply path |
| Indonesian counsel review of financing structure | 🔴 Recommended before any farmer agreement |
| Nominal addressee (AO/AA) | 🟡 "To Whomever It May Concern" stands until a name is supplied |
| Length | 🟡 6 pp (4 letter + 2 background note). Cutting the background note returns it to 4 pp with nothing lost |
| Bahasa Indonesia version | 🟡 Offered in the letter; not yet produced |
| **Send** | ⛔ **Nothing sent to Rusmin or any Indonesian party.** Gary sends |
