# Agroverse QR codes — batch sheet rows + local image compile

Read this when the operator asks to **create new serialized QR codes** on the **Main Ledger** tab **`Agroverse QR codes`**, generate **`compiled_*.png`** labels, or align with **regional handout** naming (**`LA`**, **`AUSTIN`**, etc.). **Canonical sheet layout:** `tokenomics/SCHEMA.md` → sheet **`Agroverse QR codes`**. **Currency semantics:** **`NOTES_tokenomics.md`** § *Agroverse QR codes tab* (column **I** ↔ **`Currencies`!A**).

---

## 1. Naming (column **A** — `qr_code`)

- **Payload:** Edgar check URL is `https://edgar.truesight.me/agroverse/qr-code-check?qr_code=` + **column A**. Keep **A** **short** (dense codes are harder on cheap label printers). Local compiler warns above ~28 characters (`MAX_RECOMMENDED_QR_LENGTH` in `tokenomics/python_scripts/agroverse_qr_code_generator/batch_compiler.py`).
- **Regional token:** **Los Angeles** handouts use **`LA`** (not `LOSANGELES`).
- **Product tokens in the id:** **`CC`** = **ceremonial cacao**; **`CT`** = **cacao tea** (same convention as Austin samples, e.g. `AUSTIN_CC_20260317_6`, `AUSTIN_CT_20260317_7`).
- **Batch date:** **`YYYYMMDD`** in the id (e.g. compile or campaign date).
- **Serial:** `_1`, `_2`, … within that region + product + date group.

**Example ids:** `LA_CC_20260414_1` … `LA_CC_20260414_10`, `LA_CT_20260414_1` … `LA_CT_20260414_10`.

---

## 2. Sheet tab **`Agroverse QR codes`** (workbook)

- **Spreadsheet:** [TrueSight DAO Contribution Ledger](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit) — tab **`Agroverse QR codes`** ([gid=472328231](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=472328231)).

### Column **I** (`Currency`)

- Values must **match** a **`Currencies` column A** string in the **same** workbook (ledger / sales validation). Promo rows may store the **resolved text** (not necessarily a visible `IMPORTRANGE` in every row); do **not** invent a new **I** string that is not on **`Currencies`**.

### Columns **A–H** (what the local compiler reads)

- **A:** `qr_code` (id above).
- **B:** `landing_page` — e.g. `https://www.agroverse.shop/shipments/agl4` (**CC** / ceremonial pouch line) vs `https://www.agroverse.shop/shipments/agl8` (**CT** / cacao tea); drives cacao vs non-cacao template in `batch_compiler.py` (`is_cacao` = **B** starts with `https://www.agroverse.shop`).
- **C:** `ledger` URL (e.g. `https://agroverse.shop/agl4` or `/agl8`).
- **D:** `status` — e.g. **`SAMPLE`** for regional promo chips matching existing Austin rows, or **`MINTED`** / other states per operator policy; reset **post-sale** fields when cloning **SOLD** rows (see §4).
- **E–H:** `farm name`, `state`, `country`, `Year` — **copy from the same reference row as B/C/I** (actual farm and origin, e.g. **Oscar Farm / Bahia / Brazil / 2024** for **CC** lines tied to AGL4, **La do Sitio / Para / Brazil / 2024** for **CT** lines tied to AGL8). These print on the label under the QR and drive **`compiled_{farm}_{qr_code}.png`**. **Do not** substitute the **handout city** (e.g. Los Angeles) for **E–G** unless the operator **explicitly** asks for that wording; regional promo is carried in **column A** (**`LA_…`**, **`AUSTIN_…`**) and landing URLs, not by replacing farm geography.

### Columns **J–V** (common pattern for new batches)

