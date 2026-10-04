# P57 - Nebius x NVIDIA Global AI Hackathon - concept application draft

Prepared 2026-10-04 by Codex (GPT-6 Luna) for Jaron K. Bragg. Not submitted. This is a proposed update, not a completed project. No Devpost or Nebius account was created, no API key was made, and no service or event terms were accepted.

## Opportunity

- **What it funds:** an online contest for working AI software that runs on Nebius Token Factory or Nebius AI Cloud and uses an NVIDIA open-source model.
- **Prizes:** $50,000 cash in the listed awards, plus four NVIDIA Jetson Orin Nano devices. The largest cash prize is $20,000. There are smaller cash awards for second, third, Tavily use, selected city events, and product feedback. City awards require attendance at one of the named in-person events; none is assumed here.
- **Deadline:** October 30, 2026 at 10:00 a.m. Pacific. Winners are expected around January 11, 2027.
- **How to apply:** join on Devpost, build a qualifying working app, then provide a demo URL, public open-source repo with visible license, short public YouTube demo, project description, and feedback on the Nebius and NVIDIA tools used.
- **Fit:** Zeus AI Workbench is a public MIT-licensed desktop workbench with local retrieval, local memory, tools, and action records. A focused Nemotron/Nebius inference option could fit the Best Apps and Agents or Personal AI track. The repo's README says the base app does not require a cloud service, and no Nebius integration is claimed today.
- **AI work estimate:** about 180-300 minutes to make and document a narrow demo with a runtime call to Nebius and a visible model/action record, then 15-30 minutes for the final entry after the demo exists.
- **Terms:** event entry creates a contract and requires a broad release/indemnity/defense obligation plus publicity use of name, image, and voice. Using the required Nebius API also requires a service account. The existing P39 review found broad Nebius service indemnity and terms that can permit pay-as-you-go charges after credits. Do not create an account or submit before Jaron resolves the questions in `NEEDS-JARON.md`.

## Proposed entry text

### Project name

Zeus Evidence Desk

### One-sentence description

I plan to add a controlled Nebius-hosted Nemotron option to Zeus so a builder can ask a question about public or synthetic project files, see the sources behind the answer, and inspect what the agent did.

### What I plan to build

Zeus already provides local document search, local memory, desktop tools, and an inspectable action history. The proposed change would add one optional inference route through Nebius Token Factory using an NVIDIA open-source model such as Nemotron. The app would keep its files and memory local and clearly show when a selected prompt and its retrieved passages are sent to Nebius for inference.

The demo would use public or synthetic documents only. It would show a source-backed answer, an unsupported question that the system marks as unknown, and an action record for the model request. The demo would not use private personal files, customer data, financial data, wallet connections, or live transactions. The app would not claim that remote inference keeps the prompt local; it would explain the data sent to the service.

This is a proposed, limited update to Zeus, not an existing feature or measured result. The project has no documented outside customer or researcher use today.

### Track and use of required tools

The closest track is **Best Apps and Agents**: a practical research assistant that uses a multi-step retrieval workflow and a remote Nemotron call. The exact Nebius model ID and API behavior would be selected only after the account and service terms are reviewed. The submitted demo must make an actual runtime request to Nebius Token Factory or run on Nebius AI Cloud, and must use an NVIDIA open-source model.

### What problem does it address?

When an AI assistant answers from a project archive, it is useful to know which source supports the answer and what the system did. Zeus already works on local files and records actions. This update would test whether a clearly labeled remote model can answer questions over public or synthetic material while leaving the files, retrieval index, and memory on the builder's computer. The project has not yet been evaluated with outside users.

### Who is building it?

Jaron K. Bragg is the human builder. Zeus AI Workbench is public under the MIT License. AI tools assist with research and software work. Codex (GPT-6 Luna) prepared this draft for Jaron. The new Nebius integration and demo have not been built.

### Demo and source links

- Current public repo: https://github.com/JaronKBragg7337/zeus-ai
- Project context: https://www.heartbeatobservatory.com/

The final demo URL, video, and write-up of the specific changes are not available yet. They must describe code actually built during the submission period.

## Submission boundary

The required service integration and the entry rules both carry terms that may create legal or financial obligations. The Devpost rules also grant use of the entrant's name, image, and voice for promotion. No age answer, account, API key, service terms, personal information, or submission was provided. This draft is not ready to submit.

## Sources checked

- Official event page and published requirements/prizes: https://nebiusglobalaihackathon.devpost.com/
- Official event rules: https://nebiusglobalaihackathon.devpost.com/rules
- Nebius service signup terms review: `outreach/P39-NEBIUS-AI-BUILDER-SIGNUP-DRAFT-2026-09-29.md`
- Public Zeus repo, current README and MIT license: https://github.com/JaronKBragg7337/zeus-ai
