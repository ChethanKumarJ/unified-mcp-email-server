# unified-mcp-email-server

MCP server that consolidates email from 5 project mailboxes into one normalized stream.

I was juggling 5 projects, each with its own mailbox and polling script. It was a mess. So I built one service, one schema, one loop — all 5 connectors run as concurrent tasks in a single asyncio event loop.

## Quick start

```bash
pip install -e .
python -m src.server --config config/projects.json
```

Config format:
```json
{
  "projects": [
    {"project_id": "proj-a", "provider": "gmail", "poll_interval_s": 60}
  ]
}
```

## How it works

- `connectors/` — Gmail / Outlook / IMAP adapters, all implement `MailConnector`
- single `asyncio.TaskGroup` polls all 5 concurrently — one project's 429 doesn't block the others
- `normalize.py` dedupes on `(project_id, provider_message_id)` — fixed my re-poll dupe bug
- SQLite for dev, Postgres for prod
- MCP tools: `list_emails`, `get_email`, `send_reply`, `search_across_projects`, `summarize_thread`
- MCP resources: `mail://{project_id}/inbox`, `mail://all/unified-inbox`

## What I learned

Polling 5 mailboxes separately was fine until one started rate-limiting and took down the others. Moving to one TaskGroup with independent backoff fixed it.

Dedupe was trickier than expected — Gmail message IDs aren't stable across label changes, hence the hash.

## TODO

- [ ] webhook push (Gmail Pub/Sub) instead of polling
- [ ] per-project rate-limit dashboard
- [ ] remove duplicate dedupe logic from server.py (see normalize.py TODO)
