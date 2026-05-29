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

## A. Codify existing reality — **Batch 1, ratification-ready**

> **Decision (2026-05-29):** Gary directed that the (A) "codify reality" set move
> forward. The entries below are **finalized in the whitepaper's exact amendment
> format**, ready to paste into the Amendments section of the Google Doc. They
> are acknowledgment amendments — they record changes that have *already*
> happened operationally — so the Town Hall vote is a ratification/acknowledgment.
> **Set the effective date and "Voted in …" line at the ratifying vote** and
> attach the voting-outcome screenshot per the doc's amendment convention.
> The **(B)** items below this batch still need a substantive decision and are
> NOT part of Batch 1.

---

### PASTE-READY BLOCK (whitepaper Amendments section)

**20260529A — Contribution intake via the DApp and cryptographically signed events**
*Voted in Town Hall — past into effect __________ (set at vote)*

The "webform + governors manually update the ledger" mechanism is superseded.
Contributions are submitted through the DApp (`dapp.truesight.me`) as RSA-signed
events (e.g. `[CONTRIBUTION EVENT]`, `[SALES EVENT]`, `[INVENTORY MOVEMENT]`),
dispatched through Edgar (and the dao_protocol service) to the contribution
ledger. Each member registers a digital-signature key bound to their identity;
a valid signature is the gate for a submission. Governors retain validation,
scoring, and dispute authority; intake, signature verification, and dispatch are
automated. Technical model: see the Edgar whitepaper.

**20260529B — AI agents are recognized contributors**
*Voted in Town Hall — past into effect __________ (set at vote)*

AI agents that perform DAO work (software, documentation, infrastructure) are
recognized contributors under the existing rubric (100 TDG/hour, 1 TDG/USD).
An AI-agent `[CONTRIBUTION EVENT]` must include mandatory pull-request evidence
(`github.com/TrueSightDAO/<repo>/pull/<n>`) and an explicit description of what
changed. AI-agent contributions are subject to the same governor validation and
the same dispute-resolution path (escalation to the Town Hall) as human ones.

**20260529C — Contribution-based standing (no "founding member" / founder hierarchy)**
*Voted in Town Hall — past into effect __________ (set at vote)*

Standing in the DAO is earned through contribution, not founder status. Public
and internal copy shall not use "founding member" or frame individuals as
"founders"; the term "long-time contributor" (and "supporter," where apt) is
used instead. This reaffirms the contribution-based ethos already implicit in
the tokenomics.

**20260529D — Telegram as a primary communication surface; Beer Hall is archive-only**
*Voted in Town Hall — past into effect __________ (set at vote)*

Alongside the WhatsApp community, Telegram is now a primary communication and
record surface (Telegram chat logs feed contribution/TDG scoring). The Beer Hall
WhatsApp broadcast is retired; the Beer Hall digest is published as an
archive-only, newsletter-shaped artifact (static feed + oracle advisory
snapshot) rather than a WhatsApp blast. WhatsApp-era channel policies (e.g. the
8-channel cap, Town Hall gating) are read in this multi-platform light pending
the Batch-2 review.

**20260529E — Off-chain ledger of record; public transparency surfaces; on-chain deferred**
*Voted in Town Hall — past into effect __________ (set at vote)*

TDG governance tokens and contributions are recorded on the off-chain
contribution ledger (the double-entry "offchain transactions" sheet), which is
the current system of record. Transparency is provided through public surfaces —
`treasury-cache` JSON, `truesight.me/stats/*.json`, `llms.txt`, and per-program
explorers (e.g. `mirim-bahia.truesight.me`) — rather than a live chain. TrueChain
remains a design that is not in production, and on-chain settlement (and any
exchange listing) is conditional and deferred, superseding the earlier
"Migration to Ethereum," Phantom-wallet, and "On-Chain Vault/Amendment" language
until a chain strategy is ratified (Batch 2).

**20260529F — Managed ledgers, multi-currency treasury, and AGL export-financing syndicates**
*Voted in Town Hall — past into effect __________ (set at vote)*

The treasury operates multiple managed sub-ledgers (per Agroverse shipment and
per program, e.g. Tribo Mirim Bahia) and settles in multiple currencies (USD and
Brazilian reais), with cross-currency moves recorded as `[CURRENCY CONVERSION
EVENT]`s. DAO-financed export shipments are governed by Agroverse Guild Ledger
(AGL) Export Trade Financing Syndicate Agreements. **For future AGL contracts
that are shipment financing (direct shipment with physical collateral), the voted
default fund management fee is 20%, unless a specific contract states otherwise.
Operational-fund ledgers that invest in other AGLs do not charge an additional
fee at that layer, to avoid double-charging. Existing contracts stay on their
prior terms unless amended by mutual agreement.** Details: see the Agroverse
whitepaper and the syndicate agreement template.

**20260529G — Current initiatives**
*Voted in Town Hall — past into effect __________ (set at vote)*

The DAO's active initiatives now include, in addition to Agroverse: the
Credentialing platform (`truesight.me/credentials` — contribution-based
credentials/programs), Sunmint and Edgar (each documented in its own
whitepaper), Krake / getData.io, and the Tribo Bahia Mirim capoeira practice and
donation-transparency platform (`capoeira.agroverse.shop` /
`mirim-bahia.truesight.me`). Each initiative's specifics live in its own
whitepaper/docs; this list is the index.

**20260529H — Correction: premature exit reclaims a member's managed-ledger equity, not governance tokens**
*Voted in Town Hall — past into effect __________ (set at vote)*

This corrects a factual error in the existing Treasury section. The early-exit
penalty applies to a member's **equity position in the managed ledger they
invested in** — not to their governance tokens (TDG). On premature exit, that
**managed-ledger equity position** is reclaimed at a significantly discounted
value relative to the member's initial contribution, as a penalty for early
exit. Governance tokens earned for contributions are not the instrument being
reclaimed here. The sentence in the Treasury section that states governance
tokens are reclaimed on early exit is superseded by this clause.

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
