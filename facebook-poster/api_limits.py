"""Persistent daily API-call guard.

Limits are stored in SQLite so restarting the process does not reset them.
This prevents accidental loops/retries from consuming unlimited credits.
"""
from datetime import datetime, timezone
from database import get_connection

DEFAULT_LIMITS = {
    "news_fetch": 10,
    "llm_generate": 5,
    "llm_review": 5,
    "image_generate": 3,
    "facebook_publish": 2,
}

def _today():
    return datetime.now(timezone.utc).date().isoformat()

def initialize_api_limits():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS api_usage (
                usage_date TEXT NOT NULL,
                operation TEXT NOT NULL,
                calls INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (usage_date, operation)
            )
        """)

def get_limit(operation):
    import os
    key = f"MAX_{operation.upper()}_CALLS_PER_DAY"
    try:
        return int(os.getenv(key, DEFAULT_LIMITS.get(operation, 10)))
    except ValueError:
        return DEFAULT_LIMITS.get(operation, 10)

def check_and_record(operation, amount=1):
    initialize_api_limits()
    limit = get_limit(operation)
    today = _today()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT calls FROM api_usage WHERE usage_date=? AND operation=?",
            (today, operation)
        ).fetchone()
        current = int(row["calls"]) if row else 0
        if current + amount > limit:
            raise RuntimeError(
                f"Daily API limit reached for '{operation}': "
                f"{current}/{limit}. Increase the limit in .env only if required."
            )
        connection.execute("""
            INSERT INTO api_usage(usage_date, operation, calls)
            VALUES (?, ?, ?)
            ON CONFLICT(usage_date, operation)
            DO UPDATE SET calls = calls + excluded.calls
        """, (today, operation, amount))

def usage():
    initialize_api_limits()
    today = _today()
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT operation, calls FROM api_usage WHERE usage_date=?",
            (today,)
        ).fetchall()
    return {row["operation"]: row["calls"] for row in rows}
