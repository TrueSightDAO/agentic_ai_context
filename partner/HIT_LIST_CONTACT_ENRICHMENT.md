# Hit List contact enrichment (`AI: Enrich with contact`)

Canonical narrative for future agents: what we built, how it behaves, and design choices. **Operational CLI and secrets** stay in **`market_research/HIT_LIST_CREDENTIALS.md`** (same spreadsheet as **`PARTNER_OUTREACH_PROTOCOL.md`**).

## Goal

After photo review (or manual triage), some rows need a **website-level** pass to find a B2B contact email or a **public contact form URL** before human outreach. The queue uses Hit List **Status = `AI: Enrich with contact`**. The automation must leave an audit trail that **Store Interaction History** and operators treat like human-submitted **DApp Remarks**, not a silent edit to **Hit List → Notes** alone.

## What shipped (code + CI)

| Artifact | Role |
|----------|------|
| **`market_research/scripts/hit_list_enrich_contact.py`** | Consumes rows with **`AI: Enrich with contact`** (default **10** per run): resolves **Website** or Places **website** via **`place_id`** in **Notes**, fetches pages + common `/contact` paths, regex emails + contact-form heuristic, optional **Grok** to pick one email or one form URL. Writes **Email** and/or **Contact Form URL** when found; sets **AI: Email found**, **AI: Contact Form found**, or **AI: Enrich — manual** (or manual with **no website**). |
| **`market_research/scripts/hit_list_dapp_remarks_sheet.py`** | Shared **append DApp Remarks row → apply to Hit List → mark Processed** logic (same semantics as **`physical_stores/process_dapp_remarks.py`** and the photo-review script). |
| **`market_research/scripts/hit_list_research_photo_review.py`** | Refactored to import **`append_dapp_remark_and_apply`** from the shared module (behavior unchanged). |
| **`.github/workflows/hit_list_enrich_contact.yml`** | Scheduled **hourly** at **:35 UTC** (staggered from photo review on the hour); default **10** rows; secrets **`GOOGLE_CREDENTIALS_JSON`**, **`GOOGLE_MAPS_API_KEY`**, **`GROK_API_KEY`** (optional Grok; **`--no-grok`** locally). |

**GitHub:** automation and scripts live in **`TrueSightDAO/go_to_market`** (local working copy often mounted as **`market_research/`**). Some docs still list **`content_schedule`** as an older clone name—follow the remote the workspace actually uses.

## Design decisions (discussed / locked in)

1. **Hit List Notes vs DApp Remarks**  
   Early iterations appended `[enrich-contact ISO8601] outcome=…` to **Hit List → Notes**. That conflated **discovery/places context** (e.g. `place_id`) with **operator-facing remarks**. We **stopped** writing those audit lines to **Notes** and now log only via **DApp Remarks** (see below). **Notes** remains the place for `place_id` and discovery text.

2. **Parity with human DApp + photo review**  
   Humans submit optional **remarks** through **Stores Nearby** / update flows; those land on **DApp Remarks** and are applied to **Hit List** (notably **Sales Process Notes**) by **`process_dapp_remarks.py`** or the inline apply step. Photo review uses the same pattern. Contact enrich **reuses that pipeline**: append a **DApp Remarks** row (Submission ID, Shop Name, Status, Remarks, Submitted By, Submitted At, then Processed), then apply **Status**, append **`Sales Process Notes`** with **`[Submitted At | Submitted By]`** prefix, set **Status Updated By / Date**, and set **Processed = Yes** on the remark row. That way **Store Interaction History** (`dapp/store_interaction_history.html`) shows these under **DApp Remarks** like other entries.

3. **Audit line format**  
   The **Remarks** cell (and thus the mirror in **Sales Process Notes**) uses a single-line tag for grepability: **`[enrich-contact <ISO8601 Z>] outcome=email|contact_form|manual|no_website`** plus a short **`website=`** snippet where relevant. **Submitted By** is **`hit_list_enrich_contact`**. **Submitted At** uses the same **`MM/DD/YYYY HH:MM:SS`** (UTC) style as photo review for consistency with **`process_dapp_remarks.py`**.

4. **Hit List columns required for apply**  
   The apply step **requires** **Sales Process Notes**, **Status Updated By**, and **Status Updated Date** on **Hit List** (same as photo review). If any are missing, the script fails loudly—add columns before relying on CI.

5. **Rate / schedule**  
   Enrich is lighter than Grok vision + Places photos but still HTTP-heavy. **Hourly** runs with **10** rows per run balance throughput and courtesy to target sites; cron minute **:35** avoids colliding with the photo-review workflow on the hour.

6. **PR vs direct push**  
   A batch of commits reached **`main`** via direct push before branch protection / PR discipline was enforced for that repo. **Preferred workflow** for new work: **`feature/<topic>`** → **`gh pr create`** → merge. See **`GITHUB_AGENTIC_AI_SSH.md`**. Compare range for the enrich slice (when explaining to operators): `https://github.com/TrueSightDAO/go_to_market/compare/cd8fe94%5E...1d311e7` (parent of first enrich commit through DApp Remarks logging commit—update SHAs if history is rebased).

## Related docs

- **`market_research/HIT_LIST_CREDENTIALS.md`** — spreadsheet ID, service account, discovery regions, **contact enrichment** subsection, photo review, Email Agent tabs.
- **`WORKSPACE_CONTEXT.md`** §4 — short bullets for **Research** photo review and **`AI: Enrich with contact`**.
- **`PARTNER_OUTREACH_PROTOCOL.md`** — human-in-the-loop outreach after automation.
- **`dapp/store_interaction_history.html`** — reads **DApp Remarks** via holistic hit list history API (exec URL in GAS project).

## Session / handoff note for AIs

If you extend this pipeline: keep **one** implementation of “append remark + apply + mark processed” (**`hit_list_dapp_remarks_sheet.py`**); do not fork divergent Sales Process Notes logic in the enrich script. If product asks for different **Remarks** wording, change the **`remark = f"[enrich-contact …]"`** builder in **`hit_list_enrich_contact.py`** only, unless the whole org changes the DApp Remarks schema.
