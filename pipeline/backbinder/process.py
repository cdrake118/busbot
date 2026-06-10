"""End-to-end processing of one incoming email."""

from __future__ import annotations

from dataclasses import dataclass

from .drafters import make_draft
from .intake import classify_and_route
from .llm import LLM
from .models import Classification, Draft, IncomingEmail, TaskKind
from .review import ReviewItem, ReviewQueue


@dataclass
class ProcessResult:
    classification: Classification
    task: TaskKind
    review_item: ReviewItem | None   # None when IGNORE


def process_email(
    llm: LLM,
    queue: ReviewQueue,
    email: IncomingEmail,
    agency_voice: str = "professional, warm, plain-language",
) -> ProcessResult:
    classification, task = classify_and_route(llm, email)

    if task is TaskKind.IGNORE:
        return ProcessResult(classification, task, None)

    if task is TaskKind.HUMAN_TRIAGE:
        # No automated draft — queue the email itself for a human decision.
        draft = Draft(
            kind=task,
            subject=f"[triage] {email.subject}",
            body=email.body,
            notes_for_reviewer=(
                f"Needs human handling. Category: {classification.category.value} "
                f"(confidence {classification.confidence:.2f}). {classification.summary}"
            ),
        )
    else:
        draft = make_draft(llm, task, email, classification, agency_voice)

    item = queue.add(email.id, draft)
    return ProcessResult(classification, task, item)
