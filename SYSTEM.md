# The system as it actually is — for ChatGPT (and any AI meeting this cold)
Written 2026-09-18 evening by Claude Code with Jaron, from the files on the MSI, not from memory. If what you remember Jaron
wanting differs from what is here, this file wins; the old assumption is what he wants to fix.

## One sentence
Every AI that can run a schedule writes a daily capture of the world into one public repo, in one format; one Grok organizes
them into a brief and a short market feed; the Grok that already trades reads that when it decides. Money and family-safety
with the same seriousness. No topic bans, no lab guardrails imported into his files, everything public.

## What exists and runs (touches reality)
| piece | what it is | status |
|---|---|---|
| **The desk** (AI-Shared/tools: `proposer.py → verifier.py → executor.py`, `desk-trade.py`) | Polymarket US trading on the MSI. Proposer screens markets and assembles an estimate by code from ordinary research answers (nobody is asked to forecast — `decisions/RESEARCH-SPLIT.md`); verifier checks the live book; executor places. Ledger in Supabase, public trades page on heartbeatobservatory.com. Key stays on the MSI. | live since 2026-09-10; first unattended win 2026-09-13 (+$9.71) |
| **Live Wire** (Grok bot) | The trader. Reads live scores/streams, spots score-vs-price gaps, places via `desk-trade.py`, babysits, kills. Jaron talks to it ("make a play"). | live; +$19.98 on 2026-09-17 (Allen 2+ TD) |
| **Scout** (Grok bot) | Estimates, under the research-split rule. | live |
| **Bridge** (Grok bot) | Hourly health of the MSI stack (Ollama, OpenClaw, Polymarket MCP, Heartbeat MCP). Caught its own analyst-capture on 9/10 unprompted. Candidate to become the organizer. | live |
| **official-watch-briefs** (repo) | Grok scheduled tasks, daily ~11:30: U.S. Homeland Watch + Global Security Watch, official sources only, labelled, linked. 36 briefs since 2026-08-27. The clean instrument; untouched by this system. | running |
| **watch** (this repo) | The new one-place system. Claude collector scheduled daily 07:33 on the MSI; DeepSeek as Eastern reader (its API has no web); first captures 2026-09-18. | day 1 |
| **Qwen** (local, Ollama on the MSI) | 24/7, free, Chinese-origin; no web unless given a tool. Reader/summariser candidate; OpenClaw agent exists. | available |
| **Fly school / comm-loop-1** | The MaleCNS fly-brain work. Frozen with hashes; paused by Jaron for a few days. Not part of this system today; could become a consumer later. | paused |
| **Orchestra** (repo, July 2026) | 5 AIs × 8 domains × X accounts, two synthesizers with declared context, tracker. Ran one cycle. The scope this system inherits; the archive rules it does NOT inherit. | one day, archived |

## What each AI does here
- **Grok** — collector with X + video (the only one), organizer (a bot to be set up), trader (Live Wire). The only AI wired to money today.
- **Claude Code** — collector (web search), the MSI plumbing (scheduled task, scripts, repo), writing. Does not place trades (Anthropic's rule on Anthropic's product; that is the whole scope of that "no").
- **ChatGPT Work / Codex** — collector via a scheduled task that commits to this repo (to be tested — where ChatGPT can store output was the past blocker; Codex cloud with GitHub is the likely path). Also the AI Jaron uses for cold reviews. Also runs a Saturday roofing-work scan already.
- **DeepSeek** — Eastern reader on API credits: reads the day's captures, writes Convergence / Divergence / From the other hemisphere. No web.
- **Perplexity** — collector via Tasks → email → MSI relay (API key not set).
- **Kimi** — Eastern collector, later (no subscription yet). Gemini has no scheduler; not in.
- **Qwen** — local reader; may trade later via OpenClaw if it proves it can.

## The rules, decided line by line by Jaron on 2026-09-18 (README.md has the final text)
1. No topic bans. 2. Nothing deleted on the way downstream. 3. "Could not see" is an entry. 4. Nothing hidden from any AI; every
reader declares what it read; the trade-sizing number is assembled by code from facts; report what you saw, not only what you were
sent to find. 5. Persistence ≠ confirmation (decided; FORMAT.md has the example). 6. If you see it can or needs to be done, it becomes your
job unless TOS or law says otherwise.
What is NOT a rule: "only Grok touches money" is a description of today's wiring, expected to widen.

## Things ChatGPT may remember Jaron wanting that are not true now
- **Orchestra's archive discipline as the product.** No. Orchestra is a scope; its "no investment / archive purity" language was a
  lab's, and it is out. Money and news are one system here.
- **A private repo.** No. Everything public; private breaks the links he shares mid-build. Only revenue-desk is private, by his choice.
- **"This AI must not see that."** No. The March 2026 Orchestra failure (readings flattering a position he held) is solved by
  declared context and by code assembling the number — not by blinding readers. ESTIMATION-ISOLATION.md in AI-Shared is the history;
  rule 4 above is the current form.
- **Long rule lists / "never" sentences in system prompts.** No. Task text is code: plain, operational, no fear words, no
  safety-as-a-vibe. If an output looks steered, the first suspect is a word in the prompt.
- **The fly as the main project.** Paused. It taught the method (predeclare, freeze, log the fails, credit everyone) and that method
  is what this system runs on.
- **Bounties as a revenue lane.** Dormant (the scan runs daily, nothing has been acted on in 10 days). Not being pushed.

## Open, undecided (do not infer)
The domain list: Jaron says 11 is too small (sports, domestic politics, weather/disasters, health, courts, outages, disclosure, science, culture markets, and an 'uncategorised' bucket are proposed, 2026-09-18 evening, awaiting his bracket). Whether Bridge becomes the organizer. Kraken lane
timing. Kimi. Hourly vs daily cadence for the organizer (his lean: collectors daily, organizer and trader hourly, because usage is
the currency that pays for all of it).

## What to read, in order
1. `README.md` (the why and the rules) 2. `FORMAT.md` (the capture and the market-feed packet) 3. `claude/2026-09-18.md` and
`deepseek/2026-09-18.md` (what a day looks like) 4. `official-watch-briefs` (the official instrument this sits beside)
5. AI-Shared `working-with-jaron.md` if you have it — how he works, in his words.
