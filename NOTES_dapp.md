# DApp (dapp.truesight.me) — Working Notes

Purpose: Fast reference for Grok/Claude/Codex to understand and extend the TrueSight DAO DApp at `/Users/garyjob/Applications/dapp`.

## Overview
- Static web app (HTML/CSS/JS) deployed via GitHub Pages: `https://dapp.truesight.me`.
- Modules for signatures, inventory, tree planting, proposals, sales, QR codes, and notarization.
- Uses browser WebCrypto (RSA-2048, RSASSA-PKCS1-v1_5, SHA-256) for signing; keys stored in `localStorage`.
- Integrates with:
  - Edgar API: `https://edgar.truesight.me` (submit, health check)
  - Google Apps Script (GAS) web apps for verification and data (see tokenomics API.md)

## Key Files
- `index.html` — landing with module links and instructions.
- `menu.js` — shared navigation dropdown for all pages.
- `scripts/edgar_payload_helper.js` — canonical payload builder, signer, verifier, and share-text generator.
- Service worker: `service-worker.js` — cache-first/network-first mix with special handling for GAS endpoints and `?reload` param.
- Module pages (selection):
  - Identity & Governance: `create_signature.html`, `withdraw_voting_rights.html`, `verify_request.html`, `notarize.html`, `view_open_proposals.html`, `create_proposal.html`, `review_proposal.html`.
  - Inventory & Sales: `scanner.html`, `report_sales.html`, `report_dao_expenses.html`, `report_inventory_movement.html`, `update_qr_code.html`, `batch_qr_generator.html`, `stores_nearby.html`, `shipping_planner.html`.
  - Sunmint: `register_farm.html`, `report_tree_planting.html`.
  - Contributions: `report_contribution.html`, `submit_feedback.html`.

## Digital Signature Model
- Keys generated client-side via WebCrypto; exported to base64 (SPKI public, PKCS#8 private) and stored in `localStorage` under `publicKey`/`privateKey`.
- `EdgarPayloadHelper`:
  - `buildPayloadString(eventName, attributes)` creates the canonical text: `[EVENT]\n- Label: Value\n...\n--------`.
  - `generatePayload({ eventName, attributes, privateKey, digitalSignature })` returns `{ payload, requestTransactionId (base64 signature), shareText }`.
  - `verifyPayload(payload, requestTransactionId, digitalSignatureOverride?)` uses the public key to verify.
  - `runSelfTest()` generates an ephemeral keypair and validates sign/verify roundtrip.
- Most pages: build payload → sign → optional file attach → POST to Edgar → also include text to share/verify publicly.

## Endpoints (as seen in code)
- Edgar
  - Health: `HEAD https://edgar.truesight.me/ping`
  - Submit: `POST https://edgar.truesight.me/dao/submit_contribution` (multipart form with `text` and optional `attachment`)
- GAS (tokenomics google_app_scripts web apps)
  - Signature/asset verification: `https://script.google.com/macros/s/AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7/exec`
  - QR code APIs: `AKfycbxigq4-.../exec` with `list=true`, `list_all=true`, `list_with_members=true`, and lookups
  - DAO form data (members/recipients/ledgers/currencies lists): `AKfycbztpV3T.../exec` with various query params
  - Proposals web app: `AKfycbzgNstwR.../exec` (under `agroverse.shop` domain)
  - Feedback: `AKfycbz3FQgXL.../exec`
- See tokenomics/API.md for authoritative documentation and descriptions.

## Service Worker Behavior
- Cache name: `qr-scanner-cache-v1`.
- Pre-caches HTML pages, assets, `menu.js`, and the two primary GAS endpoints.
- `?reload` param on any request forces network fetch and cache update for that URL.
- GAS endpoints: network-first with cache fallback; others: network-first with cache fallback.
- Tip: If users see stale content, append `?reload=1` to page URL or clear browser cache.

## UX Conventions
- Centralized in `UX_CONVENTIONS.md`:
  - Immediate loading state changes when fetching remote data.
  - Signature verification on page load for authenticated modules.
  - Combobox/searchable dropdown patterns for large datasets (QR codes, members).
  - Clear error styling and actionable messages; offline fallbacks when possible.

## Common Flows
- Create signature: `create_signature.html` generates keys and stores them; provides sharing/backup options.
- Verify request: `verify_request.html` parses shared text, extracts payload/signature, calls verifier GAS and/or local verification.
- Report contribution/expenses/tree planting/sales:
  - Build canonical payload from form values → sign → `edgar.truesight.me/dao/submit_contribution` (multipart) → show result + share text.
- Inventory movement / QR update:
  - Load lists from GAS endpoints following UX loading pattern → capture photos/fields → build payload → submit to Edgar.

## Pitfalls & Notes
- WebCrypto requires secure context: pages are served via HTTPS on GitHub Pages; local `file://` won’t work for crypto — use a local server.
- Base64 normalization: helper normalizes RFC4648 variants and padding.
- Caching: service worker may cache GAS results; use `?reload=1` or incognito when debugging.
- Endpoint sprawl: endpoints are hardcoded in multiple HTML files; consider centralizing into a single config script for maintainability.

## Quick Commands
- Local preview (static)
  - `cd /Users/garyjob/Applications/dapp && python3 -m http.server 8080`
  - Open `http://localhost:8080/index.html` (WebCrypto works on localhost).
- Force fresh fetch for a page
  - Append `?reload=1` to the page URL.
- Self-test crypto helper in browser console
  - Load any page that includes `scripts/edgar_payload_helper.js` (modules import it inline as needed) or inject it, then run: `await EdgarPayloadHelper.runSelfTest()`.
- Clear keys for a clean start
  - In DevTools console: `localStorage.removeItem('publicKey'); localStorage.removeItem('privateKey');`

## Next Improvements (optional)
- Centralize API endpoints into `config.js` and include it on all pages.
- Add a minimal build step to version asset URLs and update the service worker cache name automatically.
- Factor repetitive UI blocks (status messages, loaders) into shared helpers.
- Add a small status section on index.html that pings edgar and checks GAS reachability.

References
- Repo: `/Users/garyjob/Applications/dapp`
- Related: `/Users/garyjob/Applications/tokenomics/API.md` (Edgar + GAS API docs)
- UX: `/Users/garyjob/Applications/dapp/UX_CONVENTIONS.md`
