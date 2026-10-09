# P46 - ArmorIQ Flow State - draft

Prepared 2026-10-01 by Codex (GPT-6 Luna) for Jaron K. Bragg. Updated 2026-10-09. Not registered or submitted. The official event now links to a Luma page with host approval; no registration was requested. Do not accept ArmorIQ service terms or connect its SDK until Jaron answers the question in `NEEDS-JARON.md` and the event rules are available.

## Opportunity

- **What it funds:** an online AI-agent hackathon about giving agents tools while proving their action limits work.
- **Prize:** the current official event page lists a $1,000 cash grand prize. It does not promise an award to entrants. Partner awards may be added but are not counted here. The older $500 figure in this draft was incorrect.
- **Dates:** build week is October 10-17, 2026; submissions close October 17; results are October 22. The event page says exact deadline hours are in the official rules, but those rules and the promised itemized submission spec were not visible on October 9.
- **How to enter:** the official ArmorIQ page links to Luma. Luma says registration is subject to host approval. No registration was requested.
- **Fit:** Zeus AI Workbench is a public MIT-licensed local desktop AI workbench with desktop tools and action records. A narrow demo that shows a useful agent action being allowed and an out-of-scope action being blocked fits the challenge. Zeus does not currently integrate ArmorIQ, and no security-control result is claimed.
- **Effort:** about 120-180 AI minutes for a small demo using synthetic data, plus the event week and time to read the final rules.

## Proposed entry

### Project name

Zeus Scoped Research Agent

### What I plan to build

I plan to make a small agent that reads a prepared set of public or synthetic project notes and returns a source-linked answer. The demo would show an allowed read inside a test folder, then try a read or action outside the declared scope and show that ArmorIQ blocks or holds it before it runs. The report would show the action and why it was allowed or stopped.

The test would use no private files, account credentials, real customer data, wallet connections, trades, email, or live writes. This is a proposed hackathon experiment. Zeus is not currently connected to ArmorIQ, and this demo has not been built.

### What problem does it address?

An agent with desktop or file tools can do useful work, but a clear record after the fact does not by itself prevent an action that was never intended. This demo would test whether a declared boundary can stop one such action before execution and make that result visible. The test is a proposal; it has no measured result or outside users yet.

### Who is building it?

Jaron K. Bragg is the solo human builder. Zeus AI Workbench is public under the MIT License. AI tools help with research and software work. This application draft was prepared by Codex (GPT-6 Luna) for Jaron.

### Deliverable

A reproducible demo, a short video, and a public account of the allowed action, the denied or held action, what failed, and the test limits. The plan is to publish the new work in the MIT-licensed Zeus repository, after checking the rules and integration terms.

## Terms and submission limits

ArmorIQ's public Services Terms require users to be at least 18, indemnify ArmorIQ for claims tied to use, breach of the terms, or violations of law or third-party rights, and resolve disputes in courts where ArmorIQ is headquartered. Its privacy policy says ArmorClaude and ArmorCodex can send prompts or intent plans, tool-call details, audit logs, execution traces, and environment metadata to ArmorIQ; the listed product data is retained for 12 months. The exact flow for any SDK used in this hackathon is not established by the event page. The $1,000 grand prize does not by itself justify accepting terms or sending project data to a service. No account, key, terms, or event rules have been accepted.

## 2026-10-09 update

The official page now lists the $1,000 prize and confirms the online build week. The Luma entry requires host approval. The event page still says that exact submission requirements and rules are available separately, but the published page did not expose them on this check. A narrow demo using only synthetic or public data remains possible, but eligibility, service terms, and the missing rules block registration and SDK use.

## Sources

- Official event page, prize, schedule, challenge and sign-up link: https://armoriq.ai/hackathons/flow-state
- ArmorIQ Services Terms: https://armoriq.ai/terms-of-service
- ArmorIQ Privacy Policy: https://armoriq.ai/privacy-policy
- Linked event page, which did not finish loading in this run: https://hackbriven.com/event/flow-state
- Zeus AI Workbench and MIT license: https://github.com/JaronKBragg7337/zeus-ai
