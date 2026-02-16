# Governance Sources — TrueSight DAO

Single reference for where **governance** (whitepaper, proposals, voting) lives and how to pull or view it. Use this when Dr Manhattan or any LLM needs governance context.

---

## 1. Whitepapers (truesight.me — all redirect to Google Docs)

All truesight.me whitepaper URLs use a JavaScript redirect (and meta refresh) to a Google Doc. The fetch script can pull any or all of them.

| Name | URL | Doc ID | Snapshot file |
|------|-----|--------|----------------|
| **Main** (governance, project narrative) | [truesight.me/whitepaper](https://truesight.me/whitepaper) → [Google Doc](https://docs.google.com/document/d/1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic/edit?tab=t.0) | `1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic` | `WHITEPAPER_SNAPSHOT.md` |
| **Edgar** | [truesight.me/edgar/whitepaper](https://truesight.me/edgar/whitepaper) → [Google Doc](https://docs.google.com/document/d/1Ud19BdIKrg_2SvVYEfS2fxCFCwFGwuccqOD9z53k-oc/edit?tab=t.0) | `1Ud19BdIKrg_2SvVYEfS2fxCFCwFGwuccqOD9z53k-oc` | `EDGAR_WHITEPAPER_SNAPSHOT.md` |
| **Agroverse** | [truesight.me/agroverse/whitepaper](https://truesight.me/agroverse/whitepaper) → [Google Doc](https://docs.google.com/document/d/1b3JiawnqA1QNpA_XZMH6oNQ9ZVJnLRGtOWzM31YLvJs/edit?tab=t.0) | `1b3JiawnqA1QNpA_XZMH6oNQ9ZVJnLRGtOWzM31YLvJs` | `AGROVERSE_WHITEPAPER_SNAPSHOT.md` |
| **Sunmint** | [truesight.me/sunmint/whitepaper](https://truesight.me/sunmint/whitepaper) → [Google Doc](https://docs.google.com/document/d/1BcrV4rtG5cNTdcycw2H94OI-pmT-dDal3x5jPcyvWC0/edit?tab=t.0) | `1BcrV4rtG5cNTdcycw2H94OI-pmT-dDal3x5jPcyvWC0` | `SUNMINT_WHITEPAPER_SNAPSHOT.md` |

### Pulling whitepaper content (API / script)

- **Script:** `agentic_ai_context/scripts/fetch_whitepaper.py`  
  Fetches one or all whitepapers. Tries **Google Docs export URL** first (no credentials); optionally uses **Google Docs API** with `GOOGLE_APPLICATION_CREDENTIALS` or `--credentials path/to.json`.
  (See table above for doc IDs and snapshot filenames.)
- **Run (single):**  
  `cd agentic_ai_context/scripts && pip install -r requirements.txt && python fetch_whitepaper.py -o ../WHITEPAPER_SNAPSHOT.md`  
  Or: `python fetch_whitepaper.py --which edgar -o ../EDGAR_WHITEPAPER_SNAPSHOT.md` (same for `agroverse`, `sunmint`).
- **Run (all four):**  
  `python fetch_whitepaper.py --all -o ../`  
  Writes all four snapshot files in the parent directory.
- **Snapshot files:** When the script is run successfully (or content is pasted from each doc), LLMs can read these files. They may start as placeholders with instructions to refresh.
- **Browser fallback:** If the script cannot access a doc, use a browser to open the URL above, let it redirect, and extract/paste the text into the corresponding snapshot file.

---

## 2. Proposals (GitHub)

- **Repo:** [https://github.com/TrueSightDAO/proposals](https://github.com/TrueSightDAO/proposals)
- **What it is:** Main proposals repository. Community proposals are submitted via the DApp, become GitHub pull requests, and are voted on with digital signatures. After a 7-day voting period, majority YES → PR merged (approved), majority NO → PR closed (rejected).
- **Key links:**
  - **DApp (create/vote/view):** [https://truesightdao.github.io/dapp/](https://truesightdao.github.io/dapp/)
  - **Create proposal:** [https://truesightdao.github.io/dapp/create_proposal.html](https://truesightdao.github.io/dapp/create_proposal.html)
  - **Review & vote:** [https://truesightdao.github.io/dapp/review_proposal.html](https://truesightdao.github.io/dapp/review_proposal.html)
  - **View open proposals:** [https://truesightdao.github.io/dapp/view_open_proposals.html](https://truesightdao.github.io/dapp/view_open_proposals.html)
  - **Create digital signature:** [https://truesightdao.github.io/dapp/create_signature.html](https://truesightdao.github.io/dapp/create_signature.html)
- **Backend:** Google Apps Script in tokenomics repo: `tokenomics/google_app_scripts/tdg_proposal/proposal_manager.gs`
- **Pulling proposal data:** Clone the repo or use GitHub API (e.g. list PRs, get PR body and comments for votes). No browser required for repo/API access.

---

## 3. Proposals (Realms — Solana DAO UI)

- **URL:** [https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7](https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7)
- **What it is:** Realms UI for the TrueSight DAO; proposals are listed here (Solana-based DAO view).
- **Access:** **A browser is typically required** to view this page (dynamic content). Use MCP cursor-ide-browser or cursor-browser-extension to open the URL and read or extract proposal titles and status. There is no simple public REST API documented here for Realms proposal listing; scraping or browser automation is the practical option.

---

## 4. Summary for LLMs

| Source | Content | How to access |
|--------|---------|----------------|
| **Whitepapers (main)** | Governance + project narrative | Script `scripts/fetch_whitepaper.py` or `--all -o ../`; snapshot: `WHITEPAPER_SNAPSHOT.md`. Or browser to [truesight.me/whitepaper](https://truesight.me/whitepaper). |
| **Whitepapers (edgar, agroverse, sunmint)** | Edgar, Agroverse, Sunmint whitepapers | Same script: `--which edgar|agroverse|sunmint -o ../*_SNAPSHOT.md` or `--all -o ../`. Snapshots: `EDGAR_WHITEPAPER_SNAPSHOT.md`, `AGROVERSE_WHITEPAPER_SNAPSHOT.md`, `SUNMINT_WHITEPAPER_SNAPSHOT.md`. |
| **Proposals (GitHub)** | Proposal text, PRs, votes | Clone [TrueSightDAO/proposals](https://github.com/TrueSightDAO/proposals) or GitHub API. DApp links above for create/vote/view. |
| **Proposals (Realms)** | Proposals listed in Solana DAO UI | Browser: [app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7](https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7). |

When answering governance questions, Dr Manhattan (and any agent) should use this doc to know where to look and when to use the fetch script vs. browser vs. GitHub.

---

*This document is part of **agentic_ai_context**. See DR_MANHATTAN.md for strategy/onboarding and OPERATING_INSTRUCTIONS.md for reading order.*
