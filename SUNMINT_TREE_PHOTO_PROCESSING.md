# SunMint Tree & Boundary Photo Processing — distinct trees, 4 corners, submission contracts

> **Purpose:** the one place future Sophias / other LLM agents learn how to turn a batch of
> farmer tree-planting photos into (a) a count of **distinct trees** with one chosen photo each,
> (b) a **4-corner plot boundary**, and (c) well-formed `[TREE PLANTING EVENT]` and
> `[FARM BOUNDARY EVIDENCE EVENT]` submissions that parse cleanly end-to-end.
> Codified from the **2026-09-02/03 Fazenda Bom Sucesso** session (Gary + Sophia).

## 0. TL;DR

1. Get **GPS-bearing originals** (HEIC/container files, not recompressed JPGs).
2. Dedupe by md5; extract GPS with exiftool (watch the hemisphere trap).
3. Cluster into trees by **capture time** (Gary's dig-time rule), not distance alone.
4. Pick one photo per tree — **smiley faces preferred**.
5. Corners = the 4 GPS extremes; match stripped JPGs to GPS originals by pixel compare.
6. Submit with the **exact contracts** below — never an empty `Plot ID`; always both `Location` AND `Latitude`/`Longitude` for trees.

## 1. Getting GPS-bearing originals

- **Telegram / WhatsApp strip EXIF/GPS from recompressed photos.** A JPG that arrives as a
  Telegram "photo" is ~960×1280 and carries **zero GPS** (verified live: `exiftool` finds no
  GPS tags on all 14 recompressed JPGs).
- **Container originals (HEIC/MOV) sent as files keep GPS** — iPhone HEIC sent through the same
  Telegram bot arrived with full GPS (iPhone 12 Pro Max, `GPSLatitude`/`GPSLongitude` present).
- **Safest channels** (documented in SUNMINT_PLOTS_REGISTRY.md §3): email attachment,
  WhatsApp "Document", Drive, or scp — EXIF survives those reliably.
- **Verify before processing:**
  ```bash
  exiftool -GPSLatitude -GPSLongitude -DateTimeOriginal -Make -Model <files...>
  ```

## 2. EXIF extraction gotchas (each cost real time)

1. **DMS → decimal, S/W negative:** `3 deg 17' 45.96" S` → `-3.29610`, `52 deg 34' 59.39" W` → `-52.58316`.
2. **The `exiftool -s` hemisphere trap:** with `-s`, the hemisphere letter is folded INTO the
   value string (`...S`), while `GPSLatitudeRef` reads `South` (full word). A naive
   `ref in ('S','W')` check against the `-s` output **never fires** → you get positive coords
   for a southern/western plot. Parse the trailing hemisphere char off the value, or read the
   `Ref` fields with full words, or drop `-s`.
3. **Random-name re-uploads:** the same photo often arrives multiple times with random names.
   Dedupe by md5 **before** clustering; otherwise the count inflates (59 files → 24 unique).
4. **Never trust the filename** — use embedded `DateTimeOriginal` + GPS for everything.

## 3. Distinct-tree heuristic (Gary's dig-time rule — 2026-09-02)

> "Another way to decipher if the trees are distinct besides distance is to check how much
> time their photos are taken apart — since it takes time to dig a hole." — Gary Teh

### Rule
1. **Sort all tree photos by capture time.**
2. **Cluster by TIME first:**
   - photos **≤ ~60–90 s apart** at the same spot → **same tree** (you cannot dig a hole in
     under a minute) → merge, keep the best photo.
   - photos **minutes apart** (≥ ~5 min, or with other plantings in between) even at ~2 m
     separation → **distinct digging events** → keep as separate trees.
3. **Distance is a secondary signal only:** < ~3 m is inside phone GPS noise (~2–5 m), so it
   cannot disambiguate alone. Use it only to *corroborate* the time verdict.

### Worked example (Fazenda Bom Sucesso, 10 trees)
| Pair | Gap | Time apart | Verdict |
|---|---|---|---|
| 193eca20 ↔ 1d6a3a4c | 1.4 m | **11 s** | ⛔ same tree, two photos → merge |
| 95dd596c ↔ a9cf65d0 | 2.0 m | **11 m 21 s** (other tree in between) | ✅ distinct (two digging events) |
| 2c364eb3 ↔ b08309c1 | 2.2 m | **20 m 24 s** (3 trees in between) | ✅ distinct |
| all others | ≥ 7 m | 4–6 min | ✅ distinct |

Distance-only clustering over-splits (gave 14 clusters); the **time rule gives exactly 10** —
the number the farmer reported.

## 4. Photo selection — smiley-face preference

- When a tree has multiple photos and the farmer says people are in some shots, **prefer the
  photo(s) with smiling faces**.
- Tooling notes:
  - **cv2 5.x removed `CascadeClassifier`** — install `opencv-python-headless==4.10.0.84` in a
    venv (`python3 -m venv /tmp/smileenv`) for haarcascade face/smile detection.
  - HEIC needs `pillow_heif` (system python) — convert to PNG first, then detect from the venv.
  - **Low-light sapling photos defeat the smile cascade** even when faces are found → fall back
    to face-count, then first-shot, then ask the farmer. Auto-smile detection is a hint, not gospel.

## 5. 4-corner identification (plot boundary)

- The farmer walks the 4 corners and photographs a marker at each.
- **Signature:** corner photos sit at the **extremes** of the GPS cloud (often taken before/after
  the tree walk). A bounding box of all points → the 4 corners are near its corners.
- If the corners arrived as **GPS-less recompressed JPGs** but the originals exist as
  **GPS-bearing HEICs**, match them by **pixel comparison** (mean abs diff ~2/255 ≈ identical)
  and use the HEIC's GPS. (Method: resize both to a common size, mean of per-pixel abs diff.)
- Build the polygon as the **convex hull** (or corner order) of the 4 points → closed
  `[lng, lat]` ring → boundary authority **`approx`** until a walk/CAR/INCRA upgrades it.
- Sanity: all tree points should fall inside the polygon; flag outliers for the farmer
  (Fazenda Bom Sucesso: 1 of 10 trees sat ~48 m outside → asked whether the boundary or the
  tree is wrong).

## 6. Submission contract — [FARM BOUNDARY EVIDENCE EVENT]

Used by the `limites-da-fazenda` page. **Two traps that bit us — do not repeat:**

1. **NEVER send an empty `- Plot ID:` line.** The GAS parser regex
   `- Plot ID:\s*([^\n]+)` matches newlines in `\s*`, so an empty value swallows the line break
   and captures the NEXT label (we got `Plot ID = "- Boundary Type: approx"` — a mangled row,
   invalidated later). **Omit Plot ID entirely** when unknown → the backend auto-assigns `PL-###`.
   (Parser fixed in tokenomics #458 — `\s*` → `[ \t]*` — so empty fields now parse as `""`.)
2. **`Media URLs` are joined with `; `** (semicolon-space), not commas.

Canonical field order (match the live UI):
```
[FARM BOUNDARY EVIDENCE EVENT]
- Farm Name: <name>
- Is New Farm: yes|no
- Media URLs: <file1; file2; ...>        (raw github URLs or names, '; ' joined)
- Media Count: <n>
- Captured At: <ISO timestamp>
- Device GPS: <json>
- Submission Source: sunmint-limites-da-fazenda | autopilot-sophia
--------
```
Attach the **actual photo files** when possible (Edgar mirrors them to
`sunmint/images/boundaries/`); otherwise pass raw
`https://raw.githubusercontent.com/TrueSightDAO/sunmint/main/images/...` URLs.

## 7. Submission contract — [TREE PLANTING EVENT]

Used by sunmint `index.html` / `report_tree_planting.html`. **The dual-field requirement:**

- Edgar's **canonical validator** requires `Tree Count` + `Location` — without `Location` the
  submission is rejected: "Missing required fields for TREE PLANTING EVENT: Location".
- The **GAS parser** (`process_tree_planting_telegram_logs.gs`) fills Latitude (col K) /
  Longitude (col L) from `- Latitude:` / `- Longitude:` **lines in the rendered text**.
- → **Send BOTH**: canonical `Location` AND `Latitude`/`Longitude` attributes, plus the rest:
```
[TREE PLANTING EVENT]
- Tree Count: 1
- Location: "<lat>, <lng>"            (canonical — satisfies validator)
- Latitude: <decimal>                  (parser → col K)
- Longitude: <decimal>                 (parser → col L)
- Species: <species>                   (parser → col N)
- Planter: <name>                      (canonical)
- Planting Time: <ISO 8601>            (parser → col Q)
- Photo URL: https://raw.githubusercontent.com/TrueSightDAO/sunmint/main/images/<file>.jpg
- Submission Source: autopilot-sophia | dapp | farmer-app
--------
```
- **Species vocabulary is inconsistent in the wild** (`Cacau - Hybrid` pt vs `Cacao - Criolla`
  en vs bare `Cacao`). Standardize per-farm and note the exact string in the ledger. For
  Fazenda Bom Sucesso Gary specified **`Cacau - Hybrid`** for all 10.
- Photo: convert HEIC → JPEG (pillow_heif), upload to `sunmint/images/`, use the raw URL above
  (the parser's photo column and the GitHub commit URL column expect this pattern).
- Rows land in **`SunMint Tree Planting`** tab (dedup key = Telegram Message ID, col D), Status
  `NEW`; the GAS cron scans `Telegram Chat Logs` col G for the `[TREE PLANTING EVENT]` marker
  (async — propagation takes minutes).

## 8. Submission contract — [PLOT INVALIDATION EVENT]

Soft-invalidate only (never delete rows). Server-side gate: **retractor email must resolve to a
**governor or sentinel** in `dao_members.json` (Sophia = sentinel). Use for mangled/dup rows;
reason text should cite the superseding plot/event.

## 9. Verification checklist (after any submission)

- [ ] Edgar returned success (no "Missing required fields" rejection)
- [ ] Propagation: row appears in the destination tab after the async GAS cron run
- [ ] TREE PLANTING: Latitude/Longitude populated (not blank) → proves parser read the lines
- [ ] TREE PLANTING: Status `NEW`, species + photo URL present
- [ ] FARM BOUNDARY: plot row has a real `PL-###` id (not a swallowed label), farm name correct
- [ ] No duplicate rows from re-submission (dedup by Message ID / plot id)

## 10. Do / Don't

- **Do** dedupe by md5 first; sort by capture time; cluster by time, corroborate with distance.
- **Do** confirm hemisphere signs (S/W negative) before submitting — positive coords for a
  Brazilian farm are a bug.
- **Do** prefer smiley photos when the farmer mentions people; auto-detection is a hint.
- **Don't** send empty optional fields on FBE events (line-bleed); omit them entirely.
- **Don't** submit TREE PLANTING with only `Location` (parser gets blank lat/lng) or only
  `Latitude`/`Longitude` (validator rejects).
- **Don't** hand-edit ledger rows; use `[PLOT INVALIDATION EVENT]` for mangled rows.

## 11. Related

- `SUNMINT_PLOTS_REGISTRY.md` — plots registry, boundary tiers, schema
- `SUNMINT_E2E_RUNBOOK.md` — full SunMint pipeline map + incident traps
- `plans/SUNMINT_BOUNDARY_SUBMISSION_PLAN.md` — FBE pipeline roadmap (PR4 = catalog entry)
- `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` — TREE PLANTING → QR linking (schema cols)
- tokenomics PR #458 — the FBE parser line-bleed fix
