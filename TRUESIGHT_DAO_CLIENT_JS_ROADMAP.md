# TrueSight DAO Client JS — Implementation Plan & Execution Roadmap

**Status:** PLANNING — roadmap committed, implementation not started.

**Convention:** This is the tracked roadmap required by `OPERATING_INSTRUCTIONS.md` §5 before any implementation code. Keep the **Resume tracker** current as each unit lands.

---

## Problem

Three front-end repos — **capoeira**, **butterfly-effect-club**, and **oracle** — each independently reimplement the same DAO protocol integration boilerplate:

| Component | Lines duplicated across 3 repos |
|-----------|-------------------------------|
| RSA-2048 keypair generation (Web Crypto API) | ~15 lines × 3 |
| `base64ToArrayBuffer` / `arrayBufferToBase64` / `base64ToBase64Url` | ~12 lines × 3 |
| `publicKeyToSlug()` (SHA-256 → base64url → `pk-` prefix) | ~8 lines × 3 |
| Canonical payload formatting (`[EVENT NAME]\n- Label: value\n...`) | ~20 lines × 3 |
| RSASSA-PKCS1-v1_5 / SHA-256 signing | ~15 lines × 3 |
| `FormData` + `fetch` POST to Edgar | ~10 lines × 3 |
| `localStorage` key management (`publicKey`, `privateKey`) | ~8 lines × 3 |
| **Total duplicated** | **~264 lines of identical logic** |

Every new front-end project (tribomirimbahia, aora, future credentialing UIs) will repeat this pattern from scratch unless we extract it into a shared library.

## Solution

A single **zero-dependency npm package** (`@truesight/dao-client`) that any front-end can import. One source of truth for:

- RSA-2048 keypair generation (Web Crypto API)
- Canonical payload formatting and signing
- Edgar submission (`POST /dao/submit_contribution`)
- Practitioner slug derivation (`publicKeyToSlug`)
- `localStorage` key management
- TypeScript types for all event payloads

---

## 1. Pre-flight Checklist

- [ ] **Decide repo home** — Where does the npm package live?
  - Option A: New repo `TrueSightDAO/truesight-dao-client-js` (clean separation, independent versioning)
  - Option B: `TrueSightDAO/dao_protocol/packages/dao-client-js/` (alongside the Python client, single source of truth for protocol tooling)
  - **Recommendation: Option B** — the Python client (`dao_client`) already lives in `dao_protocol`; adding a JS sibling keeps protocol tooling in one place. The `dao_protocol` README already references both.
- [ ] **npm org** — Publish under `@truesight/` scope (requires npm org setup if not done)
- [ ] **Package name** — `@truesight/dao-client` (mirrors the Python `truesight-dao-client` naming)
- [ ] **Version strategy** — Start at `0.1.0`, semver. First stable release = `1.0.0` after all three consumer repos are swapped.
- [ ] **License** — Same as `dao_protocol` (MIT suggested)
- [ ] **Build tool** — `tsup` or `esbuild` for ESM + CJS dual output. Zero runtime dependencies.
- [ ] **TypeScript** — Strict mode. Ship `.d.ts` types.
- [ ] **Browser target** — ES2020 (covers `crypto.subtle`, `fetch`, `FormData`, `localStorage`). No polyfills.
- [ ] **Testing** — Vitest for unit tests. No browser automation needed (pure JS crypto + string manipulation).

---

## 2. Library Design

### 2.1 API Surface

