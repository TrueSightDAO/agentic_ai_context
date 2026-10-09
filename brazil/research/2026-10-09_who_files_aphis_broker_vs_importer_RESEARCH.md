# RESEARCH — Do *we* file APHIS, or does the customs broker?

**Date:** 2026-10-09 · **Author:** Sophia Truesight (autopilot) · thread 10800
**Question (governor):** *"Do we file Aphis or the customs broker does it?"*

---

## 0. Short answer — three files, three owners

| # | File | Who does it | Why |
|---|---|---|---|
| 1 | **APHIS PPQ 587 permit** | 🔴 **TrueTech — WE must hold it** | Bound to an **eAuth identity** (SSN / photo ID at a USDA LRA) and to **our** name. **A broker cannot hold it for us.** |
| 2 | **APHIS Core message set** (permit no. + PGA codes) | **Licensed US customs broker, in ACE/ABI** | CBP requires the **broker** to enter the Government Agency Program Code. |
| 3 | **FDA Prior Notice** | **Us — TrueTech has filed every one** | Verified from our own filings (§2). |

⇒ **A broker cannot substitute for #1.** Even a flawless broker is blocked unless **we** already hold the permit.

## 1. Every "customs broker" in our context is BRAZIL-side

All references resolve to the **despachante** — Omega's **Valéria R. Barretto, Lázaro B. Reis, Jackson P.
Ferreira** — added as **representantes in SISCOMEX/RADAR** (see
`brazil/sources/2026-05-18_omega_siscomex_representante_tutorial_notes.md`,
`brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §30-09).

**There is no US customs broker named anywhere in our context.**

## 2. 🔴 The material finding — we self-file

Every FDA Prior Notice in `fda_fsvp` is submitted **by TrueTech Inc directly** (Zhiwen Teh,
`admin@truesight.me`):

| Shipment | PN Envelope | Entry Type | Submitter |
|---|---|---|---|
| 2023-11 100 kg (Coopercabruca) | `###-8407752-9` | Consumption | **TrueTech Inc** |
| 2024-09 30 bottles molasses | `F24X24688706` | Mail (Commercial) | **TrueTech Inc** |
| 2024-10 20 kg + 88 bags nibs | `240523261506` / `240523268263` | Mail (Commercial) | **TrueTech Inc** |
| 2025-02 / 2025-06 bars | `F25X25785849` / `F25X26344037` | Mail (Commercial) | **TrueTech Inc** |
| 2025-10 | `F25X27194819` | Baggage (hand-carried) | **TrueTech Inc** |
| **2026-10, 9 articles** | **`F26X30142399`** | **Consumption** | **TrueTech Inc** |

**⚠️ Look at the Entry Types: Mail · Baggage · hand-carried.**

**This is the first true commercial air-cargo entry** (`Consumption`, AWB `047-3175-3223`, TAP `TP237`)
— and the first that is plausibly **broker-filed**.

**That is very likely why we are having this conversation now.** Every prior shipment cleared through a
channel that did not require the APHIS machinery. **This one does** — and there may be **no broker on the
file who was ever set up to transmit it.**

## 3. The legal mechanics

1. **The permit is personal and identity-bound.** APHIS eFile: you must be **eAuthenticated**, and *"if
   your eAuthentication is not Verified, you will be prompted… (Example question: What is your Social
   Security number?)."* A broker cannot be the permittee for goods it does not own — the permit attaches
   to **our entity and address**.
2. **No small-lot exemption applies.** The "permit required only for 13 plants and more" rule that
   circulates is a **live-plants / small-lot** exemption — **not applicable** to a commercial cocoa seed
   consignment.
3. **A broker MAY apply on our behalf — with authority.** The application distinguishes **Applicant**
   from **Permittee**, and APHIS accepts *"supporting documentation, such as a **Power of Attorney
   Agreement**, to prove that you have permission from the Permittee to fill out and submit this
   application on their behalf."*
   ⇒ **This is the path:** grant the broker a **POA**; the broker applies/holds. **Without POA, no.**
   Permits are **free** and run **5 years**.
4. **Transmission is unambiguously the broker's job.** APHIS: *"the Government Agency Program Code is a
   requirement in the CBP ACE… PGA Message Set and **must be entered by the broker**."* Paper-filing
   fails: *"failure to submit the message set… will result in **paper clearance** of the cargo at the
   first U.S. port of arrival and **flagging of APHIS Core** at the in-bond port of entry, **duplicating
   work**."*
5. **Both permit numbers live on the permit**, and CBP references the second:
   - system record no. — `P-00001234`
   - **APHIS Permit Number** — `556-20-201-00015` (*Prefix-Year-Ordinal Day-Sequence*)

   **Only the permittee can read these out** — which is exactly why "let the broker handle it" fails when
   nobody holds the permit.
6. **A repo-wide search for either permit-number format in `fda_fsvp` returns nothing** — confirming
   PR #1562 §4: **no APHIS permit has ever existed in our records.**

## 4. What this changes

- **The broker cannot rescue us retroactively.** The blocker sits **upstream** of the broker: nobody has
  an eAuth-verified permit for TrueTech on this commodity.
- **The assignment splits cleanly:** ***we*** get identity-verified and apply (or grant a POA); ***the
  broker*** transmits. Asking the broker to "file APHIS" from a standing start **trades emails while the
  cargo sits.**
- ⚠️ **Unverified:** whether the self-filed Prior Notice pipeline implies **no broker was retained for
  this entry**. Strong inference from our own records — **but I have seen no engagement letter either
  way.** That is a question for Gary and Omega.

## 5. Honest gaps

- **ACIR remains login-gated** — the underlying *whether-a-permit-is-required* question for
  cocoa-from-Brazil is **still not authoritatively resolved** (PR #1562 §6).
- **No US broker identified in any repo; no engagement document found.** Cannot confirm one was or was
  not retained for this entry.
- **TrueTech's eAuth / identity-verification status is unknown.** If a permit is required, **that is the
  true critical path** — and it is **5–15 business days** *after* a clean application.

## Sources

- APHIS **eFile — How to Apply for PPQ 587** (Applicant vs Permittee; POA; eAuth/SSN) — https://www.aphis.usda.gov/sites/default/files/apply-fruits-vegetables-import-permits-ppq.pdf
- APHIS **eFile** — https://www.aphis.usda.gov/efile
- APHIS **Plants with Special Requirements** — https://www.aphis.usda.gov/plant-imports/buy-plants-seeds-online/plants-special-requirements
- APHIS **APHIS Core Message Set Q&A** — https://www.aphis.usda.gov/ace/aphis-core-message-set-questions-answers
- APHIS **ACE / Filing APHIS Core** — https://www.aphis.usda.gov/ace
- CBP **APHIS ACE PGA Message Set Implementation Guide (Core)** — https://www.cbp.gov/document/guidance/aphis-ace-pga-message-set-implementation-guide-core
- **Our own filings** — `fda_fsvp/**/*prior_notice*.pdf`, `fda_fsvp/**/*fda_web_entry*.pdf`

*Analysis only. Nothing sent, nothing purchased, no money moved.*
