# ABBREVIATIONS — TrueSight DAO / SunMint glossary

Single reference for abbreviations used across agentic_ai_context, repos, and GAS projects. If you meet an acronym here, this is the expansion. If it is NOT here, it is worth adding (and ideally expanding at first use in the source doc).

## SunMint processors (GAS)

| Abbr | Expansion | What it is / where used |
|---|---|---|
| **TGM** | **Tree Growth Monitoring** | GAS processor for `[TREE GROWTH MONITORING EVENT]` — farmers submit tree-growth photos; handler (`process_tree_growth_monitoring.gs`) scans Telegram Chat Logs, mirrors media, appends tracking rows. Template for FBE. |
| **FBE** | **Farm Boundary Evidence** | GAS processor for `[FARM BOUNDARY EVIDENCE EVENT]` — boundary photos/videos capture (`limites-da-fazenda` page); handler (`process_farm_boundary_evidence.gs`) scans chat logs, upserts farm/plot row, records media. Built mirroring TGM. |
| **TGP** | **Tree Planting** | GAS action `process_tree_planting_link.js` — tree-planting link processing (QR → planted tree records). |

## Carbon / registry domain

| Abbr | Expansion | Notes |
|---|---|---|
| **MRV** | Monitoring, Reporting, Verification | Standard framework for carbon projects (measure → document → verify). |
| **VCS** | Verified Carbon Standard | Verra's carbon credit standard; a registry pathway in the SunMint roadmap (VM0047 methodology). |
| **ICVCM** | Integrity Council for the Voluntary Carbon Market | Sets quality thresholds for carbon credits (the "Core Carbon Principles"); roadmap flexes with their rules. |
| **SBTi** | Science Based Targets initiative | Sets corporate climate targets; V2.0 introduced OER tiers (see OER). |
| **OER** | (SBTi) Offsetting & Removals (tiers) | SBTi V2.0 tiers (Engaged/Advanced/Leadership) with $20/$80 floors; nature-based removals remain eligible. |
| **VVB** | Validation/Verification Body | Independent auditor for carbon projects (Plan Vivo / Verra verification). |
| **SBCE** | Sistema Brasileiro de Comércio de Emissões | Brazil's regulated emissions trading system — a roadmap registry pathway. |
| **CAR** | Cadastro Ambiental Rural | Brazil's rural environmental registry; farmer's CAR polygon is the authoritative boundary tier. |
| **INCRA** | Instituto Nacional de Colonização e Reforma Agrária | Brazil's land reform/agrarian agency; INCRA polygon is an authoritative boundary tier. |
| **ETS** | Emissions Trading System | Cap-and-trade system (e.g. EU ETS) — distinct from the voluntary carbon market. |

## Infra / tooling

| Abbr | Expansion | Notes |
|---|---|---|
| **GAS** | Google Apps Script | Serverless JS platform; the DAO's processors/webhooks live in `google_app_scripts/<scriptId>/` in tokenomics. |
| **SA** | Service Account | GCP credential used to access Sheets/Drive (e.g. `agroverse_qr_code_manager`). |
| **TTL** | Time To Live | Deploy lease lifetime (30 min); a lease past TTL is abandoned and may be taken over (leases/README). |
| **SW** | Service Worker | Offline caching layer of the farmer app (PWA). |
| **UAT** | User Acceptance Testing | The always-stop verification gate before prod promote. |
| **E2E** | End-to-End | Full-path test (capture → Edgar → dispatch → GAS → sheet). |
| **APK** | Android Package Kit | Native Android app installer (sunmint-android.apk). |
| **QR** | Quick Response | QR codes on cacao bags/trees (agroverse QR registry). |
| **PIX** | Pix | Brazil's instant payment system — farmer payout method on register_farm. |

## Version control / process

| Abbr | Expansion | Notes |
|---|---|---|
| **PR** | Pull Request | Branch → review → merge unit of work (one per turn). |
| **CI** | Continuous Integration | Automated checks (the four hard-rule checks: compile, ruff, format, pytest). |
| **API** | Application Programming Interface | e.g. GitHub Contents API (sanctioned path for api_only repos). |

---
Rule of thumb: expand an abbreviation at first use in any new doc; add any new abbreviation here.
