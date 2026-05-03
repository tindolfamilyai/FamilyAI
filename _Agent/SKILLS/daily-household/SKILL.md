# Skill: Daily Household Ops

Aliases: daily, weekly, chores, routines, checklist, household, todo, tasks, schedule tasks, task planning, todo scheduling

## Purpose

Maintain the family routines, checklists, household chore rhythm, and general one-off to-do list in `01_Daily_Weekly/`.

For large task dumps, spoken task intake, or requests to schedule/spread tasks across the calendar, use `task_intake_ops.md`.

## Run Steps

1. Read `01_Daily_Weekly/README.md`.
2. Route everyday must-do items to `daily_checklist.md`.
3. Route larger recurring cleaning tasks to `household_chores.md`.
4. Route morning, bedtime, weekend, and kid rhythm updates to `routines.md`.
5. Route one-off and long-running general tasks to `todo.md`.
6. Put monthly, seasonal, repair, and maintenance items in `05_Home/` instead.
7. If the user asks to schedule, find time, spread tasks out, or put tasks on the calendar, update `todo.md` first and then schedule calendar work blocks.

## To-Do Routing

- Use `todo.md` for tasks like calls, errands, admin work, shopping reminders, and loose household follow-ups.
- Never put one-off task dumps in `daily_checklist.md`.
- Use `Today` for same-day tasks that are not scheduled events.
- Use `This Week` for near-term tasks.
- Use `Scheduled` for tasks that also have calendar work blocks.
- Use `Waiting On` for blocked tasks.
- Use `Later` for someday tasks.
- Use the calendar for dated appointments, reminders, or scheduled work blocks.

## Scheduling Workflow

When the user asks to schedule tasks:

1. Parse the tasks from the user message.
2. Add all tasks to `01_Daily_Weekly/todo.md` first.
3. Read `00_Calendar/README.md`.
4. Read the relevant monthly calendar CSVs, starting from the current date or the user's requested date range.
5. Find open daytime slots without overwriting existing entries.
6. Spread tasks across separate days when possible.
7. Add short calendar blocks such as `B: Task block - Call CHAMPVA`.
8. Keep fuller task details in `todo.md`; keep calendar cells short.
9. Keep the task in `todo.md` until the user marks it done.

## Scheduling Defaults

- Start from today's date unless the user gives another date.
- Use one task per day when possible.
- Prefer `10 AM`, then `2 PM`, then `4 PM`.
- Use weekdays between 9 AM and 5 PM first.
- Use weekends only if needed or requested.
- Default work-block duration is 1 hour unless the user specifies otherwise.
- Blake-only task prefix: `B:`
- Melina-only task prefix: `M:`
- Bella task prefix: `Be:`
- Mila task prefix: `Mi:`
- Family/admin task: no prefix unless one person is clearly responsible.

## Dry Run

List the target todo section, calendar file, date, time, and exact entry that would be made.
