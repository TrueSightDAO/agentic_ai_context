# Service-identity onboarding to Edgar

This doc is the canonical pattern for provisioning an **autonomous
service identity** on Edgar — i.e. a bot that signs and submits events
without being a human contributor. Reusable for any future autonomous
agent: Faire Sync Bot (first instance, 2026-05-19), Etsy CSV Watcher,
krake_sinatra, Email360 sync, future per-channel sync agents, etc.

When you find yourself asking "how do I make an autonomous workflow
submit signed events without using the operator's key" — this doc.

---

## Why service identities exist

Edgar's signed-event model requires every payload to be signed by an
RSA private key that resolves to an **ACTIVE** contributor in the
Contributors Digital Signatures sheet. If you sign with the operator's
key (`Gary Teh`), the audit trail conflates human-driven and
machine-driven submissions. You can't tell at a glance which
`[INVENTORY MOVEMENT EVENT]` came from Gary narrating to Claude vs. an
autonomous cron pulling Faire orders.

The principle, from the credentialing-platform precedent: **every actor
in the system gets its own keypair**. Bots are actors. So bots get
their own identity. Audit hygiene falls out for free.

The naming convention is `<scope> Bot` — `Faire Sync Bot`, `Etsy CSV
Watcher Bot`, `krake_sinatra Bot`, etc. The `Bot` suffix makes
machine-driven submissions visible at a glance in the ledger.

---

## The five-step pattern

```
1. Governor → [CONTRIBUTOR ADD EVENT]
       creates Contributors row for bot name + +alias email
                            │
                            ▼
2. Bot keypair generated locally (RSA-2048, in memory)
                            │
                            ▼
3. Bot → [EMAIL REGISTERED EVENT]
       Edgar emails verification link to the +alias address,
       which routes to the operator's primary inbox
                            │
                            ▼
4. Script polls operator's Gmail via existing OAuth token,
   extracts vk + em from the link in the email body
                            │
                            ▼
5. Bot → [EMAIL VERIFICATION EVENT]
       Edgar flips Contributors Digital Signatures row to ACTIVE
                            │
                            ▼
   Bot private key → GitHub Actions secret
   Local copy deleted
```

End-to-end runtime: ~30 seconds when Gmail delivers promptly.

---

## Key design choices

### Why +alias email instead of a separate mailbox

Each bot needs an email field to satisfy Edgar's contributor-resolution
logic (`Contributors contact information` column D → column A). But
provisioning a dedicated mailbox per bot is unnecessary overhead.

**The +alias trick**: Gmail / Google Workspace honour `+suffix`
routing. `garyjob+faire-sync-bot@agroverse.shop` routes to
`garyjob@agroverse.shop` natively. No new mailbox to monitor; the
verification email lands in the operator's primary inbox where the
script can find it via Gmail OAuth.

The `+` suffix encodes the bot's identity, so the operator can later
filter by it (`to:garyjob+faire-sync-bot@agroverse.shop`) if they need
to see all bot-related verification emails.

### Why the bot — not the operator — submits the email events

Steps 3 and 5 use the **bot's** keypair to sign, not the operator's.
This is what Edgar's signed-event model expects: when you submit
`[EMAIL REGISTERED EVENT]` for an email, you're proving you control
the private key being registered against that email. If you signed
with the operator's key, Edgar would associate the bot's email with
the operator's key — wrong identity.

Only step 1 — `[CONTRIBUTOR ADD EVENT]` — is signed by the governor,
because creating a contributor row is a governor-only privilege.

### Why poll Gmail instead of using the loopback listener (auth.py
pattern)

The operator's `auth.py login` flow spins up a local HTTP listener
that captures the verification redirect (the user clicks the email
link, the link points at `http://127.0.0.1:PORT/verify`, the listener
extracts vk + em from the request).

For a bot setup, the loopback doesn't work — no human is going to
click the link, and the bot will eventually run in GitHub Actions
(no inbound network access). Polling Gmail via the existing OAuth
token (per `GMAIL_OAUTH_WORKFLOW.md`) is the equivalent that works
in unattended contexts.

The script sets `generation_source` to a sentinel URL
(`https://faire-sync-bot.setup/verify`) so the verification email's
link includes that prefix; the link is parsed for `?em=...&vk=...`
query params regardless of the URL host.

### Where the private key lives after onboarding

- **During setup**: `/tmp/<bot-slug>.private_key` (mode 600) for ~5
  minutes while the operator runs `gh secret set` to transfer it.
- **In production**: GitHub Actions secret
  (`<BOT_SLUG>_PRIVATE_KEY`, all caps).
- **Never**: in any committed file, in any chat log, in any
  long-lived shared location. Delete the `/tmp` copy immediately
  after the GitHub secret is set.

The GitHub Action workflow constructs an EdgarClient at runtime:
```python
EdgarClient(
    email=os.environ["FAIRE_SYNC_BOT_EMAIL"],
    public_key_b64=os.environ["FAIRE_SYNC_BOT_PUBLIC_KEY"],
    private_key_b64=os.environ["FAIRE_SYNC_BOT_PRIVATE_KEY"],
)
```

