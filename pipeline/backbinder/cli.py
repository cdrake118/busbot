"""Operator CLI.

    python -m backbinder.cli process --mailbox-file email.txt   # classify + draft + enqueue
    python -m backbinder.cli queue                              # list pending
    python -m backbinder.cli show <id>
    python -m backbinder.cli approve <id> --who cory
    python -m backbinder.cli reject <id> --who austin --note "wrong holder"
    python -m backbinder.cli stats
"""

from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

from .llm import AnthropicLLM
from .models import IncomingEmail
from .process import process_email
from .review import ReviewQueue

DEFAULT_DB = Path.home() / ".backbinder" / "review.db"


def _queue(args: argparse.Namespace) -> ReviewQueue:
    db = Path(args.db)
    db.parent.mkdir(parents=True, exist_ok=True)
    return ReviewQueue(db)


def cmd_process(args: argparse.Namespace) -> int:
    raw = Path(args.mailbox_file).read_text() if args.mailbox_file else sys.stdin.read()
    # Minimal plain-text format: first line From:, second Subject:, rest body.
    lines = raw.splitlines()
    sender = lines[0].removeprefix("From:").strip() if lines else "unknown"
    subject = lines[1].removeprefix("Subject:").strip() if len(lines) > 1 else "(no subject)"
    body = "\n".join(lines[2:]).strip()

    email = IncomingEmail(id=uuid.uuid4().hex[:12], sender=sender, subject=subject, body=body)
    result = process_email(AnthropicLLM(), _queue(args), email)

    print(f"category : {result.classification.category.value} "
          f"(confidence {result.classification.confidence:.2f})")
    print(f"task     : {result.task.value}")
    if result.review_item:
        print(f"queued   : {result.review_item.id}  -> 'queue' to review")
    else:
        print("queued   : nothing (ignored)")
    return 0


def cmd_queue(args: argparse.Namespace) -> int:
    items = _queue(args).pending()
    if not items:
        print("review queue is empty")
        return 0
    for it in items:
        print(f"{it.id}  {it.task_kind:18s} {it.subject[:60]}")
        print(f"    {it.notes}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    it = _queue(args).get(args.id)
    if it is None:
        print(f"no item {args.id}", file=sys.stderr)
        return 1
    print(f"id      : {it.id}\nstatus  : {it.status}\ntask    : {it.task_kind}")
    print(f"subject : {it.subject}\nnotes   : {it.notes}\n\n{it.body}")
    return 0


def cmd_decide(args: argparse.Namespace, action: str) -> int:
    q = _queue(args)
    fn = q.approve if action == "approve" else q.reject
    it = fn(args.id, who=args.who, note=args.note)
    print(f"{it.id} -> {it.status} by {args.who}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    for status, n in sorted(_queue(args).stats().items()):
        print(f"{status:10s} {n}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="backbinder")
    p.add_argument("--db", default=str(DEFAULT_DB))
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("process", help="classify + draft + enqueue one email")
    sp.add_argument("--mailbox-file", help="plain-text email file (default: stdin)")

    sub.add_parser("queue", help="list pending review items")

    sp = sub.add_parser("show")
    sp.add_argument("id")

    for action in ("approve", "reject"):
        sp = sub.add_parser(action)
        sp.add_argument("id")
        sp.add_argument("--who", required=True)
        sp.add_argument("--note", default="")

    sub.add_parser("stats")

    args = p.parse_args(argv)
    if args.cmd == "process":
        return cmd_process(args)
    if args.cmd == "queue":
        return cmd_queue(args)
    if args.cmd == "show":
        return cmd_show(args)
    if args.cmd in ("approve", "reject"):
        return cmd_decide(args, args.cmd)
    if args.cmd == "stats":
        return cmd_stats(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
