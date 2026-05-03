# Skill: Calendar Management

Aliases: calendar, schedule, appointment, event, reminder, task block, work block

## Purpose

Add, update, or review family calendar items and task work blocks in `00_Calendar/`.

## Run Steps

1. Read `_Agent/DATA_CONTRACTS.md` and `00_Calendar/README.md`.
2. Identify the target month file: `00_Calendar/YYYY-MM.csv`.
3. Find the date row and best hour column.
4. Use prefixes for person-specific events: `B:`, `M:`, `Be:`, `Mi:`.
5. For all-day events, place the entry in `6 AM` with `(all day)`.
6. If the event is also a medical, pet, travel, birthday, or school item, update the matching domain log.

## Task Work Blocks

Use task work blocks when the user asks to schedule, spread out, find time for, or put to-dos on the calendar.

- Add the task to `01_Daily_Weekly/todo.md` first unless it is already there.
- Default duration: 1 hour.
- Default placement: weekdays between 9 AM and 5 PM.
- Preferred time order: `10 AM`, then `2 PM`, then `4 PM`.
- Use weekends only if needed or requested.
- Do not overwrite existing calendar entries.
- If a preferred slot is occupied, choose another open slot.
- Keep the calendar entry short; keep detailed notes in `todo.md`.

Entry format:

- `B: Task block - Call CHAMPVA about ER bill`
- `M: Task block - Schedule glasses appointment`
- `Task block - Plan cruise flights`

## Dry Run

If the user asks for dry-run mode, describe the target file, row, column, and exact entry without editing.

## Safety

Do not book, cancel, or send calendar invites externally unless the user explicitly asks and confirms details.
