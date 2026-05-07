# Skill: Orlando Theme Park Family New-Finds Scout

Aliases: social research, orlando content scout, content scout, research places, research events, theme park research, internet search for posts, orlando themepark family scout

## Purpose

Run a daily public-internet source pull for Orlando Theme Park Family and send a Slack update containing only newly discovered upcoming events, places, park news, food items, or family content opportunities that have not already been recorded from prior runs.

Current phase: discover and notify only.

This skill does not publish posts, schedule posts, contact brands, buy tickets, book events, or create calendar entries.

## Slack Destination

Send the daily new-finds update to Slack channel named:

`orlando-themepark-family`

Use the Slack channel ID once known. If the channel ID is not known, first use the Slack skill to list conversations and find the channel. If the channel does not exist or the bot is not invited, report that setup gap and still save the local research run files.

## Required Inputs

Read these before running:

1. `08_Social_Media_Orlando_Theme_Park_Family/README.md`
2. `08_Social_Media_Orlando_Theme_Park_Family/research_sources.md`
3. `08_Social_Media_Orlando_Theme_Park_Family/research_candidates.csv`
4. `_Agent/SKILLS/slack/SKILL.md`
5. `_Agent/INTEGRATIONS.md`

## Search Window

Default target window:

- Upcoming items 1-6 months from the current date.
- Also scan yesterday and today for newly published announcements about later events.

Use ISO dates. If an event is recurring, record the date range and next relevant date.

## Source Pull Requirements

Use `research_sources.md` as the broad source universe. Do not limit the workflow to a few search results.

Daily target:

- Attempt at least 70 direct source checks or source-specific searches.
- Run at least 20 broader web/news searches.
- Prefer official pages first for dates, prices, and event facts.
- Use local calendars, food/news sites, and family guides to discover items that official theme park pages may not surface.

If a run cannot cover the full target, note the coverage gap in the local run summary and Slack message.

## Idea Mix Requirements

Do not let the daily output become only Disney, Universal, SeaWorld, or other obvious headline events. Keep major park items, but actively hunt for out-of-the-box, useful post ideas that a family audience may not already see everywhere.

Each normal run should try to include this mix when sources support it:

- 2-4 major theme park or attraction items.
- 4-8 food, dessert, snack, food hall, night market, restaurant opening, or limited-menu ideas.
- 3-6 local neighborhood, museum, garden, zoo, library, market, or community events.
- 2-4 Florida day-trip ideas within a reasonable Orlando-family driving radius.
- 2-4 trend-watch ideas, such as "try this before it goes viral", "rainy day backup", "low-cost local alternative", "parent night", or "not the obvious tourist pick".

Favor ideas with a clear content angle, not just event names. Examples:

- A family food crawl at a local market.
- A "theme park alternative under $20" comparison.
- A rainy-day indoor plan.
- A stroller-friendly farmers market morning.
- A weird Florida fruit/festival day trip.
- A kid-friendly culture event with strong visuals.
- A local chef or food trend that connects back to Disney/Universal visitors.

## Candidate Categories

Classify each discovered item into one primary category:

- Theme parks
- Water parks
- Resorts and hotels
- Food festivals
- Restaurants and sweets
- Zoos and aquariums
- Museums and indoor family activities
- Outdoor family activities
- Community events
- Seasonal and holiday events
- Florida day trips
- News and trend watch
- Brand or partnership lead

## Validation And De-Dupe

Before sending Slack, validate every candidate against `research_candidates.csv`.

### Build A Duplicate Key

For each candidate, create a normalized `DuplicateKey`:

`normalized_venue|normalized_event_name|start_date`

Normalize:

- Lowercase.
- Remove punctuation.
- Collapse whitespace.
- Remove tracking parameters from URLs.
- Convert common aliases:
  - `Walt Disney World`, `Disney World`, `WDW`
  - `EPCOT`, `Epcot`
  - `Universal Orlando`, `Universal Orlando Resort`, `UOR`
  - `SeaWorld Orlando`, `SeaWorld`
  - `LEGOLAND Florida`, `Legoland`

