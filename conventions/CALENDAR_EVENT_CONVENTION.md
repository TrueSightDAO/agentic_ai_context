# Calendar-event convention — create on BOTH calendars, invite the named people

> **Status: STANDING (Gary, 2026-10-10).** Any agent that creates a calendar event
> on a governor's behalf MUST apply this convention. Agents: internalise it; do not
> wait to be re-told per event.

## Why this exists — the runner that already reads it

**A calendar entry alone does not wake the autopilot — the runner does (Gary, 2026-10-10).**

That runner **already exists and is live.** `truesight_autopilot` **#524** shipped
`app/calendar_watchdog.py`: a background loop inside the FastAPI lifespan (no separate
systemd unit — the same pattern as `email_poller`, `aws_monitor`, and `followup_loop`).
Every day it:

- reads the **next 7 days** (`CALENDAR_WATCH_DAYS_AHEAD`) of events from the
  **`admin@truesight.me`** calendar **only**;
- condenses each event into attention facts — **starts within 48 h → "confirm prep"**, and
  **un-responded attendees (`needsAction`) within 7 days → "awaiting response: <emails>"**;
- posts a plain-text digest into the Telegram topic `CALENDAR_WATCH_THREAD_ID` (**41588**) and
  a **Discord channel** (`CALENDAR_WATCH_DISCORD_CHANNEL_ID`), and **mirrors native Discord
  events** into it (`CALENDAR_WATCH_DISCORD_NATIVE_EVENTS` / `_ALL_EVENTS=true`).

**So a calendar entry is a *signal to the runner*, not the runner itself.** This convention
exists only to make sure the signal lands where the runner looks, and carries enough for the
digest to be actionable.

> ⚠️ **The watchdog is read-only + advisory.** It never mutates a calendar and never messages
> anyone but its own topic — it *surfaces* ("PoA appointment in 2 days, awaiting Gary"), and a
> human acts. Contrast `followup_loop`, which can spin a **full Sophia turn** in the originating
> thread and therefore *act*. If a calendar commitment should drive an **action** rather than
> just a digest, that is a separate upgrade (see the escalation note at the end).

## The rule (two clauses)

**1. Create the event on BOTH calendars.**

| Calendar | Account | Why it matters |
|---|---|---|
| **DAO / DApp** | `admin@truesight.me` (autopilot label `admin`) | **Load-bearing for the runner.** This is the *only* calendar `calendar_watchdog` reads. An event that lives only on the governor's personal calendar is **invisible to the watchdog** — the commitment silently rots. |
| **The governor's own** | Gary: `garyjob@agroverse.shop` (label `gary`) | For the **governor's** own view — what *he* sees and is reminded by. **Not** read by the runner. |

**2. Invite the people named in the source, BY EMAIL.**

- If the source names a person with a resolvable email, add them as an **attendee** and send
  the invitation — do **not** merely describe them in the event body.
- This is **human notification, orthogonal to the runner**: the watchdog never invites anyone;
  it only *flags* un-responded attendees on its digest. So the **invite** is what pings the
  human; the **digest** is what tells the governor that the human hasn't replied yet.
