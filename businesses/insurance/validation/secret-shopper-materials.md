# Secret-Shopper Study: Outreach Materials & Protocol

*Status: DRAFT — nothing sends until Cory/Austin approve the templates, the
persona identity, and each batch. Target list is being compiled separately
(`target-list.md` when it lands). Study design: `../validation-sprint.md`.*

## Persona identity (needs a decision)

The inquiries must come from a plausible small business. Options, best first:

1. **A real business one of you actually has** (any LLC, side business, or
   consulting entity) — inquiries are then genuine comparison-shopping, which
   is the cleanest ethical footing. We are, in fact, going to need business
   insurance for the new venture — **we can shop our own real BOP/GL need.**
2. A "forming an LLC, shopping ahead of launch" framing — honest ("we're
   setting up a small consulting business and comparing agencies").
3. A fictional business — **not recommended**; weaker ethics, and a sharp CSR
   can spot it.

Recommendation: **Option 1/2 hybrid** — we genuinely need GL/E&O for the new
company. The study doubles as actual insurance shopping. Persona details to
fill in on approval: business name, state of formation, contact email
(dedicated study mailbox, e.g., a Google Workspace alias), and a
voicemail-capable phone number (Google Voice or similar — needs a ~$0 setup
you'll have to do, since agencies WILL call and we want to log it without
answering live).

## Infrastructure checklist (before batch 1)

- [ ] Dedicated mailbox: `quotes@<persona-domain>` or a plain Gmail
- [ ] Voicemail-only phone number (Google Voice); greeting: business name,
      "please email us at..."
- [ ] Logging sheet created from the schema below
- [ ] Personas approved by Cory/Austin
- [ ] Batch 1 (first 10 agencies) messages reviewed and approved

## Persona A — commercial quote request (30 agencies)

Submitted via the agency's website quote form, or email where no form exists.
Vary the wording per batch (agents will generate variants; below is the
master). Keep every factual claim true for the real persona business.

> **Subject (if email):** BOP/GL quote for a small {{industry}} business
>
> Hi — I run a small {{industry}} business in {{city, state}} ({{N}}
> people). I'm comparing options for general liability and a BOP ahead of
> {{our launch / our renewal in about 60 days}}. Could you let me know what
> you'd need from me to put together a quote, and roughly what your process
> looks like?
>
> Best,
> {{first name}}
> {{business name}} · {{phone}} · {{email}}

**What we measure** (clock starts at submission):
time-to-first-response by channel; whether the first response is personalized
or templated; number of follow-up touches over 14 days; whether they ever
call; whether anyone asks a qualifying question vs. sends a generic form.

## Persona B — COI-speed question (20 agencies)

Framed as a prospective-customer service question — the COI pain probe.

> **Subject:** Question about certificate turnaround
>
> Hi — quick question as we evaluate agencies for our {{industry}} business.
> Our {{landlord / clients}} regularly require certificates of insurance,
> sometimes same-day. If we placed our coverage through you, what's your
> typical turnaround on a COI request, and how do we submit them — email,
> portal, or a call?
>
> Thanks,
> {{first name}}, {{business name}}

**What we measure:** response time; the claimed COI turnaround (this number
is gold — it becomes the benchmark headline); whether they have a portal/
self-serve answer or "just email Susan."

## Follow-up & closure protocol

- We do not chase. One inquiry per agency; passive logging for 14 days.
- Any agency that responds with a quote process gets a polite close within
  the window: *"Thank you — we've decided to go another direction for now.
  Appreciate the quick response."* (Send to all responders; non-responders
  get nothing.)
- If an agency calls and leaves voicemail: log it; respond by email with
  either a real next step (if we're genuinely shopping them for our own
  coverage) or the polite close.
- Hard rule: no fabricated commitments, no wasted appointment slots — we
  decline any offered meeting unless it's genuine shopping for our own
  policy.

## Logging schema (`secret-shopper-log.csv`)

```
agency_id, agency_name, city, state, persona, channel_submitted,
submitted_at, first_response_at, first_response_channel,
first_response_type (personalized|template|auto-ack|none),
followup_touches_14d, ever_called (y/n), coi_turnaround_claimed,
qualifying_questions_asked (y/n), notes
```

Derived metrics for the report: median/p90 time-to-first-response;
% no-response at 14 days; % with >1 follow-up; % that called;
distribution of claimed COI turnaround; hard-market states vs others.

## Batching & approval flow

- Batch size 10; batches at least 2 business days apart (so a publicity
  fluke or holiday doesn't skew a whole batch).
- Each batch: agents prepare the 10 filled templates → Cory/Austin review →
  approve → agents submit forms/send emails the same day → log.
- Total human review time estimate: ~20 min/batch × 5 batches.

## Interview recruitment drafts (Track 2 — also need approval)

**IAOA / Facebook group post** (after we've been usefully active ~2 weeks):

> Doing some research on how independent agencies handle the back-office
> grind — COIs, renewal remarketing, the stuff that eats CSR time. We
> secret-shopped 50 agencies' response times and the data is wild. Happy to
> share the full benchmark with anyone who'll trade 20 minutes telling me
> how your shop actually handles renewals/certs. DM me. (Not selling
> anything in the call — genuinely mapping workflows.)

**Direct message / LinkedIn variant:**

> Hi {{name}} — I'm researching back-office workflows at independent
> agencies (COI turnaround, renewal remarketing load). We ran a 50-agency
> response-time study and I'll share the full results with you either way —
> would you trade 20 minutes on how {{agency}} handles it? Not a sales
> call; I'm validating whether a problem I think exists actually does.

**Honesty note:** if asked "are you building something?" the answer is yes —
*"exploring a done-for-you back-office service; that's why I want to know if
the pain is real before building it."* Transparency converts better in this
market anyway (trust data in `research/streams/11`).
