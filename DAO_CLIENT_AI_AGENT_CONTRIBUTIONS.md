# DAO client — AI agent contribution submissions (convention)

When an **AI coding assistant** completes work that should appear on the **DAO contribution ledger** (`[CONTRIBUTION EVENT]` via **Edgar**), use the **`dao_client`** Python repo so the payload matches the DApp: same RSA signing, same `POST /dao/submit_contribution` endpoint as human operators.

**Repo:** [TrueSightDAO/dao_client](https://github.com/TrueSightDAO/dao_client)  
**Credentials:** `dao_client/.env` (never commit) — `EMAIL`, `PUBLIC_KEY`, `PRIVATE_KEY` from `python3 auth.py login --email …`.

---

## Required convention (machine-checkable + human-readable)

1. **Use the dedicated CLI** (do not hand-curl Edgar for this class of work):
   ```bash
   cd ~/Applications/dao_client
   source .venv/bin/activate   # if using venv
   python3 modules/report_ai_agent_contribution.py \
     --title "Short one-line title" \
     --body-file path/to/description.md \
     --pr https://github.com/TrueSightDAO/some-repo/pull/123 \
     --pr https://github.com/TrueSightDAO/other-repo/pull/456
   ```
   Or pass `--body` instead of `--body-file` for a short inline description (still include PR URLs inside the text if you use `--body`).

2. **At least one merged (or ready) GitHub PR URL** under **`https://github.com/TrueSightDAO/`** must be supplied with **`--pr`** (repeatable). The script rejects non–TrueSightDAO URLs so personal forks do not pollute the audit trail.

3. **Be explicit in the body** (bullet list is ideal):
   - **What changed** (repos, files, behavior).
   - **Why** (safeguard, bugfix, operator workflow).
   - **Evidence:** every **`--pr`** link again inside the body under a **“GitHub”** or **“Pull requests”** heading so the Telegram / sheet line is self-contained when someone scrolls without the CLI args.

4. **`Type` field** defaults to **`AI Agent (software & documentation)`** so ledger readers can filter automation vs human time-based contributions.

5. **`Amount` / `TDG Issued`** default to **`0`** unless the operator sets real economics for the session.

6. **`Contributor(s)`** defaults from **`EMAIL`** in `.env` (local-part @ domain); override with **`--contributors "Display Name"`** when the human sponsor should be credited instead.

7. **`--generation-source`** may point at this doc or the Cursor session URL so `This submission was generated using …` is traceable:
   ```text
   https://github.com/TrueSightDAO/agentic_ai_context/blob/main/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md
   ```

8. **`--dry-run`** prints the signed payload only (no POST). Use before the real submission when debugging.

---

## Browser equivalent

Human flow: [DAO Contribution Report](https://dapp.truesight.me/report_contribution.html) (`[CONTRIBUTION EVENT]`). The CLI mirrors that event and attribute names expected by Edgar / scoring.

---

## Related context

- **`tokenomics/SCHEMA.md`** — `Telegram Chat Logs`, **Governor** column **S**, **Inventory Movement**, **Scored Expense Submissions**.
- **`sentiment_importer`** — Edgar appends **A–S** to Telegram Chat Logs; `Gdrive::Governors`.
- **`WORKSPACE_CONTEXT.md`** § Edgar / tokenomics / DApp relationships.

---

## Anti-patterns

- Submitting without **any** `github.com/TrueSightDAO/.../pull/` link when code or docs landed in GitHub.
- Vague one-line descriptions with no file/PR reference.
- Using a non–`dao_client` signing path that drifts from DApp canonical formatting.
