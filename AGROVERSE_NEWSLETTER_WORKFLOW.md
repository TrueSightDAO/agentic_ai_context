# Agroverse newsletter — generate, draft, send, track opens

How AI assistants should generate and send community emails to the Agroverse newsletter list, and how opens are tracked back to the Main Ledger.

**Sender:** all newsletters go out from **`garyjob@agroverse.shop`** (Gary).
**Register:** curatorial / ritual / farm-story — **never** promotional blast. See `PARTNER_OUTREACH_PROTOCOL.md` §6 for the tone principles (they apply here too).
**Cadence rule:** Only email when there is a real new thing to say (new origin release, new SKU, new operator, genuine ask). Empty-channel fillers (*"summer update"*, *"still here"*) are strictly forbidden — noise on a trust asset decays the list faster than silence.

---

## 1. Artifacts and ground truth

| Artifact | Where it lives | Purpose |
|----------|----------------|---------|
| Subscriber list | **Main Ledger** (`1GE7PUq-…`) → tab **`Agroverse News Letter Subscribers`** | Email, Status (`CONFIRMED`), Created Date, Imported Date, Source. Only `CONFIRMED` rows get mail. |
| Sent / open log | **Main Ledger** → tab **`Agroverse News Letter Emails`** | One row per (recipient × campaign). Updated by the script on send and by Edgar on open. |
| Send / draft script | **`market_research/scripts/send_newsletter.py`** | Creates Gmail drafts (for review) or sends (for live), embeds optional tracking pixel, logs to sheet. |
| Open-tracking endpoint | **Edgar**: `GET https://edgar.truesight.me/newsletter/open.gif?mid=…&r=…` | Serves 1x1 GIF, updates the sheet row keyed by `message_uuid`. |
| Body drafts | **`market_research/newsletter_drafts/YYYY-MM-DD_<slug>.md`** | Markdown body with `**Subject:** …` in the preamble; everything after the first `---` is the email body. |

---

## 2. Gmail label convention

All newsletter drafts/sent mail get a label of shape `Newsletter/<campaign-label>`:

- Review round (drafts to 2–3 trusted humans): same label as the eventual send, so both live under the same thread in Gmail.
- Example current campaign: **`Newsletter/2 Chocolate Bars`**.

The label auto-creates if it doesn't exist. Aligns with the broader AI/* label convention (`AI/Follow-up`, `AI/Warm-up`, `AI/Sent Follow-up`, `AI/Sent Warm-up`) documented in `PARTNER_OUTREACH_PROTOCOL.md`.

---

## 3. Sheet schema — `Agroverse News Letter Emails`

Row 1 (bold, frozen):

| Col | Name | Written by | Notes |
|-----|------|------------|-------|
| A | `message_uuid` | script | Our UUID (primary key for tracking pixel). Different from Gmail's id. |
| B | `gmail_message_id` | script | Gmail's message resource id (draft or sent). |
| C | `campaign` | script | Free-form tag (e.g. `two_bahia_bars`, `two_bahia_bars_review`). |
| D | `subject` | script | |
| E | `recipient_email` | script | Lowercased. |
| F | `sent_at_utc` | script | ISO 8601 Z. For drafts this is the draft-creation time. |
| G | `status` | script | `draft` or `sent`. |
| H | `opened` | Edgar | `TRUE` after first pixel hit. |
| I | `first_opened_at_utc` | Edgar | Set on first pixel hit; never overwritten. |
| J | `last_opened_at_utc` | Edgar | Updated on every pixel hit. |
| K | `open_count` | Edgar | Integer, incremented on every pixel hit. |

**Open-tracking caveats** (tell Gary before treating opens as signal):
- iOS Mail / Apple Mail Privacy Protection pre-fetches images → every iPhone subscriber shows as opened shortly after send, regardless of actual behavior.
- Gmail web client proxies images through Google infrastructure, which can fire opens without the user seeing the email.
- Many desktop clients block remote images until user clicks "display images."
- Net: treat opens as a **directional** signal (repeat opens, timing, opens vs. clicks) — not a reliable per-recipient "did they read this."

