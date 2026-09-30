"""Connector protocol - all 5 projects implement this."""
from typing import Protocol
from datetime import datetime
from dataclasses import dataclass

@dataclass
class RawMessage:
    provider_id: str
    thread_id: str
    from_addr: str
    to_addr: str
    subject: str
    body: str
    timestamp: datetime
    labels: list[str]

class MailConnector(Protocol):
    project_id: str

    async def fetch_new(self, since: datetime) -> list[RawMessage]: ...
    async def send_reply(self, thread_id: str, body: str) -> None: ...
    async def mark_read(self, message_id: str) -> None: ...

# TODO: implement GmailConnector with OAuth refresh
# TODO: Outlook via Graph API - need to handle delta tokens
# IMAP is the fallback for the weird legacy mailbox (project-3)
