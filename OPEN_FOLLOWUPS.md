# Open follow-ups (cross-session backlog)

> **This is the ONLY open-followups file.** Do not create variant filenames
> (`OPEN_FOLLOW_UPS.md`, `FOLLOWUPS.md`, `TODO.md`, …) — a duplicate
> `OPEN_FOLLOW_UPS.md` existed 2026-05-31 → 2026-06-06 and split the backlog
> across two files until it was merged back here; that file is now a tombstone
> pointing at this one. Sophia / autopilot agents: file new tooling gaps and
> follow-ups **here**, under `## Pending`, via PR.

Short list of **scoped follow-up tasks** future AI agents (Claude / Cursor /
Codex / Kimi / etc.) and humans can pick up between sessions. The bar is:

- One thing that didn't ship in the original PR but logically belongs after it.
- Small enough to fit in a single session (rough cap: ~60 min of focused work).
- Self-contained — the entry has enough context that someone who didn't write
  the original code can act on it without reverse-engineering history.

This file is **not** a replacement for `CONTEXT_UPDATES.md` (which is the
append-only event log) or for project-specific TODOs that live next to the
code (e.g. `# TODO:` comments, `dapp/UX_CONVENTIONS.md`, repo READMEs, or the
"Q5 parked" pattern inside individual proposal docs like
`PARTNER_VELOCITY_PROPOSAL.md`). It is the place for **cross-repo /
cross-session** items that would otherwise rot in chat transcripts.

## Workflow for agents picking up an entry

1. Read the entry. If the **Blocker** still applies, leave it alone.
2. If you're going to ship it, claim it informally by appending a line to
   `CONTEXT_UPDATES.md` (`<agent-id> | starting OPEN_FOLLOWUPS#…`) so parallel
   sessions don't duplicate work.
3. Open a PR. When merged, **move** the entry to the bottom of this file
   under `## Recently shipped` with the PR link, and append a one-line entry
   to `CONTEXT_UPDATES.md`. Keep the **Pending** list short.
4. If the entry is no longer relevant (priorities shifted, blocker permanent,
   etc.), move it to `## Closed without shipping` with a one-line reason.
   Don't silently delete history.

---

## Pending

### China GTM — cacao tea launch channels (from cosplay dinner session 2026-07-28)
**Filed 2026-07-28. Owner: Gary + Sophia.** Strategic channel map discussed over dinner with Evan / Matheus / Dr. Ye / ChaoShan group. Capture for cross-session use in the China cacao tea go-to-market (PDFs + decks in `pdfs/`).

**Confirmed channels:**
1. **Project-based learning module (Bahia)** — Chinese students based in Bahia, plugged into Evan's Model UN network. Variant of the 2025 discussion with Matheus Reis (Bahia Coop). Education + brand awareness + supply-chain talent pipeline.
2. **Dr. Ye's TCM network (cacao tea distribution + logistics)** — each patient spends ~USD$200 total with her; she amassed **10,000 TikTok/Douyin followers in 6 months** (velocity signal: ~1,667/mo, content machine works). Her channel = distribution + logistics infrastructure for cacao tea. Note: Elizabeth Wong's earlier framing — remove her as KOL, mark KOL as NEED (done in PDFs).

**TBD channels:**
3. **UN office events (Shanghai + Beijing)** — TEDx-style sessions financed by local government, ESG push, cacao sampling. Follow up on who at the UN offices to contact + government ESG program eligibility.
4. **ChaoShan (潮汕) group** — regional network that "monopolizes an entire stock" when supply is good (e.g. they control much of the world's ginseng supply). If they like the cacao supply, they could become a dominant distribution partner. Needs careful engagement — they move as a block.

**Next actions:**
- [ ] Draft supply offtake / exclusivity proposal for Oscar's Farm (40t/yr, 100-yr Criollo, Bahia) — occupy & multiply strategy
- [ ] Confirm Dr. Ye's Douyin account details + follower growth data for launch plan
- [ ] Identify UN office ESG program contact in Shanghai/Beijing
- [ ] Map ChaoShan group entry approach (who introduces us, what they'd want)
- [ ] Update PDFs/decks with these channels once confirmed

**Related files:** `pdfs/Cacao_Beverage_Opportunity_China_Market_TCM_Strategy.pdf`, `pdfs/presentations/SLIDE_MOCKDOWNS.md`, `CACAO_CHINA_PNL_MODEL.md`
