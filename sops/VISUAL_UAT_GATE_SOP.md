# SOP — Standing in for a "governor visual confirm" gate

**Owner:** Envoy (nelanco-claude) / Sophia Truesight
**Scope:** a plan or ticket has an explicit human-only acceptance item ("Gary visual
confirm," "pixels not [checked]," "human gate") blocking close-out. This SOP covers
doing that check yourself with a real browser, under explicit governor authorization
— not a substitute for authorization, a substitute for the human's eyes once
authorized.

**Status:** derived from one real case, KAN-27 (Fazenda Santa Ana farm page + SunMint
plot cross-link), 2026-11-26.

---

## 1. When this applies

A plan's acceptance checklist distinguishes *machine-checkable* (DOM exists, link
returns 200, no console errors) from *human-checkable* (does it actually look right).
The second category tends to sit "⏳ PENDING — human gate" indefinitely, because
nobody schedules five minutes to look at a page that already "passed" every
automated check.

**Do not treat an HTTP 200 / DOM-present check as satisfying a visual gate.** They
are different claims. "The gate rendered before" (KAN-27, earlier session) found
zero broken `<img>` elements and zero console errors — and still missed nothing,
because the actual defect category (iframe content, not `<img>` tags) was never in
scope of that check.

**Get explicit governor authorization before closing a ticket on your own visual
judgment.** This SOP is for *performing* the check; the governor's "check it
yourself, give go-ahead" instruction is what authorizes *acting* on the result.

## 2. Procedure

1. **Render with a real browser, not curl.** Playwright + a `chromium-*` build under
   `~/.cache/ms-playwright/` is already on this box (no `playwright install` needed —
   point `executable_path` at the existing `chrome` binary if the default launch
   can't find `chrome_headless_shell`).
2. **Screenshot full-page first, as a cheap first pass** — but do not trust a
   full-page capture's rendering of iframes (YouTube embeds, maps, anything that
   lazy-loads or needs a settle delay). See §3.
3. **For every element that looks wrong, re-verify with a targeted, settled
   screenshot**: scroll directly to that element's position, wait 2–3s, screenshot
   just the viewport. This is the single most important step in this SOP.
4. **Check the acceptance list item-by-item**, not just "does it look okay" — e.g.
   KAN-27's criteria were (a) gallery renders, (b) map renders, (c) cross-links work.
   Verify each independently (gallery: distinct correct thumbnails per tile; map:
   Leaflet/OSM tiles + marker present; cross-link: follow it and render the
   destination too, don't just check `href` exists).
5. **Follow cross-links to their destination and verify those too.** A link that
   exists is not a link that works. KAN-27's SunMint cross-link needed its own
   render+screenshot pass on `truesight.me/sunmint.html?plot=FSA-P1` to confirm the
   plot boundary popup actually shows the right farm.
6. **Report what you found, including false positives you ruled out.** If a
   full-page capture showed a defect that a targeted re-check disproved, say so
   explicitly in the close-out comment — it's evidence the check was real, not
   skipped.

## 3. The specific trap found in this session: full-page screenshots lie about iframes

**Symptom:** a full-page, stitched Playwright screenshot shows YouTube (or other
iframe) embeds as solid black boxes, even though the rest of the page (plain
`<img>` content) renders correctly in the same capture.

**Root cause:** full-page screenshot stitching scrolls the page in segments and
composites them. An iframe that was off-screen a moment ago may not have finished
painting its poster/thumbnail by the time that segment is captured — plain `<img>`
elements don't have this problem because the browser already decoded and cached
them. `page.eval_on_selector_all('img', ...)` reporting zero broken images while the
screenshot shows black boxes is the tell: the defect isn't in the DOM, it's in the
screenshot capture's timing.

**Fix / verification:** scroll directly to the iframe's position, `wait_for_timeout`
2000–3000ms, then screenshot *that viewport only* (not full-page). If it renders
correctly there, the full-page black box was an artifact — **do not report it as a
site defect.** If it's still black after a direct, settled, targeted screenshot,
that's a real finding.

**Do not conclude a site defect from a full-page screenshot alone when iframes are
involved.** This is the opposite failure mode from `UI_UX_REVIEW_SOP.md` §4.3 (a 404
page passing every naive check) — here a *working* page can look broken under a
naive check. Both directions require the same discipline: verify before reporting.

## 4. Relationship to `UI_UX_REVIEW_SOP.md`

That SOP is for adversarial review of a mockup someone *hands you* (client, vendor,
another agent) — assume it's broken until measured. This SOP is for confirming a
page *your own side already built and believes is correct* — the posture is
verification, not adversarial review, but the tooling (Playwright, targeted
screenshots, "measure before judging") is the same family of technique.

---

## Change log

| Date | Change |
|---|---|
| 2026-11-26 | Initial SOP, derived from KAN-27 visual UAT (farm page gallery false-positive + SunMint cross-link verification). |