```typescript
// === Core ===

class DaoClient {
  // Key management
  static generateKeypair(): Promise<{ publicKey: string; privateKey: string }>;
  static loadFromStorage(): { publicKey: string | null; privateKey: string | null };
  static saveToStorage(publicKey: string, privateKey: string): void;
  static clearStorage(): void;

  // Instance (auto-loads from localStorage, generates if missing)
  constructor();
  get publicKey(): string;
  get privateKey(): string;

  // Signing
  sign(eventName: string, attributes: Record<string, string>): Promise<{
    canonicalPayload: string;
    requestTxnId: string;
    shareText: string;
  }>;

  // Submission
  submit(eventName: string, attributes: Record<string, string>, options?: {
    attachment?: File;
    generationSource?: string;
  }): Promise<SubmitResult>;

  // Slug / credential URL
  getSlug(): Promise<string>;
  getCredentialUrl(program?: string): Promise<string>;
}

// === Utilities ===

function publicKeyToSlug(publicKeyBase64: string): Promise<string>;
function base64ToArrayBuffer(b64: string): ArrayBuffer;
function arrayBufferToBase64(buf: ArrayBuffer): string;
function base64ToBase64Url(b64: string): string;

// === Types ===

interface SubmitResult {
  ok: boolean;
  status: number;
  body: any;
  requestHash?: string;
  slug?: string;
  error?: string;
}

interface Keypair {
  publicKey: string;
  privateKey: string;
}
```

### 2.2 Zero-Dependency Constraint

The package MUST have zero runtime dependencies. The Web Crypto API, `fetch`, `FormData`, `TextEncoder`, `btoa`/`atob`, and `localStorage` are all available natively in every modern browser and in Node 18+.

### 2.3 Module Structure

```
packages/dao-client-js/
├── package.json
├── tsconfig.json
├── tsup.config.ts
├── src/
│   ├── index.ts              # Public API — re-exports everything
│   ├── client.ts             # DaoClient class
│   ├── crypto.ts             # Key generation, signing, base64 helpers
│   ├── slug.ts               # publicKeyToSlug
│   ├── payload.ts            # Canonical payload formatting
│   ├── submit.ts             # Edgar submission (fetch + FormData)
│   ├── storage.ts            # localStorage key management
│   └── types.ts              # TypeScript interfaces
├── test/
│   ├── crypto.test.ts
│   ├── payload.test.ts
│   ├── slug.test.ts
│   └── client.test.ts
└── README.md
```

### 2.4 Tree-Shakeable

Each module is independently importable so consumers can tree-shake unused features:

```typescript
// Import just what you need
import { publicKeyToSlug } from '@truesight/dao-client/slug';
import { signPayload } from '@truesight/dao-client/payload';
```

---

## 3. Sequenced Plan

### PR0 — Roadmap (this file)

- [x] **Roadmap committed** — `agentic_ai_context#TBD`
- [ ] **Contribution reported** — `[CONTRIBUTION EVENT]` for roadmap creation

### PR1 — Core library package

**Repo:** `dao_protocol` (new `packages/dao-client-js/` directory)

**Deliverables:**
- [ ] `package.json` with `@truesight/dao-client` name, `tsup` build config, Vitest setup
- [ ] `src/crypto.ts` — `generateKeypair()`, `sign()`, `base64ToArrayBuffer()`, `arrayBufferToBase64()`, `base64ToBase64Url()`
- [ ] `src/slug.ts` — `publicKeyToSlug()` (SHA-256 → base64url → `pk-` prefix)
- [ ] `src/payload.ts` — `buildCanonicalPayload(eventName, attributes)`, `buildShareText(canonicalPayload, publicKey, signature, sourceUrl)`
- [ ] `src/submit.ts` — `submitToEdgar(shareText, attachment?)` → `POST /dao/submit_contribution`
- [ ] `src/storage.ts` — `loadKeys()`, `saveKeys()`, `clearKeys()` for `localStorage`
- [ ] `src/client.ts` — `DaoClient` class tying it all together
- [ ] `src/index.ts` — public re-exports
- [ ] `src/types.ts` — TypeScript interfaces
- [ ] Unit tests for crypto, payload, slug, and client
- [ ] `README.md` with full API docs and quick-start example
- [ ] Publish to npm (`npm publish --access public`)

**Migration:** None yet — this is the library itself.

- [ ] **PR merged**
- [ ] **Contribution reported**

### PR2 — Swap capoeira to use the library

**Repo:** `capoeira`