Public key + email can be plain env vars or repo secrets — both are
non-confidential. Private key must be a secret.

---

## Reference implementation

`market_research/scripts/setup_faire_sync_bot.py` is the canonical
script. Copy + adapt for new bots:

```python
BOT_NAME = "Faire Sync Bot"   # ← rename
BOT_EMAIL = "garyjob+faire-sync-bot@agroverse.shop"  # ← change +suffix
BOT_KEY_PATH = Path("/tmp/faire-sync-bot.private_key")
BOT_GEN_SOURCE = "https://faire-sync-bot.setup/verify"  # any URL, just identifies the link
```

Dependencies (already in `market_research`):
- `truesight_dao_client` (Python module, in `~/Applications/dao_client`)
- `google-api-python-client` + Gmail OAuth token at
  `market_research/credentials/gmail/token.json`
- Operator's governor `.env` at `~/Applications/dao_client/.env`

Runtime:
```bash
cd ~/Applications/market_research
python3 scripts/setup_faire_sync_bot.py
```

Then:
```bash
gh secret set <BOT_SLUG>_PRIVATE_KEY --repo TrueSightDAO/<repo> < /tmp/<bot-slug>.private_key
gh secret set <BOT_SLUG>_PUBLIC_KEY  --repo TrueSightDAO/<repo> < /tmp/<bot-slug>.public_key
echo "<bot-email>" | gh secret set <BOT_SLUG>_EMAIL --repo TrueSightDAO/<repo>
rm /tmp/<bot-slug>.private_key /tmp/<bot-slug>.public_key
```

---

## Verifying ACTIVE status

After onboarding, the bot identity can be verified two ways:

1. **Via signed test event**: have the bot sign and submit any
   no-op-ish event (e.g. a `[CONTRIBUTION EVENT]` with `--dry-run`,
   which prints the signed share text without hitting Edgar). If
   signature_verification succeeds, the key is registered correctly.
2. **Via the operator's identity-management surface**: spot-check the
   `Contributors Digital Signatures` sheet on the Main Ledger — find
   the row for the bot name + bot email, confirm column D status =
   `ACTIVE`, column H verification key consumed = TRUE.

---

## Anti-patterns

- **Re-using the operator's key for bot work.** Conflates identities;
  Edgar's audit log becomes useless for distinguishing human vs.
  automated submissions.
- **Provisioning a separate Google Workspace mailbox per bot.**
  Wasteful — the +alias trick gives every bot its own routable
  email without overhead.
- **Storing the bot's private key in `.env` checked into git.**
  Even with `.gitignore`, the muscle memory of "edit .env, save,
  commit" makes this a hand grenade. GitHub Actions secrets only.
- **Submitting steps 3/5 with the operator's key.** Edgar associates
  the email with whichever key signs — wrong identity.
- **Skipping the `Bot` suffix in the contributor name.** Without
  it, the ledger doesn't visually distinguish bot vs. human
  submissions when scanning.
- **Long-running `/tmp/*.private_key` files.** Delete immediately
  after `gh secret set`. Don't leave it sitting "in case I need it
  later." Future-you doesn't need it later; you can rotate.

---

## Rotation

When a bot's private key is suspected compromised (rare, but worth
documenting):

1. Generate a new keypair for the same bot identity (re-run the setup
   script with the same `BOT_NAME` + `BOT_EMAIL`).
2. Step 1 (`[CONTRIBUTOR ADD EVENT]`) will fail with "already exists"
   — the script handles this gracefully and continues.
3. Steps 2–5 add a new keypair under the same contributor name.
   Edgar's existing precedent (`project_edgar_multiple_active_keys.md`)
   allows multiple ACTIVE keys per contributor — additive, not
   replacing.
4. Update the GitHub Actions secret to the new private key.
5. The old key remains technically ACTIVE on Edgar until manually
   deactivated (governor action via `dapp/governor_contributor_admin.html`).
   For genuine compromise, ALSO deactivate the old key.

---

## Onboarded today

| Bot | Repo where its key lives as a secret | Onboarded | Purpose |
|---|---|---|---|
| `Faire Sync Bot` | `TrueSightDAO/go_to_market` | 2026-05-19 | Faire marketplace inventory parity + order ingestion |

When adding a new bot, add a row here.

---

## Related context

- `CREDENTIALING_PLATFORM.md` — the "every actor has a keypair"
  principle is articulated there in the credentialing context; this
  doc applies it to operator infrastructure.
- `GMAIL_OAUTH_WORKFLOW.md` — Gmail OAuth setup, prerequisite for
  step 4 (polling the inbox).
- `GROWTH_MODEL.md` — service identities are how the operator's
  attention scales across loops; krake_sinatra and future bots all
  follow this pattern.
- `dao_client/dapp_digital_signature_onboarding/README.md` — the
  public reference for the underlying Contributors Digital Signatures
  sheet contract.
- `dapp/create_signature.html` — the browser-side equivalent for
  human contributor onboarding.
- `dapp/governor_contributor_admin.html` — the governor-side
  interface for managing contributors (including deactivating keys
  during rotation).

*Last refreshed 2026-05-19. Refresh when adding a new bot to the table
or when the underlying Edgar event contracts change.*
