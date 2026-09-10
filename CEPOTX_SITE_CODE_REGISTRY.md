# CEPOTX network — producer rosters & site-code registry (reference)

> **Purpose:** durable lookup for mapping a producer name or CEPOTX site code
> (`X-06-NN`) to the right sub-cooperative, and for checking whether a code is
> already assigned when new partner farms come online. Consult this BEFORE
> registering a new farm plot or assigning a plot_id, so codes are never
> invented or re-assigned.

## Canonical scheme (governor decision 2026-09-05, thread 21005/22082)

**plot_id = CEPOTX site code.** Never invent or re-assign codes. Legacy mnemonic
plot ids (SA-P1, CL-P1, LD-P1, SR-P1, RG-P1) are retired aliases — see the
anchors table below; each row lists the legacy id only as historical context.

### Alias tombstone — 2026-09-05 renames (canonical data)

The three CEPOTX-family DAO plots were renamed from mnemonic ids to their
CEPOTX site codes (SunMint Plots sheet + rebuild; thread 22082). Canonical data
carries **no 'invalid' tombstones** — the plot rows were *renamed*, not retired:

| Legacy id (retired alias) | Canonical id (since 2026-09-05) | Farm / owner | Canonical commits (TrueSightDAO/sunmint) |
|---|---|---|---|
| SA-P1 | B-06-58 | Santa Anna Fazenda — Ana Lucia Araujo de Sousa (COOPOXIN) | plots+farms rebuild `e7af93f` (23:36Z) → clean 9-plot rebuild `3713caa` (23:53Z) → satellite regen `804f359` (23:55Z) |
| CL-P1 | B-06-108 | Fazenda Cleide — Cleide Maris Suk (COOPOXIN) | same three commits |
| LD-P1 | V-06-29 | La do Sítio — Paulo | same three commits |

> **Derived artifacts that still carry legacy ids** — `sunmint/satellite/plot_SA-P1|CL-P1|LD-P1/`
> scene dirs and `sunmint/plots/by-plot/{SA-P1,CL-P1,LD-P1}.geojson` — are
> **intentionally retained as inert residue** (governor decision 2026-09-05,
> thread 22082): nothing consumes them, the satellite manifest + plots index are
> authoritative and already carry only canonical ids, and git holds the full
> rename history. Resolve any legacy-id sighting via this table; do **not**
> "fix" by deleting or by flipping a status to invalid (canonical data says the
> plot never was SA-P1 — it is B-06-58, renamed). See OPEN_FOLLOWUPS.md entry
> (filed 2026-09-05) for the optional workflow-prune / SCHEMA.md-example refresh.

## Status & provenance

| Field | Value |
|---|---|
| Source | "Lista de Produtores" document pages captured from video |
| Captured | 2026-09-05 (governor transcription, thread 21727) |
| Status | **reported / unverified** — read from video, NOT an official CEPOTX register |
| Coverage | 3 of 4 member coops. COOPOXIN rows 1–27 + 29–56 (row 28 not visible); COPOPS rows 17–33 (rows 1–16 not visible); COOPCAO rows 1–16. COPOTRAN not captured. |
| Official confirmation | pending — use as lookup aid only; confirm with CEPOTX / Jedielcio before legal or FSVP use |

## Observed site-code families (association only — prefix meaning NOT documented)

Per AGROVERSE_SUNMINT_FARM_LISTING.md §6: letter-prefix meaning is not yet
understood — **do not decode/derive**. The family→cooperative associations below
are observed from rosters + known farms and are a lookup hint, not a rule.

| Prefix | Cooperative | Observed range | Known member examples |
|---|---|---|---|
| B-06-NN | COOPOXIN | B-06-27 … B-06-151 | Fazenda Cleide B-06-108; Santa Anna (see discrepancy note) |
| U-06-NN | COPOPS | U-06-62 … U-06-78 (plus U-06-06, U-06-07) | Sítio Raimundo & Geniza U-06-07; Fazenda Santa Rosa U-06-06 |
| N-06-NN | COOPCAO | N-06-02 … N-06-52 (captured roster) + N-06-66 (governor-confirmed 2026-09-10, outside the captured roster) | Jader Adriano da Silva Santos N-06-37 (CEPOTX President); Sítio Torres (Pacajá) N-06-66 |
| V-06-NN | ? (not determined) | V-06-29 | Paulo / La do Sítio (V-06-29) |

**One code per property, not per person.** The same producer legitimately holds
multiple codes: Raimundo Silva Santos B-06-70/71/103; José Gabriel Ferreira
Santos B-06-55/120; Arlito Ferreira Neres B-06-42/66; José Aparecido da Silva
B-06-61/102; José Justino de Sousa B-06-52/142; Ana Cláudia Oliveira Rocha
N-06-43/47.

## Anchors — site codes tied to DAO-registered farms