**Changes:**
- [ ] Add `@truesight/dao-client` as dependency (via CDN script tag or npm if build step exists)
- [ ] Replace `assets/js/practice-event-submit.js` inline helpers with library imports
- [ ] Remove duplicated: `base64ToArrayBuffer`, `arrayBufferToBase64`, `base64ToBase64Url`, `publicKeyToSlug`, `generateKeypair`, `ensureKeypair`, `signRequestText`, `buildPracticeEventText`
- [ ] Keep only the capoeira-specific logic: session object shape, `[PRACTICE EVENT]` attribute mapping, `backfillUnsent`
- [ ] Verify end-to-end: generate keypair → build payload → sign → submit → credential link appears

**Testing:** Manual practice session on `capoeira.agroverse.shop`

- [ ] **PR merged**
- [ ] **Contribution reported**

### PR3 — Swap butterfly-effect-club to use the library

**Repo:** `butterfly-effect-club`

**Changes:**
- [ ] Add `@truesight/dao-client` as dependency
- [ ] Replace inline key generation, signing, and submission with library calls
- [ ] Remove duplicated helper functions
- [ ] Keep butterfly-effect-club-specific logic: cohort roster loading, admin auth, `[CREDENTIALING ATTESTATION EVENT]` attribute mapping
- [ ] Verify end-to-end: admin sign-in → attestation → Edgar submission

**Testing:** Manual attestation on `butterfly-effect-club.truesight.me`

- [ ] **PR merged**
- [ ] **Contribution reported**

### PR4 — Swap oracle to use the library

**Repo:** `oracle`

**Changes:**
- [ ] Add `@truesight/dao-client` as dependency
- [ ] Replace `assets/js/oracle-draw-submit.js` inline helpers with library imports
- [ ] Remove duplicated: `base64ToArrayBuffer`, `arrayBufferToBase64`, `base64ToBase64Url`, `publicKeyToSlug`, `generateKeypair`, `ensureKeypair`, `signRequestText`, `buildPracticeEventText`
- [ ] Keep oracle-specific logic: reading permalink construction, `[PRACTICE EVENT]` attribute mapping (hexagrams, QMDJ card), `MutationObserver` for advisory panel, `sharedFromUrl` dedup
- [ ] Verify end-to-end: cast oracle → advisory appears → auto-submit → credential link appears

**Testing:** Manual cast on `oracle.truesight.me`

- [ ] **PR merged**
- [ ] **Contribution reported**

### PR5 — Migration guide + program-template update

**Repos:** `agentic_ai_context`, `program-template`

**Changes:**
- [ ] Write `DAO_CLIENT_JS_MIGRATION_GUIDE.md` in `agentic_ai_context` — step-by-step for any future front-end to adopt `@truesight/dao-client`
- [ ] Update `program-template` to use `@truesight/dao-client` by default (so new credentialing programs start with the library)
- [ ] Update `dao_protocol/INTEGRATION_GUIDE.md` to reference the JS library alongside the Python client

- [ ] **PR merged**
- [ ] **Contribution reported**

---

## 4. Resume Tracker

| Unit | PR | Status | Contribution | Notes |
|------|----|--------|-------------|-------|
| PR0 — Roadmap | agentic_ai_context#TBD | ✅ Committed | ☐ | This file |
| PR1 — Core library | dao_protocol#TBD | ☐ | ☐ | `packages/dao-client-js/` |
| PR2 — Swap capoeira | capoeira#TBD | ☐ | ☐ | Replace inline helpers |
| PR3 — Swap butterfly-effect-club | butterfly-effect-club#TBD | ☐ | ☐ | Replace inline helpers |
| PR4 — Swap oracle | oracle#TBD | ☐ | ☐ | Replace inline helpers |
| PR5 — Migration guide + template | agentic_ai_context#TBD + program-template#TBD | ☐ | ☐ | Docs + template update |

**RESUME HERE → PR1: Create the core library package in `dao_protocol/packages/dao-client-js/`**

---

## 5. API Reference (Detailed)

### `DaoClient` class

