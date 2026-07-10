# Oracle Credentials Link Fix — Execution Roadmap

## Problem

The oracle page (oracle.truesight.me) has a `#credentialsSection` with a "My Credentials →" link (`#cvLink`) that points to `truesight.me/programs/truesight-grounding/credentials/#<slug>`, but the section is never unhidden. The `showVerifiedState()` function sets the link href but never shows `#credentialsSection`.

Additionally, there's a `#daoIdentityLinkedPanel` that also has a credentials link (`#daoIdentityCvLink`), but that one is explicitly hidden in `showVerifiedState()` with `daoIdentityCvLink.hidden = true`.

## Root Cause

In `index.html`, the `showVerifiedState()` function:
1. Sets `cvLink.href` and `cvLink.hidden = false` — correct
2. Sets `daoIdentityCvLink.hidden = true` — intentional, only one link
3. Shows `daoIdentityLinkedPanel` — but this panel doesn't show the link
4. **Never unhides `#credentialsSection`** — the section containing the link stays hidden

## Fix

In `showVerifiedState()`, add `credentialsSection.hidden = false` after setting the cvLink href.

## Sandbox Testing Environment

To prevent future regressions, set up a JSDom-based local test suite for the oracle page:

### Tools
- **Vitest** (already in dao_protocol) + **happy-dom** (already a devDep)
- Tests live in `oracle/test/` directory

### Test Plan

1. **Unit tests for JS functions** (no DOM):
   - `linesToSignature()` / `signatureToReading()` round-trip
   - `getHexagram()` with known line patterns
   - `buildReadingPayload()` shape
   - `createShareUrl()` format
   - `formatHexagramTitle()` output

2. **DOM tests with happy-dom**:
   - `showVerifiedState()` unhides `#credentialsSection`
   - `showPendingState()` shows correct message
   - `applyLinkedUI()` sets `#cvLink` href correctly
   - `handleReset()` hides all panels
   - `updateLastReadingUI()` shows/hides elements

3. **Integration test**:
   - Load `index.html` in happy-dom
   - Simulate a full cast → verify results section appears
   - Simulate DAO identity link → verify credentials link appears

### Implementation

```bash
cd oracle
npm init -y
npm install vitest happy-dom
```

Test file: `oracle/test/credentials.test.js`

### Pre-flight Checklist

- [ ] Confirm oracle repo has a `package.json` (or create one)
- [ ] Install vitest + happy-dom
- [ ] Extract JS functions from inline `<script>` into a testable module (or test via DOM evaluation)
- [ ] Write unit tests for core functions
- [ ] Write DOM tests for showVerifiedState / showPendingState
- [ ] Run `npx vitest run` — all pass
- [ ] Apply the fix (unhide credentialsSection)
- [ ] Run tests again — still pass
- [ ] Open PR with fix + tests

### Resume Tracker

| Step | Status |
|------|--------|
| Pre-flight: check oracle repo structure | ☐ |
| Set up vitest + happy-dom in oracle/ | ☐ |
| Write unit tests for core functions | ☐ |
| Write DOM tests for UI state functions | ☐ |
| Apply the fix (unhide credentialsSection) | ☐ |
| Run full test suite — green | ☐ |
| Open PR with fix + tests | ☐ |
| Merge after review | ☐ |

**RESUME HERE** → Pre-flight: check oracle repo structure
