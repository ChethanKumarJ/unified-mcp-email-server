"""Unified event loop + MCP server skeleton."""
import asyncio
import argparse
from datetime import datetime, timedelta

from mcp.server import Server

server = Server("unified-email")

# in-memory store for v1, will move to sqlite next
_store: dict[str, dict] = {}

@server.tool()
async def list_emails(project_id: str = "", unread_only: bool = False) -> str:
    """List emails, optionally filtered."""
    out = []
    for mid, m in _store.items():
        if project_id and m["project_id"] != project_id:
            continue
        if unread_only and m["is_read"]:
            continue
        out.append(f"{mid} | {m['project_id']} | {m['subject'][:60]}")
        if len(out) >= 20:
            break
    return "\n".join(out) or "no emails"

@server.tool()
async def search_across_projects(query: str) -> str:
    """Full-text search across all 5 projects."""
    q = query.lower()
    hits = []
    for mid, m in _store.items():
        if q in m["subject"].lower() or q in m["body"].lower():
            hits.append(f"{m['project_id']}/{mid}: {m['subject']}")
            if len(hits) >= 10:
                break
    return "\n".join(hits) or "no matches"

async def poll_forever(connector, interval: int = 60):
    """Poll one project forever - runs as a task in the shared loop."""
    since = datetime.now() - timedelta(hours=1)
    while True:
        try:
            msgs = await connector.fetch_new(since)
            for rm in msgs:
                # dedupe on (project_id, provider_id)
                key = f"{connector.project_id}:{rm.provider_id}"
                if key not in _store:
                    _store[key] = {
                        "project_id": connector.project_id,
                        "subject": rm.subject,
                        "body": rm.body,
                        "is_read": False,
                    }
            since = datetime.now()
        except Exception as e:
            # exponential backoff would go here - for now just log and continue
            # so one project's 429 doesn't kill the other 4
            print(f"[{connector.project_id}] poll error: {e}")
        await asyncio.sleep(interval)

async def run_loop(connectors: list):
    # the "same loop" principle - all 5 in one TaskGroup
    async with asyncio.TaskGroup() as tg:
        for c in connectors:
            tg.create_task(poll_forever(c))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    print("TODO: load connectors from config, start MCP server")
    # asyncio.run(run_loop(connectors))
