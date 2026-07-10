# krake_browser — Working Notes (Shared Context for AIs)

> **Status (2026-05-20):** Engine implementation **pending**. Three repos scaffolded with design + sample recipes; runtime not yet built. See [`OPEN_FOLLOWUPS.md` → "krake_browser engine implementation (post-scaffold)"](./OPEN_FOLLOWUPS.md) for the MVP scope.
>
> This file is a **forward spec**. Read it now so the operator pattern is in your context for when the engine ships. Until then, attempts to invoke `list_recipes` / `run_recipe` will fail (the MCP tools don't exist yet) — fall back to the relevant API path (`dao_client` for Edgar, direct GAS fetch, etc.).

## What it is

A local MCP server that drives Gary's persistent Chromium for browser-mediated operational tasks. The browser stays logged into WhatsApp Web, Instagram, LinkedIn, Facebook, the FDA portal — anywhere a session is hard to re-establish — and the engine attaches over CDP. You (the LLM) pick a recipe, supply variables, and the engine executes it click-by-click, **suspending at every `human_intervention` action** so Gary can approve, complete 2FA, or take over manually.

Two recipe repos feed the engine; both are auto-pulled into the local catalog:

- [KrakeIO/krake_browser](https://github.com/KrakeIO/krake_browser) — the engine itself
- [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) — generic platform recipes (WhatsApp, IG, LinkedIn, FB, FDA)
- [TrueSightDAO/tdg_recipes](https://github.com/TrueSightDAO/tdg_recipes) — DAO-curated wrappers (primarily partner check-ins across channels; Edgar submission helpers)

## When to invoke

Default to krake_browser any time the operator asks for browser-mediated work and a recipe exists:

| Operator says | Recipe to pick |
|---|---|
| "Check in with <partner>" / "WA check-in with <store>" | `partner_followups/check_in` (TDG wrapper) |
| "Send <message> via WhatsApp to <contact>" | `whatsapp/send_message` |
| "DM <handle> on Instagram" | TDG wrapper if it exists, else `instagram/dm_send` |
| "Connect with <person> on LinkedIn" | `linkedin/connect_request` |
| "Look up / search FDA for <facility>" | `fda/facility_search` |

**Prefer TDG wrappers when they exist.** A wrapper's `why` field encodes the DAO context (which tracker to log to, partner-naming convention, gating rules) that the generic platform recipe doesn't know about. If the `why` doesn't match the current ask, fall through to the underlying platform recipe and supply DAO-specific vars yourself.

## When NOT to invoke

- **Anything with a clean API.** Edgar → `dao_client` (Python CLI). GAS endpoints → direct fetch. Google Sheets → service-account auth. krake_browser is right *only* when there's no API and you genuinely need a browser session.
- **Unattended / scheduled work.** Recipes block at `human_intervention` until timeout (default 5 min); if Gary isn't around, they abort. For cron-style flows, build it into `dao_client` or a GAS trigger.
- **Read-only queries.** "Has <partner> heard back?" → read the tracker (Partner Check-in sheet, advisor snapshot), don't open a browser.
- **Multi-recipient batching.** The engine runs one recipe at a time and needs Gary's ack on each send. Don't try to "send the same WhatsApp message to 12 partners in one go" — loop the recipe once per partner, with explicit acks each time.

## How to invoke (mechanics)

1. **Confirm the engine is running.** If your MCP client doesn't show `list_recipes` / `run_recipe` / `ack_intervention` as available tools, ask Gary to start it (he runs `bin/krake_browser_launch` for the Chromium and `bin/krake_browser_serve` for the Sinatra + MCP server). The engine binds to `127.0.0.1` only.
2. **List the catalog** if you're not sure: `list_recipes()` returns `name`, `description`, and `why` for every recipe.
3. **Run the recipe:** `run_recipe(name: "<slug>", vars: {...})`. For TDG wrappers, vars typically come from the Hit List or Partner Check-in tracker (`PARTNER_FIRST_NAME`, `PARTNER_WHATSAPP_NAME`, `WEEKS_SINCE_LAST_TOUCH`, …). **If you're missing a variable, ask Gary** — don't guess.
4. **Acknowledge interventions explicitly:**
   - When an `intervention_required` event fires, surface the prompt + screenshot to Gary in chat.
   - Wait for his explicit confirmation. **Don't ack-and-continue on his behalf** unless he gives a standing instruction for this run.
   - Call `ack_intervention(token, "continue" | "cancel" | "skip" | "edit", payload?)` per his response.
5. **Log the outcome** to the relevant tracker:
   - **Partner check-ins** → Partner Check-in tracker (DApp UI or `dao_client check_in_partner`). Without the log row, the GAS scanner doesn't see the touch and Gary's advisors keep recommending he reach out to someone he already reached.
   - **Edgar submissions** → already logged by `dao_client` itself; no extra step.
   - **Generic platform recipes** → no automatic logging; ask Gary whether to record it somewhere.

## Recipe DSL quick reference

Recipes are JSON files. Each has `actions[]` (the steps) and optionally `columns[]` (output to extract). The action vocabulary inherits the [Krake.io DSL (2014)](http://krake.io) verbatim — `click`, `insert`, `scroll_bottom`, `wait`, `trigger_change`, `goto`, `switch_window`, `solve_captcha`, `gather` — and adds **`human_intervention`** as a first-class primitive (formalizes what `solve_captcha` was half-doing). Variable substitution is `{{VAR_NAME}}`. JSON Schema lives at `krake_recipes/schema/recipe.schema.json`.

You shouldn't need to author recipes inline (let Gary PR them to the right repo), but if he asks you to draft one in chat, follow the schema and default to a `human_intervention` before any irreversible action.

## Caveats — read these

- **Don't ack interventions silently.** The whole point of the human-intervention surface is operator approval at irreversible boundaries (sending a message, firing a connect request, submitting a form). If you `ack_intervention("continue")` without Gary saying so, real messages go to real partners.
- **Recipes drift.** Living sites (especially Instagram, LinkedIn) change DOM selectors on their own cadence. If a recipe fails on a selector, **don't edit it inline** — flag the failure to Gary; the fix is a PR against krake_recipes or tdg_recipes so every future run inherits it.
- **Retail-partner naming.** When the recipe asks for `PARTNER_FIRST_NAME`, the canonical contributor format is `First Name - Store Name` (e.g. `Kirsten - The Way Home Shop`). Don't trim the store-name suffix; the join logic downstream depends on it.
- **Edgar event dispatch is substring-matched.** Don't include literal bracketed phrases like `[CONTRIBUTION EVENT]` or `[EMAIL ... EVENT]` inside `human_intervention` prompts or recipe descriptions if the recipe will eventually feed into an Edgar submission — Edgar's dispatcher will misroute or 422.
- **Localhost only.** The CDP port (9222) and the MCP/WebSocket port are keys-to-the-kingdom — every cookie, every session. The engine refuses to start if it sees `0.0.0.0` anywhere. Don't suggest exposing them for "remote access"; that breaks the entire security model.
- **One browser, one human.** Multiple LLM sessions hammering the same krake_browser instance is undefined behavior. If two Claude sessions are active, only one should be invoking recipes at a time.

## Operator prompts that should make you reach for this

(For when Gary types into a Claude / Cursor / Kimi / Codex session)

- "Check in with <partner>" → `partner_followups/check_in` (after confirming via Hit List that it's overdue — Gary's standing rule: check the tracker before recommending outreach)
- "Ping <partner> about <topic>" → likewise
- "DM <handle> on IG" → invoke
- "Send a LinkedIn note to <person>" → invoke
- "Pull / search FDA for <facility>" → invoke
- "Submit a contribution for <thing>" → if the form lives on dao_client, use that (not krake_browser); only use krake_browser if it's the web-form path

## See also

- [`OPEN_FOLLOWUPS.md` → "krake_browser engine implementation (post-scaffold)"](./OPEN_FOLLOWUPS.md) — MVP scope, scope addendum, PAT location for KrakeIO push
- [`NOTES_dapp.md`](./NOTES_dapp.md) — the DApp tracker UIs that recipes log back to
- [`NOTES_sentiment_importer.md`](./NOTES_sentiment_importer.md) — the Edgar deploy model (related infrastructure)
