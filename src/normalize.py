"""Normalization + dedupe - composite key (project_id, provider_id)."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class NormalizedMessage:
    message_id: str  # f"{project_id}:{provider_id}" hashed
    project_id: str
    thread_id: str
    subject: str
    body: str
    timestamp: datetime
    is_read: bool = False

def normalize(project_id: str, raw) -> NormalizedMessage:
    # provider_id might have weird chars, just hash it
    import hashlib
    pid_hash = hashlib.sha256(raw.provider_id.encode()).hexdigest()[:16]
    mid = f"{project_id}_{pid_hash}"
    return NormalizedMessage(
        message_id=mid,
        project_id=project_id,
        thread_id=raw.thread_id,
        subject=raw.subject.strip(),
        body=raw.body,
        timestamp=raw.timestamp,
    )

def dedupe_key(project_id: str, provider_id: str) -> str:
    # used this in server.py too, keeping it here as the canonical version
    # TODO: remove duplicate logic from server.py
    import hashlib
    h = hashlib.sha256(provider_id.encode()).hexdigest()[:16]
    return f"{project_id}_{h}"
