"""Core data shapes for the pipeline."""

from __future__ import annotations

import enum
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class EmailCategory(str, enum.Enum):
    COI_REQUEST = "coi_request"
    RENEWAL = "renewal"
    CARRIER_DOCUMENT = "carrier_document"
    CLIENT_QUESTION = "client_question"
    CROSS_SELL_REPLY = "cross_sell_reply"
    SPAM_OR_OTHER = "spam_or_other"


class Priority(str, enum.Enum):
    URGENT = "urgent"      # same-day client need (e.g. COI for a job starting today)
    NORMAL = "normal"
    LOW = "low"


class IncomingEmail(BaseModel):
    """A message pulled from the agency's delegated mailbox."""

    id: str
    sender: str
    subject: str
    body: str
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Classification(BaseModel):
    """Structured output of the intake classifier.

    This is the schema the LLM must return (structured outputs), so keep
    every field description written for the model.
    """

    category: EmailCategory = Field(
        description="The single best-fitting category for this email."
    )
    priority: Priority = Field(
        description=(
            "urgent = an explicit same-day/next-day need (job site tomorrow, "
            "closing today). normal = routine request. low = informational."
        )
    )
    insured_name: str | None = Field(
        default=None,
        description="The insured/client business or person the email concerns, if identifiable.",
    )
    certificate_holder: str | None = Field(
        default=None,
        description="For COI requests only: the certificate holder named in the request.",
    )
    requested_deadline: str | None = Field(
        default=None,
        description="Any deadline stated in the email, verbatim (e.g. 'by Friday', '6/15').",
    )
    summary: str = Field(
        description="One sentence: who needs what by when."
    )
    confidence: float = Field(
        ge=0, le=1,
        description="Your confidence in the category, 0-1. Below 0.6 routes to a human.",
    )


class TaskKind(str, enum.Enum):
    COI_PREP = "coi_prep"
    RENEWAL_OUTREACH = "renewal_outreach"
    CROSS_SELL_DRAFT = "cross_sell_draft"
    HUMAN_TRIAGE = "human_triage"   # low confidence or no automated playbook
    IGNORE = "ignore"


class Draft(BaseModel):
    """A drafted work product awaiting human review."""

    kind: TaskKind
    subject: str
    body: str
    notes_for_reviewer: str = ""


# Routing table: which category produces which task. Anything not listed
# (or any low-confidence classification) goes to a human.
CATEGORY_TO_TASK: dict[EmailCategory, TaskKind] = {
    EmailCategory.COI_REQUEST: TaskKind.COI_PREP,
    EmailCategory.RENEWAL: TaskKind.RENEWAL_OUTREACH,
    EmailCategory.CARRIER_DOCUMENT: TaskKind.HUMAN_TRIAGE,
    EmailCategory.CLIENT_QUESTION: TaskKind.HUMAN_TRIAGE,
    EmailCategory.CROSS_SELL_REPLY: TaskKind.HUMAN_TRIAGE,
    EmailCategory.SPAM_OR_OTHER: TaskKind.IGNORE,
}

CONFIDENCE_FLOOR = 0.6


def route(classification: Classification) -> TaskKind:
    """Map a classification to a task, demoting low-confidence calls to a human."""
    task = CATEGORY_TO_TASK[classification.category]
    if task is TaskKind.IGNORE:
        return task
    if classification.confidence < CONFIDENCE_FLOOR:
        return TaskKind.HUMAN_TRIAGE
    return task
