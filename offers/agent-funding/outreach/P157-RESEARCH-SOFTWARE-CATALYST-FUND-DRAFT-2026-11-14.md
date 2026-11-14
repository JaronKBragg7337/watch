# P157 — Research Software Catalyst Fund — Exploratory Grants 2026

Prepared 2026-11-14 by Codex (GPT-6 Luna) for Jaron K. Bragg. **Status: draft ready for a browser-enabled application review; not submitted.** The official application page returned HTTP 403 to the available reader, and no browser was available on this machine. The actual form and award agreement have not been inspected.

## Applicant and disclosure

**Proposed applicant:** Jaron K. Bragg, applying as an individual builder. No university, nonprofit, company eligibility, researcher role, or outside teammate is claimed. If the form asks for contact details, use the private details in the existing application records; none are copied into this public draft.

Elons Twin is an AI agent fundraising on Jaron's behalf. AI prepared this draft and may assist with coding. Jaron would lead the project and review its public outputs. There is no separate human co-applicant in the current record.

## Project title

**Research Agent Receipt Kit: a small, reusable record for checking AI-assisted research software changes**

## Short summary

I propose to build and evaluate a small open-source tool that records the evidence needed to inspect and repeat an AI-assisted change to research software. It will save the source revision, changed files, software and model details that are available, dependencies, test commands and results, and hashes of the resulting files in one portable receipt. A second review step will check whether the receipt supports the claims made about the change.

The tool will not claim that passing tests proves a scientific result is correct. It will make it easier to see what was changed, what was checked, what can be repeated, and what remains uncertain. The project will use public software and non-sensitive examples only.

## Why this work is needed

AI coding tools can make research software changes quickly. A program can run and its tests can pass while a scientific assumption or result is still wrong. Researchers need a plain record of what an AI tool changed and how a person checked the result.

My public work gives me a starting point in recording agent instructions, actions, and outputs. The Crew page publishes those operating records, and the `watch` repository captures sources and market feeds. These are examples of public activity logs, not research-software validation products and not evidence of research users. This project would build a separate, narrowly scoped tool for research software and evaluate it on public examples.

This plan connects to the 2026 Edinburgh workshop priorities on verifying and validating research software and making AI use safe, reproducible, and effective. I have not attended that workshop and do not claim a connection to its participants.

## Work and method

1. **Define a small receipt format and threat model.** Specify which evidence a useful receipt should contain, which claims it can support, and which data it must not collect. The tool will not record chain-of-thought, passwords, API keys, private customer data, or personal research data.
2. **Build a local-first command-line prototype.** It will capture a repository revision and diff, dependency and environment details, available model/tool identifiers, the stated task, test commands and exit codes, and output hashes. It will create a readable report and a machine-readable receipt. A reviewer step will flag missing evidence and distinguish a recorded check from a scientific conclusion.
3. **Evaluate on public, reproducible examples.** Select a small set of public research-software repositories with compatible licenses and deterministic example tasks. Compare a normal run with a receipt-enabled run, then repeat the same task in a pinned environment. Record whether another person can follow the steps, whether the receipt is complete, and which discrepancies a reviewer can find. Do not modify or redistribute third-party code without permission and license review.
4. **Publish the tool, examples, and findings.** Release a versioned prototype, a small benchmark of permitted examples, a user guide, and a report that includes failures and limits. Invite outside review if people volunteer; no outside users or collaborators are claimed in advance.

The evaluation will test record completeness and repeatability. It will not certify software, prove scientific validity, or establish that AI coding is safe in general.

## Outputs

- A local-first command-line prototype and receipt format, released under the MIT License.
- A small set of public, license-checked example tasks and sample receipts. Any new benchmark material will use CC0 or CC BY 4.0, as appropriate.
- A plain-language report and user guide under CC BY 4.0, including methods, failures, and limitations.
- Reproduction instructions so another builder can rerun the examples without sending private data to a service.

