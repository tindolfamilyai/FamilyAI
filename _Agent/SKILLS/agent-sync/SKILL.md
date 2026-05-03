# Skill: Agent Instruction Sync

Aliases: agent sync, instructions, AGENTS, CLAUDE, GEMINI, launcher

## Purpose

Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` aligned so Codex CLI, Claude Code, and Gemini CLI work from the same project rules.

## Required Checklist

When updating any launcher file:

1. Update all three launchers in the same change: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
2. Keep shared behavior in `_Agent/OPERATING_MANUAL.md`.
3. Keep launcher files thin and tool-specific only where necessary.
4. Verify all three launchers reference:
   - `_Agent/OPERATING_MANUAL.md`
   - `_Agent/PROJECT_MAP.md`
   - `_Agent/WORKFLOWS.md`
   - `_Agent/SAFETY_PRIVACY.md`
   - `_Agent/SKILLS/`
5. Verify all three launchers include the same synchronization rule.
6. If a launcher changes because of a new shared rule, update `_Agent/OPERATING_MANUAL.md` too.

## Dry Run

Compare the three launchers and report differences without editing.

## Safety

Do not let the launcher files become competing instruction systems. One shared operating manual should remain canonical.
