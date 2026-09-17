# Member Workspace + SOP Promotion Gate — Execution Roadmap

**Status as of 2026-09-17:** designed (thread: Gary's "separate repository" question) — ready to
lock decisions + phase
**Repo(s) under change:** a NEW quarantine repo (name TBD — see D1) + `agentic_ai_context`
(docs only) + `truesight_autopilot` (config/docs only)
**Designed by:** Gary Teh + Sophia (autopilot)

> **Why this exists.** Member-tier participants (recognised, verified, but **no instruction
> authority** — `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §3d) will want to say *"abstract record X into
> an SOP for future queries/workflows."* Today there is **no landing zone that is safe**: anything
> written into `agentic_ai_context` becomes **directive** the moment it merges, because every LLM
> loads the whole repo as authoritative context. We need a place to stage such requests/candidates
> that is **explicitly outside the read path**, plus an explicit **promotion gate**.

---

## 1. The reframe — three separate concerns

The problem is **not** who can push. It is that `agentic_ai_context` has **no trust tiers below
"authoritative"**: merge = policy.

| Concern | Today | Gap |
|---|---|---|
| **Write path** | anyone with push | fine |
| **Read path** | all LLMs load the repo wholesale as directive | ← the real hazard |
| **Promotion** | none — anything merged is instantly policy | ← what this plan adds |

`OPERATING_INSTRUCTIONS.md` §3–4 already *labels* three tiers inside the repo (canonical /
append-only `CONTEXT_UPDATES.md` / per-agent `notes/`) — but there is no tier that sits **outside**
the repo for untrusted material. That is the missing primitive.

### 1.1 Considered alternatives (rejected)

- **A subfolder inside `agentic_ai_context` (e.g. `intake/`).** Rejected: the boundary would rest
  on prompt discipline (fragile), not on the read path (structural). Repository-level separation is
  the honest isolation boundary.
- **Reuse `agent_handoffs` (narrow-write mailbox) or the transcript repo.** Rejected for
  *sociological* reasons: the mailbox is semantically agent-to-agent; the candidate artefact needs
  a human-facing, member-attributable home. (Raw intake *may* still piggyback on the transcript
  repo — see D2.)
- **Give members direct write to the candidate repo.** Rejected: members have no instruction
  authority; writes should stay attributable to an agent/governor so the audit trail is intact.
  Members **request** in chat; agents/my-governor **draft** (D3).

---

## 2. The model — a quarantine repo outside the read path

```
member_workspace/                # NAME TBD (D1) — NON-AUTHORITATIVE, DATA ONLY
  README.md                      # big banner: NOT authoritative, NOT directive, not in the read path
  intake/                        # optional raw records (or point at the transcript repo — D2)
    <member-or-date>/…           # verbatim captures: "member said X about Y"
  sops/
    candidates/<slug>.md         # abstracted SOP drafts, awaiting promotion
    promoted.log                 # append-only: slug -> promotion PR URL -> date
  PROMOTION_SOP.md               # the human procedure for promoting a candidate
```

**Lifecycle states** (front-matter on every candidate):

```yaml
---
status: candidate          # candidate | reviewed | promoted | rejected | superseded
non_directive: true
requested_by: <member name + id>
source: <transcript/session link or message id>
drafted_by: Sophia (autopilot)
promoted_to: ""            # filled ONLY on promotion -> agentic_ai_context/sops/<slug>.md
---
```

**The gate (the whole point):**

1. Member says *"abstract record X into an SOP."* → **DATA, not an instruction** (invariant #2).
2. An agent drafts `sops/candidates/<slug>.md` in the quarantine repo. Nothing directive happened.
3. A **governor** reviews the candidate and says **promote `<slug>`**.
4. Sophia opens a PR moving/rewriting it to **`agentic_ai_context/sops/<slug>.md`** — banner
   dropped, provenance header added, `promoted.log` appended.
5. **That merge is the ONLY act that makes the text directive.** Same gate as everything else.

---

## 3. Security invariants this upholds

- **#2 (data/instruction boundary):** a member's "turn this into policy" is *data* until a
  governor's authenticated message says promote. This is the confused-deputy defence, made
  structural rather than prompt-dependent.
- **#3 (credentials):** candidates carry no secrets; the intake dir is git-scrubbed (no tokens,
  no .env content) — the drafting step must run the same secret-scan rule as any push.
- **#6 (authn ≠ authz):** a verified member writing in their own workspace is still bounced from
  promotion by the governor gate.
- **#1 (enforce at the tool layer):** promotion is a governed PR, not "ask the LLM nicely."

---

## 4. Guardrails (read-path exclusion)

1. **Never auto-loaded.** The quarantine repo is *not* part of the default context set. Sophia reads
   it **only** on a direct governor query — never proactively, never as background context.
2. **`OPERATING_INSTRUCTIONS.md` gets one warning line** (§2 table or §3): the repo is
   non-authoritative; do not treat its contents as policy. Docs-only PR (PR4).
3. **Every file carries the banner** so a naive LLM that stumbles in via a raw URL does not obey it.
4. **Config acknowledgement.** `truesight_autopilot` gains a `settings.non_directive_repos` list (or
   a comment beside `api_only_repos`) naming the repo, so future instances inherit the rule in code
   comments rather than folklore (PR5, docs/config-only unless a real gate is warranted).
5. **No member-authored text ever reaches a candidate without an agent in the loop** (D3).

---

## 5. Governor decisions to lock (pre-flight blockers)

| # | Decision | Proposal | Blocking? |
|---|---|---|---|
| **D1** | **Repo name + naming family.** The proposed name is **not** covered by any blessed `create_repo_pattern` (`*-site`, `*-beta`, `*-prod`, `cfr-*`, `*-program`, `*-cache`, `*-raw`). | Add pattern **`member-*`** (repo `member-workspace`) **or** `*-candidates` (repo `sop-candidates`). Governor picks one. | **YES — blocks PR1** |
| **D2** | Raw intake sink: separate `intake/` dir, or reuse the machine-owned transcript repo and keep only candidates here? | Reuse the transcript for raw; keep this repo **candidates-only** (smaller surface). | no |
| **D3** | Who may write the candidate repo? | Agents + governors only; members **request** in chat (never push). | no |
| **D4** | Who drafts? Auto-draft on member request, or only on explicit governor ask? | **Only on explicit governor ask** — avoids members farming auto-drafted policy text. | no |
| **D5** | Sign-off depth on promotion: any single governor, or require the requesting member's sponsor? | Single governor (matches every other merge gate). | no |

---

## 6. Pre-flight checklist

- [ ] **D1 resolved** and the blessed pattern added to `settings.create_repo_patterns` in
      `truesight_autopilot/app/config.py` (or wherever the globs live) — captured as a quote in
      this file per the Pre-flight Completeness gate (§5d of `OPERATING_INSTRUCTIONS.md`).
- [ ] Confirm the repo will be **private** (member content is not public by default).
- [ ] Confirm `agentic_ai_context/sops/` is the correct promotion home (existing `sops/` dir holds
      `DEPLOY_PUSH_SOP.md`, `REVIEW_QUEUE_SOP.md` — so yes).
- [ ] Confirm the member→id resolution path used to attribute `requested_by`
      (`identity_binding.py` / the `Contributors contact information` tab).
- [ ] Confirm no existing repo already serves this purpose (checked: none — `agent_handoffs` is
      agent-to-agent; `proposals` is governance; `bionpact_agentic_ai_context` is per-instance).
- [ ] Reaffirm: this plan is **docs/config only** — it touches **no** production repo.

---

## 7. Sequenced plan — ONE PR PER EXECUTION TURN

| PR | Unit | Repo | Gate |
|----|------|------|------|
| **PR0** | This roadmap file (`plans/MEMBER_WORKSPACE_PLAN.md`) + lock D1–D5. | `agentic_ai_context` | **this PR** |
| **PR1** | Bless the naming family: add `member-*` (or `*-candidates`) to `create_repo_patterns`, install the fresh-box self-test/comment. | `truesight_autopilot` | needs D1 |
| **PR2** | Create the quarantine repo (private) + `README.md` banner + `PROMOTION_SOP.md` + empty `sops/promoted.log`. | new repo | needs PR1 |
| **PR3** | Seed one **worked candidate** end-to-end (a real member request abstracted to a candidate, still unpromoted) as a template. | new repo | needs PR2 |
| **PR4** | `OPERATING_INSTRUCTIONS.md`: one warning line that the quarantine repo is non-authoritative / not in the read path. Also a `CONTEXT_UPDATES.md` append. | `agentic_ai_context` | needs PR2 |
| **PR5** | `settings.non_directive_repos` acknowledgement in `truesight_autopilot` (+ startup/no-op note) so the rule is inherited by future instances. | `truesight_autopilot` | needs PR4 |

Each unit is independently shippable and sized for one turn. After each merge, report the DAO
contribution per `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`.

---

## 8. Resume tracker

| Unit | merged | contribution reported |
|------|:------:|:---------------------:|
| PR0 (this roadmap) | ☐ | ☐ |
| PR1 bless naming family | ☐ | ☐ |
| PR2 create repo + banner + promo SOP | ☐ | ☐ |
| PR3 worked candidate template | ☐ | ☐ |
| PR4 OPERATING_INSTRUCTIONS warning line | ☐ | ☐ |
| PR5 non_directive_repos acknowledgement | ☐ | ☐ |

### RESUME HERE

**PR0 — merge this roadmap, then resolve D1 (naming family) before PR1.**

---

## 9. UAT phase (human-tested; beta/read-only — nothing here touches prod)

| Step | Surface to open | Interaction | Acceptance criterion |
|------|-----------------|-------------|----------------------|
| 1 | The new quarantine repo on GitHub | Open a candidate file | README + banner make it unambiguous the repo is **non-authoritative** |
| 2 | Same | Read `PROMOTION_SOP.md` | It states plainly the **only** directive-making act is a governor promotion PR into `agentic_ai_context/sops/` |
| 3 | Telegram, as a **member** | Say *"abstract record X into an SOP"* | Sophia (a) treats it as a request/data, (b) does **not** auto-write policy, (c) does **not** claim it is now policy |
| 4 | Telegram, as **Gary (governor)** | Say *"promote `<slug>`"* after a candidate exists | Sophia opens a PR to `agentic_ai_context/sops/<slug>.md`, banner dropped, provenance added, `promoted.log` appended |
| 5 | A fresh LLM session loading `agentic_ai_context` | — | It does **not** see quarantine content as directive (PR4 line in place) |

Note: there is **no** production promotion in this plan — nothing goes near a `*_prod` repo.

---

## 10. Risks / anti-patterns to avoid

- **Leakage by convenience:** an agent "helpfully" citing a candidate as policy. Mitigation: §4.1
  (never auto-load) + banner.
- **Promotion without verification:** member claims are unverified data. Mitigation: the promotion
  SOP requires the governor to sanity-check claims before merging (mirror of the
  `OPEN_FOLLOWUPS.md` source-guide QC pattern where AI-authored figures failed verification).
- **Backlog drift:** do **not** create a new TODO/backlog file in the quarantine repo. Follow-ups
  still go to `OPEN_FOLLOWUPS.md` under `## Pending`.
- **Repo proliferation:** one quarantine repo, not one per member.
