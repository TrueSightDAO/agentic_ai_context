# SunMint Mobile App (Android + iOS) — Execution Roadmap

**Status:** New. Not started.
**Owner:** Gary Teh.
**Requested by:** Gary Teh, 2026-08-23.
**Repo:** [`TrueSightDAO/sunmint_mobile`](https://github.com/TrueSightDAO/sunmint_mobile) (created, empty scaffold).
**Auto-start:** no — wait for governor's "go for it" in the handoff topic before touching code.

**Goal:** Give farmers a real, installable mobile app (Android first, iOS second) for the two things
`sunmint.truesight.me` already does — link an email, report a tree planting with a photo — that keeps
working with no internet connection, from **one shared codebase** that compiles to both platforms.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. Update the resume tracker as units land; report the DAO
> contribution after each merge (§6). §5a: **one PR per execution turn, then stop.**

---

## 0. Decisions (Gary, 2026-08-23)

| # | Decision | Choice |
|---|----------|--------|
| 0.1 | Architecture | **Capacitor** (Ionic's native-wrapper toolkit), wrapping the existing `sunmint_beta` web app. One shared web codebase (HTML/CSS/JS) compiles to a real native Android project (Gradle/APK) and a real native iOS project (Xcode/IPA) — not a from-scratch native rewrite in two languages. Chosen because: (a) the existing web app's offline-queue/camera/geo/signing logic is already built, working, and battle-tested — re-implementing it natively in Kotlin *and* Swift would mean maintaining the same logic three times (web + Android + iOS) forever after; (b) it directly satisfies "one codebase, two clients." |
| 0.2 | Distribution — Android | **Direct signed APK** (sideload — shared link, GitHub Release, or a DAO-hosted URL). No Play Store listing, no Play Console review cycle. Matches the reality that rural farmers may not reliably browse/trust the Play Store, and this avoids Google's review turnaround for every release. |
| 0.3 | Distribution — iOS | **RESOLVED (Gary, 2026-08-23): TestFlight.** Requires a paid Apple Developer Program account ($99/yr); a build is uploaded once via App Store Connect and distributed via a public TestFlight link (up to 10,000 external testers, no device pre-registration needed). Goes through a light "Beta App Review" (materially lighter than full App Store review), not a store listing. Chosen over ad-hoc distribution (manual per-device UDID registration, doesn't scale) and over the Apple Developer Enterprise Program (Apple's terms restrict it to internal/employee use — distributing to external farmers risks account revocation). This is the practical iOS equivalent of the Android direct-APK approach in §0.2. |
| 0.4 | Camera capture | Switch from the web app's `getUserMedia` + `<video>`/`<canvas>` live-preview capture to **Capacitor's native Camera plugin**, `CameraSource.Camera` (opens the OS camera UI directly, forces a live shot — no gallery/file picker). Preserves the existing app's deliberate design intent ("every report ties to a photo actually taken at the reported moment," documented in `sunmint_beta/README.md`) with a more reliable, more native permission/UX flow on both platforms than WebView `getUserMedia` (which has historically had inconsistent behavior, especially in iOS `WKWebView`). |
| 0.5 | Offline queue storage | Migrate from **IndexedDB** (web) to a **native SQLite plugin** (`@capacitor-community/sqlite`) + **Capacitor Filesystem** for photo files. Reason: IndexedDB inside a mobile WebView is subject to OS-level storage eviction under disk pressure — acceptable risk for a website tab, not acceptable for an app a farmer expects to hold weeks of unsynced reports. Native SQLite + app-private filesystem storage doesn't have this eviction risk. |
| 0.6 | RSA identity storage | Migrate the keypair from **`localStorage`** to **native secure storage** (Android Keystore / iOS Keychain, via a Capacitor secure-storage plugin). Same crypto scheme, same export format (see §1.3) — this is a security hardening, not a protocol change; Edgar sees identical signed payloads either way. |
| 0.7 | Backend changes | **None planned.** The mobile app is a pure client swap — same Edgar endpoint, same signed-event text format, same multipart photo upload. If any gap surfaces during PR4 (camera photo format/naming), fix the client to match Edgar's existing expectations, not the other way around. |
| 0.8 | Localization | Keep the existing JS `I18N` object pattern from `sunmint_beta/index.html` (PT default / EN toggle) rather than migrating to native `strings.xml` / `Localizable.strings` — it already works inside a WebView context and migrating it buys nothing for a Capacitor app. |

---

## 1. Full functionality list — current live behavior (`sunmint_beta/index.html`, read in full 2026-08-23)

This is the complete, exact spec of what the mobile app must replicate (then improve on, per §0).

### 1.1 General
- Bilingual UI: Portuguese (default) / English toggle, persisted in `localStorage['sunmint_lang']`, applied via
  `data-i18n` / `data-i18n-placeholder` attributes and a single `I18N` lookup object.
- Single-page app, no build step in the current web version (plain HTML/CSS/JS).
- SEO/social meta tags (Open Graph, Twitter Card, favicon) — not relevant to the app shell, but the TrueSight
  DAO branding/logo/app name should carry over.

### 1.2 Flow 1 — Link email (optional, secondary)
- Text input for email + submit button.
- On submit: ensures an RSA keypair exists (generates one on first use if not), signs and POSTs an
  `[EMAIL REGISTERED EVENT]` to Edgar (`https://edgar.truesight.me/dao/submit_contribution`, multipart
  `text` field only, no attachment).
- **Auto-verification**: if the app is opened via a link containing `?vk=<key>&em=<email>` (the link sent
  in the verification email), it automatically fires an `[EMAIL VERIFICATION EVENT]` on load, then strips
  those query params from the URL. The mobile app needs an equivalent deep-link / universal-link handler
  for this (Android App Links / iOS Universal Links, or at minimum a manual "paste verification link"
  fallback if deep linking isn't wired up in an early phase).
- Status messages for: missing email, sending, sent (check your email), verifying, verified, error.

### 1.3 RSA identity (shared by both flows)
- Keypair: `RSASSA-PKCS1-v1_5`, 2048-bit modulus, SHA-256 hash, generated via `crypto.subtle.generateKey`.
- Export format: public key as SPKI, private key as PKCS8, both base64-encoded — this exact format is
  what Edgar/dao_protocol/every other TrueSight DAO client (dapp, capoeira, etc.) already expects and
  verifies against. **The mobile app must produce byte-identical signatures for the same signing scheme**
  — i.e. whatever native crypto API is used (Android `java.security.KeyPairGenerator` /
  `Signature.getInstance("SHA256withRSA")`, iOS `SecKeyCreateSignature` with
  `.rsaSignatureMessagePKCS1v15SHA256`, or a Capacitor crypto plugin) must be verified byte-for-byte
  compatible with the existing `RSASSA-PKCS1-v1_5`/SHA-256/SPKI/PKCS8 scheme before this is considered done
  — this is the single highest-risk compatibility point in the whole port (see PR7's acceptance criteria).
- Currently generated once per browser/device and reused indefinitely from `localStorage`. Mobile: generate
  once per app install, store in native secure storage (§0.6).

### 1.4 Flow 2 — Report a tree planting (primary)
- **Species selector**: dropdown (Cacao - Criolla / Trinitario / Forestero / Other-with-free-text). Values
  are canonical strings matched against real historical `[TREE PLANTING EVENT]` submissions — must not
  change the canonical value strings regardless of UI language.
- **Live camera capture** (not a gallery/file picker — deliberate, see §0.4): opens the environment-facing
  camera on mobile, captures a still frame, shows a preview, allows retake. Captured as JPEG, quality 0.9.
- **Geolocation** (best-effort, non-blocking): requests device location with an 8s timeout; if denied,
  unavailable, or timed out, the report still submits with blank lat/long and an inline
  "(location not available)" note. Never blocks submission.
- **Offline-first queue-then-flush** (the core architectural feature, see `sunmint_beta/README.md`'s
  "Offline queue" section for the full rationale — re-read it before touching this in the port):
  1. Sign the `[TREE PLANTING EVENT]` payload **immediately at capture time** (network not required to sign
     — only `crypto.subtle`/native-crypto-equivalent).
  2. Queue the signed text + photo blob locally (web: IndexedDB; mobile: SQLite + Filesystem per §0.5),
     one record per report: `{id, shareText, photo, photoName, createdAt, uploaded, uploadedAt}`.
  3. **Reset the form immediately** after queuing — farmer can capture the next tree right away, independent
     of network state.
  4. **Flush the queue** opportunistically: on app launch/foreground, right after queuing a new report, and
     on network-reconnect. A record that fails to upload is left `uploaded: false` for the next attempt —
     no retry-count, no backoff, no giving up.
  5. **HTTP 409 from Edgar counts as success** — Edgar returns 409 when it already processed that exact
     signed request (common when a prior flush succeeded server-side but the client never saw the response
     on a flaky connection). Without this, that report retries forever despite already being recorded.
  6. **Pending-count badge** — shows "N reports pending upload" so the farmer isn't left guessing.
- Payload format: `[TREE PLANTING EVENT]\n- Latitude: <or blank>\n- Longitude: <or blank>\n- Species: <val>\n- Planting Time: <ISO8601>\n- Photo URL: <computed GitHub destination path>\n- Submission Source: <app identifier>\n--------` + the standard signature/Request-Transaction-ID footer every TrueSight DAO signed event uses.
- **Photo destination naming** (must stay byte-compatible — Edgar/downstream expects this exact pattern):
  `{yyyymmddhhmmss}_{first 20 alphanumeric chars of the base64 public key}.jpg`, referenced in the signed
  text's `Photo URL` field and uploaded as the multipart `attachment` alongside `text`.
- Submission result panel: shows the raw signed request text + the raw server response (debugging/audit
  aid) — worth keeping for the mobile app too, even if hidden behind a "details" disclosure by default.

### 1.5 Backend contract (must not change)
- Endpoint: `POST https://edgar.truesight.me/dao/submit_contribution`, `multipart/form-data`.
- Fields: `text` (the full signed event text, always) + `attachment` (photo blob, tree-planting events only).
- No API key / auth header — identity is proven entirely by the RSA signature inside `text`.
- No other TrueSight DAO backend service needs to change for this app to work.

---

## 2. Implementation plan

**Stack:** Capacitor (`@capacitor/core`, `@capacitor/cli`, `@capacitor/android`, `@capacitor/ios`) wrapping
the existing web app's HTML/CSS/JS (ported with minimal changes into the Capacitor project's `www/`
folder), plus native plugins:

| Plugin | Replaces | Purpose |
|---|---|---|
| `@capacitor/camera` | `getUserMedia` + `<video>`/`<canvas>` | Live native camera capture, no gallery picker (§0.4) |
| `@capacitor/geolocation` | `navigator.geolocation` | Native location, same optional/non-blocking behavior |
| `@capacitor-community/sqlite` | IndexedDB | Offline report queue (§0.5) |
| `@capacitor/filesystem` | IndexedDB blob storage | Photo file storage on-device |
| `@capacitor/network` | `window.addEventListener('online', ...)` | Reconnect-triggered queue flush |
| `@capacitor/app` | (n/a — new) | App-foreground listener, also flushes the queue |
| a secure-storage plugin (TBD at PR7 — e.g. `capacitor-secure-storage-plugin`) | `localStorage` for the RSA keypair | Android Keystore / iOS Keychain-backed storage (§0.6) |

**What does NOT change:** the Edgar endpoint, the signed-payload text format, the photo naming convention,
the 409-as-success handling, the bilingual `I18N` object, the species canonical values, the
queue-then-flush-then-reset-form sequencing. The port should be judged by how little of this logic actually
needs to be rewritten versus just re-wired to native plugin APIs.

**Highest-risk item:** byte-compatible RSA signing (§1.3) — verify this FIRST, in isolation, before building
anything else on top of it (a signature that verifies against the wrong scheme fails silently at Edgar, not
at build time).

---

## 3. Sequenced plan — one PR per execution turn (§5a)

**Android-first re-sequencing (Gary, 2026-08-23):** the governor wants an installable Android APK to
test on his own phone as soon as possible. Sophia is authorized to **auto-advance through PR2 and
PR4–PR11 without waiting for a per-PR "go"** (each is still its own feature-branch PR, human-reviewed
before merge, per §6) and should **stop at the Android UAT gate** with a direct-download APK
link/instructions ready — that stop is non-negotiable (§5c).

**iOS does not wait for Android UAT (Gary, 2026-08-23, updated):** originally PR3/PR12 were deferred
until after the governor actually tested the Android APK. That's now relaxed — **as soon as the Android
code track is done (PR11 merged), start PR3 immediately, in parallel with/without waiting for the
governor to run Android UAT.** The Android UAT gate itself is unchanged (still an always-stop for
Sophia on the Android side — she still posts the APK link and stops advancing Android-specific work
past PR11), but it no longer blocks *starting* the iOS track. PR3 is still hard-blocked on needing a Mac
(this Linux box cannot compile iOS — flag to the governor if none is accessible) and PR12 is still
hard-blocked on a provisioned Apple Developer account (governor action, not Sophia's to do unattended) —
those real constraints stand regardless of sequencing. PR13 (docs) may be done whenever convenient.

| Unit | Scope | Gate |
|------|-------|------|
| **PR0** | This roadmap. | — |
| **PR1** | Repo scaffolding: `npm init`, install Capacitor core/CLI, `npx cap init` (app id e.g. `me.truesight.sunmint`, app name "Sunmint"), copy `sunmint_beta/index.html`'s content into `www/index.html` **unmodified** as the starting point. Goal: prove the existing web logic can be wrapped at all before changing anything. | — |
| **PR2** | `npx cap add android`, configure `AndroidManifest.xml` permissions (camera, location, internet), first successful debug APK build. Smoke-test: install on an emulator/device, confirm the *unmodified* web logic (from PR1) runs inside the WebView shell — email link + tree report using the OLD `getUserMedia`/IndexedDB code, just running in a native shell. This isolates "does Capacitor work at all" from "does the native-plugin migration work." | — |
| **PR3** | `npx cap add ios`, `Info.plist` permissions, first successful build **on a Mac** (this Linux box cannot compile iOS — flag clearly who/where this build step runs; Sophia can write all iOS-side code/config, but the actual `xcodebuild`/simulator run needs a macOS environment outside this fleet). Starts right after PR11 lands — **does not wait for the governor to run Android UAT.** | Needs a Mac available; flag to governor if none is accessible. |
| **PR4** | Byte-compatible RSA signing verification (the highest-risk item, §2) — before touching camera/geo/storage, confirm the native crypto path (Capacitor plugin or custom native bridge) produces signatures Edgar accepts, using a real (or dry-run) signed event. | — |
| **PR5** | Integrate `@capacitor/camera` (`CameraSource.Camera`), replace the live-preview `getUserMedia`/canvas flow. Verify captured JPEG quality/dimensions and the photo-naming convention (§1.4) are unchanged. | — |
| **PR6** | Integrate `@capacitor/geolocation`, replace `navigator.geolocation`. Same optional/non-blocking behavior, same blank-lat/long fallback. | — |
| **PR7** | Integrate `@capacitor-community/sqlite` + `@capacitor/filesystem` for the offline queue, replacing IndexedDB. Same record shape, same queue→flush→mark-uploaded lifecycle, same 409-as-success handling, same pending-badge UI. | — |
| **PR8** | Integrate a secure-storage plugin for the RSA keypair, replacing `localStorage`. Verify the keypair survives an app restart and an app update (not just a fresh install). | — |
| **PR9** | Sync-trigger wiring: `@capacitor/network` connectivity-change listener + `@capacitor/app` foreground listener, both calling the same flush function from PR7. | — |
| **PR10** | Branding: app icon, splash screen, final app name/bundle ID. | — |
| **PR11** | Android release signing: generate a release keystore, produce a signed release APK. **Keystore file is a credential — never commit it; follow `CREDENTIAL_HANDOFF_PROTOCOL.md` for custody.** | — |
| **Android UAT** | Install the signed release APK on the governor's real Android device (direct download — GitHub Release asset or DAO-hosted URL, no Play Store); run through both flows exactly as `sunmint_beta/README.md`'s existing testing notes describe (online submit, offline submit + reconnect flush, retake, "Other" species, email link + verification link click). | **Always-stop gate (§5c).** Sophia posts the download link/instructions in the handoff topic and stops; does not proceed further unattended. |
| **PR12** | iOS distribution via **TestFlight** (§0.3, resolved): governor sets up (or delegates setup of) an Apple Developer Program account, App Store Connect app record, and a first TestFlight build upload; verify the public TestFlight link installs on a real device. | Needs the Apple Developer account provisioned; account creation/payment itself is a governor action, not Sophia's to do unattended. |
| **PR13** | Docs: `sunmint_mobile/README.md` covering build/release process for both platforms, how the app relates to `sunmint_beta`/`sunmint_prod` (the web app keeps existing independently — this is an additional client, not a replacement). | — |
| **iOS UAT** | Repeat the UAT pass above via the TestFlight build once available. | **Always-stop gate (§5c).** |

---

## 4. Checklist — acceptance criteria

- [ ] Single Capacitor codebase (`sunmint_mobile` repo) builds cleanly for both Android and iOS targets.
- [ ] Native RSA signing verified byte-compatible with the existing web app's scheme (Edgar accepts it).
- [ ] Email link + auto-verification flow produces identical `[EMAIL REGISTERED EVENT]`/`[EMAIL VERIFICATION EVENT]` payloads to the web app.
- [ ] Tree planting report: species selector (incl. "Other" free text), live native camera capture only (no gallery picker), optional geolocation, produces an identical `[TREE PLANTING EVENT]` payload including the exact photo-naming convention.
- [ ] Offline queue survives app kill/restart and OS reboot; flushes automatically on reconnect and on app foreground, with no manual action required.
- [ ] RSA keypair persists in native secure storage across app restarts and app updates.
- [ ] HTTP 409 from Edgar is treated as success (idempotent dedup), matching the web app.
- [ ] Bilingual PT/EN toggle works identically to the web app.
- [ ] Signed release APK installs and runs on a real Android device via direct distribution (no Play Store).
- [ ] Zero backend changes required — verified by the same Edgar endpoint accepting mobile-originated submissions with no server-side modification.
- [ ] iOS distribution path explicitly decided (not defaulted into) before any iOS release-signing work begins.

---

## 5. Pre-flight facts (§5d: no unit below should need to re-discover any of this)

- Edgar endpoint: `https://edgar.truesight.me/dao/submit_contribution`, multipart `text` + optional `attachment`, no auth header — identity proven by the RSA signature embedded in `text`.
- `sunmint_beta` (beta.sunmint.truesight.me) and `sunmint_prod` (sunmint.truesight.me, a GitHub fork of beta) are the existing web apps this mobile app parallels — they are **not replaced**, the mobile app is an additional client hitting the same backend.
- Photo mirror destination: `TrueSightDAO/sunmint` repo, `images/` folder — Edgar handles the actual upload server-side from the multipart `attachment`; the client only needs to reference the correct destination path in the signed text's `Photo URL` field.
- No `tokenomics/SCHEMA.md` changes anticipated — same event types, same fields, same downstream GAS processors (`process_tree_planting_telegram_logs.js` et al.) as the web app already feeds.
- `truesight_autopilot/app/config.py`'s `allowed_repos` list did **not** include `sunmint_beta` or `sunmint_prod` (only a stale `sunmint_farmer` entry) as of 2026-08-23 — fixed alongside this plan's own repo addition (§6.1) so Sophia can also work on the existing web apps without a separate gate next time.

---

## 6. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---------|----------|
| `sunmint_mobile` — code, config, plugin integration | Pre-authorized — feature branch + PR per unit, human reviews before merge. |
| Android release keystore generation | Pre-authorized (needed for distribution) — but the keystore file itself is a credential; never commit it, follow `CREDENTIAL_HANDOFF_PROTOCOL.md` for custody. |
| iOS build/signing/distribution | **RESOLVED — TestFlight (§0.3).** Apple Developer Program account creation/payment is a governor action (Sophia cannot pay for or create the account); once provisioned, build upload + TestFlight configuration is pre-authorized like any other PR unit. |
| UAT (real-device install + real Edgar submissions) | **Always-stop gate (§5c).** |

### 6.1 Allow-list fix (done as part of this handoff)
`truesight_autopilot/app/config.py`'s `allowed_repos` — added `sunmint_mobile` (PR #309, merged). Note:
`sunmint_beta`/`sunmint_prod` are still **not** in the list (only a stale `sunmint_farmer` entry exists) —
that gap was intentionally left unfixed since only the `sunmint_mobile` addition was authorized. It doesn't
block this roadmap (PR1–PR13 only touch the `sunmint_mobile` repo) but would need separate authorization
before Sophia can be asked to edit the existing web apps directly.

On 2026-08-23 the running `truesight-autopilot.service` process was found to be holding a **stale in-memory
copy** of `allowed_repos` from before PR #309 merged (config changes don't hot-reload — they need an actual
process restart). Claude restarted the service directly via SSH (governor-approved) once Sophia was
confirmed idle between turns; the reloaded process now reflects the current `config.py`. If this recurs on
a future config change, the same fix applies: confirm Sophia is idle, then restart
`truesight-autopilot.service`.

---

## 7. Resume tracker

> **RESUME HERE → PR8** (secure storage for RSA keypair) as of this edit; check Sophia's latest turn
> report for the live pointer. PR1/PR2/PR4/PR5/PR6/PR7 merged 2026-08-23. Standing auto-advance
> (governor 2026-08-23): execute PR6–PR11 back-to-back, one PR per turn, no per-PR check-in. Only
> mandatory stop on the Android side: **Android UAT gate** (§5c) — post direct-download APK link and
> STOP advancing Android-specific work for governor phone testing.
>
> **iOS no longer waits for that stop (governor, 2026-08-23, updated):** once PR11 (Android release
> signing) merges, start PR3 (iOS platform) immediately — do not wait for the governor to actually run
> Android UAT. PR3 is still blocked on needing a Mac (flag to governor if none accessible); PR12 is
> still blocked on a provisioned Apple Developer account (governor action).

| Unit | Built | Merged | Contribution reported |
|------|:----:|:------:|:---------------------:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (repo scaffolding) | ☑ | ☑ (PR #1, squash `ea732113`) | ☑ 2026-08-23 |
| PR2 (Android platform + smoke test) | ☑ | ☑ (PR #2, squash `e11416ce`) | ☑ 2026-08-23 (APK build; device smoke-test at UAT) |
| PR3 (iOS platform + smoke test) — starts right after PR11, no need to wait for Android UAT (needs Mac) | ☑ | ☑ (PR #11, squash `8a4f3b56`) | ☐ code+config done; **build blocked — needs a Mac (flagged)** |
| PR4 (RSA signing byte-compatibility) | ☑ | ☑ (PR #3, squash `4495d574`) | ☑ 2026-08-23 (BYTE-IDENTICAL proven) |
| PR5 (native camera) | ☑ | ☑ (PR #4, squash `71d66de3`) | ☑ 2026-08-23 (APK builds w/ plugin) |
| PR6 (native geolocation) | ☑ | ☑ (PR #5, squash `eba3e2d7`) | ☑ 2026-08-23 (APK builds w/ plugin) |
| PR7 (native offline queue — SQLite + Filesystem) | ☑ | ☑ (PR #6, squash `5cdd9c4a`) | ☑ 2026-08-23 (APK builds w/ plugins) |
| PR8 (native secure storage for RSA keypair) | ☑ | ☑ (PR #7, squash `8d0489bb`) | ☑ 2026-08-23 (APK builds w/ plugin) |
| PR9 (sync triggers) | ☑ | ☑ (PR #8, squash `aeecde4f`) | ☑ 2026-08-23 (APK builds w/ plugins) |
| PR10 (branding) | ☑ | ☑ (PR #9, squash `602f21be`) | ☑ 2026-08-23 (icons/splash branded, APK builds) |
| PR11 (Android release signing) | ☑ | ☑ (PR #10, squash `313a096d`) | ☑ 2026-08-23 (signed release APK, cert verified) |
| **Android UAT** | ☐ | — | ☐ **gate posted (link + SHA-256 in thread); governor to test** |
| PR12 (iOS distribution — needs Apple Developer account) | ☐ | — | ☐ needs Apple Developer account (governor) |
| PR13 (docs) | ☐ | ☐ | ☐ |
| iOS UAT | ☐ | — | ☐ |


| iOS UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** every cross-repo fact a unit below would need (Edgar's contract, the
photo-naming convention, the allow-list gap) is captured in §5 above.

---

## 8. UAT — before this reaches a real farmer's phone

| Step | What to test | Acceptance criterion |
|------|---------------|----------------------|
| 1 | Fresh install, no prior state | RSA keypair generates once, persists across app restart |
| 2 | Email link flow | `[EMAIL REGISTERED EVENT]` submits, verification email arrives, clicking it (or pasting the link) fires `[EMAIL VERIFICATION EVENT]` |
| 3 | Tree report, online | Species + live camera capture + geolocation → submits immediately, appears in `SunMint Tree Planting` sheet with correct fields |
| 4 | Tree report, offline (airplane mode) | Report queues locally, form resets immediately, pending badge shows count |
| 5 | Reconnect | Queue flushes automatically without reopening the app or tapping anything |
| 6 | Kill + relaunch app with pending reports | Queue survives, flush resumes on launch |
| 7 | "Other" species | Free-text field appears, submits the typed value verbatim |
| 8 | Retake photo | Old capture discarded, camera reopens, new capture replaces it |
| 9 | Duplicate flush (simulate a 409) | Treated as success, not retried forever |
| 10 | Direct APK install | Installs and runs on a real Android device with no Play Store involved |

---

## 9. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first) before starting the next unit.
