"""Intake: classify an incoming email into a routed task."""

from __future__ import annotations

from .llm import LLM
from .models import Classification, IncomingEmail, TaskKind, route

# Frozen system prompt (prefix-cached). Volatile email content goes in the
# user turn only — do not interpolate anything per-request into this string.
CLASSIFIER_SYSTEM = """\
You are the intake classifier for an independent insurance agency's back office.
You read one email at a time from the agency's shared mailbox and classify it.

Category guide:
- coi_request: someone needs a certificate of insurance (ACORD 25) — typically
  a client, their landlord, a general contractor, or a project owner. Words
  like "certificate", "COI", "cert holder", "additional insured".
- renewal: carrier or client correspondence about an upcoming policy renewal,
  non-renewal notice, or renewal quote.
- carrier_document: policy documents, endorsements, audit notices, commission
  statements, or other carrier paperwork that needs filing or action.
- client_question: an insured asking about their coverage, billing, or a claim.
  NEVER attempt to answer coverage questions — classification only.
- cross_sell_reply: a response to one of the agency's cross-sell campaigns.
- spam_or_other: marketing, phishing, or anything that doesn't belong.

Be conservative with confidence: if the email is ambiguous, could fit two
categories, or involves a claim or angry client, lower your confidence below
0.6 so a human handles it."""


def classify(llm: LLM, email: IncomingEmail) -> Classification:
    user = (
        f"From: {email.sender}\n"
        f"Subject: {email.subject}\n"
        f"Received: {email.received_at.isoformat()}\n\n"
        f"{email.body}"
    )
    return llm.parse(CLASSIFIER_SYSTEM, user, Classification)


def classify_and_route(llm: LLM, email: IncomingEmail) -> tuple[Classification, TaskKind]:
    classification = classify(llm, email)
    return classification, route(classification)
