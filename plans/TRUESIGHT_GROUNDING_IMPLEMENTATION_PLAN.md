# TrueSight Grounding — Implementation Plan & Roadmap

## Vision

The Oracle draw is a **daily mindfulness grounding exercise** — a morning ritual that centers you before the day's execution. Each session is recorded as a `[PRACTICE EVENT]` under the program **`truesight-grounding`**, using the same infrastructure as capoeira.

When you message the autopilot on Telegram after your morning session, it reads today's draw from `lineage-credentials` and has full context for the day's execution conversation.

---

## Program Name: `truesight-grounding`

| Field | Value |
|-------|-------|
| Program slug | `truesight-grounding` |
| Display name | TrueSight Grounding |
| Tagline | *Daily mindfulness grounding exercise* |
| Practice type | `oracle-consultation` |
| Source page | `https://oracle.truesight.me/draw.html` |
| truesight.me path | `/programs/truesight-grounding/` |

The name is intentionally broader than "oracle" — it can later include meditation, breathwork, journaling, or any grounding practice. The oracle draw is the first practice type within it.

---

## Logo Concept

**Symbol:** A circle with a single vertical line descending from the top to the center dot.

```
    ┌─────┐
    │  │  │
    │  ●  │
    └─────┘
```

**Meaning:**
- The **circle** represents wholeness, the daily cycle, grounding
- The **vertical line** is the axis mundi — the centered self, the connection between heaven and earth (I Ching)
- The **center dot** is the present moment — the still point at the center of the day's motion
- Together: **grounded, centered, ready**

**Color:** A warm earth tone — deep amber or terracotta — to evoke morning light and grounding.

**File:** `truesight_me_prod/assets/images/programs/truesight-grounding/logo.svg`

---

## Architecture

```
oracle.truesight.me (GitHub Pages)
  └── draw.html — Oracle draw page
        ├── Generates/loads RSA keypair (localStorage, same as capoeira)
        ├── User clicks "Draw" → hexagrams/cards revealed
        ├── User reviews reading, adds advisory summary
        ├── User clicks "Record Session" → builds [PRACTICE EVENT]
        ├── Signs with RSASSA-PKCS1-v1_5 / SHA-256
        └── POST → Edgar /dao/submit_contribution

Edgar (dao_protocol)
  └── Logs to Telegram Chat Logs
  └── Webhook → GAS practice_event_processing.gs
        ├── Parses [PRACTICE EVENT]
        ├── Validates program "truesight-grounding" in manifest
        ├── Derives pk-slug from public key
        └── Commits to lineage-credentials:
            programs/truesight-grounding/<pk-slug>/practice/<timestamp>-<hash>.json

truesight.me (GitHub Pages)
  └── /programs/truesight-grounding/index.html — Program landing page
  └── /programs/truesight-grounding/credentials/#<pk-slug> — Practice history viewer

Autopilot (Telegram / chat)
  └── Reads lineage-credentials for today's draw
  └── Has context for execution conversation
```

---

## Draw Flow (timing)

1. User visits `oracle.truesight.me/draw.html`
2. User clicks **"Draw"** → hexagrams/cards are revealed on screen (the reading)
3. User reviews the reading, optionally adds notes or an advisory summary
4. User clicks **"Record Session"** → the `[PRACTICE EVENT]` is built with the full context (what was drawn + the advisory), signed with the RSA keypair, and submitted to Edgar
5. The draw is now recorded in `lineage-credentials` and available for the autopilot to reference

**Key design choice:** Submission happens **after** the reading is returned, not when the user clicks "draw cards." This ensures the record captures the complete session — not just the raw draw, but what you took away from it.

---

## Event Payload Shape

```
[PRACTICE EVENT]
- Program: truesight-grounding
- Practice Type: oracle-consultation
- Practitioner Public Key: MIIB...
- Practitioner Name: Gary Teh
- Captured At: 2026-05-31T14:00:00.000Z
- Source URL: https://oracle.truesight.me/draw.html
- Payload JSON:
{
  "hexagrams": [
    {
      "number": 23,
      "name": "Splitting Apart",
      "changing_lines": [1, 3],
      "relates_to": 2,
      "relates_to_name": "The Receptive"
    }
  ],
  "qmdj_card": "The Tower",
  "advisory_summary": "Focus on structural foundations today. Avoid hasty decisions.",
  "total_minutes": 15,
  "mood": "reflective"
}
```

The `Payload JSON` is flexible — can grow to include I Ching, Tarot, QMDJ, or any future oracle method. The `practice_types` in the manifest validate it.

---

## Manifest (`lineage-credentials/programs/truesight-grounding/manifest.json`)

