# Oracle Draw — Implementation Plan & Roadmap

## Vision

Treat each Oracle consultation as a `[PRACTICE EVENT]` under the program `truesight-oracle`. Same infrastructure as capoeira — same event type, same GAS processor, same `lineage-credentials` commit trail. The Oracle draw becomes a personal practice record: hexagrams, QMDJ cards, advisory summary, timestamped and signed by your public key.

When you message the autopilot on Telegram after your morning session, it reads today's draw from `lineage-credentials` and has full context for the day's execution.

---

## Architecture

```
oracle.truesight.me (GitHub Pages)
  └── draw.html — Oracle draw page
        ├── Generates/loads RSA keypair (localStorage, same as capoeira)
        ├── Captures hexagram(s), QMDJ card, advisory summary
        ├── Builds [PRACTICE EVENT] payload
        ├── Signs with RSASSA-PKCS1-v1_5 / SHA-256
        └── POST → Edgar /dao/submit_contribution

Edgar (sentiment_importer / dao_protocol)
  └── Logs to Telegram Chat Logs
  └── Webhook → GAS practice_event_processing.gs
        ├── Parses [PRACTICE EVENT]
        ├── Validates program "truesight-oracle" in manifest
        ├── Derives pk-slug from public key
        └── Commits to lineage-credentials:
            programs/truesight-oracle/<pk-slug>/practice/<timestamp>-<hash>.json

Autopilot (Telegram / chat)
  └── Reads lineage-credentials for today's draw
  └── Has context for execution conversation
```

---

## Event Payload Shape

```
[PRACTICE EVENT]
- Program: truesight-oracle
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

## Manifest (`lineage-credentials/programs/truesight-oracle/manifest.json`)

```json
{
  "program": "truesight-oracle",
  "display_name": "TrueSight Oracle",
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
  "notes": "Personal oracle practice record. Each draw is a [PRACTICE EVENT] signed by the practitioner's key. No attestation chain needed — this is a solo practice log."
}
```

---

## Implementation Roadmap

### Phase 1 — Foundation (this session)

- [ ] **1.1** Create `lineage-credentials/programs/truesight-oracle/manifest.json`
- [ ] **1.2** Create `lineage-credentials/programs/truesight-oracle/schemas/practice/oracle-consultation.json`
- [ ] **1.3** Build `oracle.truesight.me/draw.html` — the Oracle draw page
  - Reuses `practice-event-submit.js` pattern from capoeira
  - Captures hexagram(s), QMDJ card, advisory summary
  - Signs and submits `[PRACTICE EVENT]` to Edgar
  - Shows CV link after submission
- [ ] **1.4** Test end-to-end: draw → Edgar → GAS → lineage-credentials commit

### Phase 2 — Autopilot Integration

- [ ] **2.1** Add `oracle-draw` reader to autopilot context loader
  - Reads `lineage-credentials/programs/truesight-oracle/<pk-slug>/practice/` for today's files
  - Parses the latest draw's payload
- [ ] **2.2** Wire into Telegram morning flow
  - When you message the autopilot, it checks for today's draw
  - If found, includes it in the system prompt context
  - If not found, asks if you've done your morning draw yet

### Phase 3 — Dashboard & History

- [ ] **3.1** Add draw history to `oracle.truesight.me`
  - Reads from `lineage-credentials` (same as capoeira CV pattern)
  - Shows recent draws, hexagram patterns, advisory themes
- [ ] **3.2** Optional: calendar view of draws over time

---

## Key Files

| File | Purpose |
|------|---------|
| `lineage-credentials/programs/truesight-oracle/manifest.json` | Program manifest (declares practice_types) |
| `lineage-credentials/programs/truesight-oracle/schemas/practice/oracle-consultation.json` | Payload schema |
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

---

## Execution Checklist

### Phase 1 — Foundation

- [ ] Create `lineage-credentials/programs/truesight-oracle/manifest.json`
- [ ] Create `lineage-credentials/programs/truesight-oracle/schemas/practice/oracle-consultation.json`
- [ ] Create `oracle.truesight.me/draw.html` (based on capoeira's `practice.html` pattern)
- [ ] Create `oracle.truesight.me/assets/js/oracle-draw-submit.js` (based on `practice-event-submit.js`)
- [ ] Test: submit a draw, verify it lands in `lineage-credentials`
- [ ] Verify the draw appears on `oracle.truesight.me` (or at least the CV link works)

### Phase 2 — Autopilot

- [ ] Add oracle draw reader to autopilot's context loader
- [ ] Wire into Telegram morning greeting flow
- [ ] Test: message autopilot after a draw, confirm it references the draw

### Phase 3 — Dashboard

- [ ] Build draw history view on `oracle.truesight.me`
- [ ] Add calendar/pattern visualization (optional)
