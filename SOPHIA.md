# Sophia — TrueSight DAO Autopilot Identity & Nginx Setup

## Identity

**Sophia** (Σοφία, Greek for *wisdom*) is the TrueSight DAO's wisdom layer — the unified identity for the autopilot service running on dedicated EC2 (`i-02c699d3d7efbdc82`, `us-east-1d`, t3.small, IP `100.52.234.163`).

Sophia replaces the generic "truesight_autopilot" name in all user-facing and operational contexts. The name reflects the DAO's commitment to collective intelligence: Sophia synthesises information across the ecosystem and surfaces actionable wisdom for governors, contributors, and automated systems.

## Capabilities

Sophia operates in two modes:

### 1. Oracle Advisory (`/oracle-advisory`)
- Replaces the legacy `GAS oracle_advisory_bridge` endpoint.
- Provides DAO-wide advisory context: governance proposals, treasury status, ecosystem health, and recent activity.
- Accessible at `https://sophia.truesight.me/oracle-advisory`.
- Consumes `ADVISORY_SNAPSHOT.md` (refreshed every 6h by `market_research/.github/workflows/advisory-snapshot-refresh.yml`) and other context sources.

### 2. Governor Chat (`/chat`)
- Reactive conversational interface for DAO governors via DApp `chat.html`.
- `POST /chat`, RSA-signed or JWT, DeepSeek-V3 with tool_calls for reading context/repos and opening fix PRs.

### 3. Autonomous SRE
- Proactive background monitoring: Gmail polling (GH Action failures, GAS errors), AWS CloudWatch/Cost Explorer.
- Diagnoses failures with DeepSeek-V3 (~30× cheaper than Claude/Kimi).
- Opens fix PRs autonomously — never auto-merges.

### 4. Code Generation
- Generates code, documentation, and configuration across DAO repos.
- Operates within the same safety constraints: PRs are opened for human review, never merged automatically.

## Subdomain

**`sophia.truesight.me`** — DNS A record pointing to `100.52.234.163`.

This subdomain routes all Sophia traffic through an Nginx reverse proxy on the autopilot EC2.

## Nginx Reverse Proxy Configuration

Sophia runs as a FastAPI application behind Nginx. The Nginx config is maintained in the `truesight_autopilot` repo:

**Reference:** [`truesight_autopilot/docs/SOPHIA_NGINX_SETUP.md`](https://github.com/TrueSightDAO/truesight_autopilot/blob/main/docs/SOPHIA_NGINX_SETUP.md)

### Key endpoints proxied

| Path | Upstream | Description |
|------|----------|-------------|
| `/` | `http://127.0.0.1:8000` | FastAPI app root (health check, docs) |
| `/oracle-advisory` | `http://127.0.0.1:8000` | Oracle advisory endpoint (replaces GAS bridge) |
| `/chat` | `http://127.0.0.1:8000` | Governor chat endpoint |
| `/docs` | `http://127.0.0.1:8000` | FastAPI auto-generated OpenAPI docs |

### SSL / Certbot Setup

SSL is managed via Let's Encrypt with Certbot:

1. Install Certbot and the Nginx plugin:
   ```
   apt update
   apt install -y certbot python3-certbot-nginx
   ```

2. Obtain and install a certificate for `sophia.truesight.me`:
   ```
   certbot --nginx -d sophia.truesight.me
   ```

3. Verify auto-renewal (Certbot sets up a systemd timer automatically):
   ```
   certbot renew --dry-run
   ```

Certbot auto-renews via systemd timer (`certbot.timer`). The Nginx config is updated automatically by Certbot to serve the certificate.

### Nginx Config Snippet (minimal)

```nginx
server {
    listen 80;
    server_name sophia.truesight.me;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name sophia.truesight.me;

    ssl_certificate /etc/letsencrypt/live/sophia.truesight.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sophia.truesight.me/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

See the full config in `truesight_autopilot/docs/SOPHIA_NGINX_SETUP.md`.

## Deployment

- **EC2 instance:** `i-02c699d3d7efbdc82` (`us-east-1d`, t3.small)
- **IP:** `100.52.234.163`
- **Code path:** `/opt/truesight_autopilot`
- **Systemd service:** `truesight-autopilot.service`
- **Repo:** [TrueSightDAO/truesight_autopilot](https://github.com/TrueSightDAO/truesight_autopilot)

## Safety Principles

- Sophia opens PRs for human review — never auto-merges.
- All autonomous actions are logged and auditable.
- The autopilot EC2 is separate from Edgar (`sentiment_importer`) to protect critical infrastructure.
