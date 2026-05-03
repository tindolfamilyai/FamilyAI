# Workflows

Use these workflows for common requests. If the user asks to `run skill x`, prefer the matching file in `_Agent/SKILLS/`.

## Add A Calendar Event

- Read `00_Calendar/README.md`.
- Identify the month file: `00_Calendar/YYYY-MM.csv`.
- Use the correct date row and hour column.
- Prefix person-specific events with `B:`, `M:`, `Be:`, or `Mi:`.
- For all-day events, use the `6 AM` cell and add `(all day)`.
- If the event also belongs in another log, update that log too.

## Add A General To-Do

- Prefer `_Agent/SKILLS/tasks/SKILL.md` for spoken task dumps, large lists of tasks, or requests that combine to-dos with scheduling.
- Use `01_Daily_Weekly/todo.md` for one-off tasks with no specific date/time and no better domain owner.
- Put urgent same-day items under `Today`.
- Put near-term items under `This Week`.
- Put tasks with calendar work blocks under `Scheduled`.
- Put blocked tasks under `Waiting On`.
- Put someday tasks under `Later`.
- If the task has a date or time, keep it in `todo.md` when it is still an action item and add the date/time to `00_Calendar/YYYY-MM.csv`.
- If the task repeats daily, use `01_Daily_Weekly/daily_checklist.md`.
- If the task repeats weekly, use `01_Daily_Weekly/household_chores.md`.
- If the task belongs to home, finance, meals, travel, kids, pets, or social media, route it to that domain.
- Never put one-off task dumps in `daily_checklist.md`.

## Schedule To-Dos

- Prefer `_Agent/SKILLS/tasks/SKILL.md` for scheduling task dumps or spreading multiple to-dos across the calendar.
- If the user says "add to todo," update only `01_Daily_Weekly/todo.md`.
- If the user says "schedule these," "find time," "spread these out," or "put these on the calendar," update `todo.md` first and then add calendar work blocks.
- Read `00_Calendar/README.md` before editing calendar CSVs.
- If the user gives a specific date or time, use that date or time.
- If no date is given, schedule from the current date forward.
- Use one task per day when possible.
- Prefer `10 AM`, then `2 PM`, then `4 PM`.
- Prefer weekdays from 9 AM to 5 PM; use weekends only if needed or requested.
- Use 1-hour work blocks unless the user specifies another duration.
- Do not overwrite existing calendar entries.
- Keep detailed notes in `todo.md` and short labels in calendar cells.
- Use calendar entry format `Task block - <short task>` with `B:`, `M:`, `Be:`, or `Mi:` prefix when responsibility is obvious.
- If a task belongs to another domain, keep the task in `todo.md` and optionally cross-reference the domain file.
- Keep the task in `todo.md` until the user says it is complete.

## Generate Daily Brief

- Use `_Agent/SKILLS/daily-brief/SKILL.md`.
- Default date is the system current date unless the user gives another date.
- Read local calendar, daily checklist, household chore, routines, relevant to-dos, workout, meals, and holidays.
- For Blake workout, prefer progression from `02_Health_Fitness/Workouts/Blake/blake_workouts_performed.csv` and `02_Health_Fitness/Workouts/workout_templates.md`, not date-tied placeholder rows.
- Read Bella learning plan from `03_Kids/Bella/learning_schedule_2026-05_to_2027-04.csv` and include today's learning block when available.
- Use `03_Kids/Bella/learning_log.csv` for recent learning completion context when available.
- Include Google Calendar events when available.
- Include Gmail arrivals for the target date and the previous date when available.
- Save to `_Reports/Daily_Briefs/YYYY-MM-DD_daily_brief.md` by default.
- Send to the configured Slack channel by default.
- Print the brief in chat only when the user asks for chat-only, no-save, or no-Slack behavior.
- When invoked through the `family` launcher, route daily brief prompts to `_Agent/RUNNERS/daily_brief.sh` to avoid interactive Codex permission prompts.
- If a source has no matching data, say `Not planned yet` or `None found`; do not invent content.
- If Google or Slack tools fail, still generate the local brief and list the failure in `Notes / Gaps`.
- Do not modify source files when generating the brief unless the user separately asks for updates.

## Log A Workout

- For Blake, map to a template in `02_Health_Fitness/Workouts/workout_templates.md` and append performed rows to `02_Health_Fitness/Workouts/Blake/blake_workouts_performed.csv`.
- Keep `_Archive/02_Health_Fitness/Workouts/Blake/blake_workouts_2026-05-04_to_2026-07-26.csv` as historical plan context unless explicitly asked to change it.
- Use `02_Health_Fitness/Workouts/Melina/melina_workouts.csv` for Melina.
- If the user gives a summary that belongs in `workout_plan.md`, update the Markdown dashboard as well.

## Plan Meals

- Update `02_Health_Fitness/Meal_Plans/current_week.md`.
- Update `02_Health_Fitness/Meal_Plans/meal_plan.csv`.
- Update `02_Health_Fitness/Meal_Plans/grocery_list.csv` when ingredients are known.
- Add reusable recipes to `recipes.md`.

## Log Child Health Or Growth

- Use `03_Kids/Bella/` or `03_Kids/Mila/`.
- Medical visits, vaccines, illness, and follow-up items go in `medical_log.csv`.
- Height, weight, clothing size, shoe size, and milestones go in `growth_log.csv`.
- Durable context can be added to `profile.md`.
- Add dated appointments to the calendar when a date and time are known.

## Log Pet Care

- Dog-specific vet care goes in `04_Pets/Hulk/vet_log.csv` or `04_Pets/Zeus/vet_log.csv`.
- Walks go in `04_Pets/walks_log.csv`.
- Feeding changes go in `04_Pets/feeding_schedule.md`.
- Add dated appointments to the calendar when a date and time are known.

## Log Home Work

- Maintenance tasks go in `05_Home/maintenance_log.csv`.
- Repairs go in `05_Home/repairs_log.csv`.
- Items, appliances, warranties, and serial numbers go in `05_Home/inventory.csv`.
- Seasonal and recurring reminders go in `05_Home/seasonal_reminders.md`.

## Log Finance Items

- Expenses go in `06_Finances/expenses.csv`.
- Recurring services go in `06_Finances/subscriptions.csv`.
- Budget summaries go in `06_Finances/monthly_budget.csv`.
- Goals go in `06_Finances/savings_goals.md`.
- Never execute payments, transfers, trades, or purchases.

## Plan Travel

- Create trip folders under `07_Travel/Trips/` using `YYYY-MM_Destination`.
- Start from `07_Travel/trip_template.md`, `packing_list_template.md`, and `travel_budget_template.csv`.
- Add travel dates to the calendar when known.

## Sort Inbox

- Read `_Inbox/README.md`.
- Classify each item by domain.
- Move or reference source files in the appropriate section.
- Route general one-off tasks to `01_Daily_Weekly/todo.md`.
- Put raw receipts, photos, PDFs, and screenshots in `_Attachments/` if they should be preserved.
- Summarize what was routed and what still needs user clarification.

## Generate Reports

- Put generated summaries in `_Reports/`.
- Use filenames like `YYYY-MM-DD_weekly_summary.md` or `YYYY-MM_budget_summary.md`.
- Link back to source files rather than duplicating large logs.
