# Outreach qualitative improvement loop — how to continuously refine the pipeline

**Audience:** Future AI agents (Claude, Cursor, etc.) who want to improve
the outreach pipeline based on qualitative data from interactions.

**Principle:** Every reply, every field visit remark, every "yes" and every
"no" contains signal. This doc tells you how to extract that signal and
feed it back into the system so the next batch of drafts is better than the last.

---

## 1. Data sources (where qualitative signal lives)

| Source | Location | What it contains |
|--------|----------|-----------------|
| **DApp Remarks** | Hit List spreadsheet → tab `DApp Remarks` | Field visit notes, sample drops, store-owner conversations, automated pipeline events. Human-submitted rows have RSA-key `Submitted By`. |
| **Email Agent Follow Up** | Same spreadsheet → tab `Email Agent Follow Up` | Log of sent warm-up/warmup/followup emails. `body_plain` column has full sent text. |
| **Email Agent Drafts** | Same spreadsheet → tab `Email Agent Drafts` | Draft queue. `Open`/`Click through` columns have engagement data. |
| **Email Agent Training Data** | Same spreadsheet → tab `Email Agent Training Data` | Full Gmail threads for Partnered stores (sent + received). |
| **Hit List Notes** | Hit List tab → col `Notes` | Discovery context, place_id, operator notes. |
| **Hit List Sales Process Notes** | Hit List tab → col `Sales Process Notes` | Append-only log of status changes and DApp Remark mirrors. |
| **Google Sheet ID** | `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc` | |
| **Credentials** | `market_research/google_credentials.json` (service account) + `credentials/gmail/token.json` (OAuth) | |

### Quick queries

```bash
# Field visit remarks (human-submitted)
cd market_research && source venv/bin/activate
python3 -c "
import gspread; gc = gspread.service_account(filename='google_credentials.json')
sheet = gc.open_by_key('1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc')
dr = sheet.worksheet('DApp Remarks')
data = dr.get_all_records()
# Human-submitted = Submitted By is an RSA key (very long string)
human = [r for r in data if len(r.get('Submitted By','')) > 100]
for r in human:
    print(f'[{r.get(\"Shop Name\")}] [{r.get(\"Status\")}] {r.get(\"Remarks\",\"\")[:200]}')
"

# Count reply patterns from sent mail
python3 -c "
import gspread; gc = gspread.service_account(filename='google_credentials.json')
sheet = gc.open_by_key('1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc')
fu = sheet.worksheet('Email Agent Follow Up')
data = fu.get_all_records()
# Show sent mail with status counts
from collections import Counter
c = Counter(r.get('status') for r in data)
for k,v in c.most_common(): print(f'{k}: {v}')
"
```

---

## 2. What to look for — qualitative signal types

### A. New objection patterns
When a prospect replies with a reason for saying "no" that isn't in the
objection table, extract it and add a rebuttal.

**How to detect:** Read DApp Remarks from `warmup_reply_promotion` and
`followup_reply_detected`, or scan the Email Agent Training Data for
Partnered stores.

**Where to update:**
1. `agentic_ai_context/RETAILER_ONBOARDING_PLAYBOOK.md` §9 — objection table
2. `market_research/templates/field_insights_outreach.md` — objection table
3. `market_research/scripts/suggest_warmup_prospect_drafts.py` — `grok_reply_system_prompt()`

### B. New conversion patterns (what lands)
When a store converts to Partnered, read the DApp Remarks for that store
and identify what specific moment, phrase, or feature sealed the "yes."

**How to detect:** Cross-reference Partnered stores' DApp Remarks.

**Where to update:**
1. `RETAILER_ONBOARDING_PLAYBOOK.md` §8 — "What actually lands"
2. `field_insights_outreach.md` — "Emotional hooks that convert"
3. Warm-up Grok system prompt `grok_warmup_system_prompt()` — if it's
   a pattern the draft should use proactively

