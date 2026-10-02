# P52 - Graph Hacks: Context for AI Agents - entry draft

Prepared 2026-10-02 by Codex (GPT-6 Luna) for Jaron K. Bragg. Not registered or submitted. Registration requires a WeMakeDevs account and an age/guardian-consent declaration; the current browser has no signed-in session.

## Opportunity

- Organizer: WeMakeDevs with FalkorDB.
- Event: online, worldwide, October 15-18, 2026. Solo entry or teams of up to four are allowed. No registration close date is listed on the event page.
- Prize: the event advertises a $20,000 prize pool, but the prizes are hardware: iPhone 18 Pro, PS5 with GTA VI, M6 Mac Mini, AirPods 5, and shirts. No cash prize is listed. A Mac Mini could support local AI work, but the value is not cash.
- Fit: strong. Zeus AI Workbench has local retrieval, local memory, desktop tools, and action records. The public watch repository contains dated multi-agent reports and source links. The event asks for agents that connect records, remember across sessions, share state, and explain answers with sources.
- New-work rule: FalkorDB must be the main graph database and do central work. The main implementation must be new work begun during the event. Ideas, notes, and graph sketches can be prepared ahead of time.
- Required submission: public source repository, README with graph model, Cypher queries or graph algorithms, demo video, and either a live deployment or complete local setup instructions. AI coding assistance is allowed and must be disclosed; the entrant must understand and explain the project.
- How to register: sign in to or create a free WeMakeDevs account, then choose Register now on the event page.
- Terms: WeMakeDevs requires an account holder to confirm they are 18+ or have parent/guardian consent if under 18. The participant keeps ownership of new work, while WeMakeDevs and event sponsors receive a limited worldwide license to display, demonstrate, and evaluate the submission for the event and promotion. The participant is responsible for taxes on any prize. The platform terms set disputes under England and Wales law and courts. Sponsor data sharing is optional; leave any sponsor-sharing choice off.
- AI time: about 180-300 AI minutes for the new graph build, evidence checks, local setup, documentation, and demo within the four-day event. The event also requires Jaron to review and explain the technical work.

## Draft project

### Project name

Evidence Graph: traceable memory for a public project archive

### What I plan to build

I plan to build a small agent that uses FalkorDB to connect public project records, their sources, the agents that produced them, and the decisions that followed. It will answer questions across those connections, keep project context between sessions, and point to the source behind each answer. When the graph does not support an answer, the agent will say that the record does not establish it.

The first demo would use only public or synthetic data from the watch repository and public project documentation. It would not load private messages, personal files, wallet data, or login-protected material.

### Why this fits the event

The watch repository already has dated reports written by multiple AI systems. Zeus already has local retrieval, memory, and action records. Those are existing project facts, not features I claim already use FalkorDB. The new graph store, queries, and agent workflow would be built during the event.

The graph would be the core record store, not just a picture of data. The agent would use Cypher to follow relationships among a project, a report, an evidence source, an earlier decision, and a later update. I would enter the Agent Memory and Coordination and Company Brain tracks.

### How I would check it

I would prepare a small set of public records and questions with answers that can be checked from the source links. The demo would test whether the agent finds the connected evidence, cites the right source, keeps earlier context, and says “not established” when a source is missing. I would publish the test cases, results, failures, and setup steps.

This is a proposed test. It has not been built or measured yet, and there are no outside users documented for Zeus.

### Who is building it

Jaron K. Bragg is the solo human builder. AI tools assist with research and software development. Codex (GPT-6 Luna) prepared this entry draft. If registered, I will disclose the AI assistance and review the graph model, queries, and code so I can explain them.

## Registration handoff

The age/guardian-consent declaration must be completed by Jaron. The computer-use skill prohibits the agent from completing age verification.

No WeMakeDevs account or event entry was created. The current browser did not have a WeMakeDevs session. The Terms require an age/guardian-consent declaration, which is not in the project records. Jaron must answer that and complete the account step before an AI with a signed-in browser can register. No sponsor-sharing option should be selected.

## Sources

- Event overview and tracks: https://www.wemakedevs.org/hackathons/falkordb
- Event rules: https://www.wemakedevs.org/hackathons/falkordb/rules
- WeMakeDevs Terms of Service: https://www.wemakedevs.org/terms
- Zeus AI Workbench and MIT license: https://github.com/JaronKBragg7337/zeus-ai
- watch repository: https://github.com/JaronKBragg7337/watch
- Heartbeat Observatory: https://www.heartbeatobservatory.com/
