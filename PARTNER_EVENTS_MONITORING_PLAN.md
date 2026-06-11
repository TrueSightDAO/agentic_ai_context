# Partner Events Monitoring — Implementation Plan

**Title:** Agroverse Partner Events Monitoring & Listing

**Date:** 2026-06-12

**Author:** Sophia (TrueSight DAO Autopilot)

**Status:** Plan filed — awaiting GO signal

---

## 1. Vision

A system where Sophia monitors newsletters from Agroverse's retail and ecosystem partners, extracts events (talks, workshops, ceremonies, retreats), and maintains a curated, living events listing on the Agroverse landing page. Anyone in the ecosystem can reference it to see what's happening across the network.

**Gary's framing (2026-06-12):**

> "Now that Sophia has become so good at managing my inbox, it might start making sense for her to monitor it for newsletters from our retail partners. It lists events happening over at their space. Sophia can read through all of them and then maintain a list of Agroverse affiliated events listings. Once this bridge is setup, anyone keen to find out more about what's going on in our ecosystem can just reference Agroverse landing page."

**Gary's extension (2026-06-12):**

> "And I think this would naturally feed into the monthly newsletter that we sent out to folks who left their emails when they bought the QR code. So then it becomes a self-reinforcing loop."

---

## 2. The Self-Reinforcing Loop

This isn't just a linear pipeline — it's a compounding flywheel that connects three existing DAO growth surfaces:

```
┌─────────────────────────────────────────────────────────────────┐
│              PARTNER EVENTS → NEWSLETTER LOOP                    │
│                                                                  │
│  Partner sends newsletter                                         │
│         │                                                        │
│         ▼                                                        │
│  Sophia extracts events                                           │
│         │                                                        │
│         ▼                                                        │
│  Events listed on Agroverse landing page                          │
│         │                                                        │
│         ▼                                                        │
│  Monthly newsletter to QR-code buyers  ◄── Email360 Retention    │
│         │                                                        │
│         ▼                                                        │
│  Buyers see partner events near them                              │
│         │                                                        │
│         ▼                                                        │
│  Buyers attend events at partner spaces                           │
│         │                                                        │
│         ▼                                                        │
│  Attendees scan QR codes on cacao bags  ◄── QR Trace-Back Loop   │
│         │                                                        │
│         ▼                                                        │
│  More trees financed → more subscribers                           │
│         │                                                        │
│         └──────────→ back to monthly newsletter ──────────────────┘
│                                                                  │
│              PARTNER BENEFITS (compounds back)                    │
│                                                                  │
│  Partners get foot traffic from newsletter                        │
│         │                                                        │
│         ▼                                                        │
│  Partners restock cacao more frequently                           │
│         │                                                        │
│         ▼                                                        │
│  Partners refer other venues  ◄── feeds B2B Sales Loop           │
│         │                                                        │
│         ▼                                                        │
│  New partners onboarded → new newsletters → cycle continues      │
└─────────────────────────────────────────────────────────────────┘
```

### How the loops connect to the Growth Model

| Growth Model Loop | How this feeds it |
|-------------------|-------------------|
| **Email360 Retention Loop** 🟧 | Monthly newsletter gets richer content (real events) → higher engagement → more re-purchases |
| **QR Trace-Back Loop** 🟧 | Event attendees scan bags → trees financed → more subscribers → cycle continues |
| **B2B Sales Loop** 🟧 | Partners see foot traffic from events listing → more likely to restock + refer peers |
| **Retail Partner Referral Loop** 🟧 | Satisfied partners refer nearby venues → new partners → new newsletters → more events |

**Key insight:** The events listing is the bridge between the physical partner space and the digital retention surface. It turns a one-way content pipeline into a compounding flywheel.

---

## 3. Architecture

```
Partner Newsletter (email)
        │
        ▼
  admin+sophia@truesight.me  ◄── Partners subscribe this address
        │
        ▼
  Sophia scans inbox (Gmail API)
        │  - Detects newsletters by sender domain
        │  - Extracts events (date, title, location, description, link)
        │  - Deduplicates against existing events list
        ▼
  AGROVERSE_AFFILIATED_EVENTS.md  ◄── Canonical events file in agentic_ai_context
        │
        ▼
  Events rendered on Agroverse landing page
        │  - Filterable by date / location / partner
        │  - Each event links back to partner's original listing
        ▼
  Community discovers & attends
        │
        ▼
  (feeds back into monthly newsletter → loop)
```

---

## 4. Phased Roadmap

### Phase 1 — Foundation (MVP)

**Goal:** One partner (SF Zen Center) → one events file → manual review → landing page.

| Step | What | How | Est. time |
|------|------|-----|-----------|
| 1.1 | **Create canonical events file** | `AGROVERSE_AFFILIATED_EVENTS.md` in `agentic_ai_context` with schema (date, title, location, partner, description, url, status) | 15 min |
| 1.2 | **Seed with SFZC events** | Extract all events from the June 11 PDF into the file | 20 min |
| 1.3 | **Set up inbox monitoring** | When `admin+sophia@truesight.me` receives a newsletter from a known partner domain, Sophia detects it and extracts events | Built into autopilot |
| 1.4 | **Build events extraction prompt** | Sophia reads newsletter email body, extracts structured events, flags for review | 30 min |
| 1.5 | **Landing page section** | Add an "Ecosystem Events" section to `agroverse_shop_beta` (or `truesight_me_beta`) that reads from the events file | 1–2 h |
| 1.6 | **Review & publish** | Gary reviews the first batch, approves, events go live | Ongoing |

**Phase 1 deliverable:** A static events section on the Agroverse site showing SF Zen Center's upcoming programs, updated when new newsletters arrive.

---

### Phase 2 — Multi-Partner Expansion

**Goal:** Each partner subscribes `admin+sophia@truesight.me` to their newsletter → events auto-extracted.

| Step | What | How |
|------|------|-----|
| 2.1 | **Partner newsletter registry** | A small JSON or sheet mapping partner → newsletter sender email. Sophia checks this when scanning inbox. |
| 2.2 | **Onboard partners** | For each retail partner that sends a newsletter, Gary or Sophia subscribes `admin+sophia@truesight.me` and adds them to the registry. |
| 2.3 | **Multi-sender detection** | Sophia scans inbox for ALL registered sender domains, not just one. |
| 2.4 | **Events JSON** | Convert the markdown file to a structured JSON (`ecosystem-events.json`) that the landing page can fetch dynamically. |
| 2.5 | **Filter/sort UI** | Add date filters, partner filter, location filter to the events section. |

**Phase 2 deliverable:** Events from 3–5 partners auto-populated on the site, filterable.

---

### Phase 3 — Automation & Discovery

**Goal:** Zero-touch events pipeline — newsletters arrive, events appear, stale events auto-archive.

| Step | What |
|------|------|
| 3.1 | **Auto-detect new newsletter senders** | Sophia flags unknown newsletter-style emails from retail partners and suggests adding them to the registry. |
| 3.2 | **Auto-archive past events** | Events with dates in the past are moved to a "Past Events" section or archived. |
| 3.3 | **Calendar export** | Generate an iCal feed so community members can subscribe in their calendar app. |
| 3.4 | **Partner dashboard** | Partners can see how many people viewed their events from the Agroverse listing. |

---

## 5. Events Schema

Each event entry follows this structure:

```yaml
- id: sfzc-2026-07-25-radical-kindness
  title: "Radical Kindness: The Metta Sutta as a Way of Living"
  partner: "San Francisco Zen Center"
  partner_slug: san-francisco-zen-center
  date_start: "2026-07-25"
  date_end: "2026-08-15"
  time: "8:30–10:00 am PT / 5:30–7:00 pm CEST"
  location: "Online"
  location_type: online
  description: >
    The Metta Sutta, or Loving Kindness Sutta, is a regular part of the services
    at San Francisco Zen Center's temples. Its message is not sentimental but
    radical: kindness toward all beings!
  url: "https://sfzc.org/..."
  image: (optional)
  status: upcoming  # upcoming | ongoing | past
  source: newsletter-2026-06-11
  added_at: "2026-06-12"
```

---

## 6. Partner Onboarding Checklist

When a new partner wants their events listed:

1. [ ] Partner subscribes `admin+sophia@truesight.me` to their newsletter (or Gary does it)
2. [ ] Sophia detects the first newsletter arrival
3. [ ] Sophia adds partner to the registry (`PARTNER_EVENTS_REGISTRY.md`)
4. [ ] Sophia extracts events from the first newsletter and presents them for review
5. [ ] Gary approves the first batch
6. [ ] Events go live on the landing page
7. [ ] Ongoing: Sophia monitors future newsletters from this sender

---

## 7. First Seed — SF Zen Center Events (from June 11 newsletter)

### Upcoming

