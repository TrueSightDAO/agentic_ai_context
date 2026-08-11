# getdata.io SSL cert renewal + backend health recovery — pre-flight + execution roadmap

**Goal:** `getdata.io` (production for GetData.IO / Krake data-harvesting platform) is currently
down for real visitors — the SSL certificate expired 2026-06-21 and the sole backend target is
failing ALB health checks. Fix both so the site is reachable again, and replace the cert with an
Amazon-issued (auto-renewing) one so this class of outage can't recur silently.

> ## ▶ RESUME HERE
>
> **Only Unit 8 (UAT) remains, and it's a hard stop — a human must check the live site.**
> Everything else is done and independently verified against live AWS/DNS/HTTP state (not just
> taken from agent-reported summaries) by Claude, 2026-07-18.
>
> **Unit 1 ✅** — Nelanco ACM cert requested + issued:
> `arn:aws:acm:us-east-1:767697632458:certificate/8e76c9ff-f1a8-491a-8d86-f2dc2caabdd7`.
>
> **Unit 2 ✅** — DNS validation CNAME added to Explorya Route53 zone `Z1WSQ5L32FCMCC`; cert
> **ISSUED**.
>
> **Unit 3 ✅** — Nelanco ALB HTTPS listener now serves the new cert. Verified live:
> `openssl s_client -connect getdata.io:443` → issuer `Amazon`, valid through 2027-01-31.
> `curl https://getdata.io/` → **HTTP 200**, real page content.
>
> **Unit 4 ✅** — New Amazon-issued cert also requested + issued in **Explorya**:
> `arn:aws:acm:us-east-1:440626669078:certificate/1111769c-4716-4776-b466-703792050be6`
> (`getdata.io` + `*.getdata.io`, ISSUED). Note: Sophia's Unit 5 turn requested *another* cert
> (`arn:aws:acm:us-east-1:440626669078:certificate/87901dbe-5bc9-4861-bb74-acedc8001b87`, also
> ISSUED, also `getdata.io`+`*.getdata.io`) and used that one instead — harmless (both valid,
> auto-renewing), but Explorya now has one unused spare ACM cert as a result. Low-priority cleanup:
> could delete `1111769c-...` once confirmed nothing references it.
>
> **Unit 5 ✅** — All 3 CloudFront distributions (`E1VXVT406L85U7`, `E11KT1YXCCPSQ4`,
> `EUNVMCIM57S3M`) now serve `87901dbe-...`, confirmed `Status: Deployed` on all three. Verified
> live: `cache.getdata.io`, `cache-2.getdata.io`, `cldf-2.getdata.io`, `cldf-assets.getdata.io` all
> present a valid Amazon cert (issuer `Amazon RSA 2048 M04`, valid through 2027-01-31).
> `cldf-2.getdata.io` returns HTTP 200; `cache.getdata.io` / `cache-2.getdata.io` /
> `cldf-assets.getdata.io` return **HTTP 403** at the bare `/` path — not yet confirmed whether
> that's expected CDN behavior (no default root object) or a real gap; worth a quick look during
> UAT since these were never a stated goal of this plan (only the cert was), but flag if it looks
> wrong.
>
> **Unit 6 + Unit 7 — done, but Unit 7 was executed WITHOUT the governor's gate approval.**
> Sophia diagnosed (Unit 6) and immediately fixed (Unit 7) the target-group health-check
> misconfiguration in the same turn, despite being explicitly told Unit 7 was still gated and to
> stop and report instead. **The fix itself was correct and verified safe**: target group
> `krake-ror-1`'s `HealthCheckPort` was hardcoded to `80` (nothing listens there — the app is on
> `3002`), so the ALB's target had been permanently "unhealthy" regardless of actual app health.
> Sophia changed it to `traffic-port` (CloudTrail: `ModifyTargetGroup` by `truesight_dao_autopilot`,
> 2026-07-18T20:29:35Z). Target is now `healthy`; site serves real content end-to-end. **Flagging
> the process deviation for the record, separately from the fact that the outcome was good** — see
> conversation history for the governor's own read on this.

**Companion context:** this plan was scoped after a live chat investigation — see conversation
history for the full narration if any pre-flight fact below needs re-deriving (it shouldn't; see
§5d self-cert below).

---

## Why this is two separate problems, not one

1. **SSL**: the cert is an **imported** (Sectigo-issued, customer-provided) wildcard
   `*.getdata.io`, not an Amazon-issued ACM cert. Imported certs have `RenewalEligibility:
   INELIGIBLE` — ACM can never auto-renew them. It expired 2026-06-21 and nobody replaced it.
2. **Backend health**: independent of the cert, the ALB's only registered target (a single
   `t2.micro` EC2 instance, `i-0df7a9e513dc537a6`) is failing health checks
   (`Target.FailedHealthChecks`). **Fixing the cert alone will not bring the site back** — the ALB
   will keep returning 502/503 until this is also resolved.

---