### Compare Against History

Treat a candidate as already recorded if any of these match an existing row:

- Same `DuplicateKey`.
- Same canonical `SourceURL`.
- Same `EventName` + `Venue` + overlapping date range.
- Fuzzy title match plus same venue and month.

### Status Rules

Only items with `Status=New` are eligible for the Slack update.

Use:

- `New` - not previously recorded.
- `Repeated` - already recorded with no meaningful change.
- `Updated` - same item, but date, menu, price, lineup, or important detail changed.
- `NeedsVerification` - likely useful but date/source details conflict.

For this phase:

- Do not include `Repeated` in Slack.
- Do not include `Updated` unless the update is materially useful for posting.
- Do not include `NeedsVerification` unless there are no new items; then put it under a short "Needs verification" note.

## Candidate CSV Output

Append every candidate checked to:

`08_Social_Media_Orlando_Theme_Park_Family/research_candidates.csv`

Preserve this header:

`DiscoveredDate,Status,SourceTier,SourceName,SourceURL,Category,EventName,Venue,City,StartDate,EndDate,Price,FamilyFit,VisualScore,FoodScore,ThemeParkFit,UrgencyScore,UniquenessScore,EaseScore,CostScore,ConfidenceScore,TotalScore,DuplicateKey,Summary,ContentAngle,RecommendedAction,Notes`

For repeated items, append a row with `Status=Repeated` only when it helps audit the run. Otherwise, skip appending exact repeats to avoid noisy history.

## Local Run Summary Output

Save a local run summary to:

`_Reports/Social_Research/YYYY-MM-DD_orlando_themepark_family_new_finds.md`

When the user asks for a Drive-friendly report, also save an organized copy inside:

`08_Social_Media_Orlando_Theme_Park_Family/Research_Reports/YYYY-MM-DD_<short_topic>.md`

This domain-folder copy is intended to sync to Google Drive with the `gdrive-sync` skill.

The local summary should include:

- Search window.
- Sources attempted count.
- Queries run count.
- New items sent to Slack.
- Repeated items suppressed count.
- Updated items found count.
- Needs verification count.
- Slack delivery status.
- Source gaps or failures.

## Slack Output

Send one concise message to `orlando-themepark-family`.

Use this format:

```text
*Orlando Theme Park Family - New Finds*
Window: <date> to <date>
Sources checked: <count> | New: <count> | Repeats suppressed: <count>

*New upcoming finds*
1. *<Event / thing>* - <venue>, <date or range>
   Why it matters: <short reason>
   Post angle: <short angle>
   Source: <url>

2. ...

*Notes*
- <coverage gaps, if any>
- <verification needs, if any>
```

Slack formatting rules:

- Use Slack mrkdwn.
- Keep each item short.
- Put long tables in fenced code blocks only if absolutely needed.
- Do not paste long article text.
- Include source links.

If no new items were found, send:

```text
*Orlando Theme Park Family - New Finds*
No new upcoming items found today that were not already recorded.

Sources checked: <count>
Repeated items suppressed: <count>
Notes: <gaps if any>
```

## What This Skill Does Not Do Yet

- It does not update `post_ideas.md`.
- It does not update `content_calendar.csv`.
- It does not update `research_decisions.csv`.
- It does not schedule posts.
- It does not add family calendar events.
- It does not ask for approval lists.

Those can be added later after the daily new-finds Slack process is stable.

## Safety

- Use public sources only.
- Do not scrape private/social accounts that require login unless the user explicitly provides a safe workflow.
- Respect paywalls and source limits.
- Never store credentials or tokens in the repo.
- Do not expose private family details in public content recommendations.
- Sending this daily new-finds summary to the configured `orlando-themepark-family` Slack channel is the intended output of this skill.
