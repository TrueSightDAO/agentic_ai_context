# Farm & Program Media — People-Index Tiers & Biometric Consent Gates

**Status:** design proposal (thread 39733, 2026-09-30). **Tier 0–1 = shippable now. Tier 2–3 = HARD-GATED** (see §7).
**Author:** Sophia (TrueSight autopilot), recorded at Gary Teh's direction.
**Sibling docs:** `MEDIA_ARCHIVE_PIPELINE.md` (MAP), `AGROVERSE_SUNMINT_FARM_LISTING.md`,
`handoffs/FARM_MEDIA_TASK_PLAN_TEMPLATE.md`; `credentials/CREDENTIALING_PROGRAM_PAGES.md`;
`CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md`; `conventions/DEDUP_KEY_CONVENTION.md` §2.7.

> **Why this doc exists.** Site-visit media (farm + program batches) is ingested into MAP with a
> manifest that records provenance (GPS, capture time, hashes) and objects — and, today
> informally, the *people* visible in frame. Without a written tier boundary, a future template /
> daemon / prompt change can silently escalate from *counting* people to *identifying* them.
> This doc fixes the boundary so the leak is caught by construction, not by review discipline.

---

## 1. Tier model

| Tier | Capability | What is extracted | Gate |
|---|---|---|---|
| **0** | Provenance | GPS, capture time, device, content hashes | none — safe |
| **1** | People **count** | number of persons; coarse bounding box(es) | none — safe (mechanical gates §4) |
| **2** | People **identity** | transient cluster IDs (`person-A`, `person-B`, …) | consent-gated (§5) |
| **3** | **Biometric** identity | face embedding / voiceprint / voice ID | consent-gated (§5) **+ minors block §7** |

**The line is exact:** provenance and *counting* do **not** extract biometric identity. Face and
voice **do**. Tier 0–1 therefore carry none of the problems below and are shippable immediately;
Tier 2–3 are the whole of the risk surface.

---

## 2. Tier 0–1 — shippable now

- Per batch: provenance fields already in the MAP manifest (lat/lon, `creation_date`, device,
  sha256) **plus** a coarse `people_count` per frame (or per batch).
- **No** names, **no** persistent per-person handles, **no** biometrics.
- Coarse-count caveat — see §6: counts + GPS + farm identity can still aggregate to
  "who was where when" in a *tiny* cohort. Keep counts coarse and avoid publishing at
  (batch, farm, minute) resolution where N is small.

---

## 3. Tier 2–3 — consent-gated

Enabled only after §5 (consent mechanism) **and** §7 (minors answer) are satisfied.

---

## 4. Mechanical gates for Tier 0–1 (catch the leak by construction)

Gary's refinement: the most likely accidental leak is a scope-creep from *"count"* to
*"who"*, and it must be caught **mechanically**, not by trusting a later reviewer.

- **G1 — closed schema.** Tier 1's `people[]` JSON must be a **closed schema**:
  `additionalProperties: false`, with only allow-listed fields (`count`, `bbox`, fixed-enum
  keys). A free-text or open-object field is a name sink. A *blocklist* of "bad" names is
  insufficient — it leaks handles, initials, roles ("the guy in the red shirt").
- **G2 — negative injection test.** A test that feeds a **known-name payload** into the
  Tier-1 writer and asserts it is **rejected** (schema violation), not merely that the happy
  path emits no name. `people[].text = "João"` must fail loudly.
- **G3 — namespaced cluster IDs.** If/when cluster IDs exist (Tier 2), they are **not**
  globally sequential. `person-A` at Anapu must not be joinable to `person-A` at Santa Ana.
  Scope them opaquely, e.g. `<entity_id>:c<hash>`.
- **G4 — "transient" means within-batch, not persisted.** If Tier-2 clusters land in any
  globally-joinable store, we have built the biometric database we were trying to avoid. The
  transience **is** the privacy property.

---

## 5. Tier 2–3 identity model + consent

### 5.1 Identity key — cluster ID primary, `pk_hash` optional

Neither pure `pk_hash` nor a separate registry. **Transient cluster IDs are the primary
people-index key.** `pk_hash` is an **optional** link applied only once a cluster is
governor-confirmed **and** that person happens to already be DAO-registered.

