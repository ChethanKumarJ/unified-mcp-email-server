# unified-mcp-email-server

MCP server that consolidates email from 5 project mailboxes into one normalized stream.

I was juggling 5 projects, each with its own mailbox and polling script. It was a mess. So I built one service, one schema, one loop — all 5 connectors run as concurrent tasks in a single asyncio event loop.

## Quick start

```bash
pip install -e .
python -m src.server --config config/projects.json
```

## How it works

- `connectors/` — Gmail / Outlook / IMAP adapters, all implement `MailConnector`
- single `asyncio.TaskGroup` polls all 5 concurrently
- normalization layer dedupes on `(project_id, provider_message_id)` and tags `project_id`
- SQLite for dev, Postgres for prod
- MCP tools: `list_emails`, `get_email`, `send_reply`, `search_across_projects`, `summarize_thread`

See `src/server.py` for the loop. It's simpler than it sounds.

## What I'd do next

- [ ] webhook push (Gmail Pub/Sub) instead of polling
- [ ] per-project rate-limit dashboard
