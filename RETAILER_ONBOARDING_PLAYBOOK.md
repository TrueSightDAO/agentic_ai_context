# Retailer Onboarding Playbook — USA field visits + AI outreach (v0.2)

**Status:** INTERIM **v0.2** — field-visit patterns compiled from USA retailer
visits (v0.1), **updated with the automated AI email outreach pipeline**
shipped between 2026-04-27 and 2026-05-03. The two paths (in-person field
visits AND automated warm-up emails) are now both documented.
**Last reviewed:** 2026-05-04
**Owner:** Agroverse / TrueSight (human: Gary + AI assist)

**Promotion to v1.0 when:** At least **3 additional Partnered conversions**
follow either path end-to-end without contradicting the field-visit patterns
(§8–§11) or the AI pipeline's reply-rate assumptions.

---

## 1. What this playbook is

**Two parallel paths** to convert retail leads into consignment partners:

| Path | Starting point | Channel | Automation level |
|------|---------------|---------|-----------------|
| **A — AI email outreach** | Website crawl qualifies store as circle-hosting → email enrichment → Grok-drafted warm-up email | Email | Automated discovery through draft creation; operator reviews + sends |
| **B — In-person field visits** | Shortlisted by operator → Google Maps visit → sample drop → follow-up | In-person + email | Manual; this playbook is the SOP |

Path A is described in §3. Path B is described in §4–§14.

This playbook is the **index** for both flows; the specialized docs below remain
the source of truth for their sub-steps:

| Sub-step | Authoritative doc |
|----------|-------------------|
| AI outreach state machine | [`HIT_LIST_STATE_MACHINE.md`](HIT_LIST_STATE_MACHINE.md) |
| AI outreach protocol + cadence | [`PARTNER_OUTREACH_PROTOCOL.md`](PARTNER_OUTREACH_PROTOCOL.md) |
| Post-visit email drafting | [`STORE_FOLLOW_UP_EMAIL_TEMPLATE.md`](STORE_FOLLOW_UP_EMAIL_TEMPLATE.md) |
| First-drop bag count | [`CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md`](CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md) |
| Restock / reorder logic | [`RESTOCK_RECOMMENDER_ON_THE_FLY.md`](RESTOCK_RECOMMENDER_ON_THE_FLY.md) |
| Hit List contact enrichment | [`HIT_LIST_CONTACT_ENRICHMENT.md`](HIT_LIST_CONTACT_ENRICHMENT.md) |
| Lead sourcing | [`LEAD_LIST_EXTRACTION.md`](LEAD_LIST_EXTRACTION.md) |
| Technical onboarding (post-Partnered) | [`RETAILER_TECHNICAL_ONBOARDING.md`](RETAILER_TECHNICAL_ONBOARDING.md) |
| Warm-up email tone reference | `market_research/templates/warmup_outreach_reference.md` |

## 2. Non-goals

- Wholesale / bulk industrial deals (different unit economics — see §15).
- Online-only storefronts without a physical shop.
- Replacing any of the docs linked in §1; this file indexes, not duplicates.

---

## 3. Path A — Automated AI email outreach pipeline

### 3.1 Overview

A fully automated cron pipeline that runs in GitHub Actions
(`TrueSightDAO/go_to_market`) and moves retailers from discovery through to a
Grok-generated warm-up email — with the operator reviewing and sending from
Gmail. The canonical state machine is documented in
**`HIT_LIST_STATE_MACHINE.md`**; this section is the operator-facing summary.

### 3.2 Stage-gated flow

Each stage maps to a Hit List `Status`. The **exit criterion** is what must be
true before advancing. All transitions are driven by the cron schedule below.

