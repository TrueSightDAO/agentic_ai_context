# TESTFLIGHT_RUNBOOK — SunMint iOS (bundle `me.truesight.sunmint`)

Status: **prepped 2026-08-23; execution under way — Apple Developer Program enrollment SUBMITTED 2026-08-24 (Enrollment ID M9V8VJWK26, TrueTech Inc), status "being processed" — awaiting Apple's verification email. Remaining: complete enrollment + pick an Apple-silicon / Xcode 26 build path (GitHub Actions macos runner recommended).**
The iOS code track is complete and green (see state recap below); this runbook is what we
run the moment the blockers clear.

## ⛔ Hard finding — read this first

Apple's App Store Connect upload mandate (developer.apple.com/news/upcoming-requirements):
**as of 2026-04-28, apps uploaded to App Store Connect must be built with Xcode 26 or later**
using an iOS 26+ SDK. TestFlight uploads go through App Store Connect, so this applies to
TestFlight too. **Xcode 26 dropped Intel Mac support** (Apple silicon only).

Consequence: **the current designated Mac (Gary's Intel Mac, Xcode 16.2 / iOS 18.2 SDK)
cannot produce a TestFlight-eligible archive.** It remains fine for simulator builds/UAT.

### Three viable paths (choose one)
1. **GitHub Actions macOS arm64 runner — RECOMMENDED.** `macos-15`/`macos-14` runners are
   Apple silicon and ship Xcode 26. No new hardware, no Intel wall, reproducible, and the
   workflow (below) is checked into the repo. Needs an App Store Connect API key from Gary.
2. Apple-silicon Mac (M1+) with Xcode 26 — if Gary has or buys one.
3. Rented/cloud Mac (MacStadium, AWS EC2 Mac) — paid, heavier than CI for this workload.

## State recap (verified 2026-08-23)
- Repo: TrueSightDAO/sunmint_mobile, main @ `d3765d3` (PR #21).
- iOS: **CocoaPods** package manager (not SPM — SPM's prebuilt Capacitor binary strips
  `reject`/`getString` via `$NonescapableTypes`; CocoaPods compiles from source and works).
- Plugins: `geolocation@8.1.0`, `filesystem@8.0.0`, `camera@8.1.0`; core/android/ios `8.4.2`.
- **BUILD SUCCEEDED + runs on iPhone 16 Pro simulator** (geolocation resolves; camera is
  simulator-limited by design).
- Android re-verified green after the shared downgrade: `cap sync android` + `assembleDebug`
  RC=0, `app-debug.apk` 18.4MB.
- Bundle ID already final: `me.truesight.sunmint` (`PRODUCT_BUNDLE_IDENTIFIER` + capacitor
  config). `DEVELOPMENT_TEAM` is currently **empty** — set when the account exists.
- App name: **Sunmint**. Launcher icon + splash from PR10 (a 1024px marketing icon is still
  needed for App Store Connect — see Gary list).

## Prerequisites — ALL Gary (governor) action, none automatable
1. **Apple Developer Program enrollment** ($99/yr, org account) → enroll at
   developer.apple.com/programs. Yields the **Team ID** (needed for `DEVELOPMENT_TEAM`).
2. **App Store Connect**: accept agreements; create the app record — platform iOS,
   bundle `me.truesight.sunmint`, name **Sunmint**.
3. **App Store Connect API key** (for CI uploads): App Store Connect → Users and Access →
   Integrations → App Store Connect API → generate. Save the `.p8`, **Key ID**, **Issuer ID**.
   (Or an app-specific password for `altool`/Transporter if doing it manually.)
4. **App metadata** (Gary answers): subtitle, description, keywords, category (suggest
   Food & Drink or Business), support URL, marketing URL, copyright, age-rating answers.
5. **Privacy labels** (App Store Connect → App Privacy): the app **collects** Photos
   (camera capture) and Precise Location (geolocation). Everything else: Not Collected.
6. **Export compliance**: app uses HTTPS + local RSA signing (no custom crypto export
   concern) → answer **No / exempt** on the export-compliance question.
7. **1024×1024 app icon** (App Store marketing icon) + **screenshots** (6.7" and 6.5"
   minimum; 5.5"/iPad optional). Required before external TestFlight can start.

## Execution — Path 1 (GitHub Actions, recommended)
1. Gary provisions the account + API key (above).
2. Store secrets in the repo: `APPSTORE_ISSUER_ID`, `APPSTORE_KEY_ID`,
   `APPSTORE_KEY_B64` (base64 of the .p8).
3. Land the workflow `.github/workflows/testflight.yml` in `sunmint_mobile` (YAML below;
   next PR unit once Gary confirms the account).
4. Run the workflow (manual `workflow_dispatch` or tag push) → it archives + uploads.
5. In App Store Connect: wait for build processing (~10–30 min) → enable TestFlight →
   create tester group → **Public Link** (`https://testflight.apple.com/join/…`) → share.

### testflight.yml (drop into `sunmint_mobile/.github/workflows/`)
```yaml
name: TestFlight
on:
  workflow_dispatch:
  push:
    tags: ["ios-v*"]
concurrency: { group: testflight, cancel-in-progress: false }
jobs:
  build-and-upload:
    runs-on: macos-15   # Apple silicon, Xcode 26
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npx cap sync ios
      - working-directory: ios/App
        run: pod install
      - name: Set development team
        working-directory: ios/App
        run: |
          sed -i '' 's/DEVELOPMENT_TEAM = ;/DEVELOPMENT_TEAM = ${{ secrets.APPLE_TEAM_ID }};/' \
            App.xcodeproj/project.pbxproj
      - name: Import distribution cert
        run: |
          echo "${{ secrets.DIST_CERT_P12_B64 }}" | base64 -d > cert.p12
          echo "${{ secrets.DIST_CERT_P12_PASS }}" | security import cert.p12 -P "$(cat /dev/stdin)" -k ~/Library/Keychains/login.keychain-db
          security set-key-partition-list -S apple-tool:,apple: -k "${{ secrets.KEYCHAIN_PASS }}" ~/Library/Keychains/login.keychain-db
      - name: Archive
        run: |
          xcodebuild -workspace ios/App/App.xcworkspace -scheme App -configuration Release \
            -sdk iphoneos -destination 'generic/platform=iOS' \
            -archivePath build/Sunmint.xcarchive archive \
            DEVELOPMENT_TEAM=${{ secrets.APPLE_TEAM_ID }}
      - name: Export IPA
        run: |
          /usr/libexec/PlistBuddy -c "Add :method string app-store-connect" -c "Add :signingStyle string automatic" \
            -c "Add :uploadSymbols bool true" -c "Add :stripSwiftSymbols bool true" ExportOptions.plist
          xcodebuild -exportArchive -archivePath build/Sunmint.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/ipa
      - name: Upload (altool)
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APP_SPECIFIC_PW: ${{ secrets.APP_SPECIFIC_PW }}
        run: |
          xcrun altool --upload-app -f build/ipa/*.ipa -t ios -u "$APPLE_ID" -p "$APP_SPECIFIC_PW"
```
Notes: with an ASC API key you can instead use `xcrun notarytool`/Transporter or a tool
like `altool` with `--apiKey`; the p12/keychain dance above is the classic distribution-cert
route and works either way. Secrets needed beyond the API key: `APPLE_TEAM_ID`,
`DIST_CERT_P12_B64`, `DIST_CERT_P12_PASS`, `KEYCHAIN_PASS`, `APPLE_ID`, `APP_SPECIFIC_PW`.

## Execution — Path 2/3 (Apple-silicon Mac / rented)
```bash
git pull origin main
npm ci && npx cap sync ios
cd ios/App && pod install
# Xcode: open App.xcworkspace, set Signing → Team (Gary's), bump version/build
xcodebuild -workspace App.xcworkspace -scheme App -configuration Release \
  -sdk iphoneos -destination 'generic/platform=iOS' -archivePath build/Sunmint.xcarchive archive
xcodebuild -exportArchive -archivePath build/Sunmint.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/ipa
# Upload: Xcode Organizer → Distribute → App Store Connect, or Transporter
```

## After upload (both paths)
1. App Store Connect → the build → wait for **processing**.
2. Answer export-compliance (exempt) if prompted.
3. Add tester group(s) → **External Testing** → create a **Public Link**.
4. Share the link; also add Gary + the Mac agent as **Internal** testers (no review).
5. Walk the 5 UAT flows on a real device: online submit, offline+reconnect flush, retake,
   "Other" species, email link + verification click (deep link `sunmint://` + paste fallback).

## Still open / parked
- **Simulator UAT** (5 flows) can run NOW on the Intel Mac's simulator — doesn't need
  TestFlight or the account.
- Universal/App Links (`https://…` → app) need `apple-app-site-association` on the
  sunmint web host; `sunmint://` deep links already work (PR14).
- Update this runbook + the plan once the account is provisioned and the first archive is up.
## Apple Developer Program — enrollment record (2026-08-24)

Submitted by Gary Teh from the enrollment flow (source PDF `bae8eb7a71a1434cb5b2a92c17d4b851.pdf`, 2 pages, attached in thread 13445).

| Field | Value |
|---|---|
| **Enrollment ID (reference \"serial number\")** | **M9V8VJWK26** |
| Status | Being processed — Apple verifies authority to sign legal agreements, then emails instructions to complete |
| Legal entity type | Organization |
| Legal entity name | TrueTech Inc |
| D-U-N-S® number | 119035208 |
| Address | 3041 Taraval St, San Francisco, CA 94116-2106, US |
| Website | https://truesight.me |
| Phone | +1 (442) 340-5782 |
| Work email (signature authority) | garyjob@truesight.me |
| Platforms | iOS, iPadOS, macOS, tvOS, visionOS, watchOS, App Store |
| Development tools | Swift, SwiftUI, Swift Playground, TestFlight, Xcode, Xcode Cloud, Icon Composer, SF Symbols |

**Next steps:**
1. Apple calls/emails to verify signature authority — have the Enrollment ID **M9V8VJWK26** handy (it's the reference they'll ask for).
2. Complete enrollment per Apple's emailed instructions.
3. Then: create App Store Connect app record (`me.truesight.sunmint`), generate ASC API key, land `testflight.yml` (GitHub Actions macos runner), archive + upload, publish public TestFlight link. See Execution above.

