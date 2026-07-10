# Oracle Draw — Implementation Plan & Roadmap

## Vision

Treat each morning Oracle consultation as a `[PRACTICE EVENT]` under the program **`truesight-grounding`-- a daily mindfulness grounding exercise. Same infrastructure as capoeira: same event type, same GAS processor, same `lineage-credentials` commit trail. No new backend code needed.

The flow: 
1. You visit `oracle.truesight.me/draw.html` and perform your draw
2. The reading is returned on screen (hexagrams, QMDJ card, etc.)
3. You review the reading, optionally add an advisory summary
4. You click **"Record Session"** — the full session (draw + advisory) is signed with your RSA key and submitted to Edgar
5. The event lands in `lineage-credentials/programs/truesight-grounding/<pk-slug>/practice/
6. When you message the autopilot on Telegram, it reads today's draw and has full context for execution

---

## Architecture

```
oracle.truesight.me (GitHub Pages)
  └── draw.html — Oracle draw page
        ├── Generates/loads RSA keypair (localStorage, same as capoeira/dapp)
        ├── User draws ‒ reading revealed on screen
        ├── User reviews + adds advisory summary
        ├── User clicks "Record Session"
        ├── Builds [PRACTICE EVENT] payload with full context
        ├── Signs with RSASSA-PKCS1-v1_5 / SHA-256
        └── POST → Edgar /dao/submit_contribution

Edgar (sentiment_importer / dao_protocol)
  └── Logs to Telegram Chat Logs
  └── Webhook → GAS practice_event_processing.gs (EXISTING — no changes needed)
        ├── Parses [PRACTICE EVENT]
        ├── Fetches lineage-credentials/programs/truesight-grounding/manifest.json
        ├── Validates practice_type "oracle-consultation"
        ├── Derives pk-slug from public key
        └�── Commits to lineage-credentials:
            programs/truesight-grounding/<pk-slug>/practice/<timestamp>-<hash>.json

truesight.me (GitHub Pages)
  └── programs/truesight-grounding/index.html — program page (new)
  └── programs/truesight-grounding/credentials/#<pk-slug> — credentials viewer (new)

Autopilot (Telegram / chat)
  └── Reads lineage-credentials for today's draw 
  └── Has context for execution conversation
```

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
  "display_name": "TrueSight Grounding — Morning Oracle",
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
- [ ] **1.3** Build `oracle.truesight.me/draw.html` — the Oracle draw page
  - Reuses `practice-event-submit.js` pattern from capoeira (RSA-2048 keypair in localStorage)
  - Draw → reading revealed → user reviews ‒ "Record Session" button
  - Signs and submits `[PRACTICE EVENT]` to Edgar after reading is returned
  - Shows CV link after submission
- [ ] **1.4** Create `oracle.truesight.me/assets/js/oracle-draw-submit.js` (based on `practice-event-submit.js`)
- [ ] **1.5** Test end-to-end: draw → Edgar → GAS → lineage-credentials commit

### Phase 2 — truesight.me Program Page

- [ ] **2.1** Create `truesight.me/programs/truesight-grounding/index.html` — program landing page
- [ ] **2.2** Create `truesight.me/programs/truesight-grounding/credentials/index.html` — credentials viewer (same pattern as butterfly-effect and tribomirim)
- [ ] **2.3** Add program card to `truesight.me/programs/index.html` listing

### Phase 3 — Autopilot Integration

- [ ] **3.1** Add oracle draw reader to autopilot context loader
  - Reads `lineage-credentials/programs/truesight-grounding/<pk-slug>/practice/` for today's files
  - Parses the latest draw's payload
- [ ] **3.2** Wire into Telegram morning flow
  - When you message the autopilot, it checks for today's draw
  - If found, includes it in the system prompt context
  - If not found, asks if you've done your morning grounding yet

### Phase 4 — Dashboard & History

- [ ] **4.1** Add draw history to `oracle.truesight.me`
  - Reads from `lineage-credential`s (same as capoeira CV pattern)
  - Shows recent draws, hexagram patterns, advisory themes
- [ ] **4.2** Optional: calendar view of draws over time

---

## Key Files
| File | Purpose |
|------|----------|
| `lineage-credentials/programs/truesight-grounding/manifest.json` | Program manifest (declares practice_types) |
| `lineage-credentials/programs/truesight-grounding/schemas/practice/oracle-consultation.json` | Payload schema |
| `oracle.truesight.me/draw.html` | Oracle draw page (new) |
| `oracle.truesight.me/assets/js/oracle-draw-submit.js` | Sign + submit logic (new, based on capoeira's `practice-event-submit.js`) |
| `truesight.me/programs/truesight-grounding/index.html` | Program landing page (new) |
| `truesight.me/programs/truesight-grounding/credentials/index.html` | Credentials viewer (new) |
| `agentic_ai_context/AWS_DIGITAL_INFRASTRUCTURE.md` | Server/domain reference |

---

## Design Decisions

1. **Reuse `[PRACTICE EVENT]`** — no new event type, no new GAS, no new webhook. The `Program` field routes it. The existing GAS processor already handles any program with a valid manifest.

2. **Submission after reading** — the signed event is only submitted after the user clicks "Record Session," not when cards are drawn. This ensures the record captures the complete session including the advisory summary.

3. **Anonymous by default** — the practitioner public key is the identity. No email, no name required. But since you're the sole governor, you can optionally include `Practitioner Name: Gary Teh` for clarity.

4. **Advisory summary is public** — stored in `lineage-credentials` which is a public repo. If you want private reflections, hash the summary or store a reference. The hexagrams and card draws are metadata, not secrets.

5. **No attestation chain** — unlike Butterfly Effect, there's no admin attesting to your qualification. This is a solo practice log. The `authorized_attestors` array stayes empty.

6. **Same localStorage keypair** — reuses the same `publicKey`/`privateKey` localStorage keys as the DApp and capoeira, so if you've already generated keys via `create_signature.html`, they're reused automatically.

---

## What No New GAS Means

The existing `practice_event_processing.gs` in the `tdg_credentialing` Apps Script project handles ALL programs generically:

1. It reads `Program` from the event → fetches `lineage-credentials/programs/<program>/manifest.json`
2. It validates `practice_type` against the manifest's `practice_types`
3. It commits the event to `programs/<program>/<slug>/practice/<ts>.json`

So adding `truesight-grounding` requires:
- **One new file**: `lineage-credentials/programs/truesight-grounding/manifest.json`
- **One new file**: `lineage-credentials/programs/truesight-grounding/schemas/practice/oracle-consultation.json`
- **Zero changes** to the GAS project
- **Zero new deployments**