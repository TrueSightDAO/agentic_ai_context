# Friends of the Rainforest — Landing Page & QR Placard

**Title:** Friends of the Rainforest — Event Sampling Landing Page

**Date:** 2026-06-12

**Author:** Sophia (TrueSight DAO Autopilot)

**Status:** Plan filed — awaiting GO signal to build

---

## 1. Vision

When someone tastes Agroverse ceremonial cacao or cacao tea at an event (Dual Tech Summit, SF Zen Center, partner spaces), they scan a QR code on the placard and land on a beautiful, warm page at **agroverse.shop/friends-of-the-rainforest**. The page:

- Welcomes them as a "Friend of the Rainforest"
- Tells the story of what they just drank — the farmer, the forest, the regenerative cycle
- Captures their email to stay connected
- Offers a way to bring the experience home (buy the same cacao)

This feeds directly into the Partner Events → Newsletter loop: emails captured here enter the monthly newsletter, which includes partner events, which drives more sampling, which captures more emails.

---

## 2. The Loop (how it connects)

```
Event attendee tastes cacao
        │
        ▼
  Scans QR on placard
        │
        ▼
  Lands on agroverse.shop/friends-of-the-rainforest
        │
        ├──→ Leaves email → enters Email360 newsletter
        │                      → newsletter includes partner events
        │                      → attends next event → scans again → loop
        │
        └──→ Buys cacao → scans QR on bag
                           → tree financed
                           → more subscribers
                           → loop
```

---

## 3. Implementation Plan

### Phase 1 — Landing Page (agroverse.shop/friends-of-the-rainforest)

| Step | What | Details |
|------|------|---------|
| 1.1 | Create page directory | `friends-of-the-rainforest/index.html` in `agroverse_shop_beta` |
| 1.2 | Build hero section | Warm welcome: "You just became a Friend of the Rainforest" with rainforest/cacao imagery |
| 1.3 | Story section | Short narrative about Oscar's ceremonial cacao (Bahia) and Paulo's cacao tea (Pará) — the farmers, the forest, one bag = one tree |
| 1.4 | Email capture form | Simple signup: name + email → submits to Google Sheet / Email360 list |
| 1.5 | CTA to shop | Links to ceremonial cacao and cacao tea product pages |
| 1.6 | Mobile-responsive | Must look great on a phone (most QR scans are mobile) |
| 1.7 | Analytics | GA4 + Facebook Pixel tracking on the page |
| 1.8 | Deploy to beta | Push to `agroverse_shop_beta`, verify at beta.agroverse.shop/friends-of-the-rainforest |

### Phase 2 — QR Code & Placard

| Step | What | Details |
|------|------|---------|
| 2.1 | Generate QR code | Following the DTS pattern: `DTS_FR_20260613_1` (Dual Tech Summit, Friends Rainforest, date, batch) |
| 2.2 | Design placard | Small card/tent card with QR code + CTA text |
| 2.3 | Print | Print for tomorrow's event (June 13) |

### Phase 3 — Newsletter Integration

| Step | What |
|------|------|
| 3.1 | Wire email captures into the monthly newsletter list |
| 3.2 | First newsletter includes "Welcome Friends of the Rainforest" section |

---

## 4. Page Content Draft

### Hero

> **You just became a Friend of the Rainforest.**
>
> What you drank today came from deep in the Amazon — regenerative ceremonial cacao grown by Oscar in Bahia, and cacao tea crafted by Paulo in Pará. Every bag of this cacao plants a tree in the forest that made it.

### The Story

> **Oscar's Ceremonial Cacao** — Grown in the shade of the Atlantic Forest in Bahia, Brazil. Oscar has been farming this land for generations, using regenerative practices that restore the soil and protect the watershed. One sip connects you to his family, his land, and the trees that make it possible.
>
> **Paulo's Cacao Tea** — From the heart of Pará, Paulo harvests wild cacao from the forest floor. His tea is a celebration of the Amazon's biodiversity — each cup a reminder that the forest is not just a resource to extract, but a partner to protect.

### The Invitation

> **Stay connected to the forest.**
>
> Leave your email and we'll send you stories from the farms, updates on the trees you help plant, and invitations to events like this one.
>
> [Name] [Email] [Become a Friend →]

### The CTA

> **Bring the taste home.**
>
> [Shop Ceremonial Cacao →] [Shop Cacao Tea →]

---

## 5. QR Code Spec

| Field | Value |
|-------|-------|
| QR ID | `DTS_FR_20260613_1` |
| Pattern | `{EVENT}_{PAGE}_{DATE}_{BATCH}` |
| Event | DTS = Dual Tech Summit |
| Page | FR = Friends of the Rainforest |
| Date | 20260613 = June 13, 2026 |
| Batch | 1 = first batch |
| Destination | `https://agroverse.shop/friends-of-the-rainforest` |

---

## 6. Placard Design

A small tent card (approx 5" x 7" folded) placed next to the cacao flasks.

### Front (facing attendees)

```
┌──────────────────────────────┐
│                              │
│   Friend of the Rainforest   │
│                              │
│   [QR CODE]                  │
│                              │
│   Scan to meet the farmer    │
│   who grew what you drank    │
│                              │
│   One sip plants a tree.     │
│                              │
└──────────────────────────────┘
```

### Back (optional — facing the pourer)

```
┌──────────────────────────────┐
│                              │
│   Ceremonial Cacao           │
│   Oscar's Farm, Bahia        │
│                              │
│   Cacao Tea                  │
│   Paulo's Farm, Pará         │
│                              │
│   Each bag plants a tree     │
│   in the Amazon rainforest.  │
│                              │
└──────────────────────────────┘
```

---

## 7. UAT Checklist

### Landing Page

- [ ] U1. Page loads at `beta.agroverse.shop/friends-of-the-rainforest`
- [ ] U2. Hero text renders correctly on desktop
- [ ] U3. Hero text renders correctly on mobile (375px width)
- [ ] U4. Story section displays both cacao stories
- [ ] U5. Email capture form accepts name + email
- [ ] U6. Email submission writes to the correct Google Sheet / list
- [ ] U7. Success message shows after email submission
- [ ] U8. CTA buttons link to correct product pages
- [ ] U9. All images load (no broken paths)
- [ ] U10. GA4 pageview event fires
- [ ] U11. Facebook Pixel PageView event fires
- [ ] U12. Page is mobile-responsive (no horizontal scroll, readable text)
- [ ] U13. Page loads in < 3 seconds on 4G

### QR Code

- [ ] U14. QR code scans correctly from phone camera
- [ ] U15. QR code lands on the correct URL
- [ ] U16. QR code is high enough resolution for print (300 DPI)

### Placard

- [ ] U17. Placard text is readable from 3 feet away
- [ ] U18. QR code is large enough to scan (min 2cm x 2cm)
- [ ] U19. Placard stands stably next to the flasks

---

## 8. Execution Checklist

### Pre-Build

- [ ] Gary approves the landing page content draft
- [ ] Gary confirms the QR destination URL
- [ ] Gary confirms the CTA text on the placard

### Build (Phase 1)

- [ ] Create `friends-of-the-rainforest/index.html` on `agroverse_shop_beta`
- [ ] Build hero section with warm welcome copy
- [ ] Build story section (Oscar + Paulo)
- [ ] Build email capture form (name + email → Google Sheet)
- [ ] Build CTA section (links to product pages)
- [ ] Add GA4 + Facebook Pixel tracking
- [ ] Test mobile responsiveness
- [ ] Push to `agroverse_shop_beta`
- [ ] Verify at `beta.agroverse.shop/friends-of-the-rainforest`

### Build (Phase 2)

- [ ] Generate QR code `DTS_FR_20260613_1` pointing to the page
- [ ] Design placard (can be simple print-on-paper tent card)
- [ ] Print placard for tomorrow's event

### Post-Launch

- [ ] Gary reviews the beta page
- [ ] Gary approves promotion to prod
- [ ] Sync `agroverse_shop_beta` → `agroverse_shop_prod`
- [ ] Monitor email signups from the event
- [ ] First email goes out to new Friends of the Rainforest

---

## 9. Files to Create

| File | Location | Purpose |
|------|----------|---------|
| `friends-of-the-rainforest/index.html` | `agroverse_shop_beta/` | The landing page |
| QR code image | `agroverse_shop_beta/assets/images/qr/` | QR code for the placard |

---

*Filed 2026-06-12 by Sophia. Awaiting GO signal from Gary to begin Phase 1 build.*