| # | Stage | Exit criterion | Who moves it |
|---|-------|----------------|-------------|
| 1 | **Research** | Website URL populated on Hit List row. Store discovered via Google Maps Nearby Search or `[STORE ADD EVENT]`. | `discover_apothecaries` (manual) or operator |
| 2 | **Hosts Circles detection** | Store website crawled for circle-hosting keywords (cacao ceremony, sound bath, women's circle, etc.). Column **Hosts Circles** set to `Yes` or `Not detected`. | `detect_circle_hosting_retailers.py` (hourly :50) |
| 3 | **AI: Enrich with contact** | Hosts Circles=Yes **and** no email on row → queued for Place Details + email harvesting. | `detect_circle_hosting_retailers.py` promotion from Research |
| 4a | **AI: Email found** | Grok + regex extracted a confirmed email from website/contact pages. | `hit_list_enrich_contact.py` (hourly :35) |
| 4b | **AI: Contact Form found** | Only a contact form URL surfaced. Manual follow-up required. **Terminal** — no auto-promotion. | `hit_list_enrich_contact.py` |
| 4c | **AI: Enrich — manual** | No website, no place_id, or all crawls failed. Operator triage. | `hit_list_enrich_contact.py` |
| 5 | **AI: Warm up prospect** | Email found → promoted by `email-to-warmup` cron. Now eligible for Gmail draft. | `hit_list_promote_status.py` (hourly :20) |
| 6 | **Draft created** | Grok-drafted warm-up email with PDF + 2 packaging photos as attachments, labeled **`AI/Warm-up`** in Gmail. `status='pending_review'` on **Email Agent Drafts** tab. | `suggest_warmup_prospect_drafts.py` (daily 14:00 UTC) |
| 7 | **Operator sends** | Operator reviews via `preview_warmup_drafts.py` (HTML triage with 12-rule linter), edits if needed, hits **Send** in Gmail. | Operator (manual) |
| 8 | **AI: Prospect replied** | Gmail detects inbound reply from prospect → auto-promoted. | `suggest_warmup_prospect_drafts.py` reply-promotion pass |
| 9 | **Manager Follow-up** | Operator routes replied prospect for follow-up drafting. | Operator (manual) |
| 10 | **Follow-up draft created** | Cadenced follow-up email (min 7 days since last sent), labeled **`AI/Follow-up`** in Gmail. | `suggest_manager_followup_drafts.py` (daily 14:00 UTC) |
| — | **AI: No fit signal** | Site crawled OK but zero qualifying keywords. Re-rescued on re-crawl if site changes. | `detect_circle_hosting_retailers.py` |
| — | **On Hold / Rejected / Not Appropriate** | See §11 disqualification patterns. | Operator |

### 3.3 Cron schedule (all times UTC)

| Minute | Workflow | What it does |
|--------|----------|-------------|
| `:20` | `hit_list_status_promote.yml` | `email-to-warmup` promotion (AI: Email found → AI: Warm up prospect), shortlisted-to-enrich |
| `:35` | `hit_list_enrich_contact.yml` | Place Details + website crawl + Grok email pick (AI: Enrich with contact → AI: Email found / AI: Contact Form found / AI: Enrich — manual) |
| `:50` | `detect_circle_hosting.yml` | Website crawl for circle-hosting keywords; promotion from Research + rescue from AI: No fit signal |
| `14:00 daily` | `manager-followup-drafts.yml` | Sync sent mail → suggest warm-up drafts + follow-up drafts (cadence: 7 days since last send) |

### 3.4 Operator review loop (warm-up drafts)

When the daily cron creates warm-up drafts, the operator:

1. **Runs `preview_warmup_drafts.py`** — generates an HTML triage view with a
   12-rule linter:
   - **Red flags**: empty subject/body, generic `info@` recipient, fallback
     "your shop" in body, foreign-script venue, unrendered placeholders, etc.
   - **Yellow flags**: no city/state, no Hit List notes, no DApp history.
   - **Blue badge**: Hosts Circles=Yes (higher-intent prospect).
2. **Opens flagged drafts in Gmail** — one-click deep-link from HTML, edits
   if needed, sends.
3. **Batch-sends the clean cohort** — open the `AI/Warm-up` label in Gmail, scan,
   send.
4. **Runs `sync_email_agent_followup.py`** — logs sent messages to **Email Agent
   Follow Up** tab so cadence engine stays honest.

### 3.5 Gmail label convention

Four purpose-specific labels (split 2026-04-17):

| Label | Meaning | Applied by |
|-------|---------|-----------|
| **`AI/Warm-up`** | Draft awaiting review + send (first-touch intro) | `suggest_warmup_prospect_drafts.py` |
| **`AI/Follow-up`** | Draft awaiting review + send (post-reply follow-up) | `suggest_manager_followup_drafts.py` |
| **`AI/Sent Warm-up`** | Warm-up that has been sent | `sync_email_agent_followup.py` (auto-swap) |
| **`AI/Sent Follow-up`** | Follow-up that has been sent | `sync_email_agent_followup.py` (auto-swap) |

The review labels stay clean as a "needs your eyes" queue; `sync_email_agent_followup.py`
swaps the label from review to sent after detecting the sent message.

### 3.6 What the warm-up email contains

- **Amazon rainforest restoration** lead ("each bag plants a tree, traceable
  via unique QR code"), with an Instagram reel link as 30-second visual proof.
- **Flexible options**: consignment OR wholesale/bulk, no pressure.
- **Attachments**: wholesale price list PDF + 2 packaging photos (front/back).
- **Visual companion**: `https://agroverse.shop/wholesale` (packaging, partner
  shop photos, U.S. stockists).
- **No assumption of in-person visit** — actionable entirely by email.
- **Grok-generated** with `--use-grok` flag, using the tone reference at
  `market_research/templates/warmup_outreach_reference.md`.

### 3.7 Open/click tracking

All outbound emails include tracking pixels and click-through links served by
Edgar (`GET /email_agent/open.gif` + `/email_agent/click`). Data lands on the
**Email Agent Drafts** tab (cols H–K = opens, L–P = clicks). Run
`reconcile_email_agent_drafts_stale_sent.py` if Gmail shows SENT but the sheet
still says `pending_review`.

### 3.8 Fast-track from circle detection

If `detect_circle_hosting_retailers.py` finds a store's website heavily
mentions cacao-ceremony-relevant keywords **and** the Hit List row already has
an Email column populated, the row fast-tracks directly from **Research** →
**AI: Warm up prospect** (skipping Enrich entirely). This is the fastest path
to a draft.

---

## 4. Path B — In-person field visits: overview

The remainder of this playbook (§4–§16) covers the **in-person, field-agent**
onboarding path. This path is still active for visits to stores where:
- No email was harvestable (AI: Contact Form found / AI: Enrich — manual).
- The store has been shortlisted manually (e.g., referral from a Partnered store).
- You are physically in the area and can make visits.

**When both paths converge:** A store contacted via Path A (email) may get an
in-person visit later, or a store visited via Path B may get follow-up
drafts from the Path A pipeline. The Hit List `Status` column is the shared
truth — the pipeline reads whatever status the row has.

### 4.1 Field-visit stage-gated flow

Each stage maps to a Hit List `Status`. The **exit criterion** is what must be
true before advancing.

| # | Stage | Exit criterion | Primary artifact |
|---|-------|----------------|------------------|
| 1 | **Research** | Store appears to match theme (holistic / herbal / apothecary / ceremonial). | Hit List row |
| 2 | **Shortlisted** | Contact method exists **and** store confirmed open (Google Maps current). | Hit List row + dapp store page |
| 3 | **Contacted / Visit** | In-person visit done **or** cold email+call logged. Decision-maker name captured. | DApp Remark |
| 4 | **Manager Follow-up** | Samples dropped **and** owner's availability window known (date / phone / email). | DApp Remark + sample log |
| 5 | **Meeting Scheduled** | Call or revisit time on calendar with the decision-maker. | Calendar event |
| 6 | **Followed Up** | Post-visit email sent (template per §1). Awaiting reply. | Gmail thread |
| 7 | **Partnered** | Verbal or written **yes** on consignment (or bulk order), first bags placed, QR checkout demoed. | Consignment agreement |
| — | On Hold / Rejected / Not Appropriate | See §11 disqualification patterns. | DApp Remark |

---

## 5. Pre-visit: shortlisting heuristics

Observed signals that correlate with a useful visit:

- **Instagram-lookalike shortlisting works.** "Similar profile to Go Ask
  Alice" has surfaced multiple viable leads (Earthly Essentials, Milk & Honey,
  Soul Connections, The Wild Grove Collective, The Candy Vault). Use a
  proven Partnered store as the reference profile.
- **Referrals from adjacent shops** are warm leads (e.g. Apotheca referred us
  to Unique Shop up the street).
- **Verify Google Maps status** before planning the visit. A non-trivial
  fraction of "stores" in the Hit List turn out to be permanently closed,
  temporarily closed, or miscategorized (farmer's markets, private-by-
  appointment spaces, garden plots, bookstores, chapels).
  > **Automation note:** The enrichment cron (`hit_list_enrich_contact.yml`)
  > already populates Address, City, State, Lat/Lon, and opening hours from
  > Google Places API for all Hit List rows. Manual Google Maps verification
  > is only needed for field-visit planning.

## 6. The store visit — structure

A good visit captures four things in the DApp Remark:

1. **Who you spoke to** (staff name) and **who decides** (owner name).
2. **When the decision-maker is next reachable** (day / time / phone / email).
3. **Their existing cacao / chocolate shelf** — price points, SKUs, any
   overlap with our offering.
4. **Their reaction to a taste sample** (cacao from Oscar's Farm + cacao tea
   from Paulo's Farm). The taste is what converts — see §8.

## 7. Sample drop-off protocol

- Leave **ceremonial cacao (Oscar's Farm, Bahia)** + **cacao tea (Paulo's La
  do Sitio, Pará)** as a pair. Both samples are the standard kit.
- Hand the samples to whoever is at the counter; explicitly ask them to pass
  them to the named decision-maker.
- Leave a business card with the samples.
- Log the drop-off as a DApp Remark immediately.
- Do not leave samples at stores that don't sell anything ingestible (see §11).

## 8. What actually lands — patterns from Partnered stores

Recurring moments that appear in Partnered remarks and correlate with the
"yes":

- **"A single sale plants a tree."** This has been the emotional hook that
  multiple store owners have reacted to visibly (e.g. Liza at RAVEN things
  collected).
- **QR-code checkout demo is the "aha" moment.** Walking a store owner
  through the scan-to-pay flow and showing how the $17 split is transparent
  repeatedly breaks through skepticism. Do this live, on your phone.
- **Taste profile language matters.** Reuse the descriptors from the San
  Francisco cacao circle (Christine and the chocolate tears) when describing
  Oscar's vs Paulo's 2024 harvest. Generic "it's high-quality" does not land;
  specific taste-profile language does.
- **Local representation.** Retailers want to know they are dealing with
  someone local / someone with skin in the game (being a shareholder has
  come up as a positive signal). When possible, frame yourself as a local
  representative rather than a visiting importer.
- **Lab-tested answer to allergy concerns.** Several store owners flag
  allergies when sampling; the response "all our cacao is lab tested" has
  defused this in Partnered conversations.
- **Multiple regions = feature, not bug.** Partnered stores (e.g. Lumin
  Earth Apothecary) are comfortable stocking our cacao alongside Kakao
  Laboratory and Pacha Mama cacao — frame different farms as different
  taste profiles, not competing products.

## 9. What retailers ask / worry about

| Concern | What to say |
|---------|-------------|
| "Why consignment — are you just starting out?" | "We've been operating for years. Consignment is how we onboard shopkeepers through turbulent economic conditions." |
| "Is the QR-code payment reconciliation actually reliable?" | Demo the flow on your phone; show the order trail. |
| "Is this produced in the US?" | Honest answer: Brazilian Amazon (Bahia, Pará), imported by us. Name the farms. |
| "Are there other stores around here already carrying this?" | Give an honest answer using the dapp store map. Proximity/exclusivity questions come up more than expected. |
| "How do I drink ceremonial cacao vs cacao tea?" | Have a prepared short answer for both preparations (one sip / one brew). |
| "Allergies?" | Lab-tested; offer to share lab reports. |
| "What's the retail price?" | $17 cost, $25–$35 retail range. Walk through the split math. |

## 10. Recurring decision-maker dynamics

From USA visits:

- **Staff-to-owner handoff is the norm.** Expect to pitch twice: once to a
  staff member (Danielle, Jan, Charlie, Laurels, Mary Pat, Sherry, Liz have
  all played this role in recent logs), then to the owner separately.
  Capture the staff member's name — they become your internal advocate.
- **Owner return windows.** Ask "when is [owner] next in?" and log a specific
  day (Tuesday/Thursday schedules, "back on Friday", "after Thanksgiving"
  have all shown up). This becomes your calendar trigger.
- **"Let me taste with my team."** Some owners (e.g. Holley at The Natural
  Alternative Nutrition Center) explicitly need **~1 week** with their staff
  before deciding. Set that expectation and do not re-ping early.
- **Owner travel.** Factor in that small-shop owners travel (Japan, family
  visits) — confirm return date with staff before scheduling a call.

## 11. Disqualification patterns — walk away early

Stop spending time when the store matches any of these:

| Pattern | Example stores |
|---------|----------------|
| Sells nothing ingestible (only crystals, candles, soap, cream, occult). | Moon Kissed, The Natural Toolbox, Saje Natural Wellness, 7 Chakra Apothecary |
| Voodoo / magic-only shops — explicitly does not want customers ingesting their goods. | Obatala, Island of Salvation Botanica |
| Bookstore / chapel / farmers-market miscategorized as a shop. | Garden Wedding Chapel, Garden Apothecary, Nature's Touch Nursery |
| Already sources from own supply chain (e.g. Costa Rica) with no interest in alternatives. | Anima Mundi Apothecary |
| Already carries own cacao **and** has no consignment accounting. | Apotheca |
| Temporarily or permanently closed on Google Maps. | Eye of the Cat, rosalie Apothecary, Freedom Apothecary |
| By-appointment / single-practitioner space — no foot traffic. | Thealtarhealing, Mysticmoononpark, Witchy Wanderland |

Log these as **Not Appropriate** or **Rejected** with a one-line reason so
future automation doesn't re-surface them.

## 12. Market-fit learnings (the "On Hold" shelf)

These stores are **good fits structurally but blocked by SKU gap** — they
pattern-match across multiple locations (SLO Food Co-op, Lassens SLO, Lori's
Natural Foods, Sunshine Health Foods, Abundance Food Co-op):

- **Two-tier chocolate shelf.** USA natural-foods co-ops stock a "normal"
  tier (~$5–6 per 2 oz) and an "ultra-premium" tier (~$10 per 2.3 oz,
  brands like Celia's). Ceremonial cacao powder does not map to either tier
  cleanly.
- **Gap SKU:** a **~50 g premium dark chocolate bar priced around $10** is
  the missing product needed to unlock this segment. Until it exists, park
  these as **On Hold**, not Rejected.
- **Cacao tea is an underserved bulk opportunity.** Multiple store owners
  (Pilar's Wellness Collective, Secrets of the Garden) have independently
  asked about bulk cacao tea and flagged they cannot find suppliers. This
  may be a larger wedge than ceremonial cacao for some regions.

## 13. Meta-pattern — small vs large store pitch

A consolidated observation from the Herbs of Mexico visit:

> "Smaller mom-and-pop stores where you get to pitch the owners themselves —
> they are more responsive to the story. Large stores — they are receptive
> just by stating your business as an importer and distributor of cacao from
> the Amazon rainforest. The staff simply directs you to the right person."

**Practical implication:** In small shops, lead with the farm story and
mission. In larger shops, lead with a clean elevator-pitch ("importer and
distributor of regenerative cacao from the Brazilian Amazon") and ask for
the buyer by name.

## 14. Narrative pitfalls — the Brasil Kiss lesson

Some audiences push back on the tree-planting framing on ideological grounds
(e.g. Brasil Kiss Coffeebar staff argued indigenous communities don't need
more trees imposed on them). When the audience is politically literate about
the Amazon:

- Lead with the **indigenous-inclusion** aspect of the project, not the raw
  "plant a tree" line.
- Be specific about region (Xingu river, Altamira, Pará) and land status.
- Don't improvise on governmental / political claims; say "I'll send you the
  whitepaper" and move on.

## 15. Bulk / industrial leads — escalate, don't apply this playbook

Occasionally a consignment conversation reveals a **very different opportunity**
— e.g. Third Eye Café (Manager Follow-up) asking to order **286 lbs of
Oscar's cacao paste**. When this happens, **stop** running the consignment
playbook and switch to the industrial workflow (Santos for bean-to-paste
conversion, Omega Services for freight, lab-report translation, full purchase
agreement). Log the switch clearly in the DApp Remark.

## 16. Operational checklist

### Path A (AI email outreach)

- [ ] Hit List row exists with Status = Research and Website populated.
- [ ] Hosts Circles column filled automatically (hourly cron at :50).
- [ ] Email found or contact-form/manual logged (hourly cron at :35).
- [ ] Row promoted to **AI: Warm up prospect** (hourly cron at :20).
- [ ] Warm-up draft created in Gmail with label **`AI/Warm-up`** (daily cron
      at 14:00 UTC).
- [ ] Draft reviewed via `preview_warmup_drafts.py` HTML triage, sent from
      Gmail.
- [ ] Sent mail logged via `sync_email_agent_followup.py`.
- [ ] Prospect reply detected → promoted to **AI: Prospect replied**.
- [ ] Operator routes to **Manager Follow-up** → follow-up draft created
      (label **`AI/Follow-up`**, cadenced at 7+ days).
- [ ] Consignment agreement signed (verbal or written).
- [ ] Status moved to **Partnered**.
- [ ] **Technical onboarding** completed per **`RETAILER_TECHNICAL_ONBOARDING.md`**.

### Path B (Field visits)

- [ ] Hit List row exists with Status = Research or Shortlisted.
- [ ] Google Maps currency verified (not closed).
- [ ] Visit logged as a DApp Remark with decision-maker name + next-contact
      window.
- [ ] Samples (Oscar ceremonial + Paulo cacao tea) dropped and logged.
- [ ] Follow-up email drafted via `STORE_FOLLOW_UP_EMAIL_TEMPLATE.md` within
      the cadence window set by `PARTNER_OUTREACH_PROTOCOL.md`.
- [ ] Consignment agreement signed with the named decision-maker.
- [ ] QR-checkout flow demoed live on first-bag drop.
- [ ] Price guidance shared ($17 cost, $25–$35 retail range).
- [ ] Status moved to **Partnered**; restock cadence set per
      `RESTOCK_RECOMMENDER_ON_THE_FLY.md`.
- [ ] **Technical onboarding** completed per **`RETAILER_TECHNICAL_ONBOARDING.md`**.

## 17. Link index

- Dapp store map: https://dapp.truesight.me/stores_nearby.html
- Hit List credentials: `market_research/HIT_LIST_CREDENTIALS.md`
- DApp Remarks tab: `https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc` → tab `DApp Remarks`
- Gmail review queue (AI/Warm-up): https://mail.google.com/mail/u/0/#label/AI%2FWarm-up
- Gmail review queue (AI/Follow-up): https://mail.google.com/mail/u/0/#label/AI%2FFollow-up
- Farm pages: https://agroverse.shop/farms/oscar-bahia/ · https://agroverse.shop/farms/paulo-la-do-sitio-para/
- Warm-up email tone reference: `TrueSightDAO/go_to_market` → `market_research/templates/warmup_outreach_reference.md`
- GitHub Actions (cron dashboard): https://github.com/TrueSightDAO/go_to_market/actions

## 18. Changelog

- **2026-05-04** — v0.2. Added Path A (automated AI email outreach pipeline):
  state-machine stages, cron schedule, operator review loop, Gmail label
  convention, warm-up email contents, open/click tracking, fast-track from
  circle detection. Renumbered Path B (field visits) sections. Split
  operational checklist into two paths. Added link index entries for Gmail
  labels, warm-up reference, and GitHub Actions.
- **2026-04-21** — v0.1 created. Compiled from 332 human-submitted DApp
  Remarks (17 Partnered, 47 Manager Follow-up, 19 On Hold, 13 Rejected,
  58 Not Appropriate). Synthesized landing patterns, disqualification
  patterns, two-tier shelf + premium-bar SKU gap, small vs large store
  pitch, Brasil Kiss narrative pitfall, Third Eye industrial escalation.
