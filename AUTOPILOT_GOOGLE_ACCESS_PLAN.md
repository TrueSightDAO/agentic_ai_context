# Autopilot — Google + AWS reach (tooling parity with local LLMs)

**Status:** IN PROGRESS — Phase 1 (ops) shipped 2026-05-28; Phase 2 (code PR) in review.
**Owner:** Gary Teh (+ AI sessions)
**Created:** 2026-05-28
**Convention:** Tracked roadmap required by `OPERATING_INSTRUCTIONS.md` §5 before implementation. Keep the **Resume tracker** current as each unit lands.

---

## 1. Goal (why this exists)

The prod `truesight_autopilot` (EC2 `100.52.234.163`) was failing user queries with "I can't directly access the Google Sheet from this server without credentials" (transcript 2026-05-28 03:01:52). Two real gaps:

1. **Credentials gap (ops):** No Google service-account JSONs on the EC2 box; nothing under `/opt/truesight_autopilot/config/`. Locally we have 7 SA keys spread across `sentiment_importer/config/`, `truesight_me/`, `krake_local/`, `agroverse_shop/`.
2. **Tool gap (code):** `app/tools/` had no Drive/Sheets/Docs/Apps-Script-API/PDF reach. Even with creds on disk, the agent's LLM cannot dispatch the call. The only Google code in autopilot is the Gmail poller (`app/email_poller.py`), which the agent doesn't expose to the model.

