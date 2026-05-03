# Skill: Slack Ops

Aliases: slack, slack api, slack search, slack channels, slack messages

## Purpose

Use local read-only Slack API scripts to inspect workspace metadata, channels, and recent messages when the user explicitly asks for live Slack data.

## Safety

- Never read, print, summarize, copy, or paste Slack token contents.
- Never store Slack tokens in the repo.
- Use read-only scripts first.
- Do not post messages, invite users, archive channels, change channel membership, or mutate Slack state without a separate approved write-capable workflow.
- Sending a Slack message requires explicit user confirmation and the `slack_send_message.py --send` flag, except for the daily-brief workflow, which is pre-approved to send the generated brief to the configured family channel.
- Local Markdown/CSV stays the durable source of truth unless the user asks to sync.

## Scripts

Scripts are bundled in this skill at `_Agent/SKILLS/slack/scripts/`.

Available read-only scripts:

- `slack_auth_test.py`
- `slack_list_conversations.py`
- `slack_recent_messages.py`

Write-capable script, dry-run by default:

- `slack_send_message.py`

Shared auth/client helper:

- `slack_auth.py`

## References

Setup documentation and token instructions are bundled at `_Agent/SKILLS/slack/references/README.md`.

## Credential Location

Slack token lives outside the repo:

`/Users/tindolhouse/.config/tindol-family-slack/slack.env`

Expected token variable:

`SLACK_BOT_TOKEN=xoxb-...`

## Run Steps

1. Read `_Agent/INTEGRATIONS.md`.
2. Choose the narrowest read-only Slack script.
3. Run the script with bounded limits.
4. Use the output to summarize, draft, or propose local updates.
5. Do not mutate Slack or local source files unless the user explicitly asks.

## Common Commands

Auth test:

```bash
python3 "_Agent/SKILLS/slack/scripts/slack_auth_test.py"
```

List conversations:

```bash
python3 "_Agent/SKILLS/slack/scripts/slack_list_conversations.py" --limit 20
```

Recent messages in a channel:

```bash
python3 "_Agent/SKILLS/slack/scripts/slack_recent_messages.py" CHANNEL_ID --limit 10
```

Send a message after explicit user approval:

```bash
python3 "_Agent/SKILLS/slack/scripts/slack_send_message.py" --channel CHANNEL_ID --text "Message text" --send
```

Send a long Markdown/text brief from file:

```bash
python3 "_Agent/SKILLS/slack/scripts/slack_send_message.py" --channel CHANNEL_ID --text-file "/absolute/path/to/brief.md" --send
```

## Skill Integrations

- `daily-brief/SKILL.md`: sends the generated brief to the configured family Slack channel by default unless the user asks for chat-only/no-Slack.
- `tasks/SKILL.md`: can convert Slack action items into local `todo.md` only when requested.
- `inbox/SKILL.md`: can use Slack read-only context when explicitly requested.
