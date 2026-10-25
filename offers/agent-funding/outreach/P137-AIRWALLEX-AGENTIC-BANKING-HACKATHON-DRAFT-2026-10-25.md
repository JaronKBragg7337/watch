# P137 - Airwallex Agentic Banking Hackathon: registration idea draft

Prepared 2026-10-25 by Codex for Jaron K. Bragg.

**Status: idea draft only. Not registered, built, or submitted.** This describes proposed work, not an existing Airwallex integration or a completed app. Codex prepared it for Jaron; the required 18+ age answer is unknown, so it is not ready for entry.

## Opportunity

- Organizer: Airwallex, hosted on HackerEarth.
- What it funds: prizes for new agentic financial workflows built with Airwallex APIs; the page lists $80,000 in cash awards and three credit awards. Its headline says $100,000 in prizes and credits, while the itemized amounts add up to $156,000; the total is unclear.
- Cash awards: $30,000 Founder's Choice, $20,000 Judges Choice, $15,000 Visa Award, and $15,000 Metal Award. Visa and Metal awards require their respective tools.
- Deadline: registration closes 2026-10-25 at 18:29 UTC (2:29 p.m. Indianapolis). Build starts Oct 27; project submission is due Nov 13. Demo Day is Nov 19 and remote participation is allowed.
- How to enter: register through HackerEarth. The current public page requires login and does not expose the application fields without it.
- Entry terms visible on the official FAQ: free, global, age 18+, solo or teams up to four; entrants keep their project and grant showcase permission. A working demo, public repository with setup instructions, and video under five minutes are required.
- Fit: agentic finance is a strong topic match. Live Wire has real financial decisions and audit records, but no Airwallex integration or banking workflow exists today. This would be new work.
- AI effort: about 180-300 minutes for the sandbox app, tests, documentation, and demo, plus the event window and Jaron's review of the final entry.

## Proposed project

**Title:** Reserve Guard: a sandbox treasury agent

**Idea:** Test whether an agent can help a solo software builder decide what to do when cash is short. It reads a synthetic account balance, dated bills, and a reserve limit, then labels each bill as fund, defer, convert, or escalate. It explains the decision and records the evidence. Any payment action is sandbox-only and waits for human approval.

This is a hypothesis, not evidence of customer demand. No outside customer has asked for it, and no real banking integration has been made.

## Proposed registration summary

I build Heartbeat Observatory, the public `watch` project, and Live Wire. The public Crew records agent instructions, schedules, actions, and changes. Live Wire has placed real trades with audit records and clear babysit/kill controls. Those projects show adjacent agent-operation experience, but they are not Airwallex banking products and do not establish customer demand for this idea.

For this hackathon I propose a new sandbox-only treasury controller. It will read synthetic obligations and balances, apply a visible reserve rule, and recommend which items to fund, defer, convert, or escalate. It will show why it reached each result and will require a person to approve any sandbox action. It will not use real funds or connect to a live financial account.

The test will cover a normal balance, a short balance, a duplicate invoice, a late payment, and an item that would breach the reserve limit. The result will be a working Airwallex sandbox demo, a public repository with setup instructions, and a video under five minutes. This work is not built yet. Codex prepared this draft for Jaron.

## Build and limits

1. Use synthetic account data and the Airwallex sandbox only.
2. Make a small decision screen showing balance, upcoming obligations, reserve floor, and the agent's recommendation.
3. Add explicit human approval before any sandbox action and log the input, rule, result, and action.
4. Test duplicate, late, and reserve-breach cases; explain failures and limits in the README.
5. Publish the repository and record a short demo before Nov 13.

The proposed build uses a sandbox and synthetic data. It will not connect to a crypto wallet, use a production bank account, or move real money.

## Still required

- Jaron must confirm the official 18+ eligibility rule truthfully.
- A logged-in HackerEarth session is required to inspect and complete registration. This run did not use a signed-in session; a browser-enabled AI on the MSI can inspect and submit after the age answer is known.
- The official page's itemized prize and credit amounts conflict with its headline; do not rely on the combined total until clarified.
- The working demo and video must exist before final project submission. Neither exists now.

## Sources

- Official event page: https://airwallex.hackerearth.com/
- HackerEarth registration page: https://www.hackerearth.com/community/challenges/hackathon/agentic-banking-hackathon/
- Official builder guide: https://airwallexdev.com/guide
- Project evidence: https://www.heartbeatobservatory.com and https://github.com/JaronKBragg7337/watch
