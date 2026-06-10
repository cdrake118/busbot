# BackBinder Delivery Pipeline

Email intake → classification → task routing → drafting → **human review queue**.

The review queue is the enforcement point for the GOAL.md guardrail: nothing
client-facing is sent, and no certificate is issued, without explicit human
approval. The state machine forbids `pending → sent`.

```
mailbox text ──> intake.classify (claude-opus-4-8, structured output)
                    │
                    ├── coi_request ──────> drafters.COI work packet ─┐
                    ├── renewal ──────────> drafters.renewal outreach ─┤
                    ├── (confidence < 0.6,                             ├──> ReviewQueue (SQLite)
                    │    client questions,                             │       pending → approved → sent
                    │    carrier docs) ───> human triage item ────────┘       pending → rejected
                    └── spam ─────────────> ignored
```

## Layout

| Module | Purpose |
|---|---|
| `backbinder/models.py` | Pydantic schemas + routing table (`route()` demotes low confidence to humans) |
| `backbinder/llm.py` | LLM interface; `AnthropicLLM` (adaptive thinking, cached system prompts) and `FakeLLM` for tests |
| `backbinder/intake.py` | Email classifier (frozen system prompt; volatile content in the user turn) |
| `backbinder/drafters.py` | COI packet / renewal outreach / cross-sell drafters — E&O wall lives in these prompts |
| `backbinder/review.py` | SQLite review queue with an enforced approval state machine |
| `backbinder/process.py` | One-email end-to-end orchestration |
| `backbinder/nowcerts.py` | NowCerts/Momentum API client skeleton (verify against sandbox) |
| `backbinder/cli.py` | Operator CLI: `process`, `queue`, `show`, `approve`, `reject`, `stats` |

## Run

```bash
pip install -e ".[dev]"
pytest                      # offline — FakeLLM, no API key needed

export ANTHROPIC_API_KEY=...
printf 'From: client@x.com\nSubject: need a COI\nLandlord needs cert by Fri.' \
  | python -m backbinder.cli process
python -m backbinder.cli queue
python -m backbinder.cli approve <id> --who cory
```

## Not built yet (deliberately)

- Mailbox poller (IMAP/Graph) — needs the real delegated mailbox from client #1
- NowCerts write path (certificate prep into the AMS) — needs sandbox credentials
- Renewal scheduler (90/60/30 cron) — needs real policy data
- Sending — by design, sending stays a human action until trust is earned per task type
