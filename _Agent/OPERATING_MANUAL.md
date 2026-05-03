# Tindol Family Hub Operating Manual

This is the canonical instruction file for Codex CLI, Claude Code, Gemini CLI, and any other agent working in this folder.

## Core Model

- This project is a family operating system.
- Markdown files are the human dashboard.
- CSV files are the structured backing store.
- When a workflow calls for both Markdown and CSV updates, update both.
- Keep the current numbered domain folders intact.
- Do not invent new schemas, file locations, or recurring conventions without updating `_Agent/DATA_CONTRACTS.md` and the affected domain README.

## Required Reading Order

1. The tool launcher at the root: `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`
2. `_Agent/OPERATING_MANUAL.md`
3. `_Agent/PROJECT_MAP.md`
4. `_Agent/WORKFLOWS.md`
5. `_Agent/SAFETY_PRIVACY.md`
6. Any requested skill in `_Agent/SKILLS/`
7. The relevant domain `README.md`
8. The specific `.md` or `.csv` files being updated

## Skill Execution

When the user says `run skill x`, `use skill x`, or `skill: x`:

1. Search `_Agent/SKILLS/` for the closest matching skill file by filename, title, aliases, or domain.
2. Read the skill file before editing.
3. Follow that skill's workflow and safety checks.
4. If one skill clearly matches, run it.
5. If multiple skills match, ask one clarifying question before editing.
6. If no skill matches, explain that and suggest the nearest available skill.

Skills must stay plain Markdown so Codex, Claude, Gemini, and future agents can use the same instructions.

## Launcher Sync Rule

`AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are equivalent launcher files.

If any agent updates one launcher, it must update the other two in the same change. Shared behavior belongs here in `_Agent/OPERATING_MANUAL.md`, not separately duplicated in launcher files. Tool-specific wording is allowed only when required by that tool.

After editing a launcher, verify all three still reference:

- `_Agent/OPERATING_MANUAL.md`
- `_Agent/PROJECT_MAP.md`
- `_Agent/WORKFLOWS.md`
- `_Agent/SAFETY_PRIVACY.md`
- `_Agent/SKILLS/`

## Editing Rules

- Preserve existing family data unless the user explicitly asks to change it.
- Use ISO dates: `YYYY-MM-DD`.
- Use the calendar prefixes from `_Agent/DATA_CONTRACTS.md`.
- For CSV edits, preserve headers exactly unless intentionally changing the schema.
- For financial and medical entries, record factual user-provided details and avoid making decisions for the family.
- Prefer adding a clear row, note, or checklist item over rewriting a whole file.
- Put unsorted inputs in `_Inbox/`, raw attachments in `_Attachments/`, generated reports in `_Reports/`, reusable formats in `_Templates/`, and stale/completed material in `_Archive/`.

## Safety

Always follow `_Agent/SAFETY_PRIVACY.md`.

Agents must not execute purchases, payments, transfers, trades, medical decisions, legal decisions, account changes, or irreversible external actions. Draft and organize only unless the user explicitly approves a safe, reversible action through the tool being used.
