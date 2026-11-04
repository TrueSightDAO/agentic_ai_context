# GitHub access behind the Great Firewall of China

**Use this when** you (or your local LLM) are working from a network behind the Great
Firewall and `git clone` / `git fetch` / `git push` against `github.com` fails, hangs, or is
so slow it is unusable. The workaround is to relay Git traffic through one of the existing
US-based AWS boxes, which have full GitHub reachability and credentials already configured.

## The problem

`github.com` (and `objects.githubusercontent.com` / `codeload.github.com`) is intermittently
blocked and heavily throttled from mainland China. Symptoms vary run-to-run:

- `git clone`/`git fetch` hangs indefinitely, then times out.
- A single `curl` may return `200` in under a second (as it did during the 2026-11-04 test)
  while a bulk transfer of a few MB crawls — the block is **throttling and packet-loss based,
  not a clean 403**. Do not treat "one curl worked" as "GitHub is fine."
- `scp`/`rsync` of large payloads back from a US box is slow through the same path
  (observed: a 117 MB `git bundle` did not finish in 120 s → **< 1 MB/s**).

The reliable fix is to **do the Git operation on a box that is not behind the firewall** and
transfer only a minimal payload back, or to **tunnel the traffic** through that box.

## Available relays (already configured in `~/.ssh/config`)

| Alias | Host | Role | GitHub auth present | Use for |
|-------|------|------|---------------------|---------|
| **`nelanco-claude`** | `100.57.50.48` | Envoy's interactive Claude Code box | **`gh` logged in as `garyjob` (HTTPS) + SSH key authenticated** | **Preferred relay** |
| `sophia` | `sophia.truesight.me` | production autopilot | fine-grained PAT (`TRUESIGHT_DAO_AUTOPILOT`) | fallback — prefer not to disturb |
| `californian_proxy` | `54.215.51.8` | proxy box | not verified | fallback |

`nelanco-claude` is the right choice: it is the interactive / human-driven box (not production
autonomous infra), and it is already authenticated to GitHub as `garyjob` over both HTTPS and SSH.

## Step 0 — reachability test

```bash
# Does direct GitHub work right now? (one curl is NOT proof it is usable — see above)
curl -sS -o /dev/null -w "github %{http_code} in %{time_total}s\n" --connect-timeout 8 https://github.com

# Is the relay reachable?
ssh -o ConnectTimeout=8 -o BatchMode=yes nelanco-claude 'echo RELAY_OK; hostname'
```

If `RELAY_OK` prints, the rest of this doc works regardless of what the first command said.

## Method A — one-shot get-current-code via `git bundle`

Best for "pull down the current state of a repo to work offline." Produces a single
self-contained file that clones cleanly on the local Mac.

```bash
# 1. On the relay: clone + bundle (use --single-branch / --depth 1 if you only need HEAD,
#    NOT --mirror --all, unless you genuinely need full history + all refs)
ssh nelanco-claude 'cd /tmp && rm -rf repo.git && \
  git clone --mirror https://github.com/TrueSightDAO/<repo>.git repo.git && \
  git -C repo.git bundle create /tmp/<repo>.bundle --all && \
  ls -lh /tmp/<repo>.bundle'

# 2. Pull it back and clone locally
scp nelanco-claude:/tmp/<repo>.bundle . && \
git clone <repo>.bundle <repo>

# 3. Clean up the relay
ssh nelanco-claude 'rm -rf /tmp/repo.git /tmp/<repo>.bundle'
```

**Size matters — keep the payload small.** `agentic_ai_context` itself bundles to ~117 MB
(mirror) / ~92 MB (shallow single-branch) because of large tracked PDFs; at <1 MB/s through
the firewall that is minutes-to-tens-of-minutes. For code repos (usually much smaller) it is
fine. Prefer `--single-branch --depth 1` and `git bundle ... <branch>` (not `--all`) when you
only need current code. If you only need the working tree (no history), `git archive` is
smaller still.

## Method B — live push/pull via a SOCKS tunnel

Best when you need to keep working interactively (fetch/push repeatedly) while behind the
firewall.

```bash
# 1. Open a SOCKS5 proxy through the relay (background, stays up)
ssh -fN -D 1080 nelanco-claude

# 2. Route git HTTPS through it (one-off via -c, or set in .git/config for the session)
git -c http.proxy=socks5h://127.0.0.1:1080 clone https://github.com/TrueSightDAO/<repo>.git
git -c http.proxy=socks5h://127.0.0.1:1080 pull

# For an existing repo, set it persistently:
cd <repo> && git config http.proxy socks5h://127.0.0.1:1080
```

The local Mac's own `gh` credential helper (HTTPS remote) provides auth; the tunnel only
carries bytes. Kill the tunnel when done: `pkill -f 'ssh -fN -D 1080'`.

## Caveats

1. **Never copy secrets off the box.** Move code only. Skip `.env`, `credentials/`, `*.pem`,
   and any vault material. `git bundle` carries only what git tracks, but a box clone may still
   contain committed config — do not `tar` a full working tree that includes untracked secrets.
2. **Auth scope limits what you can pull.** Sophia's PAT is fine-grained to her repos; the three
   `bionpact_*` private repos are unreadable by everyone but Bionpact. Use `nelanco-claude`
   (`garyjob`) for `TrueSightDAO` repos you own.
3. **Direct GitHub may "work" intermittently.** Don't flip-flop between direct and relayed Git
   mid-operation; pick the relay for any non-trivial transfer.
4. **The relay is shared infra.** `nelanco-claude` has historically had disk-full hangs — clean
   up your `/tmp` clone/bundle after each pull (the `rm -rf` steps above).

*Verified 2026-11-04: direct GitHub HTTP 200 in 0.76 s (unreliable); `nelanco-claude` and
`sophia` SSH OK; `nelanco-claude` `gh` = `garyjob` + SSH auth OK; clone + `git bundle` on the
box OK; 117 MB scp through firewall > 120 s (bandwidth-limited).*