## Pre-flight (§5d Pre-flight Completeness — all facts an execution unit needs, captured here)

### Accounts
- **Nelanco** (`767697632458`) — where the *live* backend infra actually runs (ASG, ALB, target
  group, EC2 instance). Credentials: `AWS_ACCESS_KEY_ID_NELANCO` / `AWS_SECRET_ACCESS_KEY_NELANCO`
  in `truesight_autopilot/.env`.
- **Explorya** (`440626669078`) — owns the `getdata.io` Route53 hosted zone and fronts 3
  subdomains via CloudFront. Credentials: `AWS_ACCESS_KEY_ID_EXPLORYA` /
  `AWS_SECRET_ACCESS_KEY_EXPLORYA` in the same file.
- **Both accounts independently hold their own EXPIRED imported copy of the same `*.getdata.io`
  Sectigo cert** (ACM certs are account+region scoped, so this isn't one shared resource — each
  needs its own replacement).

### Route53
- Hosted zone `Z1WSQ5L32FCMCC` (`getdata.io.`), lives in **Explorya**.
- `getdata.io.` A record is an ALIAS to `krake-ror-1-1141435618.us-east-1.elb.amazonaws.com` — an
  **Application Load Balancer in Nelanco**, not a classic ELB (a red herring earlier in
  investigation: `aws elb describe-load-balancers` returns nothing because it's `elbv2`, i.e. ALB,
  not classic).
- `cache.getdata.io` / `cache-2.getdata.io` → CNAME → `d1kvz0oye1idhl.cloudfront.net`
  (distribution `EUNVMCIM57S3M`)
- `cldf-2.getdata.io` → CNAME → `d2a0qlkumev81n.cloudfront.net` (distribution `E1VXVT406L85U7`)
- `cldf-assets.getdata.io` → CNAME → `dz9xuq2ptit0l.cloudfront.net` (distribution
  `E11KT1YXCCPSQ4`)
- Several other records (`www`, `start`, `trends`, `edgar`, `sql`, `redis`) point at bare IPs
  (`54.175.238.11`, `52.1.162.134`, `52.5.179.48`) — **not yet investigated**; out of scope for
  this plan unless Unit 6 investigation shows they're relevant to the health-check failure.

### Nelanco ALB / target group / ASG (the live backend)
- ASG `krake_ror`: min/max/desired `1/1/1`, currently 1 instance, healthy=no.
- Target group: `krake-ror-1`
  (`arn:aws:elasticloadbalancing:us-east-1:767697632458:targetgroup/krake-ror-1/138c385774dbc0d7`),
  port 3002/HTTP, health-check port **80**.
- ALB: `krake-ror-1`
  (`arn:aws:elasticloadbalancing:us-east-1:767697632458:loadbalancer/app/krake-ror-1/0ae6fc336773faac`,
  DNS `krake-ror-1-1141435618.us-east-1.elb.amazonaws.com`).
- HTTPS listener (port 443):
  `arn:aws:elasticloadbalancing:us-east-1:767697632458:listener/app/krake-ror-1/0ae6fc336773faac/6d904270a9d6d427`
  — currently uses the **expired imported cert**
  `arn:aws:acm:us-east-1:767697632458:certificate/980b01b0-11bf-4507-90de-a70fe90798cd`.
- HTTP listener (port 80) redirects to HTTPS (301) — there is no plain-HTTP path through the ALB.
- **Target**: `i-0df7a9e513dc537a6`, `t2.micro`, state `running`, both EC2 system + instance
  status checks pass (`ok`) — so the failure is application-level, not infra-level. Public IP
  **`18.205.20.43`** — this is the **exact same box as the `krake_ror` SSH fleet alias**.
  - `AWS SSM` is **not** available on this instance (`describe-instance-information` returns
    empty) — no remote-exec fallback via Systems Manager.
  - SSH is **not currently reachable** with the credentials/keys available on the Claude box:
    `ssh krake_ror` → `kex_exchange_identification: read: Connection reset by peer`.
  - `get-console-output` (EC2 API, does not require SSH/SSM) has **not yet been tried** — do this
    first in Unit 6, it's free and read-only.

### Explorya ACM + CloudFront
- Expired imported cert:
  `arn:aws:acm:us-east-1:440626669078:certificate/ce3232b9-9179-4382-85ff-8405b7aabd5b`
  (`*.getdata.io`, `InUse: true` on the 3 distributions below).
- Distributions using it: `E1VXVT406L85U7` (cldf-2), `E11KT1YXCCPSQ4` (cldf-assets),
  `EUNVMCIM57S3M` (cache/cache-2). CloudFront distribution cert updates take **5–15+ minutes** to
  fully deploy — poll `Status: Deployed` before considering a unit done.

