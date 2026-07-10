# Autopilot — capability manifest (single-PR refactor)

**Status:** IN PROGRESS — single PR underway.
**Owner:** Gary Teh (+ AI sessions)
**Created:** 2026-05-28
**Convention:** Tracked roadmap required by `OPERATING_INSTRUCTIONS.md` §5 before implementation. Keep the **Resume tracker** current as the PR lands.

---

## 1. Goal (why this exists)

Adding a new autopilot tool currently means editing **four** places:

1. `app/tools/<name>.py` — the implementation.
2. `app/llm_client.get_tool_schemas` — append the JSON Schema.
3. `app/main._run_tool` — append a `if func_name == "..."` dispatch branch.
4. `app/roles.py` — add the tool name to each role's `tools` list.

This is where the 2026-05-28 `merge_pr` role-gating bug hid (the schema was in place but step 4 was missed for the `infrastructure` role, so the model invented a reason it couldn't merge). It's also why every PR that adds tools is bigger than it needs to be.

A capability manifest collapses the four-place edit to **one place per tool**: each tool module exports a `TOOL_SPEC` (or `TOOL_SPECS` for multi-tool modules) that declares its schema, handler, and default role set. The rest is auto-discovery.

---

## 2. Decisions locked

| Decision | Value | Notes |
|---|---|---|
| Manifest source of truth | `TOOL_SPEC` / `TOOL_SPECS` exported from `app/tools/<name>.py` | Code, not YAML — keeps it `from app.tools.x import TOOL_SPEC` introspectable + IDE-navigable + diffable, no separate file to drift. |
| Discovery | Walk `app.tools` package at import time | One pass, results memoised. |
| ToolSpec shape | `name`, `description`, `parameters` (JSON Schema dict), `handler` (callable or `None`), `default_roles` (set or `None`) | `handler=None` means the tool is dispatched by the legacy inline branch in `app/main._run_tool` (kept for the four orchestration tools). |
| Orchestration tools stay inline (this PR) | `submit_contribution`, `open_fix_pr`, `merge_pr`, `create_dao_submission` | Each has ~100–200 LOC of inline orchestration touching session state. Their `TOOL_SPEC` declares the schema + roles (so role-gating is automatic), but the actual call path stays in `_run_tool` until a future PR migrates them with a uniform `context` dict. |
| Role validation | At module load, raise if any role lists a tool name not in the registry | Catches typos like the `merge_pr` gap before they hit prod. |
| Legacy alias | Drop the old hardcoded `get_tool_schemas()` list | Single source of truth. |

---

## 3. Pre-flight checklist

- [x] `feat/google-aws-tools` (PR #57) merged + deployed — registry will be built on top of the post-merge tree.
- [x] All existing tools have unit tests covering at least the dispatch path (mocked).
- [x] Roles include the new google + gmail + aws tools (per the 2026-05-28 work).

---

## 4. PR-1 — single refactor PR

**Sequence inside the PR, each step independently verifiable:**

| Step | Work | Verifies |
|---|---|---|
| 1 | Add `app/tool_registry.py` with `ToolSpec` dataclass + `discover_tools()` + `get_registry()` + `dispatch(func_name, args, context)`. | Registry boots, returns a non-empty list when called from a test. |
| 2 | Migrate each simple-wrapper tool module to export `TOOL_SPEC` / `TOOL_SPECS`. Schema text moves verbatim from `llm_client.py` to the module. ~22 tools, ~12 modules. | The discovered tool name set === the prior hardcoded set. |
| 3 | Add `TOOL_SPEC` entries for the four orchestration tools (`submit_contribution`, `open_fix_pr`, `merge_pr`, `create_dao_submission`) with `handler=None`. Schemas still move out of `llm_client.py`. | Manifest knows about every tool, even the ones still inline-dispatched. |
| 4 | Replace `app/llm_client.get_tool_schemas` body with a registry call. | Existing schema snapshot test passes. |
| 5 | Replace `app/main._run_tool` body — for each tool name, if `TOOL_SPEC.handler` is set, call it with the context dict; otherwise fall through to the legacy inline branches. | Existing tests + a new dispatch-equivalence test pass. |
| 6 | Add `app/roles.py` startup validation: any role tool name not in the registry → raise at import. | New regression test asserts every role validates. |
| 7 | Tests: `tests/test_tool_registry.py` — discovery, dispatch, role validation, no schema drift. | Suite stays green. |
| 8 | `app/tools/README.md` — authoring guide for new tools: TOOL_SPEC shape, role-gating, worked example, where to add a test, when to choose `handler=None` (orchestration). | New tool authors don't need to read this roadmap to know what to write. |

---

## 5. Risks & foot-guns

1. **Schema drift.** Moving schemas from one giant list to many modules — easy to miss a field. Mitigation: snapshot the prior schema list before the move; after migration, assert the new auto-discovered list deep-equals the snapshot.
2. **Import order.** `discover_tools()` imports every tool module at module load. Any top-level side effect (e.g. logging config, env reads) runs during discovery. Mitigation: each tool module's top-level remains import-safe today — verified by the existing `pytest` collection step. No new side effects introduced.
3. **Orchestration tool name in TWO places.** Until a follow-up PR moves their handlers, the four orchestration tools still need the legacy `if func_name == …:` branch AND a `TOOL_SPEC` entry. That's clearly worse than the simple ones (1 place) but still better than today (4 places). Out-of-scope to fully resolve here.
4. **Role-validation as fatal.** If a role manifest lists `tools=["typo_tool"]`, the autopilot won't boot. That's the **point** — production today already silently breaks, and this surfaces the break loudly at the right time (deploy, not in a Telegram exchange).

---

## 6. Out of scope (deliberate — see §7 of the user conversation 2026-05-28)

- **Claude skills adapter.** Skills are Anthropic-harness-shaped, not portable to a foreign tool-call loop at the granularity that would justify the adapter work.
- **OpenClaw plugin bridge.** Decision against OpenClaw is already on record (`feedback_openclaw_abandoned`; `AUTOPILOT_TELEGRAM_BETA_DEPLOY_PLAN.md` §1). Loading third-party JS into a process holding the GitHub PAT + governor RSA key + Google SAs + Gmail tokens + AWS creds is not mitigated by "separate Linux user".
- **`/skills` Telegram CRUD.** Reserved for a follow-up PR if/when manifest-driven role tweaks become a real operator need.
- **Orchestration-tool migration** (handler-on-spec for `submit_contribution` et al.). Follow-up.

---

## 7. Resume tracker

**RESUME HERE → Single PR in progress on `truesight_autopilot`.**

| Unit | PR | Merged | Deployed | Contribution reported |
|---|---|---|---|---|
| Roadmap (this file) | agentic_ai_context#TBD | ☐ | n/a | ☐ |
| PR-1 — capability manifest | truesight_autopilot#TBD | ☐ | ☐ | ☐ |
