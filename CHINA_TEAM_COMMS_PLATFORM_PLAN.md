# China Internal Team Comms Platform — Implementation Plan & Execution Roadmap

> **Status:** Draft for review · **Owner:** Gary · **Prepared by:** Sophia (autopilot) · **Date:** 2026-08-05
> **North-star tie-in:** Reliable internal comms keeps the China operation (Dongguan, Jerri/Ling, Aora events, GACC track) executing — every track on TRACK_MAP.md ultimately serves restoring 10,000 hectares of Amazon rainforest.

---

## 1. Executive Summary

Telegram — the DAO's current internal comms backbone (channel + topics) — is **blocked in mainland China**, and 2026 Great Firewall deep-packet-inspection upgrades have made MTProxy/MTProto proxy workarounds effectively unusable. The China internal team needs a reliable alternative that preserves the exact mental model we use today: **an app with individual teams, and inside each team, individual topics**.

**Recommendation: self-hosted Zulip** (Apache 2.0, free, 100% open source) with a **white-labeled Android app** (fork of the official Flutter app `zulip-flutter`), distributed as a **direct APK** (no Google Play needed in China).

- **Streams = teams/channels**, **topics = threads** — a 1:1 mapping to Telegram forums.
- Server in **AWS Hong Kong (ap-east-1)**: no ICP filing required, 20–40 ms latency to mainland (vs 200–300 ms from US/EU), no mainland legal entity needed.
- **Cost:** ~US$40–80/month all-in (small EC2 + EBS snapshots + domain).
- **Timeline:** MVP (web, single team) in ~2 weeks; full rollout (branded Android app + push) in ~6–8 weeks.

---

## 2. Problem Statement

1. **Telegram is blocked in mainland China.** Access requires a VPN; free VPNs are unreliable, and 2026 DPI upgrades target MTProto traffic — official MTProxy is reported ineffective in real-world use, and obfuscation arms-race tools require constant maintenance.
2. **The China internal team cannot reliably reach the DAO channel** where day-to-day operations, handoffs, and the Aora/China track conversations live.
3. **We want feature parity with the current workflow:** an Android app with individual teams, each team containing topics — the same structure as the Telegram channel + topic forums we run today (e.g. QR/cacao-bags topics, partner outreach, oracle threads).
4. Constraints: no Google Play availability in China, no FCM push (Google Play Services absent), no mainland hosting entity (ICP) yet.

---

## 3. Requirements

### Functional
- Android app (primary; iOS/desktop/web nice-to-have).
- Structure: **teams** and, within a team, **topics** (threads) — mirroring Telegram forums.
- 1:1 and small-group DMs.
- File/image sharing (cacao-bag photos, PDFs, event plans).
- Mentions, notifications, unread badges, search.
- Admin roles & permissions (who can create teams/topics).
- Message history retention & export/backup.

### Non-functional
- **Sovereign:** we host it, our data, no third-party SaaS dependency that can change terms overnight.
- **China-reachable:** low latency from mainland, no GFW-blocked dependencies (no Google/Firebase calls in the app path).
- **Secure:** TLS everywhere, MFA, no public signup.
- **Cheap:** under ~$100/month.
- **Maintainable:** one operator (Sophia) can run it; upgrades are scripted.

---

## 4. Research Summary — Options Compared

### Option A: Chinese enterprise SaaS (zero build)
| Platform | Strengths | Weaknesses for us |
|---|---|---|
| **Feishu / Lark (ByteDance)** | Best-in-class docs+chat, strong mobile app, free tier, topics/threads OK, multinational support (Lark global) | Data on ByteDance's platform; free tier limits; SaaS terms can change; not "ours" |
| **DingTalk (Alibaba)** | Huge in China, HR/OA strength, free | OA-focused, chat is secondary; China-only; less ideal for a lean distributed team |
| **WeCom / WeChat Work (Tencent)** | Connects to WeChat ecosystem, free | Customer-facing focus; topics/threads model weaker; not our workflow |