```json
{
  "program": "truesight-grounding",
  "display_name": "TrueSight Grounding",
  "lineage_root": null,
  "lineage_root_public_key": null,
  "authorized_attestors": [],
  "practice_types": {
    "oracle-consultation": {
      "payload_schema": "schemas/practice/oracle-consultation.json"
    }
  },
  "attestation_types": {},
  "source_pages": [
    "https://oracle.truesight.me/draw.html"
  ],
  "notes": "Daily mindfulness grounding exercise. Each session is a [PRACTICE EVENT] signed by the practitioner's key. No attestation chain needed — this is a solo practice log."
}
```

---

## Implementation Roadmap

### Phase 1 — Foundation

- [ ] **1.1** Create `lineage-credentials/programs/truesight-grounding/manifest.json`
- [ ] **1.2** Create `lineage-credentials/programs/truesight-grounding/schemas/practice/oracle-consultation.json`
- [ ] **1.3** Create logo SVG at `truesight_me_prod/assets/images/programs/truesight-grounding/logo.svg`
- [ ] **1.4** Build `oracle.truesight.me/draw.html` — the Oracle draw page
  - Reuses `practice-event-submit.js` pattern from capoeira
  - "Draw" button reveals hexagrams/cards
  - "Record Session" button signs and submits `[PRACTICE EVENT]` to Edgar
  - Shows CV link after submission
- [ ] **1.5** Create `oracle.truesight.me/assets/js/oracle-draw-submit.js`
  - Based on capoeira's `practice-event-submit.js`
  - RSA-2048 keypair generation (Web Crypto API)
  - Canonical payload formatting + signing
  - Multipart POST to Edgar
- [ ] **1.6** Create `truesight_me_prod/programs/truesight-grounding/index.html` — program landing page
  - Logo, description, link to `oracle.truesight.me/draw.html`
  - Credentials viewer at `#<pk-slug>` (same pattern as tribomirim)
- [ ] **1.7** Add `truesight-grounding` card to `truesight_me_prod/programs/index.html`
- [ ] **1.8** Test end-to-end: draw → Edgar → GAS → lineage-credentials commit

### Phase 2 — Autopilot Integration

- [ ] **2.1** Add oracle draw reader to autopilot context loader
  - Reads `lineage-credentials/programs/truesight-grounding/<pk-slug>/practice/` for today's files
  - Parses the latest draw's payload
- [ ] **2.2** Wire into Telegram morning flow
  - When you message the autopilot, it checks for today's draw
  - If found, includes it in the system prompt context
  - If not found, asks if you've done your morning grounding yet

### Phase 3 — Dashboard & History

- [ ] **3.1** Add draw history to `oracle.truesight.me`
  - Reads from `lineage-credentials` (same as capoeira CV pattern)
  - Shows recent draws, hexagram patterns, advisory themes
- [ ] **3.2** Optional: calendar view of draws over time

---

## Key Files

| File | Purpose |
|------|---------|
| `lineage-credentials/programs/truesight-grounding/manifest.json` | Program manifest (declares practice_types) |
| `lineage-credentials/programs/truesight-grounding/schemas/practice/oracle-consultation.json` | Payload schema |
| `truesight_me_prod/assets/images/programs/truesight-grounding/logo.svg` | Program logo |
| `truesight_me_prod/programs/truesight-grounding/index.html` | Program landing page + credentials viewer |
| `truesight_me_prod/programs/index.html` | Programs listing (add card) |
| `oracle.truesight.me/draw.html` | Oracle draw page (new) |
| `oracle.truesight.me/assets/js/oracle-draw-submit.js` | Sign + submit logic (new, based on capoeira's `practice-event-submit.js`) |
| `agentic_ai_context/AWS_DIGITAL_INFRASTRUCTURE.md` | Server/domain reference |

---

## Design Decisions

1. **Reuse `[PRACTICE EVENT]`** — no new event type needed. The `Program` field routes it. The GAS processor already handles any program with a valid manifest.

2. **Anonymous by default** — the practitioner public key is the identity. No email, no name required. But since you're the sole governor, you can optionally include `Practitioner Name: Gary Teh` for clarity.

3. **Advisory summary is public** — stored in `lineage-credentials` which is a public repo. If you want private reflections, hash the summary or store a reference. The hexagrams and card draws are metadata, not secrets.

4. **No attestation chain** — unlike Butterfly Effect, there's no admin attesting to your qualification. This is a solo practice log. The `authorized_attestors` array stays empty.

5. **Same localStorage keypair** — reuses the same `publicKey`/`privateKey` localStorage keys as the DApp and capoeira, so if you've already generated keys via `create_signature.html`, they're reused automatically.

6. **Submission after reading** — the `[PRACTICE EVENT]` is submitted only after the user clicks "Record Session," not when "Draw" is clicked. This ensures the record includes the advisory summary, not just the raw draw.
