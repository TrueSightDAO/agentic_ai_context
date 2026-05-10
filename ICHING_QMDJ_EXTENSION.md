# I-Ching Oracle — QMDJ extension plan

**Status:** design proposal, not yet implemented.
**Owner of the spec:** Gary.
**Repos involved:** `iching_oracle` (client + GAS), `agentic_ai_context` (this doc).

## Why extend the oracle with QiMenDunJia

The I-Ching cast and a QMDJ chart use the same moment differently:

- **I-Ching** uses the moment as the *occasion* for randomization. The hexagram
  comes from the coin throws, not from the timestamp. It tells you the *quality
  of the moment* — what is moving, what is transforming.
- **QMDJ** is *entirely* derived from the timestamp. There is no randomization;
  the chart is what it is for that solar instant. It tells you the *spatial /
  strategic structure* of the moment — where to act, when the auspicious
  window opens, which direction the energy supports.

Pairing them on the same moment T is conceptually clean: I-Ching is the
narrative/transformational lens, QMDJ is the spatial/strategic overlay. Two
classical frameworks reading the same instant. The advisory then has access
to both lenses when shaping a recommendation.

**Honest disclaimer:** combining I-Ching and QMDJ for the same question is a
*modern synthesis*, not a traditional practice. Classical practitioners
typically use them for different question-frames. The UI and the GAS prompt
should both acknowledge this so we stay intellectually honest with anyone
who knows both systems.

## Library — chart casting

Use **`lunar-javascript`** from the 6tail family
(<https://github.com/6tail/lunar-javascript>). This is the most widely
community-trusted open-source engine for Chinese calendar + metaphysics
including QMDJ. Same author maintains `lunar-python`, `lunar-java`, and
`lunar-csharp`, so output stays consistent across stacks if we ever rewrite
the backend.

Do **not** reimplement chart casting from scratch. The Ju (局) assignment
across the 24 solar terms, Yin/Yang dunjia, six Yi placement, three Wonders
positioning, Heaven Plate / Earth Plate / Doors / Stars / Spirits — every
one of these is a place where a small mistake propagates through the whole
chart.

"Verified" in this domain isn't formal — practitioners verify by
cross-checking output against multiple known-good engines. 6tail is the
closest to a community reference. When wiring it in, smoke-test against
2–3 known timestamps and compare to a reference site (e.g. 漢程網 QMDJ
chart, 元亨利貞網) before going live.

## Data flow

```
[Client / iching_oracle]
  1. User throws 6 coins → hexagram + changing lines (existing)
  2. Capture timestamp T at the moment the cast completes
  3. Compute QMDJ chart from T using lunar-javascript
     - Yin/Yang dunjia, Ju (局)
     - Six Yi placement (六儀)
     - Three Wonders (三奇 — Yi 乙, Bing 丙, Ding 丁)
     - Heaven Plate / Earth Plate
     - Eight Doors (八門)
     - Nine Stars (九星)
     - Eight Spirits (八神)
  4. POST to GAS with hexagram + changing_lines + qmdj_chart + timestamp

[GAS / oracle_advisory_bridge.gs]
  5. extractDraw_ → also pull qmdj_chart from params
  6. buildOraclePromptParts_ → add QMDJ framework reference (cached) +
     QMDJ chart block (per-call)
  7. callAdvisor_ → unchanged, the prompt-caching split keeps the new
     framework reference in the cached block

[LLM]
  8. Produces an advisory that uses I-Ching as the narrative layer and
     QMDJ as the spatial/strategic overlay. Surfaces the chart's
     structural state in plain language alongside the recommendation.
```

## Prompt structure — proposed shape

Existing structure in `oracle_advisory_bridge.gs`:

| Block            | What | Cached? |
| ---------------- | ---- | ------- |
| `header`         | `ORACLE_PROMPT_HEADER` (advisor instructions) | yes |
| `staticContext`  | `ADVISORY_SNAPSHOT_MD` + `ADVISORY_BASE_MD` | yes |
| `dynamicContext` | I-Ching draw + reminders + pending iOS intents | no |

Proposed extension:

| Block            | What | Cached? | Change |
| ---------------- | ---- | ------- | ------ |
| `header`         | Extended with QMDJ output sections | yes | edit |
| `staticContext`  | `ADVISORY_SNAPSHOT_MD` + `ADVISORY_BASE_MD` + **QMDJ_FRAMEWORK_REFERENCE** | yes | extend |
| `dynamicContext` | I-Ching draw + **QMDJ chart for moment T** + reminders + pending raws | no | extend |

The cache split holds — the QMDJ framework explanation (what each door /
star / spirit means, what counts as auspicious, what "Three Wonders +
Three Auspicious Doors in the same palace" indicates) is static across
calls and lives in the cached block. Only the chart data for the
specific moment is per-call.

## Header changes — output sections

Current `ORACLE_PROMPT_HEADER` ends with five output sections. Extended
shape, in order:

1. **Reading synthesis** (2-4 lines) — what the I Ching hexagram
   illuminates about the current situation. *Existing, unchanged.*
2. **QMDJ configuration of this moment** (3-5 lines) — *new.*
   Name the Ju (局), where the Three Wonders 三奇 (Yi, Bing, Ding) sit,
   where the Three Auspicious Doors 三吉門 (Open 開, Rest 休, Birth 生)
   sit, where the day stem sits, and any notable alignment (e.g.
   Wonder + Auspicious Door in the same palace; Death door 死門 sitting
   on the day stem; Yi 乙 wonder colliding with Geng 庚 stem). Keep it
   structural — what is true of the moment, not yet what to do.
3. **Combined frame** (1-2 lines) — *new.* How the I Ching narrative
   reading and the QMDJ structural reading point at the same situation,
   and where they reinforce or diverge.
4. **Context gaps worth naming** (1-3 bullets) — *existing, renumbered.*
5. **Priorities this week for a solo operator** (3 bullets max) —
   *existing, renumbered.*
6. **Risks / watch-outs** (3 bullets) — *existing, renumbered.*
7. **One decisive action in next 24h** — *existing, extended.*
   Where QMDJ surfaces a clear directional or timing signal (e.g. an
   Auspicious Door + Wonder in a specific palace), name it ("the action
   benefits from facing east before noon" / "wait until after the next
   2h shichen"). Don't fabricate directional advice when QMDJ doesn't
   show a clear signal — say "QMDJ does not surface a strong directional
   read here" and proceed with the I-Ching-grounded action.

The header should also carry a one-paragraph note that this is a
*modern synthesis* of two classical frameworks and that QMDJ is being
used as a structural overlay on the moment that I-Ching has already
characterized — to keep the LLM from treating them as two redundant
oracles competing for the same role.

## Static framework reference — content sketch

A reference block (~1500-2500 tokens) explaining what the LLM is
looking at. Stable across all calls. Lives in `staticContext` and is
cached.

Should cover, at minimum:

- The Nine Palaces 九宮 layout on the Luo Shu grid (which palace is
  which direction).
- The Eight Doors 八門 and which are auspicious / inauspicious / mixed
  (吉門: Open 開, Rest 休, Birth 生; 凶門: Hurt 傷, Death 死, Surprise
  驚; 中門: Du 杜, Scenery 景).
- The Three Wonders 三奇 (Yi 乙, Bing 丙, Ding 丁) and what they
  classically signify.
- The Six Yi 六儀 (Wu, Ji, Geng, Xin, Ren, Gui) and that they "hide"
  the Jia stems.
- The Eight Spirits 八神 in brief (Zhi Fu 直符, Teng She 螣蛇, Tai Yin
  太陰, Liu He 六合, Bai Hu 白虎, Xuan Wu 玄武, Jiu Di 九地, Jiu Tian
  九天) — auspicious vs inauspicious bias.
- Notable alignments worth surfacing: Three Wonders + Three Auspicious
  Doors in the same palace ("flying bird falls on the cave" 飛鳥跌穴
  and similar); Geng-stem collisions (庚 = blockage); Death door on
  day stem; etc.

Keep it descriptive, not prescriptive. The framework reference is for
the LLM to understand what it is reading; the operator-facing
interpretation comes from the per-call advisory.

## Dynamic QMDJ chart block — payload shape

Per-call, included in `dynamicContext`. About 500-1000 tokens.

Recommended JSON-ish serialization, then rendered as text:

```
QMDJ CHART (computed from timestamp T = <ISO>)
- Solar term: <name>
- Yin/Yang dunjia: <yin|yang>
- Ju (局): <number>
- Day pillar: <stem><branch>
- Hour pillar: <stem><branch>
- Zhi Fu (直符) star: <name>, sitting at palace <n>
- Zhi Shi (直使) door: <name>, sitting at palace <n>

Palaces (Luo Shu order: 1 N, 2 SW, 3 E, 4 SE, 5 center, 6 NW, 7 W, 8 NE, 9 S):
  Palace 1 (北/坎): Heaven stem=<x>, Earth stem=<y>, Door=<x>, Star=<x>, Spirit=<x>
  Palace 2 (西南/坤): ...
  ...
  Palace 9 (南/離): ...

Three Wonders 三奇:
  Yi 乙 → palace <n> (<direction>)
  Bing 丙 → palace <n>
  Ding 丁 → palace <n>

Three Auspicious Doors 三吉門:
  Open 開 → palace <n>
  Rest 休 → palace <n>
  Birth 生 → palace <n>

Notable alignments: <free-text bullets generated by lunar-javascript or
the client; e.g. "Yi 乙 + Open Door 開門 in palace 9 (south) — strong
window for outward action this shichen">.
```

The "notable alignments" line is the highest-leverage piece for the
LLM — pre-computed flags for things a practitioner would notice at a
glance. The client (or a small GAS helper) should generate these from
the chart structure.

## Risks / things to be careful about

- **Information overload for the user.** I-Ching alone gives a hexagram
  + judgment + image + changing lines. Adding QMDJ adds doors, stars,
  spirits, three wonders, six yi, palace positions. The UI should
  present QMDJ as a *collapsible "Extended Reading: QiMenDunJia"
  section* below the I-Ching reading, not above it. Default surface
  is the I-Ching narrative.
- **LLM cost.** Adding QMDJ framework reference + chart data
  meaningfully increases tokens per cast. Caching the framework
  reference (it's static) keeps marginal cost reasonable. Smoke-test
  the cache hit rate after deployment.
- **Two oracles awkwardly stapled together.** Mitigated by the prompt
  header explicitly assigning roles (I-Ching = narrative, QMDJ =
  spatial/strategic overlay).
- **Naive auto-interpretation.** QMDJ is a practitioner skill. The
  output should surface chart structure *honestly* and suggest direction
  /timing only when the chart shows a *clear* signal. When it doesn't,
  the prompt should tell the LLM to say so and fall back to the
  I-Ching-grounded action.
- **Modern-synthesis disclaimer.** The UI should note (small text,
  colophon, or info icon) that combining the two frameworks is a
  modern synthesis. Keeps us honest with practitioners.

## Implementation order — when picked up

1. **Smoke-test lunar-javascript locally.** Cast charts at 2-3 known
   timestamps, compare to a reference site. Confirm Ju, Three Wonders,
   Three Doors, Spirits all match.
2. **Wire chart casting into the client.** After coin throw, capture T,
   compute the chart, render it as a 9-palace grid in a collapsed
   "Extended Reading" section. Don't yet involve GAS — just confirm the
   chart renders correctly.
3. **Draft the QMDJ framework reference.** Produce the static text
   block. Aim for 1500-2500 tokens. Land it in `agentic_ai_context` as
   `QMDJ_FRAMEWORK_REFERENCE.md` (or similar) so GAS can fetch it the
   same way it fetches `ADVISORY_SNAPSHOT.md`.
4. **Extend `oracle_advisory_bridge.gs`.**
    - `RAW_URLS` += `qmdjFrameworkReference`.
    - `extractDraw_` += `qmdj_chart` field (JSON-encoded query param or
      multi-field split — JSON is cleaner if the client uses POST; if
      sticking to GET, multi-field).
    - `buildOraclePromptParts_` → add framework reference to
      `staticContext`, add chart block to `dynamicContext`.
    - `ORACLE_PROMPT_HEADER` → extend output sections per the header
      spec above.
5. **End-to-end smoke test.** Cast on the live page, confirm the
   advisory now includes the QMDJ configuration section and the
   combined frame, and that the decisive-action section meaningfully
   uses (or honestly declines to use) the chart's directional signal.

Each step is independently testable; don't try to ship 1-5 in a single
PR. Likely 3 PRs: client chart-casting + render, GAS + framework doc,
prompt header refinement after seeing live output.
