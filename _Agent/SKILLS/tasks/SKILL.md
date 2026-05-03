# Skill: Task Intake Ops

Aliases: task intake, capture tasks, task dump, todo intake, schedule tasks, spread tasks out

## Purpose

Capture spoken or list-style task dumps, route them into `01_Daily_Weekly/todo.md`, and optionally schedule actionable work blocks on the family calendar.

## Run Steps

1. Read `01_Daily_Weekly/todo.md`.
2. Read `00_Calendar/README.md` if the user asks to schedule, find time, spread tasks out, or put tasks on the calendar.
3. Parse the user's message into clear individual tasks.
4. Add task details to `01_Daily_Weekly/todo.md`.
5. Put unscheduled task dumps under `This Week` or `Later`.
6. Put tasks with calendar work blocks under `Scheduled`.
7. Add calendar work blocks only when scheduling is requested or clearly implied.
8. Keep detailed notes in `todo.md`; keep calendar cells short.

## Routing Rules

- Never put one-off task dumps in `daily_checklist.md`.
- Keep recurring daily routines in `daily_checklist.md`.
- Keep recurring weekly cleaning in `household_chores.md`.
- Keep long-running tasks in `todo.md` until the user marks them done.
- If a task belongs to another domain, keep the action item in `todo.md` and cross-reference the domain file when useful.
- Do not mark a task done just because it has a calendar block.

## Calendar Work Blocks

When scheduling is requested:

1. Read the relevant monthly calendar CSVs.
2. Do not overwrite existing calendar entries.
3. Use one task per day when possible.
4. Prefer weekdays between 9 AM and 5 PM.
5. Prefer `10 AM`, then `2 PM`, then `4 PM`.
6. Use weekends only if needed or requested.
7. Default duration is 1 hour unless the user says otherwise.

Entry format:

- `B: Task block - Call CHAMPVA about ER bill`
- `M: Task block - Schedule glasses appointment`
- `Be: Task block - STEM VPK paperwork`
- `Task block - Plan cruise flights`

## Dry Run

List the target todo section, target calendar file, date, time, and exact entry before editing when the user asks to preview or approve.

## Safety

Do not execute payments, purchases, travel bookings, medical decisions, or account changes. Capture the task and schedule planning time only.