**Verdict:** All are credible zero-build paths, but they are **someone else's platform** — data residency, feature drift, and free-tier terms are outside our control. Also, Gary + global team would have to adopt a Chinese SaaS too, which most won't love. Keep as fallback (especially **Lark/Feishu**) if self-hosting is rejected.

### Option B: Self-hosted open source (build once, own forever)
| Platform | Model | Mobile app | China push | Notes |
|---|---|---|---|---|
| **Zulip** | **Streams + mandatory topics** — closest to Telegram forums | Flutter app (zulip-flutter), forkable, APK downloadable | FCM-based (blocked in CN) — needs custom work (see §8) | 2 GB RAM min / 4 GB recommended; 100% open source; free; the only one with *topics* as a first-class concept |
| **Rocket.Chat** | Channels + threads (Slack-like, not topics) | React Native, white-labelable | FCM + own push; vendor channels need work | MongoDB — heavier ops; threads ≠ topics |
| **Mattermost** | Channels + threads (Slack-like) | React Native, forkable | FCM + own push; vendor channels need work | Heavier; threads ≠ topics |

**Verdict: Zulip wins** because the *topic* is the fundamental unit of organization — the exact model Gary described. Self-hosted means no per-seat cost, no data leaving our infra, and no GFW dependency except the reachable server itself.

### Option C: Build from scratch — **rejected**
Months of engineering for a solved problem; 70%+ custom enterprise chat projects fail or rot. No.

---

## 5. Recommendation — Self-Hosted Zulip + White-Label Android App

### Why Zulip (mapped to our exact ask)
| Gary's ask | Zulip equivalent |
|---|---|
| "Android app" | Forked `zulip-flutter` app, white-labeled (our name/icon/colors), direct APK |
| "Individual team" | **Stream** (or a separate Zulip **realm/organization** per team) |
| "Within the team, different topics" | **Topics** inside each stream — mandatory, named, follow-able |
| "Like what we have right now for Telegram" | 1:1 structural clone of channel + topic forums |

- **Multiple organizations** on one server are supported (subdomain per realm) — so if China team and global DAO team need hard separation, each gets its own realm; recommended default is a **single realm** with streams-per-team for simplicity.
- Free self-hosting, Apache-2.0, huge docs, active development (Flutter app is the current official mobile app since June 2025).

### What it costs
| Item | Spec | Est. / month |
|---|---|---|
| EC2 (AWS ap-east-1 Hong Kong) | t3.small–t3.medium, 20–40 GB gp3 | ~US$25–50 |
| EBS snapshot backups | weekly | ~US$2–5 |
| Domain (Route 53 / registrar) | ~US$1–2/mo amortized | ~US$2 |
| TLS certs | Let's Encrypt | $0 |
| **Total** | | **~US$30–60** |

---

## 6. Target Architecture

```
┌─────────────────────────────────────────────────────────┐
│  AWS ap-east-1 (Hong Kong) — no ICP needed              │
│                                                         │
│  EC2 t3.medium (4GB RAM)                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Zulip server (Docker or native install)        │    │
│  │  - Nginx (TLS, Let's Encrypt)                  │    │
│  │  - PostgreSQL + Redis + memcached + RabbitMQ    │    │
│  │  - Realm(s): e.g. team.truesight.me            │    │
│  │  - SMTP relay for email notifications           │    │
│  └─────────────────────────────────────────────────┘    │
│  EBS snapshot (weekly) + off-site backup of exports     │
└─────────────────────────────────────────────────────────┘
        ▲                                ▲
        │ HTTPS/WSS                        │ APK download + updates
        │                                  │
┌───────┴───────┐                 ┌────────┴────────┐
│ Android app   │                 │ Distribution    │
│ (fork of      │                 │ - Internal page │
│  zulip-flutter│                 │   / QR code     │
│  white-labeled)│                │ - Auto-update   │
└───────────────┘                 │   endpoint      │
                                  └─────────────────┘
```

