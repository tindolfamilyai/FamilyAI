# Tindol Family Hub

The Tindols: **Blake, Melina, Bella (4), Mila (2)** + dogs **Hulk & Zeus** — Orlando, FL townhome.

This folder is the family operating system. Markdown files are the human-friendly view; CSVs hold the structured data. When you ask an AI agent to log something, it updates the right `.md` *and* appends to the matching `.csv` in the right section.

---

## Sections

| # | Folder | What lives here |
|---|--------|-----------------|
| 00 | [Calendar](00_Calendar/) | Master schedule, one CSV per month (rows = dates, columns = hours 6 AM–11 PM) |
| 01 | [Daily / Weekly](01_Daily_Weekly/) | Routines, daily & weekly checklists, household chores |
| 02 | [Health & Fitness](02_Health_Fitness/) | Workouts (Blake & Melina), meal plans, grocery list, recipes |
| 03 | [Kids](03_Kids/) | One folder per child: profile, medical log, growth log |
| 04 | [Pets](04_Pets/) | Hulk & Zeus profiles, vet logs, feeding schedule, walks log |
| 05 | [Home](05_Home/) | Townhome maintenance, repairs, inventory, Orlando seasonal reminders |
| 06 | [Finances](06_Finances/) | Monthly budget, expense ledger, subscriptions, savings goals |
| 07 | [Travel](07_Travel/) | Trip templates, packing lists, per-trip folders under `Trips/` |
| 08 | [Social Media — Orlando Theme Park Family](08_Social_Media_Orlando_Theme_Park_Family/) | Content calendar, post ideas, brand deals, analytics |
| 09 | [Holidays & Birthdays](09_Holidays_Birthdays/) | Annual events, gift ideas, celebration planning |
| — | [_Inbox](_Inbox/) | Drop unsorted notes/photos/receipts here — ask an AI agent to route them |

---

## Shared AI Agent Layer

Codex CLI, Claude Code, and Gemini CLI use shared instructions in `_Agent/`.

- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are thin launcher files at the project root.
- `_Agent/OPERATING_MANUAL.md` is the canonical source of truth for all agents.
- `_Agent/SKILLS/` contains the 16 canonical portable skills, each in its own folder (`_Agent/SKILLS/<name>/SKILL.md`).
- `.agents/skills/` contains generated project-native wrappers for Codex; Gemini also discovers this folder as its project skill alias.
- `.claude/skills/` contains generated project-native wrappers for Claude Code.
- `_Agent/INTEROPERABILITY.md` is the full CLI command reference — how to invoke skills in each tool, key differences, and what to use when.
- When any agent updates one launcher, it must update all three (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) in the same change.

---

## Launching the AI from Anywhere (No Navigation Needed)

A global scaffold lets you open any configured AI tool from any directory in the terminal without `cd`-ing to this folder first.

### Shell commands (add to your terminal with `source ~/.zshrc`)

```bash
family                      # opens the active tool (Claude Code, Codex, or Gemini) from this project root
family "run daily brief"    # runs the no-approval daily brief runner

use-claude                  # switch family to Claude Code
use-codex                   # switch family to Codex CLI
use-gemini                  # switch family to Gemini CLI
ai-tool                     # print which tool is currently active
```

The active tool is stored in `~/.family-ai-tool` and persists across sessions.

### Global hidden directories

These hidden folders in your home directory (`~`) let each CLI load this project's context from any working directory:

| Path | Tool | What it does |
|------|------|--------------|
| `~/.claude/CLAUDE.md` | Claude Code | Global launcher — loaded every session, contains project root + skill dispatch table |
| `~/.claude/skills/<name>/SKILL.md` | Claude Code | 16 generated Tindol global skill wrappers — personal skills such as `sitescroll` may also exist |
| `~/.codex/AGENTS.md` | Codex CLI | Global launcher — same as above for Codex |
| `~/.codex/skills/<name>/SKILL.md` | Codex CLI | 16 generated Tindol global skill wrappers for Codex |
| `~/.gemini/GEMINI.md` | Gemini CLI | Global launcher — same as above for Gemini; project skills come from `.agents/skills/` when `family` opens this repo |

To view these folders in macOS Finder: press **Cmd + Shift + .** to toggle hidden files.

To open them in terminal:
```bash
open ~/.claude/skills
open ~/.codex/skills
```

---

## Running Skills

Skills are invoked by natural language in all three tools. The skill folder name is also a slash command in Claude Code. In Gemini, prefer natural language; Gemini may also expose skill slash commands from discovered project skills. Gemini has its own built-in `/tasks` command, so use `capture tasks` or `run skill tasks` instead of relying on a Gemini `/tasks` slash command.

### Running the Daily Brief

**From Claude Code** (with `family` from any directory):
```bash
# Launch from anywhere:
family

# Then inside the session, say any of:
run daily brief
/daily-brief
morning brief
start my day
```

Or pass it directly on launch:
```bash
family "run daily brief"
```