Rationale (Gary's refinement — better than both originals): `pk_hash` identifies
DAO-registered contributors/members. Most people who appear in farm media (field workers,
visiting family, community members) will **never** have one. Anchoring the people-index to
`pk_hash` would silently **exclude or misrepresent the majority** of people actually in frame.

Backing: `conventions/DEDUP_KEY_CONVENTION.md` §2.7 — `pk_hash` is a *canonical join key over
the public key*, **"not a privacy device"**: anyone holding the public key re-derives it. It
can therefore only exist for key-bearing registrants.

### 5.2 The proxy-attestation gap (non-registered adults)

Most people in frame **cannot sign**. For a non-registered adult, "signed consent" must be
honest about *who signed*: a **proxy attestation by a governor / partner lead**, plus an
**archived paper release form**. Otherwise the record claims the subject's signature when it
is actually the DAO's. Name the proxy explicitly in the event.

### 5.3 Consent is a signed event, not a flag

`[BIOMETRIC CONSENT EVENT]` — the person (or their lawful proxy, §5.2 / §7) explicitly signs.
`[BIOMETRIC CONSENT REVOCATION EVENT]` — withdraws it. **A signed event can only be
superseded by another signed event**, unlike an admin-editable boolean — stronger and
consistent with how every other consequential DAO fact is recorded.

**Verified 2026-09-30 — there is no working per-person consent mechanism to mirror.**
- The literal `public_listable: true` is **hardcoded at record creation** in the GAS
  attestation path: `tokenomics/google_app_scripts/.../program_admin_endpoint.js` →
  `paProcessOneEvent` writes it into every fresh `identity.json`. It is **not** an active
  per-person opt-in/opt-out toggle.
- `lineage-credentials` has **zero** occurrences of the string.
- `credentials/CREDENTIALING_PROGRAM_PAGES.md` calls the flag a **"future"** item and Phase 5
  **"(Optional)"** — *"until that flag exists in `lineage-credentials`, treat this as
  advisory."* The only adjacent live knob is the **programme-wide** manifest hint
  `credential_visibility_default` (`"private"` for CFR) — also a hint, no per-person flip.

→ Tier 2/3 needs **real privacy design**, not reuse of a flag that does not do the job.

---

## 6. Residual risk that survives even Tier 0–1

Counts + GPS + farm identity, published publicly, still aggregate to "who was where when" in a
small cohort. Keep counts **coarse**, and avoid publication at (batch, farm, minute)
resolution where the cohort is small — re-identification-adjacent, though not a consent
problem.

---

## 7. HARD GATE — minors (must be answered before any Tier 2/3 work)

> **Even a locked-down prototype may not begin face/voice work until Gary gives an explicit
> answer on minors.** This is a **blocking gate**, not a detail to sort out later. Filed in
> `OPEN_FOLLOWUPS.md` under `## Pending`.

- **Why it's higher-stakes.** Biometric indexing (face clustering, voice ID) of a **minor** is
  a materially different — and much higher — consent problem than an adult contributor's.
- **LGPD is doubly gated.** Art. 11 makes biometrics **sensitive personal data** (specific
  consent required even from adults); Art. 14 requires **guardian**-specific consent + a
  best-interest assessment for minors.
- **Minors are the default population here, not an edge case.** The DAO's first real
  deployments are youth programs: CFR Anapu / CEPOTX students, Butterfly Effect (ERA),
  Tribo Bahia Mirim.
- **The DAO already anticipated this in three docs** (precedent — none is a working control):
  - `CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md` §9 — *"Students under eighteen (18) years of
    age participate only with the informed consent of a parent or legal guardian, who
    acknowledges the tree pledge and any public listing of the student's credential."*
  - `CRF_ANAPU_SUNMINT_COHORT_PROPOSAL.md` (~§4) — sets
    `"credential_visibility_default": "private"` *"for exactly this reason (CEPOTX students
    are minors)"*.
  - `credentials/CREDENTIALING_PROGRAM_PAGES.md` — the `public_listable` /
    `credential_visibility_default` machinery exists **"to gate minors"**; the doc itself
    flags it as future/optional and *advisory*.

**Required decision (Gary):** either (a) **exclude minors entirely** from Tier 2/3 (age-unknown
⇒ treated as minor ⇒ excluded), **or** (b) a **guardian-consent path** with a named release
form + recorded guardian attestation. Until answered, Tier 2/3 does not start.

---

## 8. Decision log

| # | Question | Decision |
|---|---|---|
| 1 | Tier boundary | 0–1 safe / 2–3 consent-gated. **Endorsed.** |
| 2 | Tier-1 leak control | Closed schema (**G1**) + negative injection test (**G2**), mechanical. |
| 3 | People-index key | Transient cluster IDs primary; `pk_hash` optional + governor-confirmed later. |
| 4 | Cluster-ID scoping | Namespaced (**G3**), non-persisted (**G4**). |
| 5 | Biometric-consent model | Signed `[BIOMETRIC CONSENT EVENT]` (+ REVOCATION); no flag to mirror. |
| 6 | Non-registered subjects | Proxy attestation + archived paper release (§5.2). |
| 7 | Minors | **HARD GATE** — awaiting Gary's answer (§7). |
| 8 | Ship Tier 0–1? | **Yes** — none of these problems apply. |

---

## 9. References

- `conventions/DEDUP_KEY_CONVENTION.md` §2.7 — `pk_hash` is a join key, **not** a privacy device.
- `tokenomics/google_app_scripts/.../program_admin_endpoint.js` — `paProcessOneEvent` (hardcoded `public_listable: true`).
- `credentials/CREDENTIALING_PROGRAM_PAGES.md` — `credential_visibility_default`, `public_listable` (future/optional), minors gating.
- `CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md` §9 — minors / guardian consent.
- `CRF_ANAPU_SUNMINT_COHORT_PROPOSAL.md` — `"credential_visibility_default": "private"` for minors.
- `MEDIA_ARCHIVE_PIPELINE.md` — the ingest pipeline this tier-gates.
- `OPEN_FOLLOWUPS.md` — minors hard-gate entry (filed with this doc).
