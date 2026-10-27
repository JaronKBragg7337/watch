# P26 - Goose Grant Program: draft application

Prepared 2026-10-27 by Codex (GPT-6 Luna) for Jaron K. Bragg.

**Status: Draft concept only. Not submitted.** The program is rolling and advertises $100,000 for a 12-month project. In Chrome, the first form page showed required name, email, and country fields; the remaining five pages were not inspected because continuing would require entering contact information. No form data was entered. Jaron has not confirmed the project direction, year-long commitment, or license for new work. This is a plan, not a built Goose integration.

## Applicant

Jaron K. Bragg builds Heartbeat Observatory, the public watch system, and Zeus AI Workbench. The proposal is for an open-source project that would be built around Goose. Codex prepared this draft for Jaron.

## Project title

A Source-Backed Funding Desk for Goose

## Short description

I propose to build an open-source Goose extension for scheduled funding research. It would find public grants, ecosystem funds, and builder programs; keep the original source links with each amount, deadline, eligibility rule, and application route; and carry those facts across daily runs. It would draft application text from recorded facts and list questions it cannot answer. A person would review the draft and decide whether to submit. The extension would not connect to a wallet, sign transactions, or invent missing facts.

This is a proposed project. The current Revenue Desk runs as a scheduled Codex job on Windows and has no Goose integration. I have not built or tested this extension.

## Why this fits Goose

Goose is an open-source AI agent, and its grant call specifically invites work on long-running background operation and new agent interaction patterns. Heartbeat Observatory's public Crew shows an operating multi-agent system with published instructions, schedules, activity, and changes. The watch repository describes the daily collection workflow. Zeus AI Workbench is a separate local-first project under the MIT License, with local files, tools, and action records.

These are evidence of a working use case, not evidence of Goose adoption. I have not built a Goose extension, published benchmark results, or documented outside users for this workflow.

## What I would build

The project would make a Goose agent useful for recurring, source-backed research:

1. Add a documented way to run a bounded task on a schedule and keep its state between runs.
2. Store each opportunity with its original source, amount, deadline, eligibility, application route, status, and last-checked date.
3. Compare new page checks with the saved record and show what changed.
4. Draft application text only from known project facts. Put missing answers in a separate handoff instead of guessing.
5. Keep submission separate from research and drafting. The human decides whether to submit; the agent does not connect to wallets or sign transactions.
6. Publish setup instructions and a small test set of archived public funding pages so other Goose users can inspect and repeat the checks.

The research records would be public and would not include private contact, tax, or identity details.

## Work plan

- **Months 1-2:** Confirm the supported Goose extension and scheduling path; publish a small working version and the data format.
- **Months 3-4:** Add source capture and structured records for amounts, dates, eligibility, and application routes.
- **Months 5-6:** Add repeat checks, change detection, and duplicate handling; publish examples of changed and expired opportunities.
- **Months 7-8:** Add draft generation that separates verified facts, plans, and unknown answers; document its limits and AI disclosure.
- **Months 9-10:** Evaluate the workflow against a set of archived public calls. Report extraction errors, missed changes, and cases where the system correctly asks for a human answer.
- **Months 11-12:** Fix the issues found, publish installation and use instructions, and offer suitable changes upstream to Goose.

These are proposed milestones. No schedule, integration, or evaluation result is complete.

## Expected results

The result would be a reusable Goose extension, a documented opportunity record format, a small repeatable evaluation set, and setup instructions. The evaluation would report errors as well as successes. Success would mean that another builder can run the workflow, see where each claim came from, notice when a call changes, and see exactly what the agent cannot know.

I have not measured how much time or money the workflow saves, and I do not claim that other builders use it today.

## License

I propose releasing the new code and documentation under the MIT License, subject to Jaron confirming that choice. The existing Zeus repository is MIT-licensed; this proposal does not change the license of any existing repository.

## Support requested

The Goose page lists a $100,000 grant per project, with milestone-based payments and quarterly progress reviews. I would request the published grant amount for this 12-month work plan. The public page does not describe a required budget format or payout details. I will use the official application and payout process and will not provide a wallet or sign a transaction.

## Commitments and open questions

If selected, this project would require work across 12 months, quarterly progress updates, and delivery against milestones agreed with the program. Jaron must confirm that he can take on that commitment, that Goose is the right project direction, and that the new work should use the MIT License. The application form's full question list still needs a browser review.

## Sources

- Goose grant program: https://goose.vcorp.ai/grants/
- Application form: https://forms.gle/psHBhj8xFY8q1nHP7
- Project evidence: https://www.heartbeatobservatory.com/ and https://github.com/JaronKBragg7337/watch
- Zeus AI Workbench and MIT License: https://github.com/JaronKBragg7337/zeus-ai