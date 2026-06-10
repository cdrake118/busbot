# Phase 1 Launch Plan: AI Back-Office for Independent Insurance Agencies

*Synthesizes: vertical selection (`research/vertical-selection.md`), AMS
feasibility (`research/streams/10`), and GTM intelligence (`research/streams/11`).
Status: draft pending validation-sprint results (`validation-sprint.md`).
Working names below are placeholders until naming/domain check.*

---

## 1. The two-motion structure

- **Motion A (cash engine): productized back-office service** for independent
  agencies under ~$1.25M revenue. Target: 6–8 clients by month 9 ≈
  $100k+ annual run rate.
- **Motion B (compounding asset): the operator newsletter** for Main Street
  agency owners. Target: 3–5k verified owner subscribers by month 9;
  sponsorship revenue from ~Q4; permanent lead source for Motion A.

One vertical, one audience, two revenue lines.

## 2. Service offer (Motion A)

**Positioning:** *"Your agency's back office, run for you — same-day COIs,
every renewal chased at 90/60/30, your book cross-sold — for less than one
VA, with no one to manage."*

Sell outcomes, never "AI" (only 17% of agents trust AI; 51% are overwhelmed
by workload — the buyer wants relief, not technology). The AI is the margin
story, not the marketing story.

**Scope (fixed, productized):**
1. **COI desk** — email-parsed intake of certificate requests, ACORD 25
   prepped and queued in the AMS; *agency licensee reviews and issues*
   (ACORD compliance by design). SLA: prepped within 2 business hours.
2. **Renewal engine** — every policy touched at 90/60/30 days: remarketing
   checklist, client outreach drafts in the agency's voice, carrier document
   chasing.
3. **Cross-sell campaigns** — monthly campaign against the book (personal
   lines gap on commercial clients and vice versa), drafted for agency
   approval.
4. **Review & referral ops** — post-service Google review requests, referral
   nurture.
5. **Monthly ops report** — COI turnaround, renewal touch rate,
   campaign results. (Doubles as newsletter benchmark data, anonymized and
   with client consent.)

**Explicitly out of scope (E&O wall):** no coverage advice, no quoting
decisions, no binding, nothing client-facing without agency approval paths.
Written QA process and a one-page "our E&O posture" doc as sales collateral —
the #1 and #2 objections (inaccurate outputs 22%, data privacy 24%) get
answered before they're asked.

**Pricing:**
- **Founding clients (first 3–5): $1,000/mo**, month-to-month, in exchange
  for case-study rights and a testimonial. Raise to standard after.
- **Standard: $1,500/mo** (agencies to ~$600k revenue) / **$2,500/mo**
  (to ~$1.25M, higher COI volume). No setup fee at launch (remove friction);
  add one later.
- Anchors: a managed dedicated VA runs $2,000–4,500/mo plus management
  overhead; a part-time US CSR ~$3,500/mo true cost. We price below both.

**Delivery stack (MVP — built in this repo):**
- Access model per AMS feasibility verdict: **delegated shared mailbox +
  agency-issued AMS login** (works on 100% of AMS; matches Cover Desk/Patra
  buyer expectations). Email parsing is the intake engine.
- Agent pipeline: intake classifier → task router → drafting agents (COI
  prep, renewal outreach, cross-sell copy) → **human review queue** (Cory/
  Austin approve; later, trusted-task auto-approve) → AMS execution →
  logging/reporting.
- First native API integration: **NowCerts/Momentum** (open API, existing
  n8n nodes); steer greenfield clients there. HawkSoft Partner API (~$3k/yr)
  once ~4 clients use it. EZLynx shops served login-only.
- Per-client capacity target: ≤2 human hours/week by month 3 of a client's
  life. At 8 clients that's ~16 hrs/week of review work across both
  operators — within the 25–35 hr/week budget alongside the newsletter.

## 3. Newsletter (Motion B)

**Positioning (validated gap):** every email an agency owner gets is a news
wire, an association organ, a carrier content program, or a consultant
funnel. **We write the operator's letter**: benchmarks, staffing math, ops
teardowns for sub-$2M agencies — independent voice, no carrier or consulting
agenda.

