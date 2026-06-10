"""Drafters: turn a routed task into a Draft for the human review queue.

Every drafter output is a DRAFT. Nothing here sends anything. The E&O wall
lives in the prompts: logistics only, never coverage advice, the agency
licensee issues every certificate.
"""

from __future__ import annotations

from .llm import LLM
from .models import Classification, Draft, IncomingEmail, TaskKind

# Frozen per-task system prompts (prefix-cached). Per-agency voice/config is
# appended in the user turn, not here.
COI_SYSTEM = """\
You prepare COI work packets for an independent insurance agency.
Given a certificate request email, produce a work packet for the agency's
licensed staff containing exactly these sections:

WHO: the insured and the certificate holder (name + address if present).
WHAT: coverages/limits the request asks to evidence, and any special wording
  requested (additional insured, waiver of subrogation, primary & noncontractual).
FLAGS: anything a licensee must decide — wording the policy may not support,
  holder requirements that look unusual, missing information to chase.
REPLY DRAFT: a short, professional acknowledgment email to the requester
  confirming receipt and expected turnaround. Do not promise coverage exists.

Hard rules: you do not issue certificates, you do not confirm coverage, you do
not give coverage advice. The packet prepares a licensee to act in minutes."""

RENEWAL_SYSTEM = """\
You draft renewal outreach for an independent insurance agency.
Given a renewal notice and policy context, produce:

CHECKLIST: the remarketing checklist for the account manager (what to verify,
  which carriers plausibly fit, what client info needs updating).
CLIENT EMAIL: a warm, plain-language draft to the client in the agency's
  voice — we're working your renewal, here's what we need from you, no jargon.

Hard rules: never state premiums or coverage terms as fact, never advise the
client to change coverage. Logistics and relationship only."""

CROSS_SELL_SYSTEM = """\
You draft cross-sell campaign outreach for an independent insurance agency.
Given a client segment and the campaign angle, produce a short, personal
email draft (under 150 words) inviting a conversation — not a pitch.

Hard rules: no premium promises, no coverage recommendations, one clear
call to action (a 10-minute call), written like a human agent wrote it."""

_SYSTEM_BY_TASK = {
    TaskKind.COI_PREP: COI_SYSTEM,
    TaskKind.RENEWAL_OUTREACH: RENEWAL_SYSTEM,
    TaskKind.CROSS_SELL_DRAFT: CROSS_SELL_SYSTEM,
}


def make_draft(
    llm: LLM,
    task: TaskKind,
    email: IncomingEmail,
    classification: Classification,
    agency_voice: str = "professional, warm, plain-language",
) -> Draft:
    """Produce a Draft for an automatable task.

    HUMAN_TRIAGE and IGNORE tasks never reach this function.
    """
    system = _SYSTEM_BY_TASK[task]
    user = (
        f"Agency voice: {agency_voice}\n"
        f"Classifier summary: {classification.summary}\n"
        f"Insured: {classification.insured_name or 'unknown'}\n"
        f"Deadline stated: {classification.requested_deadline or 'none'}\n\n"
        f"--- Original email ---\n"
        f"From: {email.sender}\n"
        f"Subject: {email.subject}\n\n"
        f"{email.body}"
    )
    body = llm.draft(system, user)
    return Draft(
        kind=task,
        subject=f"[{task.value}] {classification.insured_name or email.subject}",
        body=body,
        notes_for_reviewer=(
            f"Priority: {classification.priority.value}. "
            f"Deadline: {classification.requested_deadline or 'none stated'}. "
            f"Classifier confidence: {classification.confidence:.2f}."
        ),
    )
