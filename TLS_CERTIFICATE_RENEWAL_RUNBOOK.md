# TLS Certificate Renewal Runbook — TrueSightDAO ecosystem

**Last updated:** 2026-08-09 · **Owner:** Sophia (autopilot) / Gary

This is the **single authoritative reference** for every TLS certificate in the
TrueSightDAO ecosystem — who renews it, how, and what to do when one is critical.
It exists because `edgar.truesight.me`'s cert silently expired on **2026-08-08**
(the renewal config pointed at a dead ACME account), which blocked all Edgar
submissions until manually re-issued.

---

## 1. Domain inventory (ground truth, probed 2026-08-09)

### A. Certbot-managed — Let's Encrypt via nginx on our boxes (auto-renew)

These are the subdomains whose HTTPS is enabled **via the certbot → nginx route**
(the route this runbook covers; all use HTTP-01 through the nginx authenticator
and renew via `certbot.timer`):

| Endpoint | Serving host (verified) | nginx block | Renewal | Expiry (2026-08-09) |
|---|---|---|---|---|
| `edgar.truesight.me` | seni_ror (54.211.179.126) | `edgar.conf` | `certbot.timer` (twice daily) | **2026-11-07** ✅ |
| `perch.truesight.me` | seni_ror (54.211.179.126) | `perch.conf` | `certbot.timer` | **2026-09-11** (33d — next to renew) |
| `sophia.truesight.me` | autopilot (3.214.167.219) | `sophia` | `certbot.timer` + snap timer | 2026-10-28 ✅ |
| `beta.edgar.truesight.me` | TLS live (Nov 7) — cert **not** present on seni_ror or autopilot; managing host unconfirmed | unknown | unknown | 2026-11-07 ✅ (fleet monitor covers it) |

> **Note on perch:** the autopilot box also holds a **replica** `perch.truesight.me`
> cert (expires 2026-09-11 13:11 UTC) but has **no** perch nginx :443 server block —
> it is NOT serving traffic. The live perch cert is the seni_ror one (expires
> 2026-09-11 22:05 UTC). Don't confuse the two copies.

### B. AWS ACM — Amazon-managed (auto-renew, no action)

| Endpoint | Account | Expiry |
|---|---|---|
| `getdata.io` (+`*.getdata.io`) | explorya 440626669078 | 2027-01-31 ✅ |
| `getdata.io` (+`*.getdata.io`) | nelanco 767697632458 | 2027-01-31 ✅ |

### C. GitHub Pages — Let's Encrypt auto (no action)

`truesight.me`, `www.truesight.me`, `dapp.truesight.me`, `beta.truesight.me`,
`oracle.truesight.me`, `butterfly-effect-club.truesight.me`, `heierling.truesight.me`,
`tribomirimbahia.truesight.me`, `agroverse.shop`, `www.agroverse.shop`,
`beta.agroverse.shop`, `capoeira.agroverse.shop` — all auto-renewed by GitHub, all OK.

### D. External / manual renewal (⚠️ highest risk)

| Endpoint | Issuer | Expiry | Owner | Notes |
|---|---|---|---|---|
| `chatbot.truesight.me` | Sectigo | **2026-11-08** | manual | bought cert, renew ~Oct |
| `affiliate.agroverse.shop` | ZeroSSL | **2026-09-20** (33d) | manual | **first to hit WARN** |
| `api.truesight.me` | Sectigo (edgar cert!) | 2027-01-13 | ⚠️ | **serving a stale edgar cert** — misconfig, see §6 |

### E. Known dead / no TLS (informational)

`mtproxy.truesight.me`, `claude.truesight.me`, `orchard.truesight.me`,
`www.getdata.io`, `app.getdata.io` — no listener on :443 (DNS may still point).

---

## 2. Renewal automation status (who renews what)

| Host | Timer | Status |
|---|---|---|
| **seni_ror** (edgar, perch) | `certbot.timer` — `OnCalendar=*-*-* 00,12:00:00` | ✅ enabled, healthy |
| **autopilot** (sophia) | `certbot.timer` + `snap.certbot.renew.timer` | ✅ enabled |
| **autopilot** (fleet check) | `tls-cert-check.timer` — daily 06:00 UTC | ✅ enabled (new 2026-08-09) |
| ACM / GitHub Pages | AWS / GitHub managed | ✅ n/a |

