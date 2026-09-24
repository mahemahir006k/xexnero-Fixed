"""Small local JSON cache used to reduce repeated external/file reads.

The cache is intentionally local so the app works without Redis/ElastiCache.
Set CACHE_TTL_SECONDS in .env to control freshness.
"""
import hashlib
import json
import os
import time
from pathlib import Path

from config import CACHE_DIR, CACHE_TTL_SECONDS

CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _path(namespace: str, key: str) -> Path:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{namespace}-{digest}.json"

def get(namespace: str, key: str):
    path = _path(namespace, key)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - float(payload["created_at"]) > CACHE_TTL_SECONDS:
            return None
        return payload["value"]
    except Exception:
        return None

def set(namespace: str, key: str, value):
    path = _path(namespace, key)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(
            {"created_at": time.time(), "value": value},
            ensure_ascii=False
        ),
        encoding="utf-8"
    )
    tmp.replace(path)

def clear(namespace: str | None = None):
    for path in CACHE_DIR.glob("*.json"):
        if namespace is None or path.name.startswith(f"{namespace}-"):
            try:
                path.unlink()
            except OSError:
                pass
