# sentiment_importer (Edgar) — operational notes

Production deploy and runtime gotchas for the Rails app in the
[`sentiment_importer`](https://github.com/TrueSightDAO/sentiment_importer) repo,
deployed as **Edgar** on **`https://edgar.truesight.me`**.

See **`PROJECT_INDEX.md`** for the feature surface (DAO API, Sidekiq
workers, Agroverse checkout shipping, newsletter open tracking, inventory
snapshot, etc.). This file is scoped to ops: how to deploy, what to watch,
and the gotchas that bite first-time deployers.

---

## Production topology

Two EC2 hosts in the **TRUESIGHT_DAO_AUTOPILOT** AWS account (post-2026-05-11
migration off the Cypher account). SSH aliases must exist in the operator's
`~/.ssh/config`:

| Alias          | IP              | Role                                | Systemd unit      | Monit                                          |
|----------------|-----------------|-------------------------------------|-------------------|------------------------------------------------|
| `seni_ror_new` | `3.90.179.151`  | Rails web server (port **3002**)    | `seni_ror.service`| http://3.90.179.151:2812/seni_ror              |
| `seni_sk_new`  | `54.163.216.235`| Sidekiq workers                     | `seni_sk.service` | http://54.163.216.235:2812/sidekiq             |

Repo lives at `/home/ubuntu/sentiment_importer` on both hosts. Both services
run under the `ubuntu` user. Route53 (`edgar.truesight.me`) lives in the
same TRUESIGHT_DAO_AUTOPILOT account and points at `seni_ror_new`.

> The pre-migration aliases `seni_ror` (`54.211.179.126`) and `seni_sk`
> (`3.83.175.151`) point at the Cypher-account hosts. Those instances are
> kept around for rollback only; do **not** deploy to them.

---

## Deploying master → production

From the `sentiment_importer` repo root on the operator's laptop:

```bash
./deploy.sh                 # full deploy: stage → migrate → precompile → restart both
./deploy.sh --skip-migrate  # no schema change in this release
./deploy.sh --ror-only      # Rails host only
./deploy.sh --sk-only       # Sidekiq host only
```

The script's ordering is deliberate:

1. **Stage both hosts in parallel** — `git pull --ff-only` + `bundle install`
   while old processes keep serving. Zero downtime.
2. **`rake db:migrate` from `seni_sk`** — runs *before* either restart, so
   new code never meets the old schema. (User preference: migrate from the
   Sidekiq host rather than the Rails host.)
3. **`rake assets:precompile` on `seni_ror` while the old server is still
   serving**, then `systemctl restart seni_ror`. This is the downtime win:
   systemd's `ExecStartPre` re-runs precompile on restart but finds nothing
   to do, so actual down-window drops from "full precompile" (~minutes)
   to "Rails boot" (~11s measured on 2026-04-24).
4. **`systemctl restart seni_sk`** — workers pick up new code.
5. **Health check**: port `3002` on `seni_ror`, sidekiq PID + `systemctl
   is-active` on `seni_sk`.

### There is **no** auto-deploy on master merge

No GitHub Actions, no Heroku-style integration, no push webhook, no cron,
no systemd timer polls git. Merging to `master` alone does **not** pull
new code to the servers. You MUST run `./deploy.sh` (or manually
`sudo systemctl restart seni_ror` / `seni_sk` on each host) to redeploy.

Monit has `if memory usage > 75% then restart` directives, and each
restart re-runs systemd's `git pull` `ExecStartPre`, which CAN make it
*look* like auto-deploy is happening on busy days. Don't rely on this —
it's an emergent behavior, not a designed deploy path. Under-pressure or
low-traffic hosts can sit on stale code for hours.

### Prereqs on the operator laptop

- SSH aliases `seni_ror` and `seni_sk` in `~/.ssh/config` with the right
  key.
- `gh` CLI authed (for the surrounding PR flow).
- `ubuntu@` on each host has passwordless `sudo systemctl restart` —
  AWS ubuntu default; verify with `ssh seni_ror sudo -n systemctl is-active seni_ror` if you suspect a custom image.

---

## Gotcha: env vars only live in the systemd unit

`SECRET_KEY_BASE` (and `RAILS_ENV=production`) are set via the systemd
unit's `Environment=` directives on both hosts. They are **not** in
`~ubuntu/.profile`, `~/.bashrc`, or any `.env` file that an SSH session
inherits.

Consequence: any `rake` / `rails runner` command invoked directly over
SSH fails with:

```
rake aborted!
ArgumentError: Missing `secret_key_base` for 'production' environment,
  set this string with `rails credentials:edit`
```

### Fix pattern

Extract the unit's env via `systemctl show` and export it before running
rake:

```bash
for kv in $(sudo systemctl show seni_ror --property=Environment --value); do
  export "$kv"
done
bundle exec rake assets:precompile
```

`deploy.sh` wraps this as a `load_unit_env` helper — reuse the pattern
for any one-off rake runner you write against these hosts (data
backfills, cache warmers, etc.).

---

## Migration safety

`deploy.sh` runs `db:migrate` **before** restarting `seni_ror`, so the
old Rails code sees the new schema for a few seconds. This is fine for
**additive** migrations (add column nullable, add table, add index).

Destructive migrations (drop column, rename column, change type) WILL
take the old code down during that window and require a
maintenance-mode procedure that is **not** automated in `deploy.sh`.
Write backward-compatible migrations — two-phase if necessary (add new
column, ship code that writes to both, backfill, drop old column in a
later release).

---

## Runtime watch-points

- **Monit dashboards** (linked above) are the first place to look when a
  deploy looks sick — they show PID, uptime, memory. HTTP auth may be
  required depending on the monit config; the URLs above are what the
  operator hits.
- **Logs:** `journalctl -u seni_ror.service -f` on the Rails host,
  `journalctl -u seni_sk.service -f` on the Sidekiq host.
- **`/ping`** on the Rails host for a lightweight public health probe
  after deploys (no auth). `curl -sS https://edgar.truesight.me/ping`.
- **Bundler version drift** — the lockfile was generated on 1.17.3 but
  hosts run 1.17.2. Bundler emits a warning but proceeds; not blocking
  as of 2026-04-24.

---

## Nginx — `seni_ror_new` TLS termination

`seni_ror_new` runs nginx on :80/:443 in front of the Rails app on
`127.0.0.1:3002`. TLS comes from Let's Encrypt
(`/etc/letsencrypt/live/edgar.truesight.me/`), auto-renewed by certbot.

### Where the config lives

- **Source of truth:** `/etc/nginx/sites-available/edgar.conf`
- **Loaded by nginx:** `/etc/nginx/sites-enabled/edgar.conf` — must be a
  **symlink** to `sites-available/edgar.conf`. Verify:
  `ls -la /etc/nginx/sites-enabled/edgar.conf` should show
  `… -> /etc/nginx/sites-available/edgar.conf`.

If `sites-enabled/edgar.conf` is a regular file (no `l` flag), it is a
stale separate copy and edits to `sites-available/` will not propagate.
Re-link with:

```bash
sudo rm /etc/nginx/sites-enabled/edgar.conf
sudo ln -s /etc/nginx/sites-available/edgar.conf /etc/nginx/sites-enabled/edgar.conf
sudo nginx -t && sudo systemctl reload nginx
```

### The `\$host` heredoc trap (cost us a 4-hour outage on 2026-05-11)

When generating nginx configs over SSH via `bash -c "cat > … <<'EOF'"`,
**use `$host` literally**, not `\$host`. A single-quoted heredoc
(`<<'EOF'`) does **not** expand variables, so the backslash is preserved
verbatim. nginx then parses `\$host` as the literal character `\`
followed by the variable `$host`, and forwards `Host: \edgar.truesight.me`
upstream. Rails reads that as the host, every `redirect_to` becomes
`https://\edgar.truesight.me/…`, and webrick raises
`URI::InvalidURIError: bad URI(is not URI?)` — surfaces to the operator
as **502 Bad Gateway on every redirect-issuing endpoint** (sign-in,
sign-out, post-OAuth callback, `/companies/:slug`, …) while the static
landing page keeps working.

**Correct heredoc form** (variables stay literal because of the single quotes):

```bash
ssh seni_ror_new "sudo bash -c 'cat > /etc/nginx/sites-available/edgar.conf' <<'NGINX'
server {
  listen 443 ssl http2;
  server_name edgar.truesight.me;
  location / {
    proxy_pass http://127.0.0.1:3002;
    proxy_set_header Host \$host;                # ← BUG: nginx sees literal backslash
  }
}
NGINX"
```

vs.

```bash
ssh seni_ror_new "sudo bash -c 'cat > /etc/nginx/sites-available/edgar.conf' <<'NGINX'
…
    proxy_set_header Host $host;                # ← CORRECT inside <<'…' heredoc
…
NGINX"
```

Detection: `sudo nginx -T 2>/dev/null | grep -E '\\\\\$host|\\\\\$request_uri'`
should return nothing. If it returns lines, the config is poisoned.

End-to-end probe after any nginx edit:

```bash
curl -sI https://edgar.truesight.me/companies/KWR | grep -iE '^(HTTP|location)'
# expect: HTTP/2 302  +  location: https://edgar.truesight.me/users/sign_in
# bad:    location: https://\edgar.truesight.me/users/sign_in   ← \$host trap is back
```

---

## Google OAuth — `OmniAuth.config.full_host` is mandatory

Behind nginx, OmniAuth's auto-detection of the redirect URI can collapse
to a path-only string (`/users/auth/google_oauth2/callback`), which Google
rejects with **"Error 400: invalid_request — doesn't comply with Google's
OAuth 2.0 policy"** because relative paths can never match the absolute
URLs registered as Authorized Redirect URIs.

`config/initializers/omniauth.rb` sets `OmniAuth.config.full_host` in
production (default `https://edgar.truesight.me`, override with
`EDGAR_FULL_HOST`). Do not remove it. The Authorized Redirect URI in the
GCP OAuth client must include `https://edgar.truesight.me/users/auth/google_oauth2/callback`.

> Pending hardening (not blocking): rotate the hardcoded
> `client_secret` in `config/environments/production.rb` to a systemd
> drop-in env var, and migrate the OAuth client off the legacy Krake
> GCP project (667737028020) onto a TrueSight-DAO-owned project.

---

## Related context

- **`PROJECT_INDEX.md`** — sentiment_importer row for feature surface.
- **`WORKSPACE_CONTEXT.md`** §6 — Edgar vs. krake_ror naming
  (`edgar.truesight.me` is sentiment_importer, `getdata.io` is
  krake_ror; do NOT conflate).
- **`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`** — how AI agents report
  sentiment_importer work to the DAO ledger via `dao_client`.
- **`sentiment_importer/AGENT_WORKFLOW_GUIDE.md`** — in-repo mirror of
  the deploy section (kept in sync so operators find it from the repo's
  front door too).
