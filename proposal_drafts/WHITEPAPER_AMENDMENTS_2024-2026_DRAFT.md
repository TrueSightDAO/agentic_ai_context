# Whitepaper amendments — proposed 2024–2026 addendum (DRAFT)

**Status:** DRAFT for Town Hall review — **not yet ratified**. Nothing here is in
effect until voted per the whitepaper's governance process.

**Why this exists.** The main whitepaper
([truesight.me/whitepaper](https://truesight.me/whitepaper) →
[Google Doc](https://docs.google.com/document/d/1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic/edit))
is directionally intact (mission, values, the metagame, guild lifecycle, the
100 TDG/hr + 1 TDG/USD rates, the equinox/solstice governor cadence all still
hold), but its **Amendments log ends at `20231115`** while the operational and
technical layer has moved on substantially. This addendum proposes amendment
entries that bring the constitution back in line with how the DAO actually
transacts, communicates, and settles value as of 2026-05.

Each entry below is written in the whitepaper's existing amendment format
(`YYYYMMDD — Title` + body) but dates are **placeholders** to be set at the
ratifying vote. Entries are grouped into **(A) codify existing reality** (mostly
acknowledgment — the change already happened operationally) and **(B) needs a
fresh decision** (a genuine policy choice the Assembly should make).

> **Drafting note for governors:** sibling whitepapers already cover some of
> this in their own scope — Edgar (`truesight.me/edgar/whitepaper`), Agroverse
> (`/agroverse/whitepaper`), Sunmint (`/sunmint/whitepaper`). Where that's true
> it's flagged, so the main whitepaper can *reference* rather than duplicate.

---

## A. Codify existing reality (acknowledgment amendments)

### YYYYMMDD — Contribution submission via the DApp + cryptographically signed events
The whitepaper still describes contribution claims "via this webform" with
governors manually updating the ledger. In practice, contributions are now
submitted through the **DApp** (`dapp.truesight.me`) as **RSA-2048 digitally
signed events** (e.g. `[CONTRIBUTION EVENT]`, `[SALES EVENT]`,
`[INVENTORY MOVEMENT]`), dispatched through **Edgar** (and the newer
**dao_protocol** service) to the contribution ledger. Each member registers a
key bound to their identity; signatures are the gate. Governors still validate
and score, but the intake, signature verification, and most dispatch are
automated. *Reference the Edgar whitepaper for the technical model.*
**Effect:** "webform + manual governor entry" is superseded by signed-event
intake; the ledger remains the system of record.

### YYYYMMDD — AI agents are first-class contributors
AI coding/ops agents now perform real DAO work (software, docs, infrastructure)
and earn TDG via signed `[CONTRIBUTION EVENT]`s with **mandatory PR evidence**
(`github.com/TrueSightDAO/.../pull/N`) and an explicit description. This is an
established practice, consistent with the whitepaper's existing reference to
"the AI who does the validation and scoring." **Effect:** formally recognize AI
agents as contributors under the same rubric (1 TDG/USD, 100 TDG/hr) with the
PR-evidence requirement, governed by the same dispute-resolution path.

### YYYYMMDD — Contribution-based ethos (no "founding member" / "founder" hierarchy)
Cultural norm now in force across public surfaces: standing is **earned through
contribution**, not founder status. Public copy uses "long-time contributor"
(never "founding member"); individuals are framed as supporters/contributors,
not founders. **Effect:** codify the no-founder-hierarchy language convention.

### YYYYMMDD — Telegram as a primary communication surface; Beer Hall is archive-only
The whitepaper is WhatsApp-centric (Beer Hall / Town Hall as WhatsApp channels,
the 8-channel cap, Phantom wallet). Reality: **Telegram** is now a primary
surface — Telegram chat logs feed TDG scoring — and the **Beer Hall WhatsApp
broadcast was retired** (community feedback flagged the firehose as too noisy).
The Beer Hall digest is now an **archive-only newsletter-shaped artifact**
feeding the static feed + the oracle advisory snapshot, not a WhatsApp blast.
**Effect:** acknowledge Telegram + web/newsletter surfaces alongside WhatsApp;
note the Beer Hall posting change.

### YYYYMMDD — The contribution ledger is off-chain and publicly transparent (on-chain deferred)
The whitepaper anticipates "Migration to Ethereum," an "On-Chain Vault," and an
"On-Chain Constitutional Amendment Process." Current reality: **TDG remains
off-chain** on the contribution ledger (Google Sheets, double-entry offchain
transactions), with **public transparency surfaces** instead of a live chain —
`treasury-cache` JSON, `truesight.me/stats/*.json`, `llms.txt`, and per-program
transparency explorers (e.g. `mirim-bahia.truesight.me`). **TrueChain** exists as
a design but is **not running**; LATOKEN listing is on hold. **Effect:** state
that the off-chain ledger + public transparency surfaces are the current system
of record, and that on-chain settlement is conditional/deferred (see the
Blockchain Anchoring framing) rather than imminent.

### YYYYMMDD — Managed ledgers, multi-currency treasury, and AGL export-financing syndicates
The whitepaper's treasury model is a single "TrueTech Inc holds fiat." Reality:
the DAO now operates **multiple managed sub-ledgers** (per Agroverse shipment /
program, e.g. Tribo Mirim Bahia), a **multi-currency treasury** (USD + Brazilian
reais, with Wise/Pix conversion recorded as `[CURRENCY CONVERSION EVENT]`s), and
**AGL Export Trade Financing Syndicate Agreements** (precedence: shipment
financing = 20% DAO fee; operational fund investing in other AGLs = no fee).
*Reference the Agroverse whitepaper + syndicate template.* **Effect:** extend the
treasury section to cover managed ledgers, multi-currency settlement, and the
syndicate fee structure.

### YYYYMMDD — New initiatives since 2023
Acknowledge initiatives not present in the 2023 text: the **Credentialing
platform** (`truesight.me/credentials` — contribution-based CVs/programs),
**Sunmint** and **Edgar** (each with its own whitepaper), **Krake / getData.io**,
and the **Tribo Bahia Mirim** capoeira practice + transparency platform
(`capoeira.agroverse.shop` / `mirim-bahia.truesight.me`). **Effect:** list
current initiatives and point to their respective whitepapers/docs.

---

## B. Needs a fresh decision (policy choices for the Assembly)

### TBD — Autonomous agent operating boundary
An AI autopilot (governor chat + autonomous SRE/developer) now monitors
infrastructure and **opens fix PRs but never auto-merges**; merges require an
explicit governor command. Propose ratifying this **"propose-only, human-approval
on writes"** boundary as policy, and defining what (if anything) an autonomous
agent may execute without a human in the loop. *Open question:* credential
access scope for agents (see the OPEN_FOLLOWUPS credential-vault item).

### TBD — Chain / wallet strategy of record
Reconcile the conflicting on-chain references (Ethereum migration vs. Phantom /
Solana vs. TrueChain) into a single current position: what chain (if any), what
wallet, and the trigger conditions for actually standing up on-chain settlement.

### TBD — WhatsApp 8-channel cap relevance
With Telegram now primary and several WhatsApp policies (channel caps, Town Hall
gating) written for a WhatsApp-only world, decide which of those caps/policies
still bind and which should be restated for the current multi-platform reality.

---

## Items deliberately NOT changed
Mission, core values, the metagame and three hypotheses, the guild lifecycle
(Rethink/Implement/Operate/Deprecate), the 100 TDG/hr + 1 TDG/USD rates, the
governor election cadence (top-10 / 90 days / equinox-solstice), and the
existing 2023 amendment log entries — all remain in force as written.