**Launch asset:** the secret-shopper study (validation sprint Track 1) —
"We shopped 50 independent agencies. Median time to a quote response: ___."
Publish as issue #1 + downloadable report; pitch trade press (Agency
Checklists, Insurance Journal cover this category of study).

**Cadence & format:** weekly, 5-minute read: one benchmark or teardown,
one tool/workflow note, three curated links with operator takes. Written by
AI agents from research + our service-delivery data; edited and voiced by
Cory/Austin; every issue human-approved before send.

**Growth plan:**
- Months 1–3: IAOA/FB group presence, podcast guesting (each appearance
  plugs the newsletter, not the service), the secret-shopper report as lead
  magnet, cross-promo with adjacent newsletters.
- Months 3–9: paid acquisition test per GOAL.md ad policy — beehiiv
  Boosts/Meta ads at target ≤$4/verified-owner subscriber; scale only if
  engaged-open economics support $300–500/send sponsorship math.
- Sponsor outreach from ~3k subs: 12 proven sponsor categories documented in
  `research/streams/11-insurance-gtm.md` (insurtechs, AMS vendors,
  premium finance, E&O programs, networks...). Anchor $300–500/send.

## 4. First-10-clients channel sequence (from GTM research)

| Phase | Channel | Goal | Cost |
|---|---|---|---|
| Weeks 1–8 | IAOA Facebook group: 30 days of pure usefulness, then workflow teardown posts | 3 founding clients | $0 |
| Weeks 2–16 | Podcast guesting (Agency Freedom, Insurance Guys, Insurance Dudes, Agency Intelligence network) — hook: "what AI actually does in a 4-person agency, with the E&O guardrails" | 3 clients | $0 |
| Ongoing | Referral loop: 1 month free per signed referral | 2–3 clients | margin |
| Month 3–6 | One state Big "I"/PIA convention in a hard-market state (FL/TX/LA/CA) | 1–2 clients | ~$1–4k |
| Year 1 | BrainShare or IAOA Innovation — attend, host a dinner | pipeline | ~$1–2k |
| Deferred | AMS marketplaces, SIAA/Smart Choice, cold email | — | — |

## 5. 90-day milestones

| Day | Milestone |
|---|---|
| 1–10 | Validation sprint executes (secret-shopper sends approved by Cory/Austin; interviews booked). Naming + domain + entity decision. |
| 10–21 | Go/no-go on kill criteria. If go: landing page live (service + newsletter capture), secret-shopper report drafted. |
| 21–35 | Newsletter issue #1 (the study) ships. IAOA presence active. First 2 podcast pitches out. Delivery pipeline MVP working against a NowCerts sandbox. |
| 35–60 | First founding client onboarded; delivery pipeline hardened on real volume. Issues #2–5 ship. |
| 60–90 | 3 founding clients; first case study; standard pricing listed; subscriber count target 500–1,000. |

## 6. Human vs. agent division of labor

**Agents (Claude, this repo):** research, all drafting (COI prep, renewal
sequences, campaigns, newsletter issues, social posts, podcast pitches),
pipeline code, logging/reporting, secret-shopper logistics and analysis.

**Cory & Austin (the irreplaceable 20%):** approve every external send;
sales conversations and discovery calls; podcast appearances; client
relationships; final newsletter voice; entity/banking/E&O insurance for the
business itself (get a quote — we're advising on insurance workflows, and
our own E&O posture is sales collateral).

## 7. Budget (startup costs)

| Item | Cost |
|---|---|
| Domain(s), landing page hosting | ~$50 |
| Google Workspace / M365 | ~$15/mo |
| beehiiv (scale tier when needed) | $0–$99/mo |
| n8n self-hosted + LLM API costs | ~$50–150/mo at first clients |
| E&O/professional liability quote for us | TBD (get quotes — likely $1–3k/yr) |
| State association + convention (month 3+) | ~$1–4k once |
| **Total to first revenue** | **well under $500 + the E&O policy** |

## 8. Open items requiring Cory/Austin

1. Approve secret-shopper outreach batches (validation sprint, Track 1).
2. Naming: shortlist + domain availability run next; final pick is yours.
3. Entity formation + business banking (when validation passes).
4. E&O insurance quotes for the service business.
5. Which of you fronts the newsletter/podcast voice (it needs one named
   human face; "AI-run" is the backend story, not the brand).
