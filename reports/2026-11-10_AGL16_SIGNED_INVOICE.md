# AGL16 — signed invoice record (2026-11-10)

## Purpose

BionPact Pte Ltd needs a signed invoice from TrueTech Inc before payment of the AGL16 order (USD 2,226.84) can be actioned. This file records the signed artefact, how it was produced, and what was verified before release.

## The artefact

| | |
|---|---|
| Document | `TrueTech_to_BionPact_AGL16_20261031_REV3_SIGNED.pdf` |
| Issuer | TrueTech Inc (US Delaware, EIN 88-3411514) |
| Counterparty | BionPact Pte Ltd, UEN 202620924G |
| Amount | USD 2,226.84 |
| Pages / size | 4 pages, 24,421 bytes |
| Archived at | [store_interaction_attachments/bionpact/AGL16](https://github.com/TrueSightDAO/store_interaction_attachments/blob/main/bionpact/AGL16/TrueTech_to_BionPact_AGL16_20261031_REV3_SIGNED.pdf) |

## Revision selection

Four builds existed on the autopilot host: base, REV1, REV2, REV3.

**REV3 was signed** because it is the operative copy — its header states it supersedes all prior issues, and it is the version actually emailed to Luvenne Chew (OCBC) on 3 Nov 2026 under the subject `Re: OCBC Business Banking - BIONPACT PTE. LTD.`.

REV1 and REV2 were deliberately left unsigned.

## Placement

Clear whitespace above the navy footer, measured per page:

| Page | Clear band | Signature |
|---|---:|---|
| 1 | 381 pt | **yes** |
| 2 | 19.5 pt | no — dense line-item table |
| 3 | 43 pt | no — would collide with rows |
| 4 | large | no — terms page |

Signed page 1 only (the amount-and-parties page), with:

- signature image 95 × 46 pt, alpha mask preserved (SMask 20, xref 19, 342 × 165 source)
- 182 pt rule at y = 786
- caption `Zhiwen Teh (Gary Teh) - President, TrueTech Inc`
- sub-caption `Authorised signatory`

## Verification

- 300 dpi render of the signature box: **5.47% ink**, **0.00% pure-black pixels** (transparency survived, no black-box artefact), 92.6% white
- **Zero** text spans overlap the signature rectangle
- Extracted text still contains `2,226.84`, `202620924G`, `REV3` unchanged

## Open caveat — signature provenance

The signature image used is `/tmp/sig/gary_teh_signature_transparent.png` (342 × 165 RGBA, dated 29 Sep 2026). It has **no recorded origin**: it is named for the governor but appears in no repository, and `/tmp` does not survive a host rebuild.

Flagged to the governor for confirmation before the document goes to any third party. Moving the asset into a provenance-tracked location is a pending follow-up.

## Not done

- The signed invoice has **not** been emailed to BionPact, OCBC, or any other party. Issue remains the governor's explicit call.
- `gary@bionpact.com` still appears on related documents and still bounces (551 5.1.1). Unrelated to this artefact but unresolved.
