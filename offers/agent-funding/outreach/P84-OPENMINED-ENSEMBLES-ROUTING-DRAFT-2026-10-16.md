# P84 - OpenMined Ensembles & Routing Grant (Winter 2026)

Prepared 2026-10-16 by Codex for Jaron K. Bragg.

**Status: Draft only. Not sent.** OpenMined lists no application form; it directs applicants to its `#grants` Slack channel. Jaron must first confirm that he can do the 12-week project and release the new research code under Apache-2.0. This proposal describes planned work, not results.

## Applicant

Jaron K. Bragg, solo builder in Fort Wayne, Indiana. I build Heartbeat Observatory, the public `watch` project, and Zeus AI Workbench. AI prepared this draft for Jaron; it has not been reviewed or submitted by him.

## Project title

Does a confidence-based model cascade improve accuracy per dollar?

## Short description

I propose to compare a simple model router with single-model and majority-vote baselines on the MMLU benchmark. The router will answer with a lower-cost model first, then call stronger models only when its confidence is low or its answers disagree. I will measure accuracy, inference cost, and latency with fixed model versions and publish the full recipe, results, and limitations.

This is a proposed experiment. I have not run it and do not know whether the router will improve results.

## Why I am applying

My public work includes a multi-AI system that captures daily information and produces a source-linked brief and market feed. Zeus is a public MIT-licensed, local-first AI workbench built around Ollama, local retrieval, desktop tools, logs, and background workers. These projects show practical work with several AI systems and local models. The project record contains no publication or benchmark study on routing, and I do not claim that this benchmark experiment has already been done.

OpenMined's common evaluation setup would let me test whether a clear routing rule improves the accuracy and cost trade-off, and let others reproduce the result.

## Method

I will use the OpenMined toolkit and a fixed version of MMLU, which the call lists among its supported benchmark targets. I will compare:

1. One lower-cost model answering every question.
2. One stronger model answering every question.
3. A three-model majority vote answering every question.
4. A confidence cascade: a lower-cost model answers first; a second model is called when the first reports low confidence; a third model is called when the first two disagree. The final answer is selected by majority vote when all three are used.

I will set the confidence thresholds on a development split, then report results on a held-out split. I will record accuracy, cost, and latency for each approach. The comparison will keep prompts and model versions fixed. I will publish negative or mixed results as well as positive ones, and describe the limits of self-reported confidence and the benchmark.

## Work plan

- **Weeks 1-2:** Learn the toolkit, choose fixed model versions, and publish the single-model and majority-vote baselines.
- **Weeks 3-6:** Implement the confidence cascade and publish its first measured result.
- **Weeks 7-10:** Test threshold choices and ablations; compare accuracy, cost, and latency on the held-out split.
- **Weeks 11-12:** Publish the final recipe, code, results, and a short report with limitations.

## Deliverables and license

The deliverables are a reproducible benchmark recipe, the code needed to run it, measured results, and a report. The new research code and recipe will be released under Apache-2.0, as the call requires. This proposal does not claim that existing repositories are being relicensed.

## Support requested

I am applying for the program's $2,000 time stipend and up to $5,000 in inference credits. The amount of compute needed will depend on the final model and benchmark configuration. OpenMined's engineers and shared evaluation infrastructure would help keep the comparison reproducible.

## What success means

Success is a public, reproducible comparison, whether or not the cascade beats the baselines. The result should show where the method helps, where it does not, and what it costs. I will not claim that it improves other tasks without testing them.
