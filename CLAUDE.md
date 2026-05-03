# CLAUDE.md

This is the Claude Code launcher for the Tindol Family Hub.

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

Skills live at `_Agent/SKILLS/<name>/SKILL.md` — one folder per skill. Invoke with `/skill-name` slash command or natural language.

## Repo-Native And Global Scaffolding

Canonical skills stay in `_Agent/SKILLS/<name>/SKILL.md`.

Generated wrappers let Claude Code and Codex load those skills from the repo or from any directory. Gemini loads the same project wrappers through its `.agents/skills/` alias:

- `.claude/skills/<name>/SKILL.md` — repo-native Claude wrappers generated from `_Agent/SKILL_REGISTRY.json`.
- `~/.claude/skills/<name>/SKILL.md` — global Claude wrappers generated from the same registry.
- `~/.claude/CLAUDE.md` — global launcher loaded by Claude Code for every session, regardless of working directory. Contains the project root path and skill dispatch table.
- Gemini uses `.agents/skills/<name>/SKILL.md` for repo skills and `~/.gemini/GEMINI.md` for global context. Do not generate Tindol wrappers under `.gemini/skills/` or `~/.gemini/skills/`; Gemini would load duplicate skills.

Use the `family` shell helper (defined in `~/.zshrc`) to run the repo launcher from any directory without navigating:

```bash
family status
family use claude
family use codex
family use gemini
family claude "run daily brief"
family codex "run daily brief"
family gemini "run daily brief"
```

See `_Agent/INTEROPERABILITY.md` for the full CLI command reference.

## Shared Instruction Sync

`AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are equivalent launcher files. If you update any one of them, update the other two in the same change.

Keep shared behavior in `_Agent/OPERATING_MANUAL.md`. Only use tool-specific wording here when Claude Code specifically needs it.

After editing a launcher, verify that all three launchers still reference the same shared manual, project map, workflows, skills folder, and safety rules.