**From Codex CLI** (with `family` from any directory):
```bash
# Switch to Codex and launch:
use-codex
family

# Then inside the session, say any of:
run daily brief
run skill daily-brief
morning brief
start my day
```

Or pass it directly on launch:
```bash
use-codex && family "run daily brief"
```

**From Gemini CLI** (with `family` from any directory):
```bash
# Switch to Gemini and launch:
use-gemini
family

# Then inside the session, say:
run daily brief
run daily brief chat-only
```

Or pass it directly on launch:
```bash
use-gemini && family "run daily brief"
family gemini "run daily brief chat-only"
```

The daily brief reads local calendar, workouts, meals, Bella's learning plan, and Gmail/Google Calendar. By default it saves to `_Reports/Daily_Briefs/YYYY-MM-DD_daily_brief.md` and posts to the configured family Slack channel. Add `chat-only`, `do not save`, or `do not send` to skip file save and Slack. The `family "run daily brief"` path uses `_Agent/RUNNERS/daily_brief.sh` to avoid interactive approval prompts.

### All 16 skills — quick reference

| Skill | Command | Natural language |
|-------|-------------------------|-----------------|
| Daily Brief | Claude: `/daily-brief` | run daily brief, morning brief, start my day |
| Daily Household | Claude: `/daily-household` | chores, routines, household, todo |
| Calendar | Claude: `/calendar` | calendar, schedule, add event, appointment |
| Tasks | Claude: `/tasks` | task intake, task dump, capture tasks |
| Fitness | Claude: `/fitness` | fitness, workout, log workout, exercise |
| Meals | Claude: `/meals` | meals, meal plan, grocery, recipe, dinner |
| Finance | Claude: `/finance` | finance, budget, expense, subscription |
| Home | Claude: `/home` | home, maintenance, repair, inventory |
| Kids | Claude: `/kids` | kids, Bella, Mila, growth, medical |
| Pets | Claude: `/pets` | pets, Hulk, Zeus, vet, walk |
| Travel | Claude: `/travel` | travel, trip, packing, itinerary |
| Social | Claude: `/social` | social, content, Melina, brand, analytics |
| Inbox | Claude: `/inbox` | inbox, sort, triage, organize |
| Google Workspace | Claude: `/google-workspace` | google, gmail, drive, live calendar |
| Slack | Claude: `/slack` | slack, slack messages, slack search |
| Agent Sync | Claude: `/agent-sync` | agent sync, launcher sync, AGENTS, CLAUDE, GEMINI |

---

## How to work with AI agents in this folder

### Quick examples

| You say | The agent does |
|---------|----------------|
| "Log a 30-min run, 5K" | Appends row to `02_Health_Fitness/Workouts/Blake/blake_workouts_performed.csv` |
| "Plan meals for next week" | Updates `02_Health_Fitness/Meal_Plans/current_week.md` and `meal_plan.csv` + drafts grocery list |
| "Bella has a checkup Thursday at 9 AM" | Adds to `00_Calendar/2026-MM.csv` *and* `03_Kids/Bella/medical_log.csv` |
| "Hulk got his rabies shot today, $45" | Row in `04_Pets/Hulk/vet_log.csv` |
| "We're planning a beach trip July 18–22" | Creates `07_Travel/Trips/2026-07_[Destination]/` with template copies, adds to calendar |
| "Spent $87 at Publix" | Row in `06_Finances/expenses.csv` under Groceries |
| "Sort my inbox" | Reads `_Inbox/`, routes each item to the right section |

### Conventions

- **Dates:** ISO format `YYYY-MM-DD` (so they sort correctly)
- **Calendar prefixes:** `B:` Blake, `M:` Melina, `Be:` Bella, `Mi:` Mila — no prefix = whole family
- **One folder per trip** under `07_Travel/Trips/`, named `YYYY-MM_Destination/`
- **CSVs always go in their section folder** — never the top level

### Workflow note

AI agents can categorize finances and summarize spending — but **never execute trades, transfers, payments, purchases, or account changes**. Those are always your call.

---

## Getting started — one-time setup

A few placeholders to fill in when you have a moment. None of this is urgent; the hub works without it.

- [ ] Remaining DOBs/dates for Blake + anniversary in `09_Holidays_Birthdays/annual_events.csv` (Melina, Bella, Mila done)
- [ ] Hulk & Zeus basics in `04_Pets/Hulk/profile.md` and `Zeus/profile.md` (breed, weight, vet)
- [ ] Pediatrician + daycare info in each kid's `profile.md`
- [ ] HOA contact + dues frequency in `05_Home/seasonal_reminders.md`
- [ ] Current month's recurring events copied from `09_Holidays_Birthdays/annual_events.csv` into `00_Calendar/2026-04.csv`

---

## What agents know about your family

The shared files in this folder say: family composition, that you live in an Orlando townhome, and that you prefer to work in markdown with CSVs as the structured backing. Individual tools may also have their own memory systems, but this folder is the portable source of truth.
