# CEPOTX network — producer rosters & site-code registry (agent-facing reference)

> **Purpose:** durable, agent-retrievable lookup for mapping a producer name or CEPOTX
> site code (`X-06-NN`) to the right sub-cooperative, and for checking whether a code
> is already assigned when new partner farms come online. Consult this BEFORE
> registering a new farm plot or assigning a plot_id, so codes are never invented or
> re-assigned.
>
> **Retrieval:** this file lives in agentic_ai_context on purpose — it is findable via
> `search_context` (try "COOPOXIN", "Lista de Produtores", "site code", "B-06-108") and
> readable via `read_context_file("CEPOTX_SITE_CODE_REGISTRY.md")`. Mirror of
> `fda_fsvp/suppliers/cepotx/site_codes.md` (FSVP supplier-folder copy) — keep the two
> in sync when new rosters arrive.

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
| U-06-NN | COPOPS | U-06-62 … U-06-78 (plus U-06-07) | Sítio Raimundo & Geniza U-06-07 |
| N-06-NN | COOPCAO | N-06-02 … N-06-52 | Jader Adriano da Silva Santos N-06-37 (CEPOTX President) |
| V-06-NN | ? (not determined) | V-06-29 | Paulo / La do Sítio (V-06-29) |

**One code per property, not per person.** The same producer legitimately holds
multiple codes: Raimundo Silva Santos B-06-70/71/103; José Gabriel Ferreira
Santos B-06-55/120; Arlito Ferreira Neres B-06-42/66; José Aparecido da Silva
B-06-61/102; José Justino de Sousa B-06-52/142; Ana Cláudia Oliveira Rocha
N-06-43/47.

## Anchors — site codes tied to DAO-registered farms

| Site code | Farm / plot | Registered owner | Coop | Source of DAO record |
|---|---|---|---|---|
| B-06-58 | Santa Anna Fazenda (SA-P1) | Ana Lucia Araujo de Sousa | COOPOXIN | 2026-08-30 site-visit PDF; fda_fsvp cepotx entity; shop PRs #251/#252 |
| B-06-108 | Fazenda Cleide (CL-P1) | Cleide Maris Suk | COOPOXIN | roster row 22 + fda_fsvp + 2024-07-02 site-visit PDF |
| U-06-07 | Sítio Raimundo & Geniza (RG-P1) | Raimundo Silva (COPOPS Presidente) | COPOPS | governor-provided site-app screenshot; fda_fsvp copops entity; shop PR #285 |
| V-06-29 | La do Sítio | Paulo | ? | AGROVERSE_SUNMINT_FARM_LISTING §6 |
| N-06-37 | (member property) | Jader Adriano da Silva Santos — CEPOTX President per Rota do Cacau | COOPCAO | roster + public record |

## ⚠️ Open discrepancy — B-06-56 vs B-06-58 (Ana Lucia Araujo)

- DAO records (Santa Anna farm page PRs #251/#252, fda_fsvp cepotx entity):
  **B-06-58** = Ana Lucia Araujo de Sousa.
- This roster (COOPOXIN, row 8): **B-06-56** = Ana Lúcia Araújo de Souza.
- Same person, two codes, one digit apart — a 6/8 misread on either source is
  plausible (common in low-res video/scan). **Do not change records on this
  evidence alone; verify with CEPOTX/Jedielcio at next contact**, then fix the
  wrong side. (B-06-58 does not appear anywhere in the visible COOPOXIN rows.)

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

*(row 28 not visible in capture; numbering continues 29–56)*

### COPOPS — "Lista de Produtores COPOPS" (U-06 family; rows 17–33 visible)

| Nº | Código | Nome Produtor |
|---|---|---|
| 17 | U-06-62 | Jurande Viana dos Santos |
| 18 | U-06-63 | Francisca Barbosa da Silva |
| 19 | U-06-64 | Antonio Francisco da Silva |
| 20 | U-06-65 | Maria Gracineide Sales |
| 21 | U-06-66 | Ihumarque de Oliveira Pereira |
| 22 | U-06-67 | Fernando Kaio de Oliveira Pereira |
| 23 | U-06-68 | Camila Cavalcante de Oliveira |
| 24 | U-06-69 | Almir Leite dos Anjos Junior |
| 25 | U-06-70 | Wilton Pantoja de Oliveira |
| 26 | U-06-71 | Adão Almeida Ferreira |
| 27 | U-06-72 | Adevan Barbosa de Oliveira |
| 28 | U-06-73 | Joel Evangelista |
| 29 | U-06-74 | Dilmar Santos Viana |
| 30 | U-06-75 | Darcizio Vronski |
| 31 | U-06-76 | Magno Bernardo de Lima |
| 32 | U-06-77 | Maria Pinella Barreto |
| 33 | U-06-78 | Antonio Carlos de Silva Araujo |

*(rows 1–16 not visible in capture; U-06-07 Raimundo & Geniza is a separate,
lower code confirmed from the governor's site-app screenshot — do not assume
roster numbering maps to code order)*

### COOPCAO — "Lista de Produtores COOPCAO" (N-06 family; rows 1–16)

| Nº | Código | Nome Produtor |
|---|---|---|
| 1 | N-06-02 | Antonio do Nascimento Soares |
| 2 | N-06-07 | Edinaldo Dias |
| 3 | N-06-10 | Manoel José Leite |
| 4 | N-06-27 | Eugênio Eduardo Rocha |
| 5 | N-06-28 | Valmir Feitosa Dias |
| 6 | N-06-35 | Manoel Veloso Neto |
| 7 | N-06-37 | Jader Adriano da Silva Santos |
| 8 | N-06-43 | Ana Cláudia Oliveira Rocha |
| 9 | N-06-42 | Temistio Francisco Santos |
| 10 | N-06-44 | Vanderley Feitosa Dias |
| 11 | N-06-47 | Ana Cláudia Oliveira Rocha |
| 12 | N-06-48 | José Augusto Corinia |
| 13 | N-06-49 | José Paulo Cruz Oliveira |
| 14 | N-06-50 | Juliano Cruz Oliveira |
| 15 | N-06-51 | Janilson Cruz Oliveira |
| 16 | N-06-52 | Erivaldo Moreira de Sousa |

## Related

- `AGROVERSE_SUNMINT_FARM_LISTING.md` §6 (site-code policy: never derive, record source + status)
- `fda_fsvp/suppliers/cepotx/site_codes.md` (FSVP supplier-folder mirror) + `suppliers/cepotx/entity.json`
- `OPEN_FOLLOWUPS.md` — Fazenda Dona Rosa (COOPOXIN, Medicilândia) pending listing; site-code assignment must come from CEPOTX
