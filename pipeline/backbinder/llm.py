"""LLM access layer.

One small interface so the rest of the pipeline never touches the SDK
directly and tests can inject a fake.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel

MODEL = "claude-opus-4-8"

S = TypeVar("S", bound=BaseModel)


class LLM(Protocol):
    def parse(self, system: str, user: str, schema: type[S]) -> S:
        """Return a schema-validated structured response."""
        ...

    def draft(self, system: str, user: str) -> str:
        """Return free-text output (drafting)."""
        ...


class AnthropicLLM:
    """Production implementation on the Anthropic API.

    The system prompts are frozen per task type, so they carry a cache_control
    breakpoint; the volatile email content rides in the user turn.
    """

    def __init__(self, model: str = MODEL):
        import anthropic  # lazy: tests must not require a configured client

        self._client = anthropic.Anthropic()
        self._model = model

    def parse(self, system: str, user: str, schema: type[S]) -> S:
        response = self._client.messages.parse(
            model=self._model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=[{
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user}],
            output_format=schema,
        )
        parsed = response.parsed_output
        if parsed is None:
            raise RuntimeError(
                f"structured output parse failed (stop_reason={response.stop_reason})"
            )
        return parsed

    def draft(self, system: str, user: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=[{
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user}],
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeLLM:
    """Deterministic test double. Queue up responses in order of expected calls."""

    def __init__(self) -> None:
        self.parse_responses: list[BaseModel] = []
        self.draft_responses: list[str] = []
        self.parse_calls: list[tuple[str, str]] = []
        self.draft_calls: list[tuple[str, str]] = []

    def parse(self, system: str, user: str, schema: type[S]) -> S:
        self.parse_calls.append((system, user))
        result = self.parse_responses.pop(0)
        assert isinstance(result, schema), f"queued {type(result)}, wanted {schema}"
        return result

    def draft(self, system: str, user: str) -> str:
        self.draft_calls.append((system, user))
        return self.draft_responses.pop(0)