| Site code | Farm / plot | Registered owner | Coop | Legacy plot id (retired) | Source of DAO record |
|---|---|---|---|---|---|
| B-06-58 | Santa Anna Fazenda | Ana Lucia Araujo de Sousa | COOPOXIN | SA-P1 | 2026-08-30 site-visit PDF; fda_fsvp cepotx entity; shop PRs #251/#252 |
| B-06-108 | Fazenda Cleide | Cleide Maris Suk | COOPOXIN | CL-P1 | roster row 22 + fda_fsvp + 2024-07-02 site-visit PDF |
| U-06-06 | Fazenda Santa Rosa | Antônio & Graça | COPOPS | SR-P1 | governor-provided translation screenshot (2026-09-05); sunmint plots/index.geojson; shop PRs #288/#289 |
| U-06-07 | Sítio Raimundo & Geniza | Raimundo Silva (COPOPS Presidente) | COPOPS | RG-P1 | governor-provided site-app screenshot; fda_fsvp copops entity; shop PR #285 |
| V-06-29 | La do Sítio | Paulo | ? | LD-P1 | AGROVERSE_SUNMINT_FARM_LISTING §6 |
| N-06-37 | (member property) | Jader Adriano da Silva Santos — CEPOTX President per Rota do Cacau | COOPCAO | — | roster + public record |
| N-06-66 | Sítio Torres (Pacajá) Plot 1 (cacao enrichment) | Alexandre (CoopCao director-coordinator) | COOPCAO | — | **governor-confirmed 2026-09-10** (Gary, thread 24442); SunMint Plots row 23; `sunmint/plots/index.geojson`; agroverse_shop `farms/sitio-torres-pacaja-para/` (PRs #308/#309); fda_fsvp CEPOTX `N-06-66` anchor |

## ⚠️ Open discrepancy — B-06-56 vs B-06-58 (Ana Lucia Araujo)

- DAO records (Santa Anna farm page PRs #251/#252, fda_fsvp cepotx entity):
  **B-06-58** = Ana Lucia Araujo de Sousa.
- This roster (COOPOXIN, row 8): **B-06-56** = Ana Lúcia Araújo de Souza.
- Same person, two codes, one digit apart — a 6/8 misread on either source is
  plausible (common in low-res video/scan). **Do not change records on this
  evidence alone; verify with CEPOTX/Jedielcio at next contact**, then fix the
  wrong side. (B-06-58 does not appear anywhere in the visible COOPOXIN rows.)
- The standardization in this thread keeps the DAO-record code **B-06-58**
  (matching fda_fsvp entity + shop pages + Santa Anna site-visit PDF) until
  CEPOTX confirms which side is correct.

## Rosters

### COOPOXIN — "Lista de Produtores COOPOXIN" (B-06 family; rows 1–27, 29–56 visible)

| Nº | Código | Nome Produtor |
|---|---|---|
| 1 | B-06-27 | João Moreira de Sousa |
| 2 | B-06-39 | João da Silva Araujo |
| 3 | B-06-42 | Arlito Ferreira Neres |
| 4 | B-06-51 | José Carlos de Souza |
| 5 | B-06-52 | José Justino de Sousa |
| 6 | B-06-53 | Reginaldo Silva Pinho |
| 7 | B-06-55 | José Gabriel Ferreira Santos |
| 8 | B-06-56 | Ana Lúcia Araújo de Souza |
| 9 | B-06-61 | José Aparecido da Silva |
| 10 | B-06-66 | Arlito Ferreira Neres |
| 11 | B-06-67 | Gilberto Silva de Souza |
| 12 | B-06-70 | Raimundo Silva Santos |
| 13 | B-06-71 | Raimundo Silva Santos |
| 14 | B-06-82 | José Carlos de Oliveira |
| 15 | B-06-88 | Manoel Valetim da Silva |
| 16 | B-06-90 | Afonso Matos da Silva |
| 17 | B-06-95 | Djacir Batista de Aquino |
| 18 | B-06-100 | Silvio Costa da Silva |
| 19 | B-06-101 | Oscar Rodrigues |
| 20 | B-06-102 | José Aparecido da Silva |
| 21 | B-06-103 | Raimundo Silva Santos |
| 22 | B-06-108 | Cleide Maris Suk |
| 23 | B-06-115 | Magnólia Damasceno Gerhard |
| 24 | B-06-119 | Elisandria José Dias |
| 25 | B-06-120 | José Gabriel Ferreira Santos |
| 26 | B-06-121 | José Maria da Silva Barbosa |
| 27 | B-06-122 | Maria Madalena Andrade de Oliveira |
| 29 | B-06-123 | Sebastião Vilar dos Santos |
| 30 | B-06-125 | Nilo da Silva Alencar |
| 31 | B-06-126 | Claudio da Silva |
| 32 | B-06-127 | Robson da Silva Alencar |
| 33 | B-06-128 | Jovenil Vilar dos Santos |
| 34 | B-06-129 | José Silva Santos |
| 35 | B-06-130 | Francisco Viana de Carvalho |
| 36 | B-06-131 | Aldair de Sá Lourenço |
| 37 | B-06-132 | Valdo Batista Fernandes |
| 38 | B-06-133 | Rayane da Costa Silva Nascimento |
| 39 | B-06-134 | Neyvaldo Santos Silva |
| 40 | B-06-135 | Marijane Oliveira Figueiredo Sousa |
| 41 | B-06-136 | Antonio Carlos de Souza |
| 42 | B-06-137 | Gilson Silva Santos |
| 43 | B-06-138 | Edvan Silva Santos |
| 44 | B-06-139 | Raimundo Ferreira de Araujo |
| 45 | B-06-140 | Rafael Vieira Santos |
| 46 | B-06-141 | Leonidas Lima de Jesus |
| 47 | B-06-142 | José Justino de Sousa |
| 48 | B-06-143 | Ronicleu Oliveira de Araujo |
| 49 | B-06-144 | Cleidines Oliveira de Araujo |
| 50 | B-06-145 | Rubens Silva Damasceno |
| 51 | B-06-146 | Jeson dos Santos Souza |
| 52 | B-06-147 | Justino Luciano da Silva |
| 53 | B-06-148 | Edivaldo Luiz da Silva |
| 54 | B-06-149 | Douglas Ferreira da Silva |
| 55 | B-06-150 | Edivaldo Ferreira do Nascimento |
| 56 | B-06-151 | José Geraldo Torres da Silva |
