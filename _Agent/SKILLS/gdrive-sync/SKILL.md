# Skill: Google Drive Sync

Aliases: gdrive sync, gdrive-sync, drive sync, backup to drive, sync to google drive, upload to drive

## Purpose

Sync the ten Tindol Family domain folders (`00_Calendar` through `09_Holidays_Birthdays`), the project `Docs/` folder, and the `_Reports/` folder to Google Drive, mirroring the local folder hierarchy inside a root Drive folder called `Tindol Family Hub`.

## Safety

- Never read, print, summarize, copy, or paste OAuth credential/token contents.
- Never store credentials or tokens in the repo.
- Default to dry-run — list what would be uploaded without touching Drive.
- Do not upload any files to Google Drive without explicit user confirmation and the `--sync` flag.
- Do not sync `_Agent/`, `.claude/`, `.agents/`, `.gemini/`, or any hidden directory.
- Include `/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/Docs` in the default dry-run and sync.
- Include `/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude/_Reports` in the default dry-run and sync.
- Local Markdown/CSV stays the durable source of truth; Drive is a backup, not the primary store.

## Scripts

Scripts are bundled in this skill at `_Agent/SKILLS/gdrive-sync/scripts/`.

Write-capable scripts, dry-run by default:

- `gdrive_sync.py`

Shared auth helper (from google-workspace skill):

- `_Agent/SKILLS/google-workspace/scripts/google_auth.py`

## References

Credential setup follows the same process as the `google-workspace` skill. See `_Agent/SKILLS/google-workspace/references/README.md`.

## Credential Location

Credentials and tokens live outside the repo and are shared with the google-workspace skill:

- `/Users/tindolhouse/.config/tindol-family-google/credentials.json`
- `/Users/tindolhouse/.config/tindol-family-google/token_drive_file.json`

## Run Steps

1. Read `_Agent/INTEGRATIONS.md`.
2. Run a dry-run first to confirm the file list looks correct.
3. If the list looks right, add `--sync` to upload.
4. Check Drive to confirm files appeared in the `Tindol Family Hub` folder.
5. Do not delete or move local files — Drive is a backup copy only.

## Common Commands

Dry-run (lists all files that would be uploaded, no changes made):

```bash
python3 "_Agent/SKILLS/gdrive-sync/scripts/gdrive_sync.py"
```

Sync all ten domain folders plus `Docs/` and `_Reports/` to Drive:

```bash
python3 "_Agent/SKILLS/gdrive-sync/scripts/gdrive_sync.py" --sync
```

Sync only specific numbered domain folders (e.g. Calendar and Finances):

```bash
python3 "_Agent/SKILLS/gdrive-sync/scripts/gdrive_sync.py" --sync --domains 00 06
```

Use a custom root Drive folder name:

```bash
python3 "_Agent/SKILLS/gdrive-sync/scripts/gdrive_sync.py" --sync --folder "My Family Backup"
```

## Skill Integrations

- `google-workspace/SKILL.md`: shares the `google_auth.py` helper and `token_drive_file.json` OAuth token.