### 6.1 Teams & topics mapping (Telegram → Zulip)
Recommended default: **one Zulip realm = the DAO workspace**; **one stream per team**; **topics inside each stream** preserve today's Telegram topics.

| Telegram today | Zulip target |
|---|---|
| Channel: TrueSight DAO | Realm (subdomain, e.g. `team.truesight.me`) |
| Topic: QR / Cacao bags | Stream `Cacao Ops` + topics per bag batch/QR thread |
| Topic: Partner outreach | Stream `Partners` + topics per partner |
| Topic: Oracle readings | Stream `Oracle` + topic per reading |
| Topic: China / Aora | Stream `China Ops` + topics (GACC, Aora events, comms…) |
| DM with a governor | Zulip 1:1 DM |
| Announcements (pinned) | Stream `#announcements` (topic `general`) |

If hard team separation is ever required, add a **second realm** (subdomain) — one server, N realms.

### 6.2 Why Hong Kong, not mainland
- **No ICP filing required** for servers outside mainland (ICP is determined by server location; HK needs none).
- HK→mainland latency ~20–40 ms vs 200–300 ms from US.
- No Chinese legal entity needed yet (needed for mainland hosting + ICP — too heavy for an internal tool today).
- Risk to note: HK traffic still crosses international gateways; for a lean internal team this is fine.

---