### C. Taste profile refinements
When you gather more specific taste descriptors from cacao circles,
tastings, or farmer conversations.

**Where to update:**
`market_research/templates/farm_taste_profiles.md` — farm entries

### D. Reply-rate patterns
Analyze which subject lines, which farm mentions, or which CTAs correlate
with higher reply rates.

**How to detect:** Cross-reference Email Agent Drafts (has body) with
Email Agent Follow Up (has status). Open/click data is in Drafts cols N/O.

**Where to update:**
- Warm-up Grok system prompt rules
- Warm-up fallback template (`warmup_body_template()`)

### E. Auto-reply false positives
If `is_auto_reply()` in the warmup script incorrectly filters a real reply,
or misses an auto-reply pattern.

**Where to update:**
`market_research/scripts/suggest_warmup_prospect_drafts.py` — `_AUTO_REPLY_PATTERNS`

---

## 3. Files you should update (summary table)

| File | Path | What it controls |
|------|------|-----------------|
| Farm taste profiles | `market_research/templates/farm_taste_profiles.md` | Grok system prompts (all three: warmup, reply, follow-up) |
| Field insights | `market_research/templates/field_insights_outreach.md` | Grok system prompts (all three) |
| Warmup tone reference | `market_research/templates/warmup_outreach_reference.md` | Warm-up Grok prompt (style only) |
| Warm-up system prompt | `market_research/scripts/suggest_warmup_prospect_drafts.py` → `grok_warmup_system_prompt()` | Warm-up draft generation |
| Reply system prompt | `market_research/scripts/suggest_warmup_prospect_drafts.py` → `grok_reply_system_prompt()` | Reply draft generation |
| Follow-up system prompt | `market_research/scripts/suggest_manager_followup_drafts.py` → `grok_system_prompt()` | Follow-up draft generation |
| Warm-up fallback template | `suggest_warmup_prospect_drafts.py` → `warmup_body_template()` | Non-Grok warm-up drafts |
| Reply fallback template | `suggest_warmup_prospect_drafts.py` → lines ~767 + ~779 | Non-Grok reply drafts |
| Follow-up fallback template | `suggest_manager_followup_drafts.py` → `draft_body_template()` | Non-Grok follow-up drafts |
| Auto-reply patterns | `suggest_warmup_prospect_drafts.py` → `_AUTO_REPLY_PATTERNS` | Reply filtering |
| Sales playbook | `agentic_ai_context/RETAILER_ONBOARDING_PLAYBOOK.md` | Human operator reference |
| State machine doc | `agentic_ai_context/HIT_LIST_STATE_MACHINE.md` | Pipeline state reference |

---

## 4. Shipping the change (PR flow)

All outreach pipeline code lives in `TrueSightDAO/go_to_market` (cloned as
`market_research/`). Agent docs live in `TrueSightDAO/agentic_ai_context`.

```
1. Make edits to the files above
2. Verify compilation: python3 -c "import py_compile; py_compile.compile('scripts/<file>.py', doraise=True)"
3. Branch off main: git checkout -b feature/outreach-<improvement-description>
4. Commit + push + open PR
5. Merge via gh pr merge --squash --delete-branch
6. Report DAO contribution via dao_client
```

Both repos use HTTPS remotes (`gh` auth). Never commit `.env` or token files.

---

## 5. Improvement cadence

- **After every batch of warm-up replies** (the 5 we saw on 2026-05-03): scan
  the reply bodies in DApp Remarks for new objection patterns. Add to table.
- **After every new Partnered store**: read their full DApp Remark history,
  extract what sealed the deal, add to "what lands" section.
- **Monthly**: re-read all Partnered store Email Agent Training Data threads.
  Look for language patterns the Grok drafts aren't using.
- **When a draft type feels stale**: re-read this doc's section 2, pick one
  signal type (A-E), run the query, update the relevant files.

The goal is for every qualitative interaction to make the next one better.