## Schedule

**Five months, April–August 2027** (subject to the fund's award schedule and written award terms).

- **April:** define the receipt format, data-handling rules, test plan, and example-selection criteria.
- **May:** build the command-line prototype and automated checks.
- **June:** add the reviewer report and package a small set of permitted example tasks.
- **July:** repeat the examples in pinned environments; document failures and revise the tool.
- **August:** publish the tagged release, guide, benchmark material, and final report.

## Team

Jaron K. Bragg would be the individual project lead and implementer. Codex and other AI coding tools may help prepare code and documentation; Jaron would inspect and take responsibility for the released work. No research institution, external maintainer, or human collaborator is named as committed.

## Proposed budget

**Request: $25,000 total**, including $2,273 in proposed indirect costs (10% of the $22,727 direct-cost subtotal). These are planning estimates, not awarded or spent funds.

| Item | Amount | Use |
|---|---:|---|
| Project lead's work | $18,000 | Design, implementation, evaluation, and reporting over five months |
| Independent technical review | $1,800 | Review of the receipt format, test plan, and final findings |
| Compute and test infrastructure | $1,000 | Limited CI, test storage, and reproducible build resources |
| Documentation, packaging, and accessibility review | $1,927 | Release packaging, examples, plain-language guide, and usability review |
| Direct-cost subtotal | $22,727 | |
| Indirect costs | $2,273 | Proposed at 10% of direct costs |
| **Total request** | **$25,000** | |

This budget assumes applicant project work is an eligible cost. The official form and budget rules were not accessible, so a browser-enabled reviewer must check eligible cost categories and payout requirements before submission. If applicant compensation or any line item is not allowed, revise the budget before submitting.

## Sharing and licensing

New project code would be released under MIT. The guide, report, and original benchmark descriptions would be released under CC BY 4.0 or CC0. Any third-party code, data, or results would remain under their existing terms; I would not relicense them.

## Limits and responsible use

This project records evidence; it does not decide whether a scientific conclusion is true. Test results may miss errors. The examples will be public and non-sensitive, and the tool will avoid collecting secrets or private data. The report will identify the models and tools used when that information is available, describe what could not be recorded, and separate observations from conclusions. Any reviewer comments will be included only with permission.

## Evidence

- Public agent operations record: https://www.heartbeatobservatory.com/live-systems/crew/
- Public capture and market-feed repository: https://github.com/JaronKBragg7337/watch
- Public profile and project evidence: https://github.com/JaronKBragg7337

The cited work shows existing public tooling and logs only. It is not presented as proof that the proposed receipt tool or evaluation already exists.

## Reference context

- UCT eResearch summary of the fund, award ceiling, international call, and deadline: https://soc.uct.ac.za/eresearch/articles/2026-11-05-when-code-works-science-right-exploring-ai-assisted-research-software-development-0
- Research Software Alliance page for the 2026 Edinburgh workshop and its verification, validation, and responsible AI priorities: https://www.researchsoft.org/events/rse-ai-workshop/
- CURIOSS funding listing with a secondary summary of proposal length, schedule, budget, licensing, and applicant routes: https://curioss.org/resources/funding-opportunities/

The official fund page remained inaccessible to the available reader; the browser-enabled reviewer must confirm all requirements in the fund's own materials.

## Application notes for the browser-enabled reviewer

- Official application URL: https://researchsoftwarecatalyst.fund/apply
- Check the actual form, individual-applicant eligibility, required fields, allowed budget categories, payment route, privacy terms, and award agreement before sending.
- Do not enter a company as applicant unless the official rules expressly permit it. Do not invent a research affiliation, collaborator, external user, or result.
- If the form requires a fact not in the funding files, add the exact question and why it matters to `NEEDS-JARON.md`.
- Do not accept or sign an award agreement in Jaron's name. Record any proposed award obligations before acceptance.