## 7. Security
- TLS 1.2+ (Let's Encrypt), HSTS.
- Disable public signup; invite-only (email domain or invite links).
- MFA (TOTP) enforced for all users.
- Firewall: 22 (SSH, key-only), 80/443 only; SSH restricted to known IPs (Gary/Sophia).
- Backups: weekly EBS snapshot + monthly `zulip export` to a separate bucket/box.
- Least-privilege roles: admins = Gary/Sophia; everyone else member/guest.

---

## 8. Android App: White-Label Fork + China Distribution + Push

### 8.1 Fork & rebrand
- Fork **`zulip/zulip-flutter`** (Apache-2.0, current official app).
- Rebrand: app name, launcher icon, splash, accent colors (e.g. `flutter_app_rebrand` Dart package automates package-name/icon/app-name changes).
- Point the app's default server URL at our realm; optionally pre-configure the realm so users only enter email+password (or SSO).
- Build **signed release APK** (our own keystore).
- Maintenance: rebase our fork on upstream releases for security/bug fixes (documented upgrade cadence).

### 8.2 Distribution (no Google Play)
- **Direct APK** hosted on an internal page (or our own domain) + QR code for phone install.
- Users enable "install from unknown sources" — acceptable for a small internal team; note that Chinese ROMs (MIUI, HarmonyOS) add extra install confirmation steps — plan a 1-page Chinese-language install guide.
- **Auto-update:** GitHub Releases-style endpoint or a tiny self-hosted version JSON; app checks and prompts. (Do NOT rely on Google Play update channel.)
- Optional later: Huawei AppGallery (needs HMS + registration) — only if team size grows; not needed for MVP.

### 8.3 Push notifications in China (the hard part)
**Problem:** FCM (Google's push) is blocked — Google Play Services is absent on most mainland devices, so Firebase push never arrives.

Options, in order of pragmatism:
| Option | Effort | Reliability | Notes |
|---|---|---|---|
| **A. In-app realtime + polling (MVP)** | Low | Good | App keeps a WebSocket/WSS connection to the Zulip server while open; on Android, a foreground service + periodic poll keeps messages fresh. No OS push for force-killed app. **Ship this first.** |
| **B. UnifiedPush** | Medium | Good | Open, decentralized push standard; works without Google; self-host the push server. Requires forking the app to add a UnifiedPush distributor integration + running a push endpoint. |
| **C. Vendor push SDKs (Huawei PushKit, Xiaomi MiPush, OPPO, vivo)** | High | Best | Integrate each vendor SDK into the fork (each vendor's device gets OS-level push). Zulip doesn't ship these; significant fork work, and no vendor SDK for non-vendor devices. Best long-term but heavy for MVP. |
| **D. Email fallback** | Low | Good | Zulip sends notification emails (SMTP relay) — email works fine in China; good safety net for important topics (@-mentions). |

**Recommendation:** Ship **A (WebSocket + poll + email fallback)** for MVP; evaluate **B/C** in a later phase once the team confirms push is actually a pain point (an internal team that keeps the app open often doesn't need OS push).

---

## 9. Execution Roadmap

### Phase 0 — Decisions & sign-off (≈ 1 week) — GATE: Gary
- [ ] Confirm **Zulip self-host** vs **Lark/Feishu fallback** (decision table in §4).
- [ ] Confirm **AWS ap-east-1 (HK)** hosting + budget (~$30–60/mo).
- [ ] Choose domain (e.g. `team.truesight.me` or China-facing subdomain).
- [ ] Confirm **single realm + streams-per-team** (default) vs multi-realm.
- [ ] Define initial team/stream list (China Ops, Cacao Ops, Partners, Oracle, Announcements…).
- [ ] Name/branding for the white-labeled app (or use Agroverse/TrueSight branding).
- [ ] Decide push approach: MVP = Option A only (WebSocket+poll+email) — revisit B/C after pilot.

### Phase 1 — Infrastructure (≈ 3–5 days)
- [ ] Create EC2 t3.medium in **ap-east-1** (Ubuntu 22.04/24.04 LTS), 30 GB gp3, Elastic IP.
- [ ] Route 53 (or registrar) DNS: A record for realm subdomain; MX/SPF for notification email.
- [ ] Security group: SSH from known IPs only; 80/443 open; no public signup.
- [ ] Set up Let's Encrypt (certbot) + HSTS.
- [ ] SMTP relay for notification emails (e.g. SES or a lightweight relay; verify deliverability to CN inboxes).
- [ ] Backup plan: weekly EBS snapshot + monthly `zulip export` to secondary storage; test restore once.

### Phase 2 — Zulip server deploy & config (≈ 3–5 days)
- [ ] Install Zulip (native installer or Docker) per official docs; **upgrade path documented**.
- [ ] Create realm + organization settings (name, logo, invite-only).
- [ ] Create admin accounts (Gary, Sophia); enforce MFA.
- [ ] Create initial streams/teams + topic templates (from Phase 0 list).
- [ ] Configure roles/permissions (who can create streams/topics).
- [ ] Configure uploads (file sharing) + storage limits.
- [ ] Smoke-test from mainland (ask Jerri/Ling to test latency + connectivity from Dongguan).

### Phase 3 — Teams/topics scaffolding + pilot (≈ 1 week) — GATE: pilot sign-off
- [ ] Seed the mapping from §6.1 (port current Telegram topic names to Zulip topics).
- [ ] Invite pilot users (Gary, Jerri, Ling, Liz, + 1–2 ops).
- [ ] Run a 1-week pilot on web/mobile; collect feedback (structure OK? latency? features?).
- [ ] Decide on push escalation (A→B/C) based on real usage.

### Phase 4 — Android app (≈ 2–3 weeks)
- [ ] Fork `zulip/zulip-flutter`; set up Flutter build env (or CI on the autopilot box).
- [ ] Rebrand (name, icon, splash, colors); set default server URL.
- [ ] Generate signing keystore; build signed release APK.
- [ ] Host APK on internal page + QR code; write Chinese-language install guide (unknown-sources steps per ROM).
- [ ] Auto-update check (version JSON endpoint) + in-app prompt.
- [ ] Test on representative devices (Xiaomi/Huawei/OPPO/vivo) in mainland.

### Phase 5 — Push (escalation, optional) (≈ 1–2 weeks)
- [ ] If pilot says push is needed: implement UnifiedPush (Option B) or vendor SDKs (Option C) in the fork.
- [ ] Self-host push endpoint; test on vendor ROMs.

### Phase 6 — Migration & rollout (≈ 1 week) — GATE: Gary approval
- [ ] Announce cutover; run Telegram + Zulip in parallel for 2 weeks.
- [ ] Port remaining active threads (copy/archive important topics).
- [ ] Deprecate Telegram for China team (keep for global/Gary if desired).
- [ ] Train team (1-page cheat sheet: streams vs topics vs DMs).
- [ ] Handover runbook to Sophia (backups, upgrades, user add/remove, incident response).

---

## 10. Migration from Telegram (concrete)
1. Export what matters: pin important topics/decisions (copy into Zulip topics; not a bulk import tool for Telegram→Zulip — manual port for ~dozens of topics is fine).
2. Parallel-run for 2 weeks; keep Telegram as archive.
3. Update all internal links/notebooks that reference the Telegram channel.

---

## 11. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| GFW blocks/throttles our HK server | Low–Med | High | HK is generally reachable; keep TLS/443 standard; monitor from mainland; fallback = Lark/Feishu; optional second region later |
| Push doesn't work well (no FCM) | Med | Med | MVP = WebSocket+poll+email; escalate to UnifiedPush/vendor SDKs only if needed |
| Fork maintenance burden (zulip-flutter rebase) | Med | Med | Schedule quarterly rebase; pin upstream releases; keep fork deltas minimal (branding only) |
| User adoption (new app, new habits) | Med | Med | 1:1 structure with Telegram; parallel run; short cheat sheet; name it well |
| Chinese ROM install friction | Med | Low–Med | Install guide per ROM; QR + page; test on team's actual devices |
| Server ops burden on Sophia | Med | Low | Scripted deploy/backup/upgrade; runbook; small surface |
| Email notifications blocked/delayed in CN | Low–Med | Low | Use reputable SMTP relay; treat email as fallback only |

---

## 12. Success Criteria (measurable)
- China team members (Jerri, Ling, + ops) actively using the app daily for ≥2 weeks post-cutover.
- 100% of active Telegram topics ported to Zulip topics (parity).
- App installs on all pilot devices; no open critical bug > 48 h.
- Latency from Dongguan ≤ ~100 ms round-trip (subjective: "feels instant").
- Push (if escalated) delivered within ~30 s on vendor ROMs.
- Total infra cost ≤ $100/month.

---

## 13. Open Questions for Gary
1. Self-host (Zulip) or fall back to Lark/Feishu? (I recommend self-host.)
2. Domain/branding for the app — TrueSight, Agroverse, or something China-friendly?
3. Should the **China team get its own realm** (hard-separated from global) or share one workspace with streams-per-team? (Default: shared, streams-per-team.)
4. Is OS-level push a must-have at launch, or is in-app + email acceptable for the pilot? (Recommend: pilot without OS push.)
5. Who are the first 5–10 pilot users (names + emails)?
6. Any need for **video/voice calls** built in? (Zulip calls need a third-party bridge — flag if required.)

---

## 14. Key References
- Zulip: https://zulip.com/self-hosting · https://github.com/zulip/zulip · multi-org: https://zulip.readthedocs.io/en/stable/production/multiple-organizations.html
- Zulip mobile (Flutter): https://github.com/zulip/zulip-flutter
- Rocket.Chat white-label: https://developer.rocket.chat/docs/mobile-app-white-labelling
- Mattermost custom mobile: https://docs.mattermost.com/deployment-guide/mobile/distribute-custom-mobile-apps.html
- UnifiedPush: https://unifiedpush.org
- China hosting/ICP facts: HK = no ICP, 20–40 ms latency (chinafy.com / flow.asia guides)
- Feishu/Lark/DingTalk/WeCom comparison: jetservices.com.cn guide

---
*Prepared for Gary · TrueSightDAO · purpose: heal the world with love — restore 10,000 hectares of Amazon rainforest.*
