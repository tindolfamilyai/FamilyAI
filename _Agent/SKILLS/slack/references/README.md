# Slack Tools

Read-only Python scripts for Slack Web API access.

These scripts use Python's standard library only.

## Secret Storage

Slack token is outside the repo:

`/Users/tindolhouse/.config/tindol-family-slack/slack.env`

Expected content:

```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
```

Do not paste token contents into chat or Markdown.

## Suggested Bot Token Scopes

- `channels:read`
- `groups:read`
- `im:read`
- `mpim:read`
- `channels:history`
- `groups:history`
- `im:history`
- `mpim:history`

For sending messages, also add:

- `chat:write`
- `im:write`

## First Run

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/slack_auth_test.py"
```

## Scripts

- `slack_auth_test.py`: verify token and print workspace/user metadata.
- `slack_list_conversations.py`: list visible Slack conversations.
- `slack_recent_messages.py`: print recent messages from a specific conversation id.
- `slack_send_message.py`: send a message to a channel id or user id after explicit `--send`.
  - Supports `--text` and `--text-file` for longer messages.
- `slack_auth.py`: shared token/API helper.

## Send Message Examples

Dry run:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/slack_send_message.py" --channel C123 --text "Test from Tindol Family Hub" --dry-run
```

Send to a channel/conversation id:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/slack_send_message.py" --channel C123 --text "Test from Tindol Family Hub" --send
```

Send a DM to a Slack user id:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/slack_send_message.py" --user U123 --text "Test from Tindol Family Hub" --send
```

Send from a file:

```bash
python3 "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Agent/SKILLS/slack/scripts/slack_send_message.py" --channel C123 --text-file "/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Reports/Daily_Briefs/2026-04-29_daily_brief.md" --send
```

## Environment Overrides

- `SLACK_BOT_TOKEN`
- `TINDOL_SLACK_TOKEN_FILE`
