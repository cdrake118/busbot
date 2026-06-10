"""Human review queue.

SQLite-backed. This is the enforcement point for the GOAL.md guardrail:
nothing is sent or executed unless a human approved it here first.
"""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .models import Draft

_SCHEMA = """
CREATE TABLE IF NOT EXISTS review_items (
    id TEXT PRIMARY KEY,
    email_id TEXT NOT NULL,
    task_kind TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    decided_at TEXT,
    decided_by TEXT,
    decision_note TEXT
);
"""

VALID_TRANSITIONS = {
    "pending": {"approved", "rejected"},
    "approved": {"sent"},
    "rejected": set(),
    "sent": set(),
}


@dataclass
class ReviewItem:
    id: str
    email_id: str
    task_kind: str
    subject: str
    body: str
    notes: str
    status: str
    created_at: str
    decided_at: str | None = None
    decided_by: str | None = None
    decision_note: str | None = None


class ReviewQueue:
    def __init__(self, db_path: str | Path):
        self._conn = sqlite3.connect(str(db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(_SCHEMA)
        self._conn.commit()

    def add(self, email_id: str, draft: Draft) -> ReviewItem:
        item = ReviewItem(
            id=uuid.uuid4().hex[:12],
            email_id=email_id,
            task_kind=draft.kind.value,
            subject=draft.subject,
            body=draft.body,
            notes=draft.notes_for_reviewer,
            status="pending",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._conn.execute(
            "INSERT INTO review_items (id, email_id, task_kind, subject, body, notes, status, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (item.id, item.email_id, item.task_kind, item.subject,
             item.body, item.notes, item.status, item.created_at),
        )
        self._conn.commit()
        return item

    def get(self, item_id: str) -> ReviewItem | None:
        row = self._conn.execute(
            "SELECT * FROM review_items WHERE id = ?", (item_id,)
        ).fetchone()
        return ReviewItem(**dict(row)) if row else None

    def pending(self) -> list[ReviewItem]:
        rows = self._conn.execute(
            "SELECT * FROM review_items WHERE status = 'pending' ORDER BY created_at"
        ).fetchall()
        return [ReviewItem(**dict(r)) for r in rows]

    def _transition(self, item_id: str, new_status: str, who: str, note: str) -> ReviewItem:
        item = self.get(item_id)
        if item is None:
            raise KeyError(f"no review item {item_id}")
        if new_status not in VALID_TRANSITIONS[item.status]:
            raise ValueError(f"cannot move {item_id} from {item.status} to {new_status}")
        self._conn.execute(
            "UPDATE review_items SET status = ?, decided_at = ?, decided_by = ?, decision_note = ?"
            " WHERE id = ?",
            (new_status, datetime.now(timezone.utc).isoformat(), who, note, item_id),
        )
        self._conn.commit()
        result = self.get(item_id)
        assert result is not None
        return result

    def approve(self, item_id: str, who: str, note: str = "") -> ReviewItem:
        return self._transition(item_id, "approved", who, note)

    def reject(self, item_id: str, who: str, note: str = "") -> ReviewItem:
        return self._transition(item_id, "rejected", who, note)

    def mark_sent(self, item_id: str, who: str, note: str = "") -> ReviewItem:
        """Only approved items can be marked sent — enforced by the transition table."""
        return self._transition(item_id, "sent", who, note)

    def stats(self) -> dict[str, int]:
        rows = self._conn.execute(
            "SELECT status, COUNT(*) AS n FROM review_items GROUP BY status"
        ).fetchall()
        return {r["status"]: r["n"] for r in rows}
