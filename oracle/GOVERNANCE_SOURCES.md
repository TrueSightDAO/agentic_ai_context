# Governance Sources — TrueSight DAO

Single reference for where **governance** (whitepaper, proposals, voting) lives and how to pull or view it. Use this when Dr Manhattan or any LLM needs governance context.

---

## 1. Whitepapers (static pages in the `truesight_me` repo — source of truth)

> **⚠️ 2026-05 — the Google Docs are DEPRECATED.** The whitepapers are now
> **hand-authored static HTML pages in the `truesight_me` repo**, served at
> `truesight.me/...`. **Read the repo page (or the live URL) for current
> content.** Do **NOT** treat the old Google Doc, `scripts/fetch_whitepaper.py`,
> or the `*_WHITEPAPER_SNAPSHOT.md` files as the source of truth — they were
> captured from the retired Docs and may not match the live page.

| Name | Live URL | **Source of truth (repo page)** | Deprecated Google Doc |
|------|----------|---------------------------------|------------------------|
| **Main** | [truesight.me/whitepaper/](https://truesight.me/whitepaper/) | `truesight_me/whitepaper/index.html` | `1P-IJq71…` (retired) |
| **Edgar** | [truesight.me/edgar/whitepaper/](https://truesight.me/edgar/whitepaper/) | `truesight_me/edgar/whitepaper/index.html` | `1Ud19Bd…` (retired) |
| **Agroverse** | [truesight.me/agroverse/whitepaper/](https://truesight.me/agroverse/whitepaper/) | `truesight_me/agroverse/whitepaper/index.html` | `1b3Jiawn…` (retired) |
| **Sunmint** | [truesight.me/sunmint/whitepaper/](https://truesight.me/sunmint/whitepaper/) | `truesight_me/sunmint/whitepaper/index.html` | `1BcrV4rt…` (retired) |

`truesight_me` is the beta base (→ `beta.truesight.me`); production `truesight.me`
deploys from **`truesight_me_prod`** (see **WORKSPACE_CONTEXT.md** §6). Edit the
page in `truesight_me`, open a PR, then promote to prod — do **not**
`gh repo sync --force` (CNAME divergence).

### Reading / editing whitepaper content

- **Read current content:** open the repo page `truesight_me/<area/>whitepaper/index.html`
  (plain static HTML), or `curl` the live `truesight.me/...` URL. The Main
  whitepaper has its `#amendments` section and `#rubric` table inline in the page.
- **Change a whitepaper:** edit the HTML page in `truesight_me` via a normal PR
  (governance approval still applies for substantive/constitutional changes).
  **There is no Google Doc to edit anymore.**
- **Deprecated tooling (history only):** `scripts/fetch_whitepaper.py`, the
  `*_WHITEPAPER_SNAPSHOT.md` files, and the
  `truesight_me/credentials/whitepaper-google-sa.json` SA all targeted the
  retired Google Docs. Don't rely on them for current content.

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
- **Proposal drafts (this repo):** `agentic_ai_context/proposal_drafts/` — ready-to-paste drafts for Create Proposal (e.g. AGL 20% fund management fee standard).

---

## 3. Proposals (Realms — Solana DAO UI)

- **URL:** [https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7](https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7)
- **What it is:** Realms UI for the TrueSight DAO; proposals are listed here (Solana-based DAO view).
- **Access:** **A browser is typically required** to view this page (dynamic content). Use MCP cursor-ide-browser or cursor-browser-extension to open the URL and read or extract proposal titles and status. There is no simple public REST API documented here for Realms proposal listing; scraping or browser automation is the practical option.

---

## 4. Summary for LLMs

| Source | Content | How to access |
|--------|---------|----------------|
| **Whitepapers (main)** | Governance + project narrative | **Read `truesight_me/whitepaper/index.html`** (static page; source of truth) or live [truesight.me/whitepaper/](https://truesight.me/whitepaper/). Google Doc + `fetch_whitepaper.py` + `WHITEPAPER_SNAPSHOT.md` are **deprecated** (see §1). |
| **Whitepapers (edgar, agroverse, sunmint)** | Edgar, Agroverse, Sunmint whitepapers | Read the repo pages `truesight_me/{edgar,agroverse,sunmint}/whitepaper/index.html` (or the live `truesight.me/...` URLs). Old Docs + `*_SNAPSHOT.md` deprecated (see §1). |
| **Proposals (GitHub)** | Proposal text, PRs, votes | Clone [TrueSightDAO/proposals](https://github.com/TrueSightDAO/proposals) or GitHub API. DApp links above for create/vote/view. |
| **Proposals (Realms)** | Proposals listed in Solana DAO UI | Browser: [app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7](https://app.realms.today/dao/2yH36PrWii3RthpHtdJVYaPgBzfcSLe7oevvGRavrut7). |

When answering governance questions, Dr Manhattan (and any agent) should use this doc to know where to look and when to use the fetch script vs. browser vs. GitHub.

---

## 5. Syndicate agreements (Export Trade Financing)

- **Template & drafts:** See `SYNDICATE_AGREEMENTS.md` for how to draft new Export Trade Financing Syndicate Agreements (AGL shipments, operational funds). Template and AGL14/AGL15 drafts live in `notarizations/`. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging).
- **Source data:** Shipment Ledger Listing (Google Sheets): https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=483234653

---

## 6. Voting rights cash-out and USD provisions

- **What it is:** Contributors can cash out their TDG voting rights for USD (or other assets). The **theoretical value** per voting right = total_assets / voting_rights_circulated. However, **actual cash-out is limited by USD reserves**.
- **USD provisions for cash-out:** In the Contribution Ledger's "off chain asset balance" sheet, the row "USD - provisions for voting rights cash out" (Column A) indicates how much USD is set aside for payouts. This is the realistic limit for cash-out. Contributors receive a proportional share: (their_rights / total_rights) × provisions.
- **Source:** Off-chain asset balance tab: https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=2083442561
- **API:** `web_app.gs` (tokenomics) returns `usd_provisions_for_cash_out`. DApp withdraw page uses this to cap the amount input and show the limit.
- **Blog post:** [Understanding Assets Under Management (AUM)](https://truesight.me/blog/posts/understanding-assets-under-management-aum-truesight-dao-comprehensive-asset-tracking.html) explains asset tracking and the off-chain balance.

---

*This document is part of **agentic_ai_context**. See DR_MANHATTAN.md for strategy/onboarding, SYNDICATE_AGREEMENTS.md for syndicate drafting, and OPERATING_INSTRUCTIONS.md for reading order.*
