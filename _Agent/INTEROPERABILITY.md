# Interoperability Guide — Claude Code + Codex CLI + Gemini CLI

How to use Claude Code, Codex CLI, and Gemini CLI with the Tindol Family Hub: commands, skill invocation, key differences, and when to prefer each tool.

---

## Launching Any Tool

From any directory in the terminal, use the `family` wrapper (add to shell with `source ~/.zshrc`):

```bash
family                         # opens the active tool in the project root
family "run daily brief"       # runs the no-approval daily brief runner
family status                  # shows active tool and installed/missing state
family codex "run daily brief"
family claude "run daily brief"
family gemini "run daily brief"
```

Check or switch which tool is active:

```bash
ai-tool       # shortcut for: family status
use-claude    # shortcut for: family use claude
use-codex     # shortcut for: family use codex
use-gemini    # shortcut for: family use gemini
```

The active tool is stored in `~/.family-ai-tool` and persists across sessions and shell restarts.

Daily brief prompts passed through `family` are intercepted and routed to `_Agent/RUNNERS/daily_brief.sh` so they run without interactive approval prompts. Use `chat-only`, `do not save`, or `do not send` in the prompt to skip file save and Slack.

---

## Claude Code

### How to start

```bash
family                  # opens from project root
claude                  # opens from current directory; must already be in project root
```

### How skills are invoked

Claude Code discovers generated wrappers from `.claude/skills/<name>/SKILL.md` in this repo and `~/.claude/skills/<name>/SKILL.md` globally.

Use either slash commands or natural language:

```text
/daily-brief
run daily brief
run skill calendar
use skill inbox
```

### Useful commands

| Command | What it does |
|---|---|
| `/help` | List built-in slash commands |
| `/plan` | Review a step-by-step plan before edits |
| `/memory` | View and manage persistent memory |
| `/<skill>` | Invoke a Tindol skill by folder name |

---

## Codex CLI

### How to start

```bash
family                  # opens from project root
codex                   # opens from current directory; must already be in project root
```

### How skills are invoked

Codex discovers generated wrappers from `.agents/skills/<name>/SKILL.md` in this repo and `~/.codex/skills/<name>/SKILL.md` globally.

Codex has no slash command system; use natural language:

```text
run daily brief
run skill daily-brief
log Blake's workout
plan meals this week
```

Codex project root detection is configured in `~/.codex/config.toml`:

```toml
project_root_markers = [".git", "AGENTS.md"]
```

---

## Gemini CLI

### How to start

```bash
family                  # opens from project root
gemini                  # opens from current directory; must already be in project root
```

### How skills are invoked

Gemini discovers project wrappers from the `.agents/skills/` alias in this repo. Do not also place Tindol wrappers under `.gemini/skills/` or `~/.gemini/skills/`; Gemini will load duplicates and rename skill commands.

Use natural language for all skills:

```text
run daily brief
run skill daily-brief
sort my inbox
capture these tasks
```

Gemini has a built-in `/tasks` command, so the Tindol `tasks` skill should be invoked with natural language such as `capture these tasks` or `run skill tasks`.

Use natural language for daily brief prompts:

```text
run daily brief chat-only
```

Useful Gemini commands:

| Command | What it does |
|---|---|
| `/skills list` | List discovered skills |
| `/skills reload` | Reload skills from disk |
| `/commands list` | List custom commands |
| `/commands reload` | Reload custom commands |
| `/memory show` | Show loaded `GEMINI.md` context |
| `/trust` | Trust the current workspace for project skills |

`family gemini ...` launches with `--skip-trust` from the project root. The direct daily brief runner uses `--approval-mode=yolo` only for that narrow no-approval automation path.

---

## Side-by-Side Comparison

| Feature | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|
| Project launcher | `CLAUDE.md` | `AGENTS.md` | `GEMINI.md` |
| Project skills | `.claude/skills/` | `.agents/skills/` | `.agents/skills/` alias |
| Global launcher | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `~/.gemini/GEMINI.md` |
| Global skills | `~/.claude/skills/` | `~/.codex/skills/` | None for Tindol skills; use `family` to open the project root |
| Skill invocation | `/skill-name` or natural language | Natural language | Natural language; skill slash commands may appear when discovered |
| No-approval daily brief | `family "run daily brief"` via Codex engine | `family "run daily brief"` via Codex engine | `family gemini "run daily brief"` via Gemini engine |
| Switch to this tool | `use-claude && family` | `use-codex && family` | `use-gemini && family` |

---

## Running Skills — Quick Reference

All 16 skills work in all three tools with the same natural language. Use any phrase from the Aliases section of the skill, or explicitly say `run skill <folder-name>`.

| Skill folder | Claude slash command | Gemini command | Natural language triggers |
|---|---|---|---|
| `daily-brief` | `/daily-brief` | Natural language | daily brief, morning brief, start my day |
| `daily-household` | `/daily-household` | - | chores, routines, household, todo, checklist |
| `calendar` | `/calendar` | - | calendar, schedule, appointment, add event |
| `tasks` | `/tasks` | - | task intake, task dump, capture tasks, spread tasks |
| `fitness` | `/fitness` | - | fitness, workout, log workout, exercise |
| `meals` | `/meals` | - | meals, meal plan, grocery, recipe, dinner |
| `finance` | `/finance` | - | finance, budget, expense, subscription, savings |
| `home` | `/home` | - | home, maintenance, repair, inventory, warranty |
| `kids` | `/kids` | - | kids, Bella, Mila, growth, medical, learning |
| `pets` | `/pets` | - | pets, Hulk, Zeus, vet, walk, feeding |
| `travel` | `/travel` | - | travel, trip, packing, itinerary, vacation |
| `social` | `/social` | - | social, content, Melina, brand, analytics |
| `inbox` | `/inbox` | - | inbox, sort, triage, organize |
| `google-workspace` | `/google-workspace` | - | google, gmail, calendar live, drive search |
| `slack` | `/slack` | - | slack, slack messages, slack search |
| `agent-sync` | `/agent-sync` | - | agent sync, launcher sync, AGENTS, CLAUDE, GEMINI |

---

## Updating Skills

**Source of truth:** `_Agent/SKILLS/<name>/SKILL.md`

Edit skill content only there. Generated wrappers in `.agents/skills/`, `.claude/skills/`, `~/.codex/skills/`, and `~/.claude/skills/` are thin pointers. Gemini uses `.agents/skills/` directly, so it should not have duplicate Tindol wrappers in `.gemini/skills/` or `~/.gemini/skills/`.

After changing a canonical skill, run:

```bash
python3 _Agent/RUNNERS/sync_skill_wrappers.py --project --global
python3 _Agent/RUNNERS/sync_skill_wrappers.py --check --project --global
python3 _Agent/RUNNERS/check_interop.py
```

If the project root path ever changes, update `_Agent/SKILL_REGISTRY.json`, `_Agent/RUNNERS/family.sh`, global launchers, and regenerate wrappers.
