# Governance Sources — TrueSight DAO

Single reference for where **governance** (whitepaper, proposals, voting) lives and how to pull or view it. Use this when Dr Manhattan or any LLM needs governance context.

---

## 1. Whitepaper (governance and project narrative)

- **URL (public):** [https://truesight.me/whitepaper](https://truesight.me/whitepaper)
- **Behavior:** JavaScript redirect (and meta refresh) to a Google Doc. Governance and project narrative are in that document.
- **Canonical Google Doc:**  
  `https://docs.google.com/document/d/1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic/edit`  
  **Doc ID:** `1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic`

### Pulling whitepaper content (API / script)

- **Script:** `agentic_ai_context/scripts/fetch_whitepaper.py`  
  Fetches whitepaper text and can write a snapshot (e.g. `WHITEPAPER_SNAPSHOT.md`) for use by LLMs or other tools.
  - Tries **Google Docs export URL** first (no credentials; works if doc is “anyone with link can view”).
  - Optionally uses **Google Docs API** with credentials (set `GOOGLE_APPLICATION_CREDENTIALS` or pass `--credentials path/to.json`) for docs that require auth.
- **Run:**  
  `cd agentic_ai_context/scripts && pip install -r requirements.txt && python fetch_whitepaper.py -o ../WHITEPAPER_SNAPSHOT.md`
- **Snapshot file:** `agentic_ai_context/WHITEPAPER_SNAPSHOT.md` — When the script is run successfully (or content is pasted from the doc), LLMs can read this file for whitepaper content without running the script. It may start as a placeholder with instructions to refresh.
- **Browser fallback:** If the script cannot access the doc (e.g. doc is private), use a browser (e.g. MCP cursor-ide-browser) to open [https://truesight.me/whitepaper](https://truesight.me/whitepaper), let it redirect, and extract the visible text; paste into `WHITEPAPER_SNAPSHOT.md` or use the content in context.

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
| **Whitepaper** | Governance + project narrative | Script `scripts/fetch_whitepaper.py`; or browser to [truesight.me/whitepaper](https://truesight.me/whitepaper). Doc ID: `1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic`. |
| **Proposals (GitHub)** | Proposal text, PRs, votes | Clone [TrueSightDAO/proposals](https://github.com/TrueSightDAO/proposals) or GitHub API. DApp links above for create/vote/view. |
| **Proposals (Realms)** | Proposals listed in Solana DAO UI | Browser: [app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7](https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7). |

When answering governance questions, Dr Manhattan (and any agent) should use this doc to know where to look and when to use the fetch script vs. browser vs. GitHub.

---

*This document is part of **agentic_ai_context**. See DR_MANHATTAN.md for strategy/onboarding and OPERATING_INSTRUCTIONS.md for reading order.*