- **J:** QR creation date **`YYYYMMDD`**.
- **K:** GitHub raw path to **`compiled_{farm}_{qr_code}.png`** under `tokenomics/.../package_qr_codes/`. Existing rows use a **formula** that references **E** and **A** on the **same row** (substitute spaces in **E** with underscores for the filename). When **appending** new rows via API, either (a) **write the same formula shape** with the correct **row number** after you know the inserted row, or (b) leave **K** blank until images exist, then paste the formula pattern from a neighboring row and let Sheets adjust row refs.
- **L–R, T:** Leave **empty** for fresh chips (owner email, onboarding, planting, geo, video, seedling photo, price) unless the operator explicitly wants defaults.
- **S:** `Product Image` URL if the operator reuses a standard product shot.
- **U / V:** `Manager Name` and **`Ledger Name`** (e.g. **AGL4** with **CC** rows, **AGL8** with **CT** rows) when those conventions apply.

**Width:** New rows are often written as **22 columns A–V** so the tab stays aligned with existing blocks.

---

## 3. Operator workflow (manual)

1. Pick **product line** (**CC** vs **CT**) and an **existing template row** (same **B/C/I** / ledger family) — e.g. prior **Austin** **`SAMPLE`** rows for that line.
2. **Insert** new rows; set **A** to new ids; **copy E–H** from that template (farm, state, country, year); set **J** to today’s batch date if appropriate.
3. **Clear** any columns that were filled **after** a chip was sold or onboarded (owner email, planting dates, review dates, etc.) so new rows match **pre-sale** expectations.
4. If **D** is **`GIFT`**, still reset post-sale columns the same way.
5. **Column K:** Use the same **compiled_** GitHub URL pattern as sibling rows once **A** and **E** are set.

---

## 4. Local image generation (`batch_compiler.py`)

- **Repo path:** `tokenomics/python_scripts/agroverse_qr_code_generator/`
- **Credentials:** `gdrive_key.json` in that directory (service account with **Sheets** access; **gitignored** — obtain from operator; never commit).
- **Venv:** `source /Users/garyjob/Applications/tokenomics/python_scripts/venv/bin/activate` (or project venv with `google-api-python-client`, `google-auth`, `qrcode`, `Pillow`).
- **Optional:** Clear **`package_qr_codes/to_print/*.png`** so only **new** compiles are obvious; the script also writes to **`package_qr_codes/`** and skips rows whose **`compiled_{farm_name}_{qr_code}.png`** already exists in **`package_qr_codes/`** (not only `to_print`).
- **Example command** (paths relative to `agroverse_qr_code_generator/`):

```bash
cd /Users/garyjob/Applications/tokenomics/python_scripts/agroverse_qr_code_generator
source /Users/garyjob/Applications/tokenomics/python_scripts/venv/bin/activate
python3 batch_compiler.py \
  --credentials gdrive_key.json \
  --sheet-url "https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/" \
  --sheet-name "Agroverse QR codes" \
  --output-dir package_qr_codes \
  --box-size 12 \
  --border 8 \
  --logo-ratio 0.25 \
  --font-family "/System/Library/Fonts/Helvetica.ttc" \
  --auto-continue
```

- **Output filenames:** `compiled_{farm_name}_{qr_code}.png` with **`farm_name`** from column **E** (spaces → underscores in the file name). **Farm / state / country** must stay within a reasonable length for the label (the compiler centers text; very long **E–G** can overflow the template).

---

## 5. Automation notes (for agents)

- **Sheets API:** `google.oauth2.service_account` + `googleapiclient.discovery.build('sheets','v4')` with scope **`https://www.googleapis.com/auth/spreadsheets`**. **Append** `A:V` rows, then **`values.update`** column **K** with row-specific formulas if you are not pasting formulas in the first pass.
- **Before bulk-adding ids:** Query column **A** for duplicates.
- **After compile:** Commit **`package_qr_codes/*.png`** to **`TrueSightDAO/tokenomics`** when the operator wants GitHub URLs in **K** to resolve; CI or other pipelines may also apply.

---

## 6. Related docs

- **`agentic_ai_context/NOTES_tokenomics.md`** — clasp, Stripe **P**, and **Agroverse QR codes** tab bullets.
- **`agentic_ai_context/WORKSPACE_CONTEXT.md`** — workspace-wide tokenomics / **I** ↔ **`Currencies`!A** pointer.
- **`tokenomics/SCHEMA.md`** — column-by-column **`Agroverse QR codes`** definition.