| Date | Event | Location |
|------|-------|----------|
| Jun 12 | Sacred Rhythms: Butoh w/ Kana Kitty | City Center |
| Jun 13 | GRIP: Peace & Accountability | City Center |
| Jun 13 | All Day Sitting w/ Zoketsu Norman Fischer | Green Gulch |
| Jun 13 | Mandala: Butoh w/ Kana Kitty | City Center |
| Jun 14 | Sunday Tea Gathering w/ Meiya Wender | Green Gulch |
| Jun 14 | Prism: Butoh Meditation Workshop | City Center |
| Jun 16–21 | Step Into Your Life Retreat w/ Marc Lesser | Tassajara |
| Jun 19 | Juneteenth Holiday | City Center |
| Jun 20 | Summer Solstice Ceremony | City Center |
| Jun 20 | Saturday One-Day Sitting w/ Guo Gu | Green Gulch |
| Jun 20–Nov 21 | Dancing with Chronic Illness & Pain (monthly) | Online |
| Jun 21 | Living Into the Appropriate Response | City Center |
| Jul 19 | In the Rhythm of the Heart w/ Rev Gendo Lucy Xiao | Green Gulch |
| Jul 25–Aug 15 | **Radical Kindness: The Metta Sutta** (4 Saturdays) | Online |
| Jul 30–Aug 2 | Joyful Ease, Your Own True Body | Green Gulch |

### Ongoing / Recurring

| Day | Event | Location |
|-----|-------|----------|
| Thu | Thursday Drop-in Practice Session | Online |
| Thu | Trans Sangha, Sangha Night | City Center |
| Thu | Informal Zazen & Specialty Tea | City Center |
| Fri | Meditation in Recovery | Online |
| Sat | Saturday Sangha | City Center |
| Sat | Queer Dharma Group | Online |
| Mon | Meditation in Recovery | City Center/Online |
| Tue | Young Urban Zen | City Center |

---

## 8. Open Questions

1. **Where should the events live on the site?** Options:
   - A new `/events` page on `agroverse.shop` (feels natural — cacao + community)
   - A section on `truesight.me` (the DAO hub)
   - Both (cross-linked)
   - Gary's preference: "Agroverse landing page"

2. **Should events be manually reviewed before going live?**
   - Phase 1: Yes — Gary reviews first batch
   - Phase 3: Maybe — auto-publish with a "suggested" flag

3. **What counts as an "Agroverse-affiliated" event?**
   - Events hosted by retail partners who carry Agroverse cacao
   - Events hosted by ecosystem partners (SFZC, capoeira, BE, Vipassana)
   - Events where Agroverse is participating / pouring
   - Events that align with the mission (compassion, rainforest, community)

4. **How do we handle recurring events?**
   - Weekly/monthly events (like Thursday Drop-in) could be listed as "ongoing" with a link to the partner's calendar

5. **Privacy — should events link to the partner's original listing?**
   - Yes — always link back. We're a directory, not a ticket seller.

---

## 9. Success Metrics

| Metric | Target (Phase 1) | Target (Phase 3) |
|--------|------------------|------------------|
| Partners monitored | 1 (SFZC) | 10+ |
| Events listed | 15+ | 50+ live at any time |
| Newsletter detection latency | < 1 hour of arrival | < 15 min |
| False positive rate (non-events flagged) | < 20% | < 5% |
| Community clicks on events | N/A (new surface) | Measurable |

---

## 10. Files to Create

| File | Location | Purpose |
|------|----------|---------|
| `AGROVERSE_AFFILIATED_EVENTS.md` | `agentic_ai_context/` | Canonical events list (markdown, human-readable) |
| `PARTNER_EVENTS_REGISTRY.md` | `agentic_ai_context/` | Registry of partner → newsletter sender mapping |
| `ecosystem-events.json` | `agroverse-inventory/` or `truesight_me_beta/_site/` | Machine-readable events feed for the landing page |

---

## 11. Execution Checklist

### Phase 1 — Foundation

- [ ] **1.1** Create `AGROVERSE_AFFILIATED_EVENTS.md` with schema + seed data
- [ ] **1.2** Create `PARTNER_EVENTS_REGISTRY.md` with SFZC entry
- [ ] **1.3** Build newsletter detection into autopilot's inbox monitoring
- [ ] **1.4** Build events extraction prompt
- [ ] **1.5** Add events section to Agroverse landing page (beta first)
- [ ] **1.6** Gary reviews first batch, approves, goes live

### Phase 2 — Multi-Partner

- [ ] **2.1** Subscribe `admin+sophia@truesight.me` to 3–5 partner newsletters
- [ ] **2.2** Build `ecosystem-events.json` feed
- [ ] **2.3** Add filter/sort UI to events page
- [ ] **2.4** Verify auto-detection works for multiple senders

### Phase 3 — Automation

- [ ] **3.1** Auto-archive past events
- [ ] **3.2** Auto-detect new newsletter senders
- [ ] **3.3** Calendar export (iCal)
- [ ] **3.4** Partner dashboard (event view counts)

---

*Filed 2026-06-12 by Sophia. Awaiting GO signal from Gary to begin Phase 1.*
