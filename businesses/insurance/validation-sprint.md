# Validation Sprint: Independent Insurance Agencies

*Goal: within 1–2 weeks, confirm or kill the insurance-agency vertical before
building anything. Budget: ~$0. Kill criteria at the bottom. Outputs double
as the newsletter's first data asset and the service's first sales evidence.*

Decision per `research/vertical-selection.md`: insurance agencies confirmed
as the Phase 1 vertical (service + newsletter).

---

## Track 1: Secret-shopper study (the data asset)

Replicates the Clio Legal Trends methodology that exposed law-firm intake
failure — for small independent insurance agencies. The published result
becomes the newsletter's launch lead magnet ("We contacted 50 independent
agencies as a customer. Here's what happened.") and the service's opening
sales statistic.

**Design**
- Sample: 50 independent agencies across 8–10 states, sub-$1.25M profile
  (5 or fewer staff per website/LinkedIn), drawn from state Big "I" member
  directories and Google Maps. Exclude captive agents (State Farm, Allstate)
  — different economics.
- Persona A (30 agencies, new-business): small-business owner requesting a
  BOP/GL quote via the agency's website form or email.
- Persona B (20 agencies, service): existing-customer-style COI request
  framed as a prospective question ("how fast could you issue a certificate
  if we moved our coverage to you?").
- Measure: time-to-first-response (form, email), response channel, number of
  follow-up touches over 14 days, whether anyone ever called, quality of the
  response (personalized vs template), after-hours handling.
- Hypotheses to test (from the research, all currently vendor-sourced):
  H1: median first response > 8 business hours. H2: ≥30% never respond.
  H3: ≤20% follow up more than once. If these fail — agencies respond fast
  and persistently — the speed-to-lead pitch dies and the offer reweights
  toward back-office (COI/renewal) work.

**Ethics/legal guardrails**
- No fake commitments: inquiries are framed as genuine shopping (and any
  agency that responds well gets a polite "we went another direction" close).
- No recording of calls without consent; we log timestamps and channel only.
- Findings published in aggregate; no agency named negatively.

**Execution note**
- AI agents can draft every inquiry and log every response, but each outbound
  message is an external action: **batch-reviewed and approved by Cory/Austin
  before sending** per GOAL.md guardrails. Estimated human time: ~2 hours of
  review across the sprint.

## Track 2: Five operator conversations

**Recruiting sources** (refined by the GTM research in progress): agency-owner
Facebook groups, r/InsurancePros, state Big "I" chapter directories, LinkedIn.
Offer: 20 minutes, we share the secret-shopper benchmark data with them first.

**Interview guide (20 min)**
1. Walk me through yesterday: what ate your CSR's/your time? (listen for:
   COIs, renewals, carrier portals, data re-entry)
2. Do you use or have you used a VA or outsourcing firm (Cover Desk, Patra,
   etc.)? What do you pay? What do they do badly?
3. Renewals: what's your process 90 days out? Who chases what? What slips?
4. Cross-sell: do you run any systematic campaign against your book? Why not?
5. If a service guaranteed every COI out in under 10 minutes and every
   renewal touched at 90/60/30 days, what would that be worth monthly?
   (anchor test: react to $1,500)
6. What would make you NOT trust an outside vendor in your AMS? (E&O, data,
   carrier rules — capture objection language verbatim)
7. What do you read/listen to for the business? (validates newsletter
   channel assumptions)

**What we're listening for**
- Does the $1,400–2,600/mo VA line item actually exist at the sub-$1.25M
  tier, or only at $2M+?
- Is COI volume meaningful for small commercial books, or concentrated in
  construction-heavy agencies (which would sharpen targeting)?
- Verbatim pain language for landing-page copy.

## Track 3: Technical feasibility (in progress — research agent)

AMS integration access (HawkSoft / EZLynx / NowCerts partner APIs vs.
login-based VA-model access), COI workflow mechanics, and what existing
insurance VA firms do. Results land in `research/streams/10-ams-feasibility.md`.

## Kill criteria (from vertical-selection.md, made testable)

| # | Signal | Threshold | Action if failed |
|---|---|---|---|
| K1 | Willingness to pay | <3 of 5 operators react positively to $1,500/mo (or all anchor below $1,000) | Drop to vertical #2 (restoration), re-run sprint |
| K2 | AMS access | All major small-tier AMS closed to third parties AND login-based access violates ToS | Same |
| K3 | Pain validation | Secret-shopper shows fast, persistent responses (H1–H3 all fail) AND operators rank back-office pain low | Same |
| K4 | Reachability | Cannot book 5 operator conversations within 2 weeks of trying | Treat as a serious GTM warning; reassess channel plan before proceeding |

## Sprint outputs
1. `secret-shopper-results.md` + dataset (becomes newsletter issue #1 / lead magnet)
2. Five interview summaries with verbatim quotes
3. AMS feasibility verdict
4. Go/no-go memo updating this file
