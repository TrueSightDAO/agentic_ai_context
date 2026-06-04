# Aora Experience — execution roadmap

**Owner:** Gary Teh · **Started:** 2026-06-04 · **Status:** ACTIVE

Aora is the front-of-house name (China launch with Mr. Cao's GO/Nucleus network); the
engine is Agroverse Lineage (`truesight.me/lineage.html` — experiential-learning
credentialing). Online piece will eventually sit at **experience.agroverse.shop**,
following the `capoeira.agroverse.shop` pattern (setting-aware session generator).

**Context:** Mr. Cao asked Gary to design two learning modules — **1. Agroforestry**
and **2. Supply Chain** — for the Aora pilot program (mentors + children co-creating;
"TED for children", content a 6-year-old can grasp; senses: see/smell/taste/hear/create).
Jerri (China team) needs initial ideas + a rough timeline to line up events
(salons of ~25 in Guangzhou/Shenzhen/Dongguan/Changsha/Shanghai; main launch
≤100 ppl Shenzhen or Songshan Lake). Gary in China ~Jul 7 – end Jul 2026.

## Decisions locked (Gary, 2026-06-04)

1. **Documents-first** — md + PDF for the two modules now; site/session-generator is a fast follow. Don't block Jerri on software.
2. **Repo = `TrueSightDAO/aora`** (local `~/Applications/aora`). "Aora" is the brand.
3. **Module boundary is engine-agnostic** — exercises are atomic tagged units any engine (Kaon's GO app or our own LLM-built one) can recompose; Agroforestry = forest→dried bean, Supply Chain = bag→bar→you, QR provenance as Supply Chain finale (runs on Agroverse QR + ledger stack, no Kaon dependency).
4. **Bilingual** — EN canonical authored by us; Jerri's team owns zh-CN translations in the same repo (`index.zh-CN.md` next to each `index.md`).
5. **PDFs versioned in the `aora` repo** next to source md (generated, committed). PDF is the China-proof artifact (GitHub/Pages unreliable behind GFW; share PDFs via WhatsApp/Feishu).

## Pre-flight

- [x] `gh` auth works for TrueSightDAO org (existing repos push fine over HTTPS)
- [x] PDF tooling on this machine: `weasyprint` + python `markdown` ✓
- [x] Reference schema: `capoeira/data/moves.json` (id/theme/difficulty/duration/video/notes)
- [ ] Confirm with Jerri which settings China salons will actually have (assume **workshop** + **kitchen**; no farm/factory/warehouse until Brazil/US legs)

## Sequenced plan

| Unit | What | Status |
|------|------|--------|
| **PR0** | This roadmap (agentic_ai_context) | merged ☐ · contribution reported ☐ |
| **PR1** | `TrueSightDAO/aora` repo: README (purpose, layout, bilingual convention, engine-agnostic note), `modules/agroforestry/index.md`, `modules/supply_chain/index.md`, zh-CN stubs, `scripts/build_pdfs.py`, generated PDFs in `pdfs/` | merged ☐ · contribution reported ☐ |
| **PR2** | zh-CN intake — Jerri's team translates; we review structure only | not started (theirs) |
| **PR3** | Fast follow: `data/exercises.json` (1:1 with module exercise tables) + session-generator scaffold + GitHub Pages → experience.agroverse.shop CNAME | not started |
| **PR4** | Credentialing tie-in: `programs/<aora>/manifest.json` on credentialing platform, `experience.agroverse.shop` in `source_pages[]` | not started |

**RESUME HERE → PR1** (if PR1 shows merged, resume at PR3 unless Jerri feedback arrived first).

## Timeline communicated to Jerri

- ~Jun 11: v0.1 module outlines (md + PDF, EN) to Jerri
- Jun 12–25: revise w/ Jerri+Evan; exercises.json + generator scaffold; zh-CN pass (Jerri's team)
- By Jul 4: pilot-ready facilitator session plans for workshop + kitchen settings
- Jul 7–end Jul: run salons live in China; freeze main-event content ~1 wk prior

## Related

- `capoeira/` — session-generator pattern + moves.json schema to mirror
- `truesight_me/lineage.html` — credentialing pitch this program instantiates
- Chocolate mold thread (Jerri point 1) is separate — polycarbonate 27.5×17.5cm, 4×50g cavities; not covered by this plan
