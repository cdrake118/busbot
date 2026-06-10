# Stream 10: AMS Integration Feasibility for a Third-Party AI-Ops Vendor (Kill-Criterion K2)

*19 search/fetch operations across vendor terms pages, docs, and practitioner sources. Verdict: kill criterion NOT triggered.*

## 1. AMS distribution among sub-$1.25M agencies

Per Catalyit / Big "I" **2024 State of Tech** survey data: HawkSoft ~11% of independent agencies (4.4/5 satisfaction), EZLynx ~10% overall but **~19% in lower revenue brackets**; HawkSoft runs 7% (<$500K) to 12% ($1–3M). Applied Epic and AMS360 dominate only at larger tiers ([Catalyit State of Tech](https://catalyit.com/state-of-tech), [2024 report PDF](https://www.iabforme.com/wp-content/uploads/2024/09/2024-State-of-Tech-Report.pdf)). The small-agency tier is fragmented across EZLynx, HawkSoft, NowCerts/Momentum, QQCatalyst, Jenesis, plus CRM layers (AgencyZoom, Better Agency). **Confidence: medium** (figures from search extraction of the official report).

Pricing tiers: HawkSoft ~$250/mo base + ~$94/user ([HawkSoft pricing guide](https://blog.hawksoft.com/guide-to-ams-pricing)); EZLynx from ~$350/mo, quote-based ([Capterra](https://www.capterra.com/p/102928/EZLynx/)); Momentum AMP (NowCerts) from **$169/mo + $45/seat**, $900 onboarding ([momentumamp.com/pricing](https://momentumamp.com/pricing)). Practitioners recommend HawkSoft or NowCerts for small agencies ([QuoteSweep AMS comparison 2026](https://www.quotesweep.com/blog/ams-comparison-2026)). **Confidence: high.**

## 2. API access per AMS

| AMS | API for 3rd parties? | Gate / cost | Confidence |
|---|---|---|---|
| **NowCerts / Momentum AMP** | **Yes — genuinely open.** Public REST API at api.nowcerts.com; any agency account with the "API Integration" agent role gets credentials; public Postman collection; community n8n nodes exist | No partner approval; works via the *agency's own account* | **High** — [support article](https://support.momentumamp.com/support/solutions/articles/156000373566-using-the-momentum-ams-rest-api), [api.nowcerts.com](https://api.nowcerts.com/), [n8n node](https://github.com/ReduceMyIns/n8n-nodes-momentum) |
| **HawkSoft** | Yes — Partner API v3.0 (2-way read/write), partner-gated | Apply via opportunities@hawksoft.com; Letter of Agreement + agency consent; **$3,000/yr API fee (waivable in writing)** + **$2,400/yr Marketplace placement**; closed to AMS competitors | **Medium-high** — [partner.hawksoft.app](https://partner.hawksoft.app/), [API terms](https://www.hawksoft.com/terms/api/), [Marketplace terms](https://www.hawksoft.com/terms/marketplace/) |
| **EZLynx (Applied)** | API exists but marketed as "EZLynx for Enterprise"; vendor channel is EZLynx Connect (~114 partners), contact-based, no self-serve signup, no published pricing | Effectively gated | **Medium** — [EZLynx API solutions](https://www.ezlynx.com/products/ezlynx-api-solutions/), [EZLynx Connect](https://www.ezlynx.com/connect.html) |
| **QQ Catalyst (Vertafore)** | Documented public API: register as API partner, OAuth2, sandbox, 60 req/min | Lightweight registration; docs date to QQ Solutions era — Vertafore responsiveness unverified | **Medium** — [api.qqcatalyst.com](https://api.qqcatalyst.com/), [GitHub](https://github.com/QQSolutions/QQCatalystAPI) |
| **AgencyZoom (Vertafore)** | Yes — public OpenAPI docs + Zapier | Low friction | **Medium-high** — [app.agencyzoom.com/openapi](https://app.agencyzoom.com/openapi/) |
| **Jenesis** | No open API; Zapier-based (JenesisLink) | Zapier only | **Medium-high** — [Jenesis integrations](https://www.jenesissoftware.com/2025/06/unlocking-the-power-of-integrations-with-your-agency-management-system/) |
| **Better Agency** | Acquired by GloveBox (Dec 2024); in transition — risky to build against | — | **Medium** — [Tracxn](https://tracxn.com/d/companies/better-agency/__aMq82jgwj7rtg7ceytBRsw8xQ1SG9uoV7mWCx329phc) |

## 3. Workaround viability if APIs are gated

Standard, established practice — not fringe:
- **Zapier/Make/n8n** routinely bridge AMS, email, and CRMs; NowCerts ships Zapier/Gmail/Twilio natively ([Activepieces roundup](https://www.activepieces.com/blog/top-insurance-workflow-automation-tools)).
- **RPA on user logins is a venture-funded business model**: Quandri ($8.5M Series A) runs bots inside broker management systems and carrier portals for renewal reviews, requoting, document chasing ([Quandri](https://www.quandri.io/), [TechCrunch](https://techcrunch.com/2023/06/28/quandri-raises-8-5m-series-a-to-bring-process-automation-to-insurance-brokers-and-agencies/)). BPOs advertise "system-native execution" inside AMS360/Epic with no API ([Selectsys](https://www.selectsys.com/blog/best-insurance-bpo-providers-2025-comparison)).
- **ToS risk**: no public AMS-vendor ToS clause prohibiting agency-authorized login automation was found. The real restriction is on the **carrier portal** side — some carriers restrict offshore/non-employee access and MFA forces human-in-the-loop coordination ([VA Picker guide](https://vapicker.com/blog/best-virtual-assistant-companies-for-insurance-agents)). **Confidence: medium** (absence of evidence — flag for per-AMS legal review).

## 4. COI handling

- Named COI trackers skew enterprise: **myCOI requires ~200+ incoming certificates minimum** ([Certificial comparison](https://www.certificial.com/blog-post/best-mycoi-alternatives-2026)); TrustLayer is compliance-team oriented; Certificate Hero targets brokers (Brown & Brown deal) with Epic/AMS360/Sagitta integration ([PR Newswire](https://www.prnewswire.com/news-releases/certificate-hero-selected-by-brown--brown-to-streamline-certificate-issuance-302483916.html)). **The sub-$1.25M agency COI niche is underserved.**
- Technical workflow: COIs are ACORD 25 forms generated from the AMS certificate module prefilled with policy data; NowCerts has built-in self-serve certificate issuance and a Jan 2025 Certificial partnership ([NowCerts](https://www.nowcerts.com/features/self-serve-certificates), [BusinessWire](https://www.businesswire.com/news/home/20250128270839/en/)).
- **Compliance constraints (real but manageable)**: ACORD forms require an end-user license held by the *agency* (free for Big "I" members since Dec 2025); vendors cannot sublicense ACORD forms; ACORD 25s must be issued under a **licensed agent/broker's authority** — the service preps/automates, the agency licensee issues ([ACORD FAQ](https://www.acord.org/forms-pages/acord-forms/forms-faq), [ACORD-Big I news](https://www.acord.org/ACORD-about/acord-news/2025/12/04/acord-license-available-for-big-i-members), [acord25.com](https://acord25.com/who-can-sign-an-acord-25-certificate/)). **Confidence: high.**

## 5. Insurance VA/outsourcing incumbents

- **Cover Desk**: 1,500+ Philippines/Mexico VAs, 600+ agencies, official Vertafore partner; market all-in cost ~$1,500–3,000/VA/mo ([coverdesk.com](https://coverdesk.com/), [Vertafore partner page](https://www.vertafore.com/cover-desk), [Sonant cost guide](https://www.sonant.ai/blog/insurance-virtual-assistant-cost)). Budget shops ~$8/hr ([VirtualNexgen](https://virtualnexgen.com/blog/insurance-virtual-assistant-portal-fatigue)).
- **Patra / ResourcePro**: per-seat/FTE billing, work performed *inside client systems* with client logins ([Patra VA](https://www.patracorp.com/services/virtual-assistant/)). **WAHVE**: US-based retiree staffing, 12.5–15% placement fee ([wahve.com](https://wahve.com/)).
- **Access model = client-provided AMS user logins + mailbox + carrier portal credentials**, governed by NDAs, least-privilege, MFA relay workarounds. AI use is nascent marketing-layer, not deep automation. **Confidence: medium-high.**

## 6. Mailbox + AMS login model

Small agencies live in Outlook/Gmail + AMS; the entire VA industry (thousands of seats) operates on mailbox + login access with no API. COI requests, carrier docs, and renewal notices all arrive by email — the mailbox is the natural intake surface. Caveats: carrier-portal access restrictions, MFA coordination, E&O coverage review for delegated work. **Confidence: high.**

## Verdict

**(a) Feasibility: YES — kill criterion K2 NOT triggered.** NowCerts/Momentum is fully open; HawkSoft open to small vendors for ~$3,000–5,400/yr; QQ Catalyst and AgencyZoom have documented APIs. Only EZLynx (enterprise-gated) and Jenesis (Zapier-only) lack accessible APIs — both reachable via the login/mailbox model that incumbent VA firms and funded RPA startups already use at scale.

**(b) Recommended MVP access model: hybrid "VA-model + selective API."**
1. **Universal baseline**: delegated mailbox access (M365/Google Workspace shared mailbox) + agency-issued AMS user login — works on 100% of AMS, zero partner approval, matches buyer expectations set by Cover Desk/Patra.
2. **Email parsing as the intake engine** for COI requests, carrier docs, renewal notices.
3. **First native API: NowCerts/Momentum** (open, documented, includes certificate workflows; n8n nodes exist) — consider steering greenfield clients there. **Second: HawkSoft** once revenue justifies ~$3K/yr. Defer EZLynx API; serve EZLynx shops via login model.

**(c) Showstoppers: none fatal. Watch items:**
- ACORD licensing: agency holds the license; licensed person stands behind issued ACORD 25s — structure as "prep and queue, agency issues/approves."
- Carrier portals (not AMS) are the ToS choke point; MFA requires human-in-the-loop design.
- EZLynx gating means the largest single small-agency segment (~19% in low revenue brackets) is login-model-only initially.
- Get written agency authorization and review each AMS EULA before deploying browser automation.
- Don't build against Better Agency (post-acquisition flux).
