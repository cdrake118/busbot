"""Offline tests — FakeLLM, temp SQLite. No network, no API key."""

import pytest

from backbinder.llm import FakeLLM
from backbinder.models import (
    Classification,
    EmailCategory,
    IncomingEmail,
    Priority,
    TaskKind,
    route,
)
from backbinder.process import process_email
from backbinder.review import ReviewQueue


def _email(**kw) -> IncomingEmail:
    defaults = dict(
        id="em1",
        sender="office@acmeplumbing.com",
        subject="Need a certificate for our landlord",
        body="Hi, our landlord at 41 Main St needs a COI naming them as additional insured by Friday.",
    )
    defaults.update(kw)
    return IncomingEmail(**defaults)


def _classification(**kw) -> Classification:
    defaults = dict(
        category=EmailCategory.COI_REQUEST,
        priority=Priority.NORMAL,
        insured_name="Acme Plumbing",
        certificate_holder="41 Main St Landlord LLC",
        requested_deadline="by Friday",
        summary="Acme Plumbing needs a COI for their landlord by Friday.",
        confidence=0.95,
    )
    defaults.update(kw)
    return Classification(**defaults)


# --- routing -----------------------------------------------------------------

def test_route_coi_to_coi_prep():
    assert route(_classification()) is TaskKind.COI_PREP


def test_route_low_confidence_to_human():
    assert route(_classification(confidence=0.4)) is TaskKind.HUMAN_TRIAGE


def test_route_spam_ignored_even_at_low_confidence():
    c = _classification(category=EmailCategory.SPAM_OR_OTHER, confidence=0.3)
    assert route(c) is TaskKind.IGNORE


def test_route_client_question_always_human():
    c = _classification(category=EmailCategory.CLIENT_QUESTION, confidence=0.99)
    assert route(c) is TaskKind.HUMAN_TRIAGE


# --- end-to-end processing -----------------------------------------------------

def test_coi_email_produces_pending_review_item(tmp_path):
    llm = FakeLLM()
    llm.parse_responses.append(_classification())
    llm.draft_responses.append("WHO: Acme Plumbing / 41 Main St Landlord LLC\nWHAT: GL, AI wording...")
    queue = ReviewQueue(tmp_path / "q.db")

    result = process_email(llm, queue, _email())

    assert result.task is TaskKind.COI_PREP
    assert result.review_item is not None
    assert result.review_item.status == "pending"
    assert queue.pending()[0].id == result.review_item.id
    # the volatile email content must ride in the user turn, not the system prompt
    system, user = llm.draft_calls[0]
    assert "41 Main St" in user
    assert "41 Main St" not in system


def test_spam_is_ignored_and_never_drafted(tmp_path):
    llm = FakeLLM()
    llm.parse_responses.append(
        _classification(category=EmailCategory.SPAM_OR_OTHER, confidence=0.9)
    )
    queue = ReviewQueue(tmp_path / "q.db")

    result = process_email(llm, queue, _email(subject="WIN A FREE CRUISE"))

    assert result.review_item is None
    assert llm.draft_calls == []
    assert queue.pending() == []


def test_low_confidence_goes_to_human_without_llm_draft(tmp_path):
    llm = FakeLLM()
    llm.parse_responses.append(_classification(confidence=0.5))
    queue = ReviewQueue(tmp_path / "q.db")

    result = process_email(llm, queue, _email())

    assert result.task is TaskKind.HUMAN_TRIAGE
    assert result.review_item is not None
    assert llm.draft_calls == []  # no automated draft for triage
    assert "Needs human handling" in result.review_item.notes


# --- review queue guardrails ---------------------------------------------------

def test_nothing_sendable_without_approval(tmp_path):
    llm = FakeLLM()
    llm.parse_responses.append(_classification())
    llm.draft_responses.append("packet")
    queue = ReviewQueue(tmp_path / "q.db")
    item = process_email(llm, queue, _email()).review_item
    assert item is not None

    # pending -> sent is forbidden
    with pytest.raises(ValueError):
        queue.mark_sent(item.id, who="cory")

    queue.approve(item.id, who="cory", note="looks right")
    sent = queue.mark_sent(item.id, who="cory")
    assert sent.status == "sent"


def test_rejected_is_terminal(tmp_path):
    queue = ReviewQueue(tmp_path / "q.db")
    llm = FakeLLM()
    llm.parse_responses.append(_classification())
    llm.draft_responses.append("packet")
    item = process_email(llm, queue, _email()).review_item
    assert item is not None

    queue.reject(item.id, who="austin", note="wrong holder")
    with pytest.raises(ValueError):
        queue.approve(item.id, who="austin")
    with pytest.raises(ValueError):
        queue.mark_sent(item.id, who="austin")


def test_stats(tmp_path):
    queue = ReviewQueue(tmp_path / "q.db")
    llm = FakeLLM()
    for i in range(3):
        llm.parse_responses.append(_classification())
        llm.draft_responses.append("packet")
        process_email(llm, queue, _email(id=f"em{i}"))
    items = queue.pending()
    queue.approve(items[0].id, who="cory")
    assert queue.stats() == {"pending": 2, "approved": 1}
