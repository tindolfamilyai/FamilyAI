# Skill: Daily Brief

Aliases: daily brief, morning brief, today, what's today, start my day, daily plan

## Purpose

Build a same-day family operating brief from local files plus live Google Calendar and Gmail context.

Default behavior for this skill is to save the brief and send it to the configured family Slack channel.
Use chat-only mode only when the user explicitly says `chat-only`, `do not save`, or `do not send to Slack`.
When invoked through the `family` launcher, use `_Agent/RUNNERS/daily_brief.sh` so Codex or Gemini runs with network access enabled and without interactive approval prompts.

## Inputs To Read

For the target date:

1. `00_Calendar/YYYY-MM.csv` for scheduled items (local calendar).
2. `01_Daily_Weekly/daily_checklist.md` for core daily tasks.
3. `01_Daily_Weekly/household_chores.md` for the weekday chore.
4. `01_Daily_Weekly/routines.md` for morning, dog, and bedtime routines.
5. `01_Daily_Weekly/todo.md` for Today items and Scheduled items whose calendar block is today.
6. `02_Health_Fitness/Workouts/Blake/blake_workouts_performed.csv` for Blake's last completed and next suggested session.
7. `02_Health_Fitness/Workouts/workout_templates.md` for session order and exercise mapping.
8. `02_Health_Fitness/Workouts/workout_plan.md` as fallback only when performed-log context is missing.
9. `02_Health_Fitness/Meal_Plans/current_week.md` and `meal_plan.csv` for meals matching the date or weekday.
10. `02_Health_Fitness/Meal_Plans/Recipes/<recipe_file>.md` — once the dinner is identified from `current_week.md`, read the matching recipe file from the `Recipes/` folder and include it in full in the brief under `## Tonight's Dinner`.
11. `09_Holidays_Birthdays/annual_events.csv` for holidays, birthdays, and annual events matching the date.
12. `02_Health_Fitness/nutrition_goals.md` only for short macro context if meals are blank or the user asks for nutrition focus.
12. Google Calendar live events via `_Agent/SKILLS/google-workspace/scripts/calendar_list_today.py` for the target date when available. In interactive CLI sessions, do not request escalation only for this optional source; skip it if network access is not already available and note the gap.
13. Gmail arrivals via `_Agent/SKILLS/google-workspace/scripts/gmail_recent_by_date.py` for target date and prior day when available. In interactive CLI sessions, do not request escalation only for this optional source; skip it if network access is not already available and note the gap.
14. `03_Kids/Bella/learning_schedule_2026-05_to_2027-04.csv` for Bella's daily learning plan.
15. `03_Kids/Bella/learning_curriculum.md` for fallback activity guidance and minimum-day structure.
16. `03_Kids/Bella/learning_log.csv` for latest completion context when available.

## Date Rules

- Default date is the system current date.
- If the user gives a date, use that date.
- Use the date's weekday to choose the household chore.
- For Blake workout, use performed-log progression:
  - find most recent completed session in `blake_workouts_performed.csv`,
  - advance to the next session in `workout_templates.md` cycle,
  - if the next session is behind today's date, label it as catch-up.
- If performed-log data is missing, fall back to weekday mapping in `workout_plan.md`.
- Use `MM-DD` to match annual events.
- If a dated source has no matching row or blank content, say `Not planned yet` or `None found`; do not invent content.
- For the dinner recipe: look up the day of week in `current_week.md`, find the dinner name in that row, then look for a matching file in `02_Health_Fitness/Meal_Plans/Recipes/`. Convert the dinner name to snake_case to find the file (e.g. "Chicken Rice Bowls" → `chicken_rice_bowls.md`). If no matching recipe file exists, show `## Tonight's Dinner` with just the meal name and a note that no recipe file is saved yet.

## Output Destination

- Default output: save to file and send to Slack channel `C0AUWRU29V5`.
- Chat-only mode: print in chat and skip file save and Slack only when the user explicitly requests chat-only/no-save/no-Slack.
- Saved path: `_Reports/Daily_Briefs/YYYY-MM-DD_daily_brief.md`.
- Default Slack destination: `--channel C0AUWRU29V5` (General).
- If the user provides another Slack destination (`--channel` or `--user` style target), use that.
- Do not modify source files when generating a brief, unless the user separately asks for updates.
- If Google or Slack tools fail, still produce the local brief and list the failure in `Notes / Gaps`.

