# Lab Report Translation — English Summaries for Agroverse Shipments

**Read this** when the task involves translating Portuguese lab reports to English, adding English summaries to shipment pages, or extracting/translating PDF lab reports.

---

## Overview

Agroverse shipment pages (AGL4, AGL8, etc.) display lab reports that are **authoritative documents in Portuguese**. We do **not** create English PDF copies (we are not the authority). Instead we:

1. **Display an English summary** on the shipment page
2. **Link to the original Portuguese PDF** for verification

---

## Workflow

### 1. Extract PDF Text

Use `pdfplumber` to extract text from the Portuguese PDF:

```python
import pdfplumber
with pdfplumber.open("path_or_url") as pdf:
    text = "\n\n".join(p.extract_text() or "" for p in pdf.pages)
```

Or fetch from raw GitHub URL first:

```bash
curl -sL -o /tmp/report.pdf "https://raw.githubusercontent.com/TrueSightDAO/notarizations/main/FILENAME.pdf"
```

### 2. Translate via Grok API

**Script:** `agroverse_shop/scripts/translate_lab_report.py`

**Grok API key location:**
- Env var: `GROK_API_KEY`
- Or: `video_editor/.env` (same key used for video editing)

**Usage:**
```bash
# From PDF URL
python translate_lab_report.py "https://raw.githubusercontent.com/TrueSightDAO/notarizations/main/20250714215834_gary_teh_oscar_lab_report.pdf" --id "AGL4"

# From local file
python translate_lab_report.py /tmp/oscar_lab.pdf --id "AGL4"

# From stdin (pre-extracted text)
cat extracted.txt | python translate_lab_report.py --text --id "AGL4"
```

**Output:** JSON with `summary`, `key_results`, `full_translation`.

**Note:** If Grok returns 429 (credits exhausted), translate manually from the extracted Portuguese text.

### 3. Add Summary to Shipment Page

**Location:** `agroverse_shop/shipments/{agl_id}/index.html`  
**Section:** "Transparency in Action" (before or after the documents list)

**HTML pattern:**
```html
<div class="lab-report-summary" style="margin-bottom: 1.5rem; padding: 1.25rem; background: rgba(59, 51, 51, 0.04); border-radius: 12px; border-left: 4px solid var(--color-accent);">
  <h4 style="margin: 0 0 0.75rem 0; font-size: 1.1rem;">Lab Report (English Summary)</h4>
  <p style="margin: 0 0 0.75rem 0; font-size: 0.95rem; line-height: 1.6; color: var(--color-text);">
    [ENGLISH SUMMARY - 2–4 sentences: report ID, sample type, key results, compliance]
  </p>
  <a href="https://raw.githubusercontent.com/TrueSightDAO/notarizations/main/[FILENAME].pdf" rel="noopener noreferrer" target="_blank" style="font-size: 0.9rem; color: var(--color-primary); text-decoration: underline;">View original report (Portuguese PDF)</a>
</div>
```

**Summary content:** Include report number, sample type, heavy metals results (Arsenic, Cadmium, Lead, Copper), ANVISA compliance, methodology (ICP-MS).

---

## Lab Report URLs (Raw GitHub)

| Shipment | Report ID | Raw PDF URL |
|----------|-----------|-------------|
| AGL4 (Oscar) | LAP-339.2025.B | `20250714215834_gary_teh_oscar_lab_report.pdf` |
| AGL8 (Paulo) | LAP-340.2025.B | `20250714215751_gary_teh_para_lab_report.pdf` |

Base: `https://raw.githubusercontent.com/TrueSightDAO/notarizations/main/`

---

## PDF Structure (Portuguese)

Typical sections:
- **01. Dados Contratação** — Contract/solicitor info
- **02. Dados da Amostragem** — Sample description, location, dates
- **03. Resultados** — Heavy metals (Arsênio, Cádmio, Chumbo, Cobre) in mg/kg
- **04. Informações Importantes** — Test metadata
- **Legislação** — ANVISA IN 160 compliance

---

## Key Files

| File | Purpose |
|------|---------|
| `agroverse_shop/scripts/translate_lab_report.py` | PDF extraction + Grok translation |
| `agroverse_shop/shipments/agl4/index.html` | AGL4 shipment page |
| `agroverse_shop/shipments/agl8/index.html` | AGL8 shipment page |
| `video_editor/.env` | Grok API key (GROK_API_KEY) |

---

## Dependencies

- `pdfplumber` — PDF text extraction
- `requests` — Grok API calls
- `python-dotenv` — Load .env (optional)