## 3. Monitoring — `tls-cert-check.timer` (NEW 2026-08-09)

Runs **daily 06:00 UTC** on the autopilot box. Checks all live endpoints' cert
`notAfter`, flags WARN (<30d) / CRITICAL (<15d) / EXPIRED, and posts a
**Telegram alert** to the working group on CRITICAL. Output:
`/opt/truesight_autopilot/artifacts/tls_cert_status.txt`.

```bash
systemctl status tls-cert-check.timer        # enabled, next run 06:00
journalctl -u tls-cert-check.service -n 40   # last run output
```

Manual run: `sudo systemctl start tls-cert-check.service`.
Script: `/opt/truesight_autopilot/scripts/tls_cert_check.sh` (deployed; source lives
in the truesight_autopilot repo — promote via PR per SOP).

## 4. Incident postmortem — 2026-08-08 edgar cert expiry

- **Symptoms:** all `submit_contribution` calls failed with
  `SSLCertVerificationError: certificate has expired`; `edgar.truesight.me` TLS broken.
- **Root cause:** renewal config (`/etc/letsencrypt/renewal/edgar.truesight.me.conf`)
  used `authenticator = dns-route53` (the EXPLORYA-era method) and referenced a
  **stale ACME account** under the retired v01 API — but the NELANCO box only has
  the `nginx`/`standalone`/`webroot` plugins and no such account. Every auto-renewal
  since the migration had silently failed; the cert expired 2026-08-08 23:12 UTC.
- **Fix (applied):** `sudo certbot certonly --nginx -d edgar.truesight.me` → fresh
  Let's Encrypt cert (valid to 2026-11-07), rewrote the renewal config to
  `authenticator = nginx` / `installer = nginx` with a **new v02 ACME account**.
  Verified: `certbot renew --dry-run` → *all simulated renewals succeeded*.
- **Prevention now in place:** corrected renewal config + `tls-cert-check.timer`
  daily monitor + this runbook. The same failure mode is now caught within 24h.

## 5. Emergency renewal procedure

### Certbot (our boxes — edgar / perch / sophia / beta.edgar)

```bash
# On the host serving the cert:
sudo certbot certonly --nginx -d <domain>     # HTTP-01 via nginx (fast, no plugin needed)
#   or if nginx isn't the serving host:
sudo certbot certonly --webroot -w /var/www/html -d <domain>
sudo systemctl reload nginx                   # make the new cert live
sudo certbot renew --dry-run                  # confirm the automated path works
```

**Golden rules:**
- Use the **nginx** authenticator (or webroot) — NOT `dns-route53` unless the
  `certbot-dns-route53` plugin + IAM creds are installed on that box.
- After ANY manual issue, run `certbot renew --dry-run` to prove the timer path.

### AWS ACM — no action (Amazon auto-renews); imported certs (expired ones at
`*.getdata.io` 2026-06-21) are superseded by Amazon-issued certs — safe to ignore.

### External (chatbot, affiliate) — buy/renew via issuer; update this runbook when done.

## 6. Open issues / callouts

- ⚠️ **`api.truesight.me` serves a stale `edgar.truesight.me` Sectigo cert** (valid
  to Jan 2027, wrong CN). It works (browsers warn) but is a misconfig — the nginx
  block on the API host should serve a proper `api.truesight.me` cert. **Follow-up.**
- ⚠️ **`affiliate.agroverse.shop`** (ZeroSSL, expires **2026-09-20**) is the nearest
  manual renewal — monitor will alert at Sep 5 (15d).
- ⚠️ **`beta.edgar.truesight.me`** — TLS live but the managing certbot host is
  unconfirmed (not on seni_ror or autopilot). Locate it so its renewal timer can be
  verified. **Follow-up.**
- Dead endpoints (`mtproxy`, `claude`, `orchard`, `www/app.getdata.io`) — DNS still
  points; consider pruning or documenting as intentionally offline.

## 7. Runbook test-drive (done 2026-08-09)

- `sudo certbot renew --dry-run --cert-name edgar.truesight.me --no-random-sleep-on-renew`
  → **Congratulations, all simulated renewals succeeded** ✅
- `tls-cert-check` first run → all 16 live endpoints OK, FAIL=0 ✅
- `certbot.timer` on seni_ror → enabled, next run within 12h ✅