## Output Format

Use this structure:

```md
# Daily Brief — <Weekday>, <YYYY-MM-DD>

## Today At A Glance
- Holiday / Birthday:
  - <event or None found>
- Main Focus:
  - <1-3 focus items derived from calendar, chore, workout, or key to-dos>

## Calendar
### Local Calendar
- <time> — <entry>

### Google Calendar
- <time> — <entry or None found>

## Workout
- Blake: <next suggested session from performed log, or catch-up note, or fallback from `workout_plan.md`, or Not planned yet>
- Melina: <today's workout or No specific workout set in `workout_plan.md`>

## Meals
- Breakfast: <meal or Not planned yet>
- Lunch: <meal or Not planned yet>
- Dinner: <meal name or Not planned yet>
- Protein focus:
  - Blake target: <target if available>
  - Melina target: <target if available>

## Tonight's Dinner — <Dinner Name>
**Prep:** <X min> · **Cook:** <X min>

### What You Need
- <grocery item> — <quantity>

### Steps
1. <step>

### Portions
| Person | <key fields> | Est. Protein | Est. Cal |
|--------|-------------|--------------|----------|
| Blake | ... | ~Xg | ~X |
| Melina | ... | ~Xg | ~X |
| Bella | ... | ~Xg | ~X |
| Mila | ... | ~Xg | ~X |

### Kid Notes
- Bella: <note>
- Mila: <note>

### Leftovers
<leftover note>

## Email Arrivals
### Today — <YYYY-MM-DD>
- **From:** <sender>
  **Date:** <timestamp>
  **Subject:** <subject>
  **Snippet:** <snippet>

### Yesterday — <YYYY-MM-DD>
- **From:** <sender>
  **Date:** <timestamp>
  **Subject:** <subject>
  **Snippet:** <snippet>

## Daily Checklist
### Core Four
- [ ] Dishes
- [ ] Trash
- [ ] Laundry
- [ ] Toys

### Morning
- [ ] Coffee + breakfast
- [ ] Bella & Mila breakfast + dressed
- [ ] Hulk & Zeus fed + morning walk
- [ ] Make beds
- [ ] Quick kitchen wipe-down

### Midday
- [ ] Lunch
- [ ] Mila nap
- [ ] Mid-day toy reset

### Evening
- [ ] Dinner + family meal
- [ ] Hulk & Zeus evening walk + feed
- [ ] Bath time
- [ ] Bedtime routine
- [ ] Final dishes + kitchen reset

## Today's Chore
<Weekday> — <chore title>
- [ ] <chore item>

## Routines
- Morning: <summary>
- Dogs: <summary>
- Bedtime: <summary>

## Relevant To-Dos
- [ ] <today's todo or scheduled todo>

## Bella Learning
- Today's focus:
  - Letter: <letter focus or Not planned yet>
  - Number: <number focus or Not planned yet>
- Suggested 20-40 min plan:
  - Writing: <writing focus>
  - Read-aloud: <read prompt>
  - Fine motor: <fine motor task>
- Minimum version:
  - <minimum version or Not planned yet>
- Recent log note:
  - <latest note or None logged>

## Notes / Gaps
- <missing meal, holiday, workout, or source data notes>
- <Google or Slack tool failures, if any>
```

## Today's Example

For `2026-04-29`, Wednesday, the brief should include:

- Calendar: `10 AM — B: Task block - Call CHAMPVA about ER bill`
- Workout: `Blake: Cardio + Stretch — Zone 2 / intervals + stretching`
- Chore: `Wednesday — Mop`
- Holiday / Birthday: `None found`
- Meals: `Not planned yet` if the current meal plan is blank

## Slack Delivery Rules

- Slack is automatic for daily-brief runs unless the user explicitly asks for chat-only/no-Slack.
- Default Slack destination is `C0AUWRU29V5`.
- Use `_Agent/SKILLS/slack/scripts/slack_send_message.py --text-file ... --send` for long briefs.
- If brief length is too large for Slack posting, send a short summary and include saved brief path when available.

## Safety

This skill is authorized to save the generated daily brief and post it to the configured family Slack channel by default. Do not execute payments, bookings, appointments, medical decisions, or unrelated external actions.
