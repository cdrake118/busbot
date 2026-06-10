"""BackBinder delivery pipeline.

Email intake -> classification -> task routing -> drafting -> human review queue.
Nothing leaves the review queue without human approval (GOAL.md guardrail).
"""

__version__ = "0.1.0"
