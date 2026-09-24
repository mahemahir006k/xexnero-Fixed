"""Low-cost batch analytics.

Events are stored locally and summarized on demand/daily. No AI call is made
for each event; this avoids multiplying model/API usage.
"""
from datetime import datetime, timezone
from database import get_connection

def initialize_analytics():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                status TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT NOT NULL
            )
        """)

def record_event(event_type, status="ok", metadata=""):
    initialize_analytics()
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO analytics_events(event_type, status, metadata, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            event_type, status, metadata,
            datetime.now(timezone.utc).isoformat()
        ))

def daily_summary():
    initialize_analytics()
    today = datetime.now(timezone.utc).date().isoformat()
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT event_type, status, COUNT(*) AS count
            FROM analytics_events
            WHERE substr(created_at, 1, 10) = ?
            GROUP BY event_type, status
            ORDER BY event_type, status
        """, (today,)).fetchall()
    return [
        {
            "event_type": r["event_type"],
            "status": r["status"],
            "count": r["count"]
        }
        for r in rows
    ]
