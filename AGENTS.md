# AGENTS.md

This is the Codex CLI launcher for the Tindol Family Hub.

## Read First

Before answering or editing, read:

1. `_Agent/OPERATING_MANUAL.md`
2. `_Agent/PROJECT_MAP.md`
3. `_Agent/WORKFLOWS.md`
4. `_Agent/SAFETY_PRIVACY.md`
5. Any requested skill in `_Agent/SKILLS/<name>/SKILL.md`
6. The relevant domain `README.md`
7. The specific `.md` or `.csv` files being updated

## Skill Location

Skills live at `_Agent/SKILLS/<name>/SKILL.md` — one folder per skill. Invoke by natural language or `run skill <name>`.

## Repo-Native And Global Scaffolding

Canonical skills stay in `_Agent/SKILLS/<name>/SKILL.md`.

Generated wrappers let Codex and Claude load those skills from the repo or from any directory. Gemini loads the same project wrappers through its `.agents/skills/` alias:

- `.agents/skills/<name>/SKILL.md` — repo-native Codex wrappers generated from `_Agent/SKILL_REGISTRY.json`; Gemini also discovers these as project skills.
- `~/.codex/skills/<name>/SKILL.md` — global Codex wrappers generated from the same registry.
- `~/.codex/AGENTS.md` — global launcher loaded by Codex for every session, regardless of working directory. Contains the project root path and skill dispatch table.
- Gemini uses `.agents/skills/<name>/SKILL.md` for repo skills and `~/.gemini/GEMINI.md` for global context. Do not generate Tindol wrappers under `.gemini/skills/` or `~/.gemini/skills/`; Gemini would load duplicate skills.

Use the `family` shell helper (defined in `~/.zshrc`) to run the repo launcher from any directory without navigating:

```bash
family status
family use codex
family use claude
family use gemini
family codex "run daily brief"
family claude "run daily brief"
family gemini "run daily brief"
```

See `_Agent/INTEROPERABILITY.md` for the full CLI command reference.

## Shared Instruction Sync

`AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are equivalent launcher files. If you update any one of them, update the other two in the same change.

Keep shared behavior in `_Agent/OPERATING_MANUAL.md`. Only use tool-specific wording here when Codex CLI specifically needs it.

After editing a launcher, verify that all three launchers still reference the same shared manual, project map, workflows, skills folder, and safety rules.
