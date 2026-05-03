# Skill: Google Workspace Ops

Aliases: google workspace, google calendar, gmail, google drive, live calendar, email search, drive search

## Purpose

Use local read-only Google Workspace scripts to enrich the Tindol Family Hub with live Google Calendar, Gmail, and Drive metadata.

## Safety

- Never read, print, summarize, copy, or paste OAuth credential/token contents.
- Never store credentials or tokens in the repo.
- Use read-only scripts first.
- Do not send emails, create calendar events, upload files, delete files, or change labels without a separate approved write-capable workflow.
- Sending email requires explicit user confirmation and the `gmail_send.py --send` flag.
- Creating calendar events requires explicit user confirmation and the `calendar_create_event.py --create` flag.
- Creating Drive files requires explicit user confirmation and the `drive_create_text_file.py --create` flag.
- Local Markdown/CSV stays the durable source of truth unless the user asks to sync.

## Scripts

Scripts are bundled in this skill at `_Agent/SKILLS/google-workspace/scripts/`.

Available read-only scripts:

- `calendar_list_today.py`
- `gmail_search.py`
- `gmail_recent_by_date.py`
- `gmail_recent_full.py`
- `drive_list_recent.py`
- `drive_print_tree.py`

Write-capable scripts, dry-run by default:

- `gmail_send.py`
- `calendar_create_event.py`
- `drive_create_text_file.py`

Shared auth helper:

- `google_auth.py`

## References

Setup documentation and credential instructions are bundled at `_Agent/SKILLS/google-workspace/references/README.md`.

## Credential Location

Credentials and tokens live outside the repo:

- `/Users/tindolhouse/.config/tindol-family-google/credentials.json`
- `/Users/tindolhouse/.config/tindol-family-google/token.json`

## Run Steps

1. Read `_Agent/INTEGRATIONS.md`.
2. Choose the narrowest read-only script.
3. Run the script with a bounded query or date range.
4. Use the output to summarize, draft, or propose local updates.
5. Do not mutate Google data or local source files unless the user explicitly asks.

## Common Commands

Calendar today:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/calendar_list_today.py"
```

Gmail search:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/gmail_search.py" "from:example@example.com newer_than:30d"
```

Gmail arrivals by date:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/gmail_recent_by_date.py" --date 2026-04-29
```

Drive recent files:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/drive_list_recent.py"
```

Drive folder tree:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/drive_print_tree.py" "Tindol"
```

Send email after explicit approval:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/gmail_send.py" --to user@example.com --subject "Subject" --body "Message" --send
```

Create calendar event after explicit approval:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/calendar_create_event.py" --summary "Appointment" --start "2026-05-03T09:00:00" --create
```

Create Drive text file after explicit approval:

```bash
python3 "_Agent/SKILLS/google-workspace/scripts/drive_create_text_file.py" --folder "Tindol Family Hub" --filename "note.txt" --text "Message" --create
```

## Skill Integrations

- `daily-brief/SKILL.md`: may call Google Calendar and Gmail read-only tools to include live events and email arrivals.
- `tasks/SKILL.md`: local to-do remains source of truth; Google Calendar writes need a future write-capable workflow.
- `finance/SKILL.md`: Gmail/Drive can help find bills and receipts read-only.
- `inbox/SKILL.md`: Gmail can provide email context when explicitly requested.
