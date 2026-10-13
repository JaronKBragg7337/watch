# P44 - Open Agent Hackathon 2026 - registration draft

Prepared 2026-10-01 and rechecked 2026-10-13 by Codex (GPT-6 Luna) for Jaron K. Bragg. Not submitted. The official page now says registration closes October 22. Registration requires a GenAI Academy sign-in; no account or event registration was created in this lane. Confirm the 16+ eligibility answer in `NEEDS-JARON.md` before registering.

## Opportunity

- **What it funds:** an online build contest for production-oriented AI agents. The page lists up to $20,000 in total value: $15,000 in cash and $5,000 in in-kind rewards. It lists $2,000 / $1,350 / $1,000 for each of three challenge tracks (the Reasoning Architecture second-place prize is $1,300), $1,000 / $600 / $400 for the Wildcard, and a separate $2,000 Bright Data bounty. Awards are not guaranteed.
- **Who can enter:** worldwide; solo or teams of up to five; age 16 or older at the start of the build.
- **Cost:** free entry.
- **Dates:** registration closes October 22, onboarding is October 21, and the build window is October 22 at 00:00 UTC through October 27 at 23:45 UTC. Results are announced November 6.
- **How to register:** open the course page and choose “Register now” using a GenAI Academy account. No payment or subscription is stated on the current event page.
- **Effort:** about 180-300 AI minutes to build, check, document, and demo a small project. The event runs across six calendar days. Entries must use Cursor for development, integrate Zetaris, and run on NVIDIA Nemotron directly or through Meterless.
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

I plan to use Cursor for development, connect Zetaris as the data layer, and run the planned agent on NVIDIA Nemotron directly or through Meterless. I would use only public or synthetic project documents. Bright Data is optional and has a separate bounty. Zeus does not currently include these integrations; none is claimed as done.

## Submission handoff

The official course page was rechecked on 2026-10-13. Registration closes Oct 22; the build runs Oct 22-27. Entries need Zetaris, Cursor, and NVIDIA Nemotron, and the submission needs a 1-4 minute demo video, slide deck, public GitHub repository, and README through HackOS. Registration requires a GenAI Academy account. Jaron's age remains unknown, so no account, age declaration, payment, or event registration was made. If the sign-in flow asks for other eligibility facts, do not guess; record any unknown required answer in `NEEDS-JARON.md`.

## Sources

- Official course and registration details: https://academy.genai.works/courses/open-agent-hackathon-2026/details
- Zeus AI Workbench, README and MIT license: https://github.com/JaronKBragg7337/zeus-ai
- Project background: https://www.heartbeatobservatory.com/
