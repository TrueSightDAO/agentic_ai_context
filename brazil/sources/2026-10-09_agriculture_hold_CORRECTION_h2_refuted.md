# CORRECTION — the FDA Prior Notice **was** filed; my H2 is retracted

**Date:** 2026-10-09 · **Author:** Sophia Truesight (autopilot) · thread 10800
**Corrects:** `brazil/sources/2026-10-09_cbp_agriculture_hold_rootcause_hypotheses.md` (PR #1557)
**Trigger:** governor, verbatim — *"We did submit FDA prior notice check the FDA FSVP repo"*

---

## 1. The governor was right. I was wrong. Here is exactly how.

| | |
|---|---|
| **What I asserted** | "FDA Prior Notice not confirmed filed" — H2, rated 🟠 STRONG |
| **What is true** | **Filed 2026-10-06 22:54:52 EDT, envelope `F26X30142399`**, 9 articles, net 302.06 kg |
| **Evidence** | `fda_fsvp/suppliers/black_king/20261006_fda_prior_notice_cacao_9_articles_sfo_air.pdf` |

### Root cause of my error — two compounding failures

1. **I trusted a stale status line.** §5.6 of the checklist still read `unfiled`. That line was written
   **02/10** when the working plan was for **Iolanda (Omega)** to file it. Gary then filed it himself on
   **06/10**, via PNSI, under TrueTech. The line was never updated.
2. **I searched the wrong repo.** I grepped `agentic_ai_context` for `F26X30142399` and for
   `prior notice` artifacts and found none — so I concluded "no evidence of filing". But the artefact
   lives **only** in `fda_fsvp`. **Absence of evidence in the wrong repository is not absence of the artefact.**
   The governor had to point me at the right repo.

> **Process lesson (worth generalising):** a lane-record status line is a *claim about* the FSVP repo,
> not a substitute for it. For any US-import compliance fact, **check `fda_fsvp` directly** — the
> authoritative artefact lives there by design (`SHIPMENT_DOCUMENTATION_PROCESS.md` step 6).

## 2. Revised hypothesis ranking

| # | Hypothesis (from PR #1557) | Rating then | Rating now | Why |
|---|---|---|---|---|
| **H1** | Phyto/APHIS cert never obtained | 🔴🔴 strongest | 🔴🔴 **sole leader** | strengthened — see §3 |
| **H2** | FDA PN not filed | 🟠 strong | ❌ **REFUTED** | `F26X30142399` filed 06/10, timing compliant |
| **H3** | Pallet material wood vs plastic / no IPPC stamp | 🔴 high impact | 🔴 unchanged | still unverified; cheapest decisive check |
| **H4** | HS `1810.00.00` (AWB) vs `1801.00.00` (invoice) | 🟠 medium-high | 🟠 unchanged | still never reconciled |
| **H5** | Stale `2106.90.00` tea code on the AWB | 🟡 medium | ❌ **WITHDRAWN** | the filed PN declares cacao tea too — AWB and PN **agree**, nothing stale |
| **H6** | PN/entry field mismatch | 🟡 medium | 🟡 **narrowed, but 2 new specifics** | PN↔net-weight now verified consistent; but see §4 |

**Net effect: the field of plausible causes narrowed from six to four, and one of them (H1) is now
materially stronger.** A correction that sharpens the answer is worth more than one that flatters it.

## 3. Why H1 (phyto / APHIS) now stands alone

1. **FDA ≠ APHIS.** The Prior Notice satisfies **FDA** food-import requirements. It does **not**
   satisfy **APHIS** plant-health requirements. Different agency, different gate, different paperwork.
2. **No plant-health document exists anywhere in `fda_fsvp`.** A repo-wide search for
   `phyto*`, `aphis*`, `ppq*`, `permit*`, `ispm*` across all suppliers returns **nothing** — no
   phytosanitary certificate (PPQ 587 / NPPO-issued), no APHIS import permit.
3. **Our own process doc assumes it away.** `fsvp/SHIPMENT_DOCUMENTATION_PROCESS.md` states:
   *"US lane does **not** need MAPA (only the China/GACC lane does)."* That is precisely the
   assumption a **CBP agriculture hold on a plant-product consignment** would falsify.
4. **The question was still open.** Omega asked on **29/09** whether the importer requires a
   phytosanitary certificate + Import Licence. **It was never answered** (§5.9 #1).

⇒ Prior notices being correctly filed makes the *plant-health* gap **more** visible, not less: the
FDA box was ticked and the APHIS box was not.

## 4. New discrepancies surfaced during verification

| # | Item | Detail |
|---|---|---|
| 1 | **Flight number** | PN says **`TP237`**; the AWB requests **`TP028`** |
| 2 | **Importer address** | PN uses **3041 Taraval St** (registered CBP address — correct); AWB consignee says **1423 Hayes St** |

Both are arrival-document mismatches CBP can flag. Neither implies misconduct — both are the kind of
stale-field drift that this lane has now produced repeatedly.

## 5. What I would still ask CBP/broker (re-cut after the correction)

- **What is the stated reason for the agriculture hold?** Any **emergency action notice** or CBP message?
- **Is a phytosanitary certificate or APHIS import permit required** for this HTS line? **Written answer.**
- Did the **entry** match the PN on **flight (TP237 vs TP028)** and **importer address**?
- **Photograph the pallets** — wood vs HDPE, **IPPC stamp** present? (unchanged; fastest check)
- Reconcile the **PN confirmation number** with the broker's **entry filing**.

## 6. Standing correction to the PR #1557 document

PR #1557 is **merged and therefore immutable as history** — this file is its correction, not a rewrite.
Where PR #1557 says the Prior Notice was unconfirmed/unfiled, **read this file instead.** The
pallet (H3) and HS (H4) findings are unaffected. See
`brazil/sources/2026-10-06_fda_prior_notice_F26X30142399_filed.md` for the full PN record.

*Analysis only. Nothing sent, nothing purchased, no money moved.*