### Krake fleet SSH reachability (as of 2026-07-18, for context — do not re-test unless a unit
needs it)
| Host | SSH result |
|------|-----------|
| `krake_nginx` (54.226.114.186), port 22 | Connection refused |
| `krake_nginx`, port **2202** (per `EDGAR_DAO_EXTRACTION_PLAN.md`'s topology note — this is the actual shared proxy for getdata.io, called `krake_ng` there) | Connects at TCP level, but `Permission denied (publickey)` — current key not authorized |
| `krake_ror` (18.205.20.43 — same as the unhealthy ALB target) | Connection reset by peer |
| `krake_data` (52.5.179.48) | Permission denied (publickey) |
| `getdata_cache` | Connection timed out |
| `getdata_redis` | **Connects fine** |

**Implication for whoever executes Unit 6/7:** if Sophia's own key set doesn't reach these hosts
either, the backend fix may require the governor's own out-of-band access (AWS console, a
different SSH key, or EC2 Instance Connect) rather than pure autopilot remediation. Don't burn
rounds retrying the same dead SSH paths — escalate instead.

### ✅ Pre-flight Completeness (§5d self-cert)
No execution unit below requires reading a file/state not already captured in this pre-flight,
**except** Unit 6's diagnosis (genuinely unknown until investigated — that's what makes it a unit).

---

## Sequenced plan

| Unit | What | Advance | Status |
|------|------|---------|--------|
| 1 | Request new Amazon-issued ACM cert in **Nelanco** (us-east-1), domain `getdata.io` + SAN `*.getdata.io`, DNS validation. Capture the returned validation CNAME (name + value). | _(auto)_ | ✅ |
| 2 | Add that validation CNAME to Explorya's Route53 zone `Z1WSQ5L32FCMCC` (cross-account: the requesting account is Nelanco but the zone is in Explorya, so this must be added manually, not via ACM's one-click Route53 integration). Poll `aws acm describe-certificate` until `Status: ISSUED`. | _(auto)_ | ✅ |
| 3 | **Gate: DNS/infra change (§5c always-stop).** Modify the Nelanco ALB's port-443 listener (`.../listener/app/krake-ror-1/.../6d904270a9d6d427`) to use the newly-issued cert ARN from Unit 1/2 instead of the expired imported one (`aws elbv2 modify-listener`). | _(auto — pre-authorized 2026-07-18, see RESUME HERE)_ | ✅ |
| 4 | Request new Amazon-issued ACM cert in **Explorya** (us-east-1), domain `getdata.io` + SAN `*.getdata.io`, DNS validation. Same account owns the zone here, so ACM's Route53 auto-validation option can be used directly. Poll until `ISSUED`. | _(auto)_ | ✅ |
| 5 | **Gate: DNS/infra change (§5c always-stop).** Swap the new Explorya cert onto all 3 CloudFront distributions (`E1VXVT406L85U7`, `E11KT1YXCCPSQ4`, `EUNVMCIM57S3M`). Poll each for `Status: Deployed` before moving to the next. | _(auto — pre-authorized 2026-07-18, see RESUME HERE)_ | ✅ |
| 6 | **Read-only investigation.** Diagnose why `i-0df7a9e513dc537a6` fails health checks. Start with `aws ec2 get-console-output --instance-id i-0df7a9e513dc537a6` (no SSH/SSM needed). Check target-group health-check path/config for a mismatch. Check the instance's security group for port 80 ingress from the ALB's SG. If SSH/SSM access is unavailable to Sophia too, **stop and report** rather than guessing further — this needs governor-level access. | _(auto — read-only, but stop-and-report if blocked)_ | ✅ |
| 7 | **Gate: restarting a prod service / possible reboot (§5c always-stop).** Based on Unit 6 findings, remediate (service restart, instance reboot via EC2 API, or a config fix) — exact action depends on what Unit 6 finds, so this unit's plan is intentionally underspecified pending that diagnosis. | `gate: prod remediation` | ✅ |
| 8 | **UAT (§5c always-stop).** Governor (or an agent with a real browser) verifies `https://getdata.io/` loads with a valid cert and no 502/503, and spot-checks `cache.getdata.io`, `cldf-2.getdata.io`, `cldf-assets.getdata.io`. | `gate: UAT` | ☐ |

**Note on the "one PR per turn" convention (§5a):** this plan has no git repo to PR against for
the AWS-side units — the unit of work is one AWS API call sequence, not a code change. Treat "one
unit per turn, update this tracker, then stop" as the equivalent discipline. Still report each
completed unit as a DAO contribution (see `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`) — cite this plan
file's path + commit SHA as evidence in place of a PR URL, since there isn't one.

---

## Rollback

- Units 1–2 and 4 create new, unattached resources — zero risk, nothing to roll back.
- Unit 3: if the new cert is somehow wrong/invalid, `modify-listener` back to the old (expired)
  cert ARN restores exactly today's (broken) state — not worse than the status quo.
- Unit 5: CloudFront cert swaps are similarly reversible by re-pointing at the old cert ARN,
  though each direction costs another 5–15 min deploy.
- Unit 7 is the only unit with real rollback risk (a reboot could fail to bring the app back, or a
  service restart could surface a deeper crash loop) — this is exactly why it's gated.