```typescript
class DaoClient {
  /**
   * Generate a new RSA-2048 keypair using Web Crypto API.
   * Keys are exported as SPKI (public) and PKCS#8 (private) base64 strings.
   */
  static generateKeypair(): Promise<Keypair>;

  /**
   * Load keys from localStorage.
   * Keys are stored under 'publicKey' and 'privateKey' keys.
   */
  static loadFromStorage(): { publicKey: string | null; privateKey: string | null };

  /**
   * Save keys to localStorage.
   */
  static saveToStorage(publicKey: string, privateKey: string): void;

  /**
   * Clear keys from localStorage.
   */
  static clearStorage(): void;

  /**
   * Create a new client instance.
   * Auto-loads keys from localStorage. If no keys exist, generates new ones.
   */
  constructor();

  /** The base64 SPKI public key. */
  get publicKey(): string;

  /** The base64 PKCS#8 private key. */
  get privateKey(): string;

  /**
   * Sign a canonical event payload.
   *
   * @param eventName - The event name, e.g. 'PRACTICE EVENT', 'CONTRIBUTION EVENT'
   * @param attributes - Key-value pairs of event attributes
   * @returns The canonical payload, request transaction ID, and full share text
   */
  sign(eventName: string, attributes: Record<string, string>): Promise<{
    canonicalPayload: string;
    requestTxnId: string;
    shareText: string;
  }>;

  /**
   * Sign and submit an event to Edgar.
   *
   * @param eventName - The event name
   * @param attributes - Key-value pairs of event attributes
   * @param options - Optional: attachment file, generation source URL override
   * @returns Submission result with status, body, and slug
   */
  submit(
    eventName: string,
    attributes: Record<string, string>,
    options?: {
      attachment?: File;
      generationSource?: string;
    }
  ): Promise<SubmitResult>;

  /**
   * Derive the practitioner slug from the public key.
   * slug = "pk-" + base64url(SHA-256(publicKeyBytes)).slice(0, 12)
   */
  getSlug(): Promise<string>;

  /**
   * Get the full credential URL for a program.
   * Default program: 'truesight-grounding'
   */
  getCredentialUrl(program?: string): Promise<string>;
}
```

### Utility Functions

```typescript
/**
 * Derive a practitioner slug from a base64-encoded SPKI public key.
 *
 * @param publicKeyBase64 - The base64-encoded public key
 * @returns The slug, e.g. "pk-a1b2c3d4e5f6"
 */
function publicKeyToSlug(publicKeyBase64: string): Promise<string>;

/**
 * Convert a base64 string to an ArrayBuffer.
 */
function base64ToArrayBuffer(b64: string): ArrayBuffer;

/**
 * Convert an ArrayBuffer to a base64 string.
 */
function arrayBufferToBase64(buf: ArrayBuffer): string;

/**
 * Convert a base64 string to a base64url string (no padding).
 */
function base64ToBase64Url(b64: string): string;
```

### Types

```typescript
interface SubmitResult {
  /** Whether the submission was successful (HTTP 200) */
  ok: boolean;
  /** HTTP status code */
  status: number;
  /** Parsed response body */
  body: any;
  /** The request transaction ID (RSA signature) */
  requestHash?: string;
  /** The practitioner slug derived from the public key */
  slug?: string;
  /** Error message if submission failed */
  error?: string;
}

interface Keypair {
  publicKey: string;
  privateKey: string;
}
```

---

## 6. Migration Guide (for consumer repos)

### Before (current pattern in all 3 repos)

Each repo has a `practice-event-submit.js` or `oracle-draw-submit.js` that contains:

```javascript
// ~80 lines of duplicated boilerplate
function base64ToArrayBuffer(b64) { ... }
function arrayBufferToBase64(buf) { ... }
function base64ToBase64Url(b64) { ... }
async function publicKeyToSlug(pub) { ... }
async function generateKeypair() { ... }
async function ensureKeypair() { ... }
async function signRequestText(text) { ... }
function buildPracticeEventText(session, opts) { ... }
```

### After

```javascript
import { DaoClient, publicKeyToSlug } from '@truesight/dao-client';

const client = new DaoClient();

// Build event-specific attributes
const attributes = {
  'Program': 'capoeira-tribo-mirim',
  'Practice Type': 'training-session',
  'Practitioner Public Key': client.publicKey,
  'Captured At': session.completedAt,
  'Payload JSON': JSON.stringify(payload, null, 2),
};

// Submit — one call replaces ~80 lines
const result = await client.submit('PRACTICE EVENT', attributes);

// Get credential URL
const cvUrl = await client.getCredentialUrl('tribomirim');
```

