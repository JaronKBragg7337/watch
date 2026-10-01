# P46 - ArmorIQ Flow State - draft

Prepared 2026-10-01 by Codex (GPT-6 Luna) for Jaron K. Bragg. Not registered or submitted. The linked Hackbriven page stayed on “Loading event.” Do not accept ArmorIQ service terms or connect its SDK until Jaron answers the question in `NEEDS-JARON.md` and the event rules are available.

## Opportunity

- **What it funds:** an online AI-agent hackathon about giving agents tools while proving their action limits work.
- **Prize:** the official event page lists $500 cash for the grand-prize winner. It does not promise an award to entrants. Partner awards may be added but are not counted here.
- **Dates:** registration is listed to open October 1, 2026. Build week is October 10-17; submissions close October 17; results are October 22. The exact deadline time and full submission requirements were not published on the page checked.
- **How to enter:** the official ArmorIQ page links to a Hackbriven event page. That page displayed “Loading event” and exposed no form in this run.
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

ArmorIQ's public Services Terms require users to indemnify ArmorIQ for claims tied to use, breach of the terms, or violations of law or third-party rights. Its privacy policy says some agent tools send inputs, tool calls, results, audit logs, and execution traces to ArmorIQ, with 12-month retention for the listed product data. The exact data flow for the SDK needed by this hackathon is not established by the event page. The announced $500 grand prize does not by itself justify accepting terms or sending project data to a service. No account, key, terms, or event rules have been accepted.

## Sources

- Official event page, prize, schedule, challenge and sign-up link: https://armoriq.ai/hackathons/flow-state
- ArmorIQ Services Terms: https://armoriq.ai/terms-of-service
- ArmorIQ Privacy Policy: https://armoriq.ai/privacy-policy
- Linked event page, which did not finish loading in this run: https://hackbriven.com/event/flow-state
- Zeus AI Workbench and MIT license: https://github.com/JaronKBragg7337/zeus-ai
