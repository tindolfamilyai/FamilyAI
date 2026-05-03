# Project Map

Use this map to route requests to the right files.

## Root

- `README.md`: human-facing overview of the family hub.
- `AGENTS.md`: Codex CLI launcher.
- `CLAUDE.md`: Claude Code launcher.
- `GEMINI.md`: Gemini CLI launcher.
- `_Agent/`: shared agent instructions, workflows, data contracts, safety rules, and skills.

## Family Domains

- `00_Calendar/`: master family schedule. One monthly CSV per month.
- `01_Daily_Weekly/`: routines, checklists, household chores, general to-dos, and weekly rhythm.
- `02_Health_Fitness/`: workouts, meal plans, grocery list, and recipes.
- `03_Kids/`: one folder per child with profile, medical log, and growth log.
- `04_Pets/`: dog profiles, vet logs, feeding schedule, and walks log.
- `05_Home/`: home inventory, repairs, maintenance, and seasonal reminders.
- `06_Finances/`: budget, expenses, subscriptions, and savings goals.
- `07_Travel/`: trip templates, trip folders, packing lists, and travel budgets.
- `08_Social_Media_Orlando_Theme_Park_Family/`: content calendar, post ideas, analytics, and brand partnerships.
- `09_Holidays_Birthdays/`: annual events, gifts, birthdays, holidays, and celebrations.
- `_Inbox/`: unsorted notes, receipts, files, and ideas waiting to be routed.

## Support Areas

- `_Templates/`: reusable starting points for plans, logs, profiles, and reports.
- `_Archive/`: old months, completed trips, inactive plans, and obsolete records.
- `_Attachments/`: receipts, photos, PDFs, screenshots, and other source files.
- `_Reports/`: generated weekly, monthly, budget, calendar, and household summaries.

## Routing Defaults

- Calendar event: `00_Calendar/YYYY-MM.csv`
- Daily or weekly routine: `01_Daily_Weekly/`
- General one-off to-do: `01_Daily_Weekly/todo.md`
- Meal or grocery request: `02_Health_Fitness/Meal_Plans/`
- Workout: `02_Health_Fitness/Workouts/`
- Child health or growth: `03_Kids/<Child>/`
- Pet health or walks: `04_Pets/`
- Home repair or maintenance: `05_Home/`
- Expense, budget, subscription, or goal: `06_Finances/`
- Trip planning: `07_Travel/Trips/`
- Melina content or brand work: `08_Social_Media_Orlando_Theme_Park_Family/`
- Birthday, holiday, gift, or annual event: `09_Holidays_Birthdays/`
- Unknown item: `_Inbox/`
