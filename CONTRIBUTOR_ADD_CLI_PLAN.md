# Contributor Add CLI — Implementation Plan

## Context

There is no CLI method for adding a DAO contributor. The only path is through the DApp web page (`governor_contributor_admin.html`), which requires a browser-session digital signature. Sophia needs a CLI so she can execute contributor adds directly when the governor asks.

Edgar already accepts `[CONTRIBUTOR ADD EVENT]` — it logs to Telegram Chat Logs, and the GAS handler (`ContributorAddHandler.js`) reads those logs, dedups against the "New Contributor" tab, appends to "Contributors contact information", and fires the onboarding email. The GAS handler does NOT gate on governor status — any signed submission works.

## PR Sequence

### PR1 — `dao_protocol`: Add contributor CLI module

- **File:** `truesight_dao_client/modules/add_contributor.py`
- **Console script:** `truesight-dao-add-contributor` in `pyproject.toml`
- **Pattern:** Uses `build_event_cli` from `edgar_client.py` (same as `add_partner.py`)
- **Fields:** `Contributor Name`, `Contributor Email`
- **Status:** ✅ Already written, PR #123 open

### PR2 — `truesight_autopilot`: Wire `CONTRIBUTOR ADD EVENT` into submit_contribution tool

- **File:** `app/main.py` — add `CONTRIBUTOR ADD EVENT` to the event dispatch (line 1715 area)
- **What changes:** Currently the `submit_contribution` tool special-cases `INVENTORY MOVEMENT` and `QR CODE REGISTRATION`. For `CONTRIBUTOR ADD EVENT`, it should call `EdgarLogger.submit_contribution()` directly (same as the default path).
- **Why needed:** So Sophia can call `submit_contribution(event_name="CONTRIBUTOR ADD EVENT", attributes={"Contributor Name": "...", "Contributor Email": "..."})` directly when the governor asks.

### PR3 — Add David Campbell (execution, not a PR)

- Run: `truesight-dao-add-contributor --contributor-name "David Campbell" --contributor-email "david@soha.center"`
- Verify row appears in Telegram Chat Logs → GAS processes it → David gets onboarding email

## Gates

| Gate | Condition | Who |
|------|-----------|-----|
| G1 | PR1 merged | Governor says "go" or "merge it" |
| G2 | PR1 deployed to autopilot | Sophia: git pull + pip install |
| G3 | PR1 dry-run test passes | Sophia: `--dry-run` output verified |
| G4 | PR2 merged | Governor reviews + merges |
| G5 | PR2 deployed to autopilot | Sophia: `deploy_autopilot()` |
| G6 | David Campbell added | Sophia runs CLI, verifies in GAS |

## RESUME HERE

PR1 is already open at `dao_protocol` PR #123. On GO:
1. Merge PR #123
2. Pull + reinstall on autopilot
3. Dry-run test
4. STOP — report results, wait for governor to proceed to PR2

## Acceptance

- [ ] `truesight-dao-add-contributor --help` prints usage
- [ ] `--dry-run` prints signed payload without hitting Edgar
- [ ] Real run adds a row to Telegram Chat Logs
- [ ] GAS handler processes the row → contributor appears in "Contributors contact information"
- [ ] Sophia can call `submit_contribution` with `CONTRIBUTOR ADD EVENT` directly