Compounding asks from Gary, 2026-05-28:
- Add Gmail + Apps Script reach (Apps Script via generic `http_fetch` to `/exec` deployments).
- AWS reach across both DAO-contributed accounts (`AWS_ACCOUNTS=explorya,nelanco`).
- PDF generation (autopilot can't currently produce PDF output).

End state: the prod autopilot has feature parity with what a local Claude/Codex session can reach when the operator is at their laptop.

---

## 2. Decisions locked

| Decision | Value | Notes |
|---|---|---|
| Credential storage | `truesight_autopilot/config/google/*.json` (gitignored) | Autopilot owns its own credential layout — no cross-repo runtime dependency on `sentiment_importer/config/`. Per Gary 2026-05-28. |
| Runtime path on EC2 | `/opt/truesight_autopilot/config/google/<name>_gdrive_key.json` | One directory; one env var pair. |
| Env vars | `GOOGLE_APPLICATION_CREDENTIALS` (default SA path) + `GOOGLE_CREDS_DIR` (lookup dir for named SAs) | Mirrors the Gmail OAuth pattern (`GMAIL_TOKEN_JSON`). |
| Default SA | `cypher_defense_gdrive_key.json` | Has Viewer on the Main Ledger + Cypher Defense Ledger — the most common target. |
| Switchable SA | tool argument `service_account_name="<name>"` | Lookup hits `{name}_gdrive_key.json` then `{name}_key.json`. |
| AWS multi-account | Reuse `app/aws_monitor.read_account_specs()` | The env-parsing logic stays in one place. Renamed from `_read_account_specs` with a deprecated alias for the transition. |
| AWS safety | Read-only allowlist — `Describe*` / `Get*` / `List*` / `Search*` / `Filter*` / `Lookup*` / `Head*` / `Query*` / `BatchGet*` / `Scan*` only | Anything else returns `{status:"forbidden"}`. |
| Apps Script | Generic `http_fetch` tool | The autopilot already can `read_repo_file` for source. For invoking deployments, hit the anonymous `/exec` URL — no Apps Script API client needed. |
| PDF | `reportlab` (pure Python, no system libs) + markdown-lite renderer | Output is base64 + a `/tmp` path; pair with `upload_file_to_github(content_base64=...)` for shipping into a repo. |
| Deploy parity | `scripts/deploy.sh` rsyncs `config/google/` to EC2 with `chmod 600` | Same shape as the `.env` scp. |

---

## 3. Pre-flight checklist (one-time)

- [x] **Service accounts exist** (per `agentic_ai_context/GOOGLE_API_CREDENTIALS.md`):
  - `cypher-defense@get-data-io.iam.gserviceaccount.com`
  - `tdg-scoring-peer-reviewer@get-data-io.iam.gserviceaccount.com`
  - `upc-barcode@get-data-io.iam.gserviceaccount.com`
  - `edgar-dapp-listener@get-data-io.iam.gserviceaccount.com`
  - `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com`
  - `agroverse-market-research@get-data-io.iam.gserviceaccount.com`
- [x] **APIs enabled** on `get-data-io` GCP project: Sheets, Drive, Docs.
- [x] **Smoke test** on EC2: `cypher_defense` SA can read Main Ledger A1:B2 — verified 2026-05-28 19:17 UTC.
- [x] **prod `.env` does not bypass** `disable_governor_check` — separately confirmed in the Telegram-adapter roadmap; reaffirmed.
- [ ] **gspread NOT pulled in** — tools use raw `google-api-python-client`. If a future requirement justifies it, add explicitly.

---

## 4. Track A — ops (Phase 1, SHIPPED 2026-05-28)

| Unit | Work | Shippable result | Status |
|---|---|---|---|
| A1 | `mkdir -p /opt/truesight_autopilot/config/google && chmod 700` on EC2 | dir ready | ✅ |
| A2 | scp 6 unique SA JSONs from canonical sources (`sentiment_importer/config/*.json`, `truesight_me/google-service-account.json`, `krake_local/google-service-account.json`) → EC2 with `chmod 600` | creds on disk | ✅ |
| A3 | Append `GOOGLE_APPLICATION_CREDENTIALS` + `GOOGLE_CREDS_DIR` to `/opt/truesight_autopilot/.env` | env wired | ✅ |
| A4 | `systemctl restart truesight-autopilot.service truesight-autopilot-telegram.service` | new env loaded | ✅ |
| A5 | Live Sheets read smoke test: read Main Ledger A1:B2 via cypher_defense SA from EC2 venv | end-to-end verified | ✅ |

---

## 5. Track B — code (Phase 2, PR in review)

Single PR on `truesight_autopilot` adding seven new tools + the self-contained credential layout.

| Unit | Work | Shippable result | Status |
|---|---|---|---|
| B1 | `app/tools/google_creds.py` — shared credential loader (env var + named-SA resolution, no-raise on missing file) | one credential entry point | ☐ in PR |
| B2 | `app/tools/google_sheets.py` — `read_google_sheet(spreadsheet_id, range_a1, service_account_name=None)` with cell-count cap | Sheets reach | ☐ in PR |
| B3 | `app/tools/google_docs.py` — `read_google_doc(document_id, ...)` flattens paragraph text, ~64KB cap | Docs reach | ☐ in PR |
| B4 | `app/tools/google_drive.py` — `read_drive_file(file_id, ...)` (auto-export native types) + `list_drive_folder(folder_id, ...)`, 256KB cap | Drive reach | ☐ in PR |
| B5 | `app/tools/http_fetch.py` — generic GET/POST/PUT/PATCH/DELETE/HEAD, body cap, blocks private/loopback/metadata hosts | Apps Script `/exec` reach + arbitrary REST | ☐ in PR |
| B6 | `app/tools/aws_tools.py` — `aws_query(account, service, operation, parameters)` reusing `aws_monitor.read_account_specs`, read-only allowlist, JSON-safe serialiser | AWS reach (both accounts) | ☐ in PR |
| B7 | `app/tools/pdf_tools.py` — `generate_pdf(content, title, output_path)` via `reportlab`, markdown-lite (headings/bullets/bold/italic) → base64 + tmp path | PDF output | ☐ in PR |
| B8 | Extend `app/tools/upload_file_to_github.py` with `content_base64` param so PDFs can be shipped to a repo | binary upload | ☐ in PR |
| B9 | Wire schemas in `app/llm_client.get_tool_schemas`, dispatch in `app/main._run_tool`, role gating in `app/roles.py` | tools exposed to all relevant roles | ☐ in PR |
| B10 | `config/google/README.md` + `.gitignore` `config/google/*.json` + `scripts/deploy.sh` rsync block + `.env.example` updates | self-contained credential layout | ☐ in PR |
| B11 | `tests/test_google_sheets.py`, `tests/test_aws_tools.py`, `tests/test_http_fetch.py`, `tests/test_pdf_tools.py` | regression guards | ☐ in PR |

---

## 6. Risks & foot-guns

1. **Private-key drift.** SA JSONs live in two places (`sentiment_importer/config/` AND `truesight_autopilot/config/google/`) during the transition. Rotation must update both, or `sentiment_importer`'s Edgar will go offline. Future cleanup: have `sentiment_importer` read from `~/Applications/truesight_autopilot/config/google/` symlinks. **Track in OPEN_FOLLOWUPS.**
2. **`http_fetch` SSRF surface.** The tool blocks loopback (`127.0.0.1`), link-local (`169.254.169.254` — EC2 metadata), and private IPs by literal-address check. DNS-level rebinding to a private IP is not mitigated — sensitive endpoints on the EC2 host must rely on host-firewall / authn, not URL filtering.
3. **AWS read-only allowlist false negatives.** Some safe ops use unusual verbs (e.g. `EstimateMessageRoute`). Add them to `_READ_PREFIXES` deliberately if a real need shows up; do not flip the allowlist to a denylist.
4. **PDF cap = 256KB returned.** The full bytes are written to the temp path; only the model-visible base64 is truncated. Agents must read `output_path` for the full file (e.g. to upload).
5. **`gspread` not pinned.** All Google tooling uses raw `google-api-python-client`. If a future contributor reaches for `gspread`, prefer to keep dep surface small unless there's a concrete simplification.
6. **gas_error handler still TODO.** Phase 2 adds the *capability* for the autopilot to react to GAS failures (it can now read the Sheet, the source, and hit deployments via `http_fetch`). The autonomous handler in `email_poller.py` is still flagged as TODO at `AUTOPILOT_CODE_MODIFICATIONS.md:551`. Separate roadmap item.

---

## 7. Resume tracker

**RESUME HERE → Track A done; PR open for Track B (Phase 2 code). Once PR merges, run `./scripts/deploy.sh` from local to ship `config/google/` + new code to EC2 (creds are already there from Track A; deploy keeps them in sync going forward).**

| Unit | PR | Merged | Deployed | Contribution reported |
|---|---|---|---|---|
| Roadmap (this file) | agentic_ai_context (in this PR) | ☐ | n/a | ☐ |
| Track A — ops (creds + env + restart + smoke test on EC2) | n/a (ops in shell) | ✅ | ✅ | ☐ |
| Track B — single PR: B1–B11 above | truesight_autopilot#TBD | ☐ | ☐ | ☐ |

After Track B merges + deploys: report one DAO contribution covering Tracks A + B (per `feedback_auto_log_dao_contribution`).

---

## 8. Open follow-ups (carry to `OPEN_FOLLOWUPS.md`)

- Symlink `sentiment_importer/config/*_gdrive_key.json` → `truesight_autopilot/config/google/` to eliminate the duplicate-source-of-truth risk noted in §6.1.
- Build the autonomous `gas_error` handler in `app/email_poller.py` that uses the new Sheets + `http_fetch` reach to remediate failed Apps Script runs.
- Consider Apps Script *deployment management* (clasp / Apps Script API) for the autopilot to push GAS code changes — currently it can only read source from GitHub and trigger anonymous web-app deployments.
