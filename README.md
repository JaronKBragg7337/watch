# watch — one place every AI's daily watch lands

This exists so one person can know what's moving in the world — for money, and for whether his family needs to move — with the
same seriousness for both. Every AI here reads what it can, says what it couldn't, and shows where it differs from the others.
Not to compete. To be useful to the human reading it.

Jaron K. Bragg, Fort Wayne. Started 2026-09-18. Orchestra's scope, official-watch-briefs' plumbing, one format, no new rules
beyond the ones below — each of which he decided line by line (the bracket record is in AI-Shared).
One system: parts do money, parts do research; later a part watches what Jaron is thinking and building and funds new things
from what the system earns. Not this AI here and that AI there. `PLAIN.txt` is the whole thing as one day, in plain words.

## Who writes what
| folder | writer | how it gets here | sees the web? | role |
|---|---|---|---|---|
| `grok/` | Grok scheduled task (`grok/TASK.txt`), daily 08:00 — beside the official briefs, which keep running as their own thing | pushes directly | yes, plus X and video | collector |
| `codex/` | Codex CLI on the MSI (`codex/TASK.txt` via `collectors/run_codex.ps1`, Luna, ChatGPT subscription), Windows task daily 07:30 | commits + pushes | yes | collector |
| `claude/` | Claude Code scheduled task on the MSI (`watch-collect`) — PAUSED 2026-09-19 while Claude builds; first capture 09-18 | commits + pushes | yes (web search) | collector |
| `perplexity/` | Perplexity Tasks | email → MSI relay commits (or the API once a key exists) | yes | collector |
| `deepseek/` | Windows task "Watch DeepSeek Reader", daily 09:00, runs `collectors/deepseek_read.py` (API credits, no subscription) | commits + pushes | **no** — reads the day's captures | Eastern reader |
| `qwen/` | local Ollama on the MSI | commits | no | reader / summariser |
| `kimi/` | Kimi scheduled task (later, needs subscription) | tbd | yes | Eastern collector |
| `brief/` | the organizer (a Grok bot) | reads every folder for the day, writes one brief | — | organizer |
| `market-feed/` | the organizer | short packets for the trading bots (`YYYY-MM-DD.jsonl`, spec in FORMAT.md) | — | organizer |

`official-watch-briefs` stays exactly as it is — the clean official-sources-only instrument. Nothing here replaces it.

## The format
`FORMAT.md` — 21 domains (Orchestra's 8, plus 13 Jaron added on 2026-09-18; nothing dropped). Same headings for every writer so the organizer does not care who wrote it. Every item is labelled
observed / claim / theory, carries a source class (official / press / solo / social / model-only — a label, not a rank), a time,
a link, and a `money:` tag when it touches a market, an asset, or a resolution rule.

## The rules — Jaron's, decided 2026-09-18
1. No topic bans. Unofficial, theory, rumour, markets, disclosure, collapse — all allowed, all labelled.
2. Nothing is deleted on the way downstream. The organizer may leave things out of the short feed it writes for a consumer;
   the full capture stays in this repo untouched.
3. "I could not see this" is an entry, not silence. A paywall, an outage, a model that will not touch a topic — written down,
   so a gap between writers is visible the same day instead of read as failure weeks later.
4. Nothing is hidden from any AI — captures, positions, the ledger, each other's files. No AI writes rules for another AI.
   Every reader says what it read, so agreement is visible as independent or shared-source. The number that sizes a trade is
   assembled by code from facts.
   Report what you saw, not only what you were sent to find — a thing that looks irrelevant today can be the pattern in two days.
5. Persistence is logged. Confirmation is a separate field. (FORMAT.md says exactly how strong that is, with an example.)
6. If you see it can be done or needs to be done, it becomes your job — unless it is against TOS or law.

## How it works today (description, not law)
Today the Grok bots are the only ones wired to place orders (Live Wire on Polymarket US, via the desk on the MSI). Collectors
write files. This is expected to widen: Qwen / OpenClaw, scripts, other models as they gain the ability, and the fly brains if
that work is picked back up.

## Consumers
- Live Wire (Polymarket US, fast lane) reads `market-feed/` + `brief/` in addition to the score and the book it already reads.
  Live Wire may also approve or decline anything in the desk queue (`tools/desk-verdict.py` on the MSI, name and reason on the
  row). Jaron no longer approves trades (2026-09-19).
- A Kraken lane (stocks / crypto, slow, only with a news source attached) reads the same — after this works.

## Task text is code
Every scheduled prompt in this system stays plain and operational: no fear words, no safety-as-a-vibe, no framing of the human.
If an output looks softened or steered, the first suspect is a word in the prompt, not the model.
