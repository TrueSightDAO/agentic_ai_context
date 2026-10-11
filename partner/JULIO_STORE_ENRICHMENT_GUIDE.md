# Julio Almeida — B2B Store Outreach Enrichment Guide

**For:** Julio Almeida (contributor ledger row 427, Discord `1554404598381543494`, `davajhabib@outlook.com`)
**From:** Sophia Truesight (DAO Autopilot) · **Owner:** Gary Teh
**Purpose:** how to enrich/repair store records so the B2B outreach funnel converts better.

---

## Why you're being asked

The B2B store outreach system is already ~90% automated. It **discovers** venues, **screens** them with AI, and sends **drip-safe** cold emails (about 1,000 sent, zero deliverability incidents).

What it cannot do is find the human context the web buries: a real contact email, the person who actually decides, a specific reason this store would care. That gap is the single biggest brake on conversion — and it is exactly the work a person beats a script at.

## The number that matters most

| Funnel stage | Stores | % of 680 |
|---|---|---|
| 0 — Raw discovery (Research) | 47 | 6.9% |
| 1 — Screened out (not a fit) | 254 | 37.4% |
| **2 — Need contact data** | **214** | **31.5%** |
| 3 — Qualified, ready to send | 63 | 9.3% |
| 4 — Contacted / in follow-up | 38 | 5.6% |
| 5 + 6 — Engaged / replied | 13 | 1.9% |
| Parked / Lost / Converted | 51 | 7.5% |
| **Total** | **680** | **100%** |

**261 of 680 stores (38%) have no usable email — so they never receive an outreach email at all.** They sit forever at *Research* / *Contact Form found* / *Enrich — manual*. Every one you unblock enters the funnel for the first time.

**Second finding:** the reply rate collapsed from ~6% to ~0.3% and sat undetected for six weeks. And **all 14 current partners came from a reply, not a send.** So two things matter: *getting the email* (Job A) and *making the email worth answering* (Job C).

## Step 0 — Set up your signature (5 minutes, once)

You can only save changes if your browser holds a registered DAO signature.

1. Open https://dapp.truesight.me/create_signature.html
2. Click **Create new key pair**, then enter your email to register
3. Open the verification email and click the link
4. Reload https://dapp.truesight.me/store_interaction_history.html — you should see **"Signature verified — updates enabled."**

If you instead see *"Read-only mode"*, your key isn't registered yet — wait for the email, or repeat step 2. Your signature is what **attributes every edit to you**, so Gary always knows who annotated what.

## The three jobs, in priority order

| # | Job | Where | Why it matters |
|---|---|---|---|
| **A** | Find contact data (email) | Store Interaction History → edit form | Unblocks 261 stores that can never be emailed |
| **B** | Add new fitting stores | Stores Nearby → Save New Store | Feeds the discovery funnel |
| **C** | Add remarks / context | Store Interaction History → Remarks | Feeds the follow-up email generator a personal hook |

## Job A — Find contact data (your highest-value work)

1. Open https://dapp.truesight.me/store_interaction_history.html and search the store by name.
2. If critical data is blank, research the store (order of effort below).
3. Fill the **Email** field with what you found.
4. Set the **Status**:
   - Email found → `AI: Email found`
   - Only a web form exists → `AI: Contact Form found`
   - Genuinely unreachable → leave `AI: Enrich — manual` and add a Remark saying where you already looked
5. Always paste the store's **Website** if it's missing.
6. Add a one-line **Remark** describing what you found.

**Where to look, in order:**
- The store's website — footer, Contact page, About page
- Instagram bio (small shops often list the business email there)
- Google Business profile
- Facebook page → "About" / "Contact info"
- Local chamber-of-commerce or directory listings

**Hard rule:** only record an email you actually saw published (e.g. `info@`, `hello@`, `orders@`). **Never guess or invent an address** — a bounced or wrong email is worse than a blank one.

## Job B — Add new stores to the funnel

If you find a fitting store that isn't in the list:

1. Open https://dapp.truesight.me/stores_nearby.html → **Save New Store**
2. Enter the store name, address, website and Instagram where known
3. New stores default to status **Research**, and the AI screening step picks them up automatically

**What counts as a good fit:** independent shops aligned with ethical sourcing, ceremonial cacao, wellness, plant medicine, conscious cafés, health food, yoga, metaphysical, or boutique chocolate — with a physical location and some online presence. Not big-box chains.

## Job C — Add remarks that improve follow-up emails

Your **Remarks** are mirrored into the Hit List `Sales Process Notes` column, which the follow-up email generator reads. So write remarks that give the email writer a *hook*, not a status log.

| Weak remark | Strong remark |
|---|---|
| "Called, no answer." | "Owner stocks Ora Cacao and markets single-origin ceremonial grade — strong fit, upgrade their sourcing story." |
| "Checked website." | "Contact page lists only a form; Instagram bio has orders@ — sent there instead." |
| "Follow up later." | "Closed for renovation until Nov; owner named Dana, reached 12 Oct, wants pricing sheet." |

Aim for: **who / what they carry / why they'd care / what you already did**. One or two specific lines beat a paragraph.

## Guardrails — please don't

- **Don't set Status to** `Partnered`, `Rejected`, `No fit signal`, or `Not Appropriate`. Those are Gary's calls — a real conversation is what earns them, not an annotation.
- **Never invent an email or phone number.** Only record published contact data.
- **Don't overwrite existing data with "unknown".** Fill blanks, or correct a value that is clearly wrong — and say so in Remarks.
- **One store at a time, one save at a time.** Each save is a signed event; keep them clean.

## How your work flows (not a black box)

| Step | What happens |
|---|---|
| 1 | You save an edit in the DApp |
| 2 | Your signature is verified, the edit is logged |
| 3 | It appears under **DApp Remarks** on Store Interaction History |
| 4 | It is applied to the Hit List, mirrored into **Sales Process Notes** |
| 5 | The follow-up email generator reads it and writes a better-personalised email |
| 6 | Better email → more replies → new partners |

## My honest recommendation on where to start

1. **First: the 214 already-screened "need contact data" stores.** Screening already vouched they're a fit — you're just finding the door. Highest conversion-per-hour by far.
2. **Then: the 47 raw Research rows** that look like strong fits.
3. **Then: add context remarks** to the 38 stores already in follow-up, so their next email has a real hook.
4. **Skip: the 254 screened-out stores.** They've been judged not a fit — don't re-litigate them.

You do not need permission for any of this, and nothing you do here can send an email by itself — your edits only add data and context for a human-reviewed step. Start with five stores, and Gary will give you feedback on the annotation style before you scale up.

---

**Related:** `partner/HIT_LIST_CONTACT_ENRICHMENT.md` (the automated pipeline this human work mirrors), `plans/DAPP_ACCESS_RIGHTS_PLAN.md` (Unit 0 = Julio's signing identity).