- Information flow, not an approval gate: use the default `send_updates` (`all`). Pass
  `send_updates='none'` only on an explicit governor instruction (e.g. *"just block my
  calendar, don't mail anyone"*).

## Resolving a named person → email (the joining step)

The single source of truth for people→email is the Main Ledger
**`Contributors contact information`** tab
(`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`), **column D = Email** — the same registry the
channel adapters bind identities against (`AUTOPILOT_CHANNEL_INTEGRATIONS.md` §3b). Then fall
back, in order, to:

1. A known per-person convention/template (e.g. the store/partner email template).
2. A **thread-stated** address (*"loop in X at x@…"*).

Never invent an address. If a named person has **no** resolvable email, put them in the event
**body** as the responsible/coordination party — do **not** fabricate an invite.

## What "send" means by surface

| Surface | Event creator | Invite addressing | "Send" semantics |
|---|---|---|---|
| **Autopilot** (Sophia / Bionpact) | `calendar_create_event` / `calendar_update_event` (`app/tools/google_calendar.py`) | `attendees[]` = **real email addresses** (resolved above) | `send_updates` defaults to `all` → a real invite email goes out |
| **Operator / local LLM** (Claude Code on the Mac, `osascript`) | AppleScript `make new event` | `attendee` objects; Apple Calendar **cannot resolve a Telegram/Discord handle → email** — you must supply the email | For Google-backed accounts the invite mails on the organizer's next sync |

## The Discord `@handle` case — and how it is solved

A person given only as a Telegram handle or a Discord username (e.g. `@Fricardo`) is **not** an
email, and neither surface can invite a bare social handle. **Resolution is the joining step,
and it already exists:**

- The Main Ledger **`Contributors contact information`** tab maps a *social id → email* in a
  single row: **col D Email · col G Discord ID (bare 19-digit snowflake) · col H Telegram
  Handle · col X Telegram ID (numeric)** — exactly how the channel adapters turn `@handle` into
  a verified person (`AUTOPILOT_CHANNEL_INTEGRATIONS.md` §3b).
- **So: look the handle up in that tab → read col D → invite that email.** If the handle is not
  bound there, ask the governor for the address (or seed the column) — do not guess.
- Inviting a recipient's Google Calendar needs only that the email is a Google (or
  Google-connected) address; a non-Google address still receives an emailed `.ics` invitation
  — the desired outcome either way.
- **The channel is irrelevant to the mechanism.** On Discord — unlike Telegram, where a forum
  *topic* is the thread — the unit is a **channel** (see `GLOSSARY.md`), and the invite is still
  addressed by **email**, never by the Discord/Telegram handle. Governance (who may instruct)
  lives in the adapter's role gate; this convention is unchanged by it.

## Governed-by / escalation

- Creating an event on the governor's own calendar for the governor's own commitment is **not**
  an approval gate — create it (both calendars) and report the link(s).
- Inviting **third parties** is an outward information flow (same class as sending mail): do it
  when the source names them; if the governor says to hold the invite, use `send_updates='none'`
  and say so in the reply.
- **Per-recipient caveat, state it once:** if a governor's Google account is not shared with
  (or not writable by) the autopilot's `admin@truesight.me` identity, a `send_updates` invite
  **between the two calendars** may not deliver. Say so rather than silently assuming the
  invite went out.
- **Action upgrade (open design question).** Today the calendar watchdog is **notify-only**. If
  a calendar commitment should *trigger action* (chase the person, prep the document), the path
  is to let the watchdog escalate into a thread turn (like `followup_loop`) or emit a fenced
  `followup` block — see `plans/SOPHIA_FOLLOWUP_MONITOR_PLAN.md` and `OPEN_FOLLOWUPS.md`. **Not
  built for calendars yet.**

## Worked example (2026-10-10)

Gary forwarded a WhatsApp screenshot — a São Paulo **power-of-attorney** appointment,
**13 Oct 2026, 10:00 BRT**, at Rua das Palmeiras 353 — confirmed by **Francine Borba
(Flow Vista)**, with sworn translator **Maria Rita** meeting him there. Applied:

- created on **both** calendars (his + `admin@`); timezone pinned to `America/Sao_Paulo` — the
  **appointment's** location decides the tz, not the reader's;
- invited `garyjob@gmail.com` + `garyjob@agroverse.shop`;
- **Francine / Maria Rita were named but had no email on file** → captured in the event **body**
  as the people to coordinate with, rather than fabricating invites;
- **year inferred** (*"October 13"* → 2026) from the current date + corroborating Brazil travel
  already on the calendar — and the inference was *stated in the reply* so it can be corrected.
- The same restart that armed the watchdog confirmed it end-to-end: journal shows
  `Calendar watchdog: posted digest (msg_id=41944)` + a Discord digest + `mirrored 5 native
  Discord event(s)` — so this very event will appear in the daily digest until it passes.

---

*Created 2026-10-10 (thread with Gary; framing corrected same day after Gary's challenge —
"a calendar entry alone does not wake the autopilot"). See also: `OPERATING_INSTRUCTIONS.md` §2
read-order, `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §3b, `GLOSSARY.md` ("Both calendars"),
`plans/SOPHIA_FOLLOWUP_MONITOR_PLAN.md`.*
