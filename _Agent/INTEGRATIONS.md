# Integrations

This file documents optional external integrations for the Tindol Family Hub.

## Google Workspace

Google Calendar, Gmail, and Google Drive can be used by local scripts and agent skills when the user explicitly asks for live Google data.

## Paths

Project path:

`/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/`

Script path:

`/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/google-workspace/scripts/`

Credential folder outside the repo:

`/Users/tindolhouse/.config/tindol-family-google/`

Credential file:

`/Users/tindolhouse/.config/tindol-family-google/credentials.json`

Token file created after OAuth:

`/Users/tindolhouse/.config/tindol-family-google/token.json`

Gmail send token file:

`/Users/tindolhouse/.config/tindol-family-google/token_gmail_send.json`

Drive file token file:

`/Users/tindolhouse/.config/tindol-family-google/token_drive_file.json`

Calendar event token file:

`/Users/tindolhouse/.config/tindol-family-google/token_calendar_event.json`

## Safety Rules

- Do not store OAuth credentials or tokens in the project repo.
- Do not print, summarize, copy, paste, or inspect credential/token contents.
- Scripts may read credential/token files only to authenticate Google API calls.
- Start with read-only scopes.
- Write-capable scripts require a separate plan and explicit confirmation rules.
- Gmail send uses a separate token file and only requests `https://www.googleapis.com/auth/gmail.send`.
- Drive file creation uses a separate token file and only requests `https://www.googleapis.com/auth/drive.file`.
- Calendar event creation uses a separate token file and only requests `https://www.googleapis.com/auth/calendar.events`.
- Local Markdown/CSV remains the durable family source of truth unless the user asks to sync with Google.

## Read-Only Scopes

- Calendar: `https://www.googleapis.com/auth/calendar.readonly`
- Gmail: `https://www.googleapis.com/auth/gmail.readonly`
- Drive metadata: `https://www.googleapis.com/auth/drive.metadata.readonly`

## Write-Capable Google Scopes

- Gmail send: `https://www.googleapis.com/auth/gmail.send`
- Drive file create/manage: `https://www.googleapis.com/auth/drive.file`
- Calendar event create/manage: `https://www.googleapis.com/auth/calendar.events`

## Setup

Create the external credential folder:

```bash
mkdir -p "/Users/tindolhouse/.config/tindol-family-google"
chmod 700 "/Users/tindolhouse/.config/tindol-family-google"
```

Move the downloaded OAuth desktop app file:

```bash
mv "/path/to/credentials.json" "/Users/tindolhouse/.config/tindol-family-google/credentials.json"
chmod 600 "/Users/tindolhouse/.config/tindol-family-google/credentials.json"
```

Install the Python dependencies:

```bash
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Run the first test:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/google-workspace/scripts/calendar_list_today.py"
```

The first run opens a browser OAuth flow and creates:

`/Users/tindolhouse/.config/tindol-family-google/token.json`

## Environment Overrides

Scripts default to the paths above, but support overrides:

- `TINDOL_GOOGLE_CREDENTIALS`
- `TINDOL_GOOGLE_TOKEN`
- `TINDOL_GOOGLE_TIMEZONE`

## Slack

Slack can be used by local scripts and agent skills when the user explicitly asks for live Slack data.

Slack script path:

`/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/`

Slack credential folder outside the repo:

`/Users/tindolhouse/.config/tindol-family-slack/`

Slack token file:

`/Users/tindolhouse/.config/tindol-family-slack/slack.env`

Expected token variable:

`SLACK_BOT_TOKEN=xoxb-...`

Optional override:

`TINDOL_SLACK_TOKEN_FILE=/path/to/slack.env`

### Slack Safety Rules

- Do not store Slack tokens in the project repo.
- Do not print, summarize, copy, paste, or inspect Slack token contents.
- Scripts may read the token only to authenticate Slack API calls.
- Start with read-only methods.
- Write-capable scripts such as posting messages require a separate plan and explicit confirmation rules.
- Slack data should enrich the family hub; local Markdown/CSV remains the durable source of truth unless the user asks to sync.

### Suggested Slack Bot Token Scopes

For read-only starter scripts:

- `channels:read`
- `groups:read`
- `im:read`
- `mpim:read`
- `channels:history`
- `groups:history`
- `im:history`
- `mpim:history`

For message sending:

- `chat:write`
- `im:write`

Slack apps only see conversations allowed by token scopes and app membership. For private channels and DMs, the app must have the right scopes and access.

Official references:

- Slack tokens: https://docs.slack.dev/authentication/tokens/
- `conversations.list`: https://docs.slack.dev/reference/methods/conversations.list
- `conversations.history`: https://docs.slack.dev/reference/methods/conversations.history

### Slack Setup

Create the external token folder:

```bash
mkdir -p "/Users/tindolhouse/.config/tindol-family-slack"
chmod 700 "/Users/tindolhouse/.config/tindol-family-slack"
```

Create the token file:

```bash
printf 'SLACK_BOT_TOKEN=xoxb-your-token-here\n' > "/Users/tindolhouse/.config/tindol-family-slack/slack.env"
chmod 600 "/Users/tindolhouse/.config/tindol-family-slack/slack.env"
```

Run the first test:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/slack_auth_test.py"
```
