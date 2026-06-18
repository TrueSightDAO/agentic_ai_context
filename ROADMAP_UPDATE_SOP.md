# SOP: Updating the Live Track Map (Roadmap)

> **Standard operating procedure** for updating the active track map at **truesight.me/roadmap**.
> Follow this whenever a governor says "update the roadmap" or "update the track map."

---

## 1. Where the data lives

| Layer | Location | Purpose |
|-------|----------|---------|
| **Source of truth** | `agentic_ai_context/TRACK_MAP.md` | Human-readable track map with dependency diagram, detail tables, and quick reference. Edit this first. |
| **JSON data** | `agentic_ai_context/tracks.json` | Machine-readable track data. The website loads this via `fetch()`. Must stay in sync with TRACK_MAP.md. |
| **Static HTML** | `truesight_me_beta/roadmap/index.html` | The rendered page. Embeds the Mermaid diagram and track cards. Update only when the layout changes, not for data changes. |
| **Attachments** | `.github/attachments/` | Screenshots, receipts, evidence referenced by tracks. Upload here and link from the track data. |

---

## 2. When to update

- A track status changes (e.g. Gate → Blocked, Blocked → In Progress, Offline → Active)
- A new track is added (new partner, new initiative, new blocker)
- A track is completed (move to "Completed" section or remove)
- A next check-in date passes and needs updating
- A governor explicitly says "update the roadmap"

---

## 3. How to update (step by step)

### 3.1. Gather current state

Before making changes, check the current state of each track:

1. **Read `TRACK_MAP.md`** — understand the current dependency diagram and track details
2. **Check open PRs** on relevant repos — are there new PRs that change a track's status?
3. **Check email/Telegram** — are there new introductions, meeting invites, or blockers?
4. **Ask the governor** — if anything is unclear, ask before changing

### 3.2. Edit the source of truth

Make changes to `agentic_ai_context/TRACK_MAP.md` via a PR:

```
repo: agentic_ai_context
branch: feat/update-track-map-YYYY-MM-DD
```

**What to update:**

| Element | How to update |
|---------|---------------|
| **Mermaid diagram** | Add/remove nodes and arrows. Use CSS classes: `gate` (red), `blocked` (amber), `offline` (gray), `new` (blue). |
| **Quick reference table** | Add/remove rows. Update status, owner, next check-in, blocker columns. |
| **Track detail cards** | Add/remove sections. Update goal, status, owner, next milestone, dependencies, blocks, key docs. |
| **Last updated date** | Change the date at the bottom of the file. |

**When adding a new track:**
- Add a node in the Mermaid diagram with the correct CSS class
- Add a row in the quick reference table
- Add a detail card section with all fields filled
- Link to key docs in agentic_ai_context or `.github/attachments/`

**When marking a track as completed:**
- Remove its node from the Mermaid diagram (or move to a "Completed" section)
- Remove its row from the quick reference table
- Remove its detail card (or move to a "Completed Tracks" section at the bottom)

### 3.3. Update the JSON data

After updating `TRACK_MAP.md`, update `agentic_ai_context/tracks.json` to match:

```json
{
  "last_updated": "2026-06-19",
  "tracks": [
    {
      "id": "brazil-export-entity",
      "name": "Brazil Export Entity (CNPJ / NF-e / CNAE)",
      "status": "gate",
      "owner": "Matheus / Paloma / Gary",
      "next_checkin": "~2026-06-26",
      "blocked_by": "Legal Entity Structuring",
      "blocks": ["Chocolate Subscription Delivery", "China / Aora Events", "Jul 10 Kopi Bar Tasting", "Chives Root", "Michael Johnson"],
      "goal": "Create new Brazilian CNPJ with correct CNAE...",
      "docs": ["BRAZIL_EXPORT_ENTITY_BRIEF.md"],
      "downstream_chain": "Matheus → Omega Services → SeaCoast Logistics → Kirsten"
    }
  ]
}
```

**Status values:** `gate`, `blocked`, `offline`, `new`, `active`, `completed`

### 3.4. Update the static HTML (if needed)

Only update `truesight_me_beta/roadmap/index.html` when:
- The page layout changes (new section, different card design)
- A new CSS class is needed for a status type
- The Mermaid theme or configuration changes

**Do NOT** update the HTML just for data changes — data changes go in `TRACK_MAP.md` and `tracks.json`.

### 3.5. Deploy

**Step 1: Merge to beta**
```
1. Merge PR on agentic_ai_context (TRACK_MAP.md + tracks.json)
2. If HTML changed: merge PR on truesight_me_beta
3. Governor reviews at beta.truesight.me/roadmap
```

**Step 2: Promote to production**
```
1. Governor says "promote to prod" or "sync to prod"
2. Call sync_beta_to_prod(prod_repo="truesight_me_prod")
3. If conflict: report to governor — do NOT force sync
```

---

## 4. Quick reference

| Action | Repo | Branch prefix | Files to change |
|--------|------|---------------|-----------------|
| Update track data | agentic_ai_context | `feat/update-track-map-*` | `TRACK_MAP.md`, `tracks.json` |
| Update page layout | truesight_me_beta | `feat/roadmap-layout-*` | `roadmap/index.html` |
| Add attachment | .github | `feat/add-attachment-*` | `attachments/*` |

---

## 5. Example: Governor says "update the roadmap"

1. **Ask** "What changed?" if not specified
2. **Read** current `TRACK_MAP.md` and `tracks.json`
3. **Make changes** via PR to agentic_ai_context
4. **Merge** PR
5. **Tell governor** "Updated. The changes will reflect on beta.truesight.me/roadmap. Want me to promote to prod?"
6. **On approval:** `sync_beta_to_prod(prod_repo="truesight_me_prod")`

---

*Last updated: 2026-06-19*
