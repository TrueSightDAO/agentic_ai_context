# Local mobile emulator setup (Android + iOS)

How to spin up a local **Android emulator** and **iOS Simulator** on this Mac (Intel x86_64,
macOS 14.5) for testing the mobile apps without a physical device. Verified end-to-end
2026-08-23 while UAT-ing the SunMint mobile app (`TrueSightDAO/sunmint_mobile`).

The iOS Simulator is a real Mac/Xcode capability (not an "emulator"); the Android emulator
uses the Android SDK. Both are already installed on this machine — this doc is the reference
to re-create or re-run them.

---

## Android emulator

### One-time install

```bash
# JDK 21 (Capacitor 8 needs Java 21; sdkmanager needs Java). Formula installs user-writable, no sudo.
brew install openjdk@21

# Android SDK command-line tools + platform-tools
brew install --cask android-commandlinetools android-platform-tools
```

### Per-session env

```bash
export JAVA_HOME="/usr/local/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
export ANDROID_HOME="/usr/local/share/android-commandlinetools"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
```

### Install SDK packages (one-time)

```bash
yes | sdkmanager --licenses
sdkmanager "platform-tools" "emulator" "system-images;android-35;google_apis;x86_64" "platforms;android-35" "build-tools;35.0.0"
```

⚠️ **Gotcha — `platform-tools` must live under `$ANDROID_HOME`.** The Homebrew cask drops `adb`
in `/usr/local/share/android-platform-tools` (NOT under the SDK root), and the emulator refuses
to start with `FATAL | Cannot find valid sdk root` until you also run `sdkmanager "platform-tools"`
so it lands at `$ANDROID_HOME/platform-tools/`.

⚠️ **Intel Mac → `x86_64` system image** (Apple Silicon would use `arm64-v8a`).

### Create + boot an AVD (already exists: `sunmint_test`)

```bash
echo "no" | avdmanager create avd -n sunmint_test -k "system-images;android-35;google_apis;x86_64" -d "pixel_7" --force
nohup emulator -avd sunmint_test -gpu auto -no-snapshot-save -no-boot-anim > /tmp/emulator.log 2>&1 &
adb wait-for-device          # then wait for: adb shell getprop sys.boot_completed → 1
```

### Install + launch an APK

```bash
adb -e install -r /path/to/app.apk
adb -e shell pm grant <appId> android.permission.CAMERA
adb -e shell pm grant <appId> android.permission.ACCESS_FINE_LOCATION
adb -e shell monkey -p <appId> -c android.intent.category.LAUNCHER 1
```

Camera is a **virtual** camera (animated scene by default) — real-device capture behavior differs
slightly, but capture→preview→submit works. Location is spoofable via the emulator's "…" → Location.

### Building the app from source (Android)

`cd <repo>/android && ./gradlew assembleDebug` needs `JAVA_HOME` + `ANDROID_HOME` set above. The
release `assembleRelease` additionally needs `android/keystore.properties` + the release keystore
(which lives on the autopilot box, not this Mac). For quick testing, prefer installing the prebuilt
APK from the GitHub release instead of building.

---

## iOS Simulator

### Prereq (already present)

Xcode 16.2 (`/Applications/Xcode.app`), iOS 18.2 SDK + Simulator runtime. **No code signing is
needed for simulator builds** (only for a real device / TestFlight, which needs the Apple Developer
account).

### List + boot a device

```bash
xcodebuild -version
xcrun simctl list devices available      # grab an iPhone UDID (e.g. iPhone 16 Pro)
xcrun simctl boot <UDID>
open -a Simulator
```

### Build a Capacitor app for the simulator

Capacitor 8 CLI requires **Node >=22** (this Mac's default `node` is 20 via nvm, so export the
Homebrew keg):

```bash
brew install node@22
export PATH="/usr/local/opt/node@22/bin:$PATH"
cd <repo> && npm install && npx cap sync ios
```

```bash
cd ios/App
xcodebuild -project App.xcodeproj -scheme App -configuration Debug \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  -derivedDataPath /tmp/app-dd build

xcrun simctl install <UDID> /tmp/app-dd/Build/Products/Debug-iphonesimulator/App.app
xcrun simctl launch <UDID> <bundleId>     # e.g. me.truesight.sunmint
```

### Known issue (sunmint_mobile, 2026-08-23)

The iOS build currently fails with Swift errors (`value of type 'CAPPluginCall' has no member
'reject'`, `missing argument for parameter #2 in call`) because the Capacitor 8 **plugins**
(`@capacitor/app@8.1.1`, `@capacitor/filesystem@8.1.3`, `@aparajita/capacitor-secure-storage@8.0.0`)
ship Capacitor-7-style Swift that was removed in Capacitor 8 core. **Not a version-pin problem**
(tested 8.5.0 / 8.4.2 / 8.2.0 — all fail). Tracked in `SUNMINT_MOBILE_APP_PLAN.md` / Telegram
thread 13445. The Simulator itself is fine; only the app build is blocked.

---

## sunmint_mobile quick reference

- Repo: `TrueSightDAO/sunmint_mobile` (clone to `~/Applications/sunmint_mobile`).
- Android APK (prebuilt, installs via `adb -e install`):
  `https://github.com/TrueSightDAO/sunmint_mobile/releases/download/v0.1.0-android-uat/sunmint-android-uat.apk`
- iOS: `npx cap sync ios` then the `xcodebuild` above (blocked until the plugin Swift issue is fixed).
- App id: `me.truesight.sunmint` (Android + iOS).