### Step-by-step for each repo

1. Add the library (CDN script tag for static HTML sites, npm install for build-step projects)
2. Import `DaoClient` at the top of the submission module
3. Replace all helper functions with library calls
4. Keep only event-specific logic (attribute mapping, session object shape)
5. Test end-to-end

---

## 7. CDN Distribution (for static HTML sites)

Capoeira, oracle, and butterfly-effect-club are all static HTML sites (no build step). The library must be available via CDN:

```html
<!-- ES Module (modern browsers) -->
<script type="module">
  import { DaoClient } from 'https://cdn.jsdelivr.net/npm/@truesight/dao-client@0.1.0/dist/index.mjs';
</script>

<!-- IIFE (legacy) -->
<script src="https://cdn.jsdelivr.net/npm/@truesight/dao-client@0.1.0/dist/index.global.js"></script>
```

The `tsup` build config must output:
- `dist/index.mjs` — ESM
- `dist/index.cjs` — CommonJS
- `dist/index.global.js` — IIFE (window.TruesightDaoClient)

---

## 8. Future Considerations

- **Node.js support** — The library already works in Node 18+ (Web Crypto API, `fetch`, `FormData` are all native). No changes needed.
- **React Native** — May need polyfills for `crypto.subtle`. Not a priority.
- **Deno / Bun** — Should work out of the box (both implement Web Crypto API and `fetch`).
- **Event type constants** — Future PR could add typed constants for all event names and attribute keys, reducing typos.
- **Auto-generated TypeScript types from dao_protocol** — Long-term, the event schemas in `dao_protocol/INTEGRATION_GUIDE.md` could generate TypeScript types automatically.

---

## 9. Appendix: Duplicated Code Inventory

### capoeira (`assets/js/practice-event-submit.js`)

| Function | Lines | Notes |
|----------|-------|-------|
| `base64ToArrayBuffer` | 4 | Identical across all 3 |
| `arrayBufferToBase64` | 4 | Identical across all 3 |
| `base64ToBase64Url` | 3 | Identical across all 3 |
| `publicKeyToSlug` | 5 | Identical across all 3 |
| `generateKeypair` | 10 | Identical across all 3 |
| `ensureKeypair` | 6 | Identical across all 3 |
| `getStoredPublicKey` | 2 | Identical across all 3 |
| `getCvUrl` | 5 | Identical across all 3 |
| `buildPracticeEventText` | 20 | Capoeira-specific (session object) |
| `signRequestText` | 12 | Identical across all 3 |
| `submitSession` | 30 | Capoeira-specific (history backfill) |
| `backfillUnsent` | 15 | Capoeira-specific |

### butterfly-effect-club (`index.html` inline scripts)

Similar pattern — key generation, signing, and submission inlined in the admin console HTML.

### oracle (`assets/js/oracle-draw-submit.js`)

| Function | Lines | Notes |
|----------|-------|-------|
| `base64ToArrayBuffer` | 4 | Identical |
| `arrayBufferToBase64` | 4 | Identical |
| `base64ToBase64Url` | 3 | Identical |
| `publicKeyToSlug` | 5 | Identical |
| `generateKeypair` | 10 | Identical |
| `ensureKeypair` | 6 | Identical |
| `getStoredPublicKey` | 2 | Identical |
| `getCvUrl` | 5 | Identical |
| `buildPracticeEventText` | 30 | Oracle-specific (hexagrams, QMDJ) |
| `signRequestText` | 12 | Identical |
| `submitSession` | 45 | Oracle-specific (advisory observer, dedup) |
| `buildReadingPermalink` | 15 | Oracle-specific |

### Total duplicated lines that move to the library: **~88 lines**

---

## 10. Changelog

| Date | Change |
|------|--------|
| 2026-06-07 | Initial roadmap created |
