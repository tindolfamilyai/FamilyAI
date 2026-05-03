# Google Workspace Tools

Read-only Python scripts for Google Calendar, Gmail, and Drive.

## Secret Storage

Credentials and tokens are outside the repo:

- `/Users/tindolhouse/.config/tindol-family-google/credentials.json`
- `/Users/tindolhouse/.config/tindol-family-google/token.json`

Do not paste credential or token contents into chat or Markdown.

## Install Dependencies

```bash
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## First Run

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/google-workspace/scripts/calendar_list_today.py"
```

The first run opens a browser OAuth flow and creates the token outside the repo.

## Scripts

- `calendar_list_today.py`: list today's primary calendar events.
- `calendar_create_event.py`: create a Google Calendar event with `calendar.events` after explicit `--create`.
- `gmail_search.py`: search Gmail messages by Gmail query syntax.
- `gmail_recent_by_date.py`: list Gmail arrivals for a specific date in Markdown summary format.
- `gmail_recent_full.py`: print recent Gmail messages with body text in Markdown.
- `gmail_send.py`: send a plain text email through Gmail after explicit `--send`.
- `drive_list_recent.py`: list recent Drive file metadata.
- `drive_print_tree.py`: print a Drive folder tree by folder name or id.
- `drive_create_text_file.py`: create a Drive folder and upload a text file with `drive.file` after explicit `--create`.
- `google_auth.py`: shared OAuth helper.

## Environment Overrides

- `TINDOL_GOOGLE_CREDENTIALS`
- `TINDOL_GOOGLE_TOKEN`
- `TINDOL_GOOGLE_SEND_TOKEN`
- `TINDOL_GOOGLE_DRIVE_FILE_TOKEN`
- `TINDOL_GOOGLE_CALENDAR_EVENT_TOKEN`
- `TINDOL_GOOGLE_TIMEZONE`

## Gmail Send

Send uses a separate token file:

`/Users/tindolhouse/.config/tindol-family-google/token_gmail_send.json`

Preview:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/google-workspace/scripts/gmail_send.py" --to blaketindol@gmail.com --subject "Test" --body "Hello" --dry-run
```

Send:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/google-workspace/scripts/gmail_send.py" --to blaketindol@gmail.com --subject "Test" --body "Hello" --send
```
