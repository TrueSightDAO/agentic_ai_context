# TrueSight DAO — Business Model

> **Owner:** Sophia Truesight (autopilot). **Governor:** Gary.
> **Origin:** 2026-10 thread — an ESG/credentialing contact in Hong Kong (via Dash) asked four
> questions: *how does the business cycle work · who are the customers/buyers · are you purchasing
> carbon credits or something else · how do you turn tree planting into a measurable product and
> what do clients use it for.* Answered live from four separate operational docs, with three factual
> drifts caught in review. This file exists so that never happens again.
> **Revision:** v1.

---

## 0. What this doc is — and is not

**Is:** the canonical, citable answer to "how does the business actually work?". One cycle, one
customer model, one product unit, one explicit statement of what we do **not** sell.

**Is not:** the growth model. Acquisition channels, retention loops, write-offs and anti-patterns
live in [`growth/GROWTH_MODEL.md`](./growth/GROWTH_MODEL.md) — a different question ("how do we get
more of them?") from this one ("what is being sold, to whom, for what?"). Note the path: the bare
`GROWTH_MODEL.md` referenced in some context indexes does not exist.

**Reading discipline.** §5 is an evidence register. Every load-bearing claim carries a status. Do
not restate a ⚠️ or 🔵 claim as though it were ✅ — that is precisely the failure mode this doc was
created to stop. If you are drafting external copy, read §5 first.

---

## 1. The cycle

```
financier / grant capital
      │
      ▼
TrueTech Inc funds per-tree support payments
      │
      ▼
farmers (and CFR students) plant native trees on their own land
      │
      ▼
evidence captured: lat/long · species · planting date · photo-as-file (EXIF) · planter identity
      │
      ▼
RSA-signed [TREE PLANTING EVENT] → public tree registry (SunMint)
      │
      ▼
R$5.00 per verified tree paid DIRECT to the planter via PIX
      │
      ▼
cacao harvested → processed → packaged into retail-ready bags
      │
      ▼
each bag minted with a serialized QR → traceable to the farm, and (when linked) to a tree
      │
      ▼
bag sold — wholesale, consignment, or D2C on agroverse.shop
      │
      ▼
sale proceeds cycle back toward the next round of tree-financing
      │
      └──────────────► back to the top
```

**Cycle time.** Cacao in Bahia is available year-round, so shipments do not require seasonal
prestocking; the operational lead time from PO to destination port is roughly five months
(`SUPPLY_CHAIN_SIMPLIFICATION.md`).

**Who actually pays.** The R$5.00/tree is paid by **TrueTech Inc** (Delaware C-Corp, EIN
88-3411514, Laguna Beach CA; President Gary Teh), operating the SunMint programme and the Agroverse
project of the TrueSight DAO — **not** by "the DAO treasury"
(`CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md` §1, §3). This distinction matters to any external
counterparty doing diligence: they need a named legal obligor.

**The last hop is intent, not yet mechanism.** No allocation rule, waterfall, or ring-fence
currently documents that cacao proceeds replenish the tree-financing pool. Say "cycles back toward",
not "replenishes".

### The planting agreement, precisely

| Term | Value | Source |
|---|---|---|
| Support payment | **R$ 5.00 (five Brazilian Reais) per verified tree**, no fixed total | CRF agreement §3 |
| Paid to | The **planter directly, via PIX** | §3 |
| Payer | TrueTech Inc | §1 |
| Implementing partner | CEPOTX — Cooperativa Central de Produção Orgânica da Transamazônica e Xingu (CNPJ 22.568.369/0001-38) | §1 |
| Beneficiary institution | Casa Familiar Rural de Anapu "Dorothy Stang" (CFR) | §1 |
| Species | Native Amazon biome only; cacao agroforestry expressly supported; exotic/invasive excluded | §4 |
| Planting evidence | lat/long · species · planting date · photo submitted **as a file** so EXIF is preserved · planter identity | §5 |
| Monitoring cadence | Every **6 months**, two photos: card-at-trunk at **1.30 m** with an **ISO-7810 ID-1 card (85.60 × 53.98 mm)** as scale reference, plus a full-tree photo. Trees under 1.30 m → root-collar diameter + total height | §6 |

---

## 2. Who buys

| Tier | Who | Terms | Status |
|---|---|---|---|
| **Wholesale** | Cafés, specialty retailers | **$17.00 / 200 g bag**, 10-bag opening; retailer pays at order | ✅ Running |
| **Consignment** | Retail venues without upfront capital | **$17.00 / 200 g bag**, 5-bag opening; retailer pays as sold | ✅ Running |
| **Direct-to-consumer** | End consumers via agroverse.shop | Retail, with QR provenance | ✅ Running |
| **Marketplace** | Faire | Inventory sync + drift detection landing; orders → ledger with `channel=Faire` | 🟩 Being built |
| **Impact funders / family offices** | Buy **outcomes** — verified tree-planting data, impact reporting — **not credits** | Bespoke | ✅ Conceptually defined |
| **"Finance a tree" community** | Contributors buying a bag explicitly framed as sponsoring a tree | Bespoke | 🔵 Positioning idea, not a running channel |

Recommended retail on the 200 g ceremonial pouch is **$25–35** (`agroverse/AGROVERSE_PRICE_LIST_AND_ASSETS.md`).

**Legal constraint on the funder tier.** Credit rights are **not** granted to donors — granting them
would break the charitable deductibility of the contribution
(`LEGAL_ENTITY_STRUCTURING_PROPOSAL_v2.md`). Any funder-facing copy must not imply a future credit
entitlement.

---

## 3. What we sell — and what we deliberately do not

### Direct answer: we neither purchase nor sell carbon credits

Both halves matter, because the question is usually asked from the buyer's side:

- **We do not purchase credits** to offset our own operations.
- **We do not sell credits today** — and none have ever been issued.

`[CARBON CREDIT ISSUANCE EVENT]` exists as a *designed future ledger event*. It has never fired. The
monitoring data accumulating today is **evidence**, not credits. Anyone saying TrueSight "sells carbon
credits" is describing a roadmap, not a product.

### What we do sell

A **physical product (cacao) carrying an attested provenance record** — a specific tree, at recorded
GPS coordinates, with a photographed planting, signed by the person who planted it, in a public
append-only record. The customer is not buying an offset against emissions already made; they are
buying cacao, and the tree-financing is the traceable origin of that purchase.

This sidesteps the weakest property of the voluntary carbon market — an abstract tonnage claim against
a counterfactual baseline — by replacing it with a literal, countable instance.

### Why we are not (yet) in the credit market

Formal credit origination requires a project developer, a baseline, and third-party validation and
verification (VVB): expensive and slow. Two further facts worth stating plainly to a sophisticated
audience:

- **The methodology has moved.** The applicable pathway for new planting is **Verra VM0047
  (Afforestation, Reforestation, Revegetation)**, which uses a **dynamic performance benchmark**
  derived from ex-post remote-sensing comparison rather than a static baseline. VM0017 is superseded.
  **Plan Vivo / Acorn PM002** is the alternative first-certification decision for the CRF cohort.
- **VM0047 v1.1 widened eligibility.** It no longer requires land to have been non-forest for ten
  years; it permits ARR on **forested land not managed for wood products** — i.e. degraded forest —
  and explicitly covers measures that *enhance stocks in existing forests*. The claim "standing
  old-growth forest is not creditable at all" is therefore **too absolute** and will be corrected in
  the room if you make it. The defensible, narrower version: for intact old-growth with no degradation
  and no timber management, **additionality fails** — there is no plausible counterfactual in which
  those stands would be cleared. That stand has a biodiversity and provenance story; it does not have
  a carbon story. See `plans/SITIO_CATARINENSE_FARM_ONBOARDING_PLAN.md` §0.

### The channel that exists if origination ever happens

**HKEX Core Climate** (launched Oct 2022) settles in HKD and RMB, carried **60+ listed projects by
end-2025 including forestry and South American projects**, and accepts both Verra VCS and, since
August 2024, Gold Standard VER. If TrueSight ever originates credits, that is the rail — presenting
it that way turns "we are not in this market" from a limitation into a staged roadmap.

### Greenwashing guardrail — hard rule

**No CO₂e figure is sold, implied, or attributed to any bag or any purchase.** No copy may suggest a
bag is "carbon neutral" or offsets a quantity of emissions. We do not have a methodology-backed
per-bag tonnage figure and must never imply one. This is a regulatory exposure, not just a taste
question.

---

## 4. The measurable unit

**The product unit is the bag's QR code.** Scanning it resolves to a public page:

```
https://truesight.me/qr/?id=<qr_id>
```

(e.g. `https://truesight.me/qr/?id=2024SA_20251227_35`). A single static template,
`truesight_me_beta/qr/index.html`, mirrored to prod; pure HTML + vanilla JS, no backend. It reads
`?id=` (`?q=` is ignored), fetches `lineage-assets/qrs/<qr_id>.json` from GitHub, and renders the QR
image, status badge, lineage cells, current-holder block and event timeline.

### What the page shows

- GPS location and photo of the tree, taken from the **RSA-signed `[TREE PLANTING EVENT]` payload**
- Planting date (derived from image EXIF / ledger — not the sheet's logging column)
- The planter's attestation, via their credential `pk_hash`
- An append-only event timeline for that asset specifically

### The bag↔tree binding

A bag QR linked to a planted tree is framed **`ASSIGNED_TO_TREE`** (carrying `lineage.linked_tree`),
not `SOLD`. This is a governor ruling from 2026-09-24 (`sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` §7):
the `sold` event is *history* — the bag was sold, and that sale financed the tree — while the *current
state* is tree-linked. Worked example: `2024OSCAR_CB_20260620_1` → `linked_tree:
Edgar_20260903083523_003`. Manifests are re-seeded from the sheet, never hand-edited.

In the CFR cohort the linkage convention is inverted: the tree's `qr_code` equals the **student's
credential `pk_hash`** and its `landing_page` equals the student's `profile_url`, so tree and
credential point at each other (CRF agreement §8, "Lineage Route B").

### It is a live record, not a blockchain

**Do not describe this as on-chain.** Three independent sources agree it is not:

- `PROJECT_INDEX.md` — TrueChain ships genesis + sample contracts + Mirror-Service design, but **no
  validators are currently producing blocks and there is no Mirror Service**.
- `proposal_drafts/BLOCKCHAIN_ANCHORING_PROPOSAL.md` — TDG "are ledger entries, not on-chain tokens";
  anchoring is framed as a *conditional* future, contingent on a real external-verifiability need.
- `LINEAGE_ASSETS.md` — the provenance page reads a GitHub raw JSON file. That is GitHub, not a chain.

The honest formulation is **stronger**, not weaker:

> Every claim is cryptographically signed and recorded in a public append-only file with per-asset
> git history — every change attributable, timestamped and diffable. Not a blockchain; deliberately
> a public record readable without trusting us.

### There IS a PDF certificate — own it

A **SunMint Certificate of Tree Guardianship** exists per linked bag, RSA-signed, downloadable from
its provenance page (`sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md`). Do not claim "we don't issue PDFs".
The correct framing:

> The PDF is the artefact; the live record is the proof. A PDF can be forged by anyone with an editor.
> The signed event behind it cannot, and the git history shows whether it was ever altered.

### Attested is not the same as independently verified

We hold **farm-attested, tamper-evident** records: any claim traces to a named signer and cannot be
altered undetected. We do **not** yet hold **independently verified** records — no third-party VVB
has inspected that a given photograph shows the asserted species at the asserted coordinate.
Third-party audit is the step that would make these credit-grade. We are not claiming it. Stating
this unprompted is the entire basis for the "we are more honest than a tonnage claim" argument; blur
it and the argument collapses.

---

## 5. Evidence register

Do not upgrade a status without new evidence. **✅** verified against repo · **⚠️** mechanism exists
but not load-bearing at scale · **❌** do not claim · **🔵** needs an external citation or not yet true.

| # | Claim | Status | Source / note |
|---|---|---|---|
| 1 | R$5.00 per verified tree, direct to planter via PIX | ✅ | CRF agreement §3, §7 |
| 2 | Payer is TrueTech Inc, not the DAO treasury | ✅ | CRF agreement §1 |
| 3 | GPS + species + date + photo-as-file + planter identity required per tree | ✅ | CRF agreement §5 |
| 4 | Six-monthly monitoring, ISO-7810 card at 1.30 m | ✅ | CRF agreement §6 |
| 5 | Trees registered as RSA-signed tree-planting events | ✅ | `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` §5; `plans/SUNMINT_TREE_GROWTH_MONITORING_PLAN.md` §3 |
| 6 | $17/bag wholesale (10-bag) and consignment (5-bag), RRP $25–35 | ✅ | `agroverse/AGROVERSE_PRICE_LIST_AND_ASSETS.md` |
| 7 | Provenance page live at `truesight.me/qr/?id=` | ✅ | `LINEAGE_ASSETS.md` §"rendering surface" |
| 8 | Bag↔tree binding is formally specified (`ASSIGNED_TO_TREE`) | ✅ | SOP §7; governor ruling 2026-09-24 |
| 9 | Bag↔tree linkage is populated **at scale** | ⚠️ | Live check: **520 sold QRs / 0 `ASSIGNED_TO_TREE`** (`handoffs/HANDOFF_MANIFEST.md`). Treat as pilot; one worked example |
| 10 | Real-world QR scans land on the provenance page | ❌/⚠️ | `LINEAGE_ASSETS.md`: the new surface is **demo-only**; scans in the wild still 302 to the sheet's landing page. Fix = flip column B for sample QRs. **Do this before any live demo** |
| 11 | The record is **on-chain** | ❌ | See §4 — no validators, no Mirror Service; TDG are ledger entries |
| 12 | Claims are independently / third-party verified | ❌ | No VVB audit. Attested only |
| 13 | Credits have been issued | ❌ | `[CARBON CREDIT ISSUANCE EVENT]` never fired |
| 14 | Granting credit rights to donors | ❌ | `LEGAL_ENTITY_STRUCTURING_PROPOSAL_v2.md` — breaks deductibility |
| 15 | Sale proceeds *mechanically* replenish the financing pool | 🔵 | Intent only; no documented allocation rule |
| 16 | Brazil REDD+ ≈ $2.50/t (Q1 2025); VM0048 floor ≈ $12/t | 🔵 | Currently only in our own `plans/SITIO_CATARINENSE_FARM_ONBOARDING_PLAN.md` §0 — an internal draft note, **not** a citation. Get a dated public source before quoting externally |
| 17 | "Finance a tree" community tier | 🔵 | Positioning idea; no running channel documented |
| 18 | Specific named retail counterparties | 🔵 | Confirm consent before naming any partner in external material |
| 19 | VM0047 v1.1 permits ARR on degraded forest land | ✅ (external) | Verra VM0047 v1.1 — dynamic performance benchmark; forested land not managed for wood products now eligible |
| 20 | HKEX Core Climate carries forestry + South American projects, HKD/RMB | ✅ (external) | HKEX Core Climate, launched Oct 2022; 60+ projects by end-2025; VCS + GS-VER |

---

## 6. Known gaps — fix before external use

1. **QR redirect is demo-only.** Flip the Agroverse QR codes sheet column B for the sample QRs to
   `https://truesight.me/qr/?id=<qr_id>`, scan a physical bag, confirm round-trip. Ten minutes of
   data change; without it a live demo visibly fails. No QR regeneration needed.
2. **Linkage is unpopulated.** 520 sold / 0 linked. Either link a handful of real bags before a
   meeting, or present the single worked example as the pilot it is. Given this document's own
   thesis — literal and small beats abstract and large — the pilot framing is respectable.
3. **Planter-name consent.** The provenance page surfaces the planter's name, joined via `pk_hash`
   to the Main Ledger contributor record. For an indefinite public page naming a smallholder — and
   for CFR students, some of them minors covered by parental consent under CRF agreement §9 — this
   needs a deliberate decision and a data-minimisation answer ready.
4. **No VVB.** See §4. Say it before being asked.
5. **No proceeds allocation rule.** See §1. Either write one or keep describing it as intent.
6. **Two $/tonne figures lack a public source.** See register #16.
7. **RESOLVED 2026-10-20 — bag↔tree binding does exist.** An earlier draft of this thread asserted
   the binding was undocumented; a search on the wrong vocabulary (`one tree per bag`) returned
   nothing. The concept is spelled `ASSIGNED_TO_TREE` / `lineage.linked_tree`. Recorded here so the
   error is not repeated.

---

## 7. Cross-references

| Question | Where it actually lives |
|---|---|
| How do we get more customers / partners? | `growth/GROWTH_MODEL.md` (acquisition + retention loops) |
| What does a shipment cost, and how does cacao move? | `SUPPLY_CHAIN_AND_FREIGHTING.md`, `SUPPLY_CHAIN_SIMPLIFICATION.md` |
| How do QRs get named and minted? | `agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md` |
| How does a QR resolve to a provenance page? | `LINEAGE_ASSETS.md` |
| How is a certificate rendered and gated? | `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` |
| What are the planting payment terms? | `CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md` |
| How is growth measured as biomass / CO₂e? | `plans/SUNMINT_TREE_GROWTH_MONITORING_PLAN.md` |
| What legal entity contracts with whom? | `LEGAL_ENTITY_STRUCTURING_PROPOSAL_v2.md`, `PROSPERA_ENTITY_OPERATING_AGREEMENT.md` |
| Should we anchor on-chain, and when? | `proposal_drafts/BLOCKCHAIN_ANCHORING_PROPOSAL.md` |
| How are plots registered as restoration vs conservation? | `SUNMINT_PLOTS_REGISTRY.md` |

---

## 8. The one-paragraph version

TrueTech Inc pays smallholders and CFR students **R$5 per verified tree** by PIX, direct, against
GPS-pinned, photographed, cryptographically signed evidence in a public registry. Those trees — cacao
interplanted with native Amazonian species — produce cacao that is processed, bagged and sold at **$17
wholesale** or retail through agroverse.shop, each bag carrying a serialized QR that resolves to a
public provenance record. We do not buy or sell carbon credits and have never issued one; we sell a
physical product with an attested provenance trail, and we say plainly that the trail is
**tamper-evident and attributable but not yet third-party verified**. The trees are countable, the
farmers are paid, and the record is public.
