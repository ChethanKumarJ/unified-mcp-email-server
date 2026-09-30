"""test dedupe - I kept getting dupes on re-poll until I added the composite key"""
from src.normalize import dedupe_key

def test_dedupe_key_stable():
    k1 = dedupe_key("proj-a", "gmail-123")
    k2 = dedupe_key("proj-a", "gmail-123")
    assert k1 == k2

def test_dedupe_key_isolated():
    # same provider_id, different projects -> different keys
    k1 = dedupe_key("proj-a", "123")
    k2 = dedupe_key("proj-b", "123")
    assert k1 != k2