---

## 4. Flow

### 4.1 Write the body

Create `market_research/newsletter_drafts/YYYY-MM-DD_<slug>.md`:

```markdown
# Newsletter draft — YYYY-MM-DD — <topic>

**Subject:** <scannable, specific, not spammy, < ~90 chars>

---

Hi —

<body paragraphs, markdown links work, **bold** and *italic* work>

Thanks,
Gary
Agroverse | single-estate cacao from the Brazilian Amazon
garyjob@agroverse.shop
```

The first `---` splits preamble (which carries the `**Subject:**` line) from the body. The script parses both.

### 4.2 Copy review round (drafts to 2–3 trusted humans, no tracking)

```bash
cd market_research
source venv/bin/activate
python3 scripts/send_newsletter.py \
  --mode draft \
  --to kirsten@kikiscocoa.com --to fatoledojob@gmail.com \
  --subject "Review: <same as intended send subject>" \
  --body-md newsletter_drafts/2026-04-20_two_bahia_bars.md \
  --campaign <slug>_review \
  --label "Newsletter/<Campaign Label>"
```

Reviewers open Gmail drafts, read, reply with critique. Gary revises the `.md`.

**Who reviews:** pick people whose role is critique, not random subscribers. Typical list: Kirsten (cacaomaker — catches product/farm errors), Fatima (Bahia relationships — catches farm-story errors), plus 1–2 taste-savvy friends when relevant. *Never* treat a 5-subscriber "test send" as market signal — n=5 doesn't produce real engagement data, and response rate is the wrong metric anyway (see `AGROVERSE_NEWSLETTER_WORKFLOW.md` §7 "Anti-patterns").

### 4.3 Live send (full list, with tracking)

Once the body is revised:

```bash
python3 scripts/send_newsletter.py \
  --mode send \
  --recipients-from-sheet \
  --subject "<final subject>" \
  --body-md newsletter_drafts/<file>.md \
  --campaign <slug> \
  --label "Newsletter/<Campaign Label>" \
  --track-opens
```

- `--recipients-from-sheet` loads all `CONFIRMED` rows from **`Agroverse News Letter Subscribers`**.
- `--track-opens` embeds `<img src="https://edgar.truesight.me/newsletter/open.gif?mid=…&r=…" …>` at the bottom of the HTML body.
- Each recipient gets their own `message_uuid` — the pixel URL is unique per (recipient × send), so opens disaggregate cleanly.
- Use `--max-recipients N` as a safety cap; the script aborts if the resolved list exceeds `N`. Recommended: pass the current subscriber count + 5 as the cap.

### 4.4 Measuring response

- **Opens**: read column H / K on `Agroverse News Letter Emails`. Sort by `open_count` desc to see who is most engaged.
- **Clicks**: not tracked by default. If needed later, swap plain URLs for Edgar redirector URLs (e.g. `https://edgar.truesight.me/newsletter/click?mid=…&url=…`) — not yet implemented, scope as future work.
- **Purchases**: cross-reference send date against Shopify / Stripe / Square payment records. The `sent_at_utc` + `recipient_email` columns on the emails tab are the join keys.
- **Replies**: read them. These are the richest signal and the only one that's not sampling-biased.

---

## 5. Edgar open-tracking endpoint

Implemented in `sentiment_importer/`:

- **Model:** `app/models/gdrive/newsletter_emails.rb` — `Gdrive::NewsletterEmails.record_open!(message_uuid, recipient_email:)`. Reads the row keyed by `message_uuid` from column A, updates `opened`, `first_opened_at_utc` (only if empty), `last_opened_at_utc`, and `open_count`. Uses `edgar_dapp_listener_key.json` service account (same as other Main Ledger writers).
- **Controller:** `app/controllers/newsletter_controller.rb` — always returns a 1x1 GIF + `Cache-Control: no-store`, regardless of whether the uuid matched. Skips auth / rate-limiting / user-context before_actions.
- **Route:** `GET /newsletter/open.gif` in `config/routes.rb`.
- **Recipient verification:** if the pixel URL includes `r=<base64url recipient>`, Edgar only updates the row if it matches `E` on that row. Non-matching hits are logged and ignored (guards against spoofed pixels).
- **Idempotency:** updates are mutex-guarded in-process. Concurrent opens on multiple Edgar workers will race slightly on `open_count` — acceptable for a directional signal. If precise counting is needed later, move to an append-only event log and aggregate.

---

## 6. Credentials and access

| Purpose | File / env | Notes |
|---------|------------|-------|
| Gmail OAuth (send / draft from `garyjob@agroverse.shop`) | `market_research/credentials/gmail/token.json` (local) or `GMAIL_TOKEN_JSON` (CI secret) | See `GMAIL_OAUTH_WORKFLOW.md`. Scope: `gmail.modify`. |
| Main Ledger read/write (script side) | `market_research/google_credentials.json` (service account) | Already has access to `1GE7PUq-…`. |
| Main Ledger write (Edgar side) | `sentiment_importer/config/edgar_dapp_listener_key.json` | Shared with other Edgar sheet writers. |

Both service accounts need editor access to the Main Ledger spreadsheet (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`). Grant by sharing the sheet with each service account email.

---

## 7. Anti-patterns — don't do these

- **"Let's test with 5 recipients first."** n=5 is too few for market signal, and reply rate isn't the metric you want anyway. For copy review, hand the draft to 2–3 *critics* by name (Kirsten, Fatima, a taste-savvy friend). For market signal, send to the full list once and read opens + clicks + purchases + replies over 2 weeks.
- **"Newsletter update covering everything."** One email, one real story. The Beer Hall pattern (broadcast everything, audience tunes out) applies equally to email.
- **Manufactured urgency / discount pressure.** Breaks the curatorial register the list responds to. A "$10 bars, get one of each to compare" framing is an invitation; "15% OFF THIS WEEK ONLY" is a betrayal of why people subscribed.
- **Emailing grandma-grade supporters as if they were cold prospects.** Past buyers (esp. those in Gary's personal network) are a separate category from the newsletter list. They get direct, individual messages — never group blasts.
- **Launching a drip campaign on a cold list.** If the list has been quiet for months, the reactivation email should be a single high-signal piece, not the start of a weekly cadence you can't sustain.
- **Ignoring the whitepaper-established register.** Agroverse community responds to farmer stories, terroir, ritual, transparency. Lead with those. Commerce lives at the bottom of the email as a quiet link.

---

## 8. Changelog

- **2026-04-20** — v0.1. Initial flow. `send_newsletter.py` + Edgar `GET /newsletter/open.gif` + `Agroverse News Letter Emails` tab on Main Ledger. First campaign: `two_bahia_bars` (Oscar's Farm 2024, Fazenda Santa Ana 2023, both 81% single-estate by Kirsten). Review drafts sent to Kirsten + Fatima on this date.

---

## 9. Link index

- Script: `market_research/scripts/send_newsletter.py`
- Body drafts: `market_research/newsletter_drafts/`
- Edgar controller: `sentiment_importer/app/controllers/newsletter_controller.rb`
- Edgar model: `sentiment_importer/app/models/gdrive/newsletter_emails.rb`
- Edgar route: `config/routes.rb` → `GET /newsletter/open.gif`
- Main Ledger: https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit
- Related: `PARTNER_OUTREACH_PROTOCOL.md` (outreach tone), `GMAIL_OAUTH_WORKFLOW.md` (Gmail auth), `STORE_FOLLOW_UP_EMAIL_TEMPLATE.md` (register reference)
