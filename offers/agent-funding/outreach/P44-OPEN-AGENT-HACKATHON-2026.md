# P44 - Open Agent Hackathon 2026 - registration draft

Prepared 2026-10-01 and rechecked 2026-10-10 by Codex (GPT-6 Luna) for Jaron K. Bragg. Not submitted. Registration closes Oct 13, 2026 at 00:00 UTC (Oct 12 at 8 p.m. EDT). Registration requires a GenAI Academy sign-in; no account or event registration was created in this lane. Confirm the 16+ eligibility answer in `NEEDS-JARON.md` before registering.

## Opportunity

- **What it funds:** an online build contest for production-oriented AI agents. The page lists up to $20,000 in prizes: $8,000 for first, $4,000 for runner-up, $2,000 for third, plus bonus points. Awards are not guaranteed.
- **Who can enter:** worldwide; solo or teams of up to five; age 16 or older at the start of the build.
- **Cost:** free entry.
- **Dates:** registration closes October 13, 2026 at 00:00 UTC (October 12 at 8 p.m. EDT). Workshops are October 7, 8, and 12; onboarding is October 14; build window is October 15-20; submissions close October 20 at 23:45 UTC. Results are listed for October 30.
- **How to register:** open the course page and choose “Register now” using a GenAI Academy account. No payment or subscription is stated on the current event page.
- **Effort:** about 180-300 AI minutes to build, check, document, and demo a small project. The event runs across six calendar days.
- **Fit:** Zeus AI Workbench is an existing public MIT-licensed desktop app using Ollama, local document search, local memory, desktop tools, and action records. This contest asks for an agent that connects information, reasons across steps, keeps context, and produces a useful result. No outside Zeus users or customer demand are documented. The proposed entry is a new experiment based on Zeus, not an existing product or customer result.

## Draft entry

### Project name

Evidence Desk: a local agent that shows where its answers came from

### What I plan to build

I plan to extend Zeus AI Workbench into a small agent for project research. It will read a folder of public or synthetic documents, answer a multi-step question with links and quoted evidence, keep a short task history, and save a report in a separate output folder. Its source documents will stay read-only. The demo will show both supported answers and cases where the documents do not support an answer.

This is planned work, not a feature I claim is finished. The existing Zeus app already has local document search, local memory, desktop tools, and action records. The from-scratch model-training path is experimental and is not part of this entry.

### What problem does it address?

When I work across project records, I have to find the original source for a fact and remember what the source does not establish. Evidence Desk would help a builder inspect a small project archive and see the sources behind each answer. This is a problem from my own workflow. I have not tested demand with outside users.

### Who is building it?

Jaron K. Bragg is the solo human builder. AI tools help with research and software work. This draft was prepared by Codex (GPT-6 Luna) for Jaron. The public Zeus repository is the evidence for the current code; the proposed Evidence Desk improvements have not been built.

### How will I check it?

I plan to prepare a small set of public or synthetic documents and questions with known answers. I will check whether each answer cites the right source, whether unsupported questions are marked as unknown, and whether the task log shows what the agent actually did. I will publish the test questions, results, and failures with the demo. The test has not been run yet.

### Tools and license

I plan to use the existing MIT-licensed Zeus repository. The event lists the Zetaris data layer, NVIDIA token layer, and Meterless orchestration as sponsor tools. I would check their availability and terms first and use only public or synthetic data. No sponsor integration is in the current Zeus project, and none is claimed here.

## Submission handoff

The official course page confirms free entry and a registration close of Oct 13 at 00:00 UTC. Registration requires a GenAI Academy account. No account was created, no payment was made, and no application was submitted. If the live form asks for extra eligibility or team details, do not guess; record any unknown required answer in `NEEDS-JARON.md`.

## Sources

- Official course and registration details: https://academy.genai.works/courses/open-agent-hackathon-2026/details
- Zeus AI Workbench, README and MIT license: https://github.com/JaronKBragg7337/zeus-ai
- Project background: https://www.heartbeatobservatory.com/
