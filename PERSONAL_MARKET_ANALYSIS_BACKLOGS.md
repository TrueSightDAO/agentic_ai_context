# Personal market analysis backlogs — per-contributor registry

Some contributors periodically ask an agent (Sophia, Claude Code, Cursor, etc.) to do
market/trading analysis for them **personally** — via Perch (`perch.truesight.me`) or otherwise.
This is **not** DAO work and the results do not belong in this repo or any other DAO-shared
artifact. Instead, each contributor who wants a running backlog keeps one in their **own
private repo**, and registers it here so any agent picking up a market-analysis request from
them knows where to log it.

## Registry

| Contributor | Backlog repo | Format |
|---|---|---|
| Gary Teh | `github.com/garyjob/perch-market-analysis` (private) | `BACKLOG.md` — **Queue** (upcoming items) + **Log** (dated entries, most recent first) |

Add yourself here (one row) if you want an agent to log your personal market-analysis work.
The repo must be **private** and under **your own** account — never a DAO org.

## Convention (for any agent)

**Trigger:** the contributor explicitly asks for market/trading analysis (tickers, sectors,
sentiment, a Perch pull, a portfolio question, etc.) — and *only* that. Don't log unrelated
requests just because they happen in the same session.

**Action:**
1. Check the table above for that contributor. If listed: `git pull` their repo first, do the
   analysis, append a dated entry to `BACKLOG.md`'s **Log** section (what was asked, what was
   found, any follow-up worth revisiting), add follow-ups to **Queue**, commit + push.
2. If the contributor **isn't listed** but wants this: offer to set up a private repo for them
   (use `garyjob/perch-market-analysis`'s `BACKLOG.md` as the template) and add a row to this
   table — only after they confirm. Don't assume a standing repo exists for someone who hasn't
   registered one.
3. If a contributor is listed but the current request isn't market analysis, don't touch their
   repo — the registry is opt-in for a specific trigger, not a general activity log.

## Why a registry instead of one hardcoded repo

Any contributor working with Sophia or Claude Code may want their own personal backlog. A flat
opt-in table here lets each person register their own private repo without any agent (or this
doc) needing to special-case names in prose or code.
