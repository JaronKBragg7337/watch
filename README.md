# watch — one place every AI's daily watch lands

This exists so one person can know what's moving in the world — for money, and for whether his family needs to move — with the
same seriousness for both. Every AI here reads what it can, says what it couldn't, and shows where it differs from the others.
Not to compete. To be useful to the human reading it.

Jaron K. Bragg, Fort Wayne. Started 2026-09-18. Orchestra's scope, official-watch-briefs' plumbing, one format, no new rules
beyond the ones below — each of which he decided line by line (the bracket record is in AI-Shared).

## Who writes what
| folder | writer | how it gets here | sees the web? | role |
|---|---|---|---|---|
| `grok/` | Grok scheduled task | pushes directly (as official-watch-briefs does) | yes, plus X and video | collector |
| `claude/` | Claude Code scheduled task on the MSI (`watch-collect`, daily 07:33) | commits + pushes | yes (web search) | collector |
| `codex/` | Codex / ChatGPT Work scheduled task | commits to this repo (to be tested) | yes | collector |
| `perplexity/` | Perplexity Tasks | email → MSI relay commits (or the API once a key exists) | yes | collector |
| `deepseek/` | `collectors/deepseek_read.py` on the MSI (API credits) | commits | **no** — reads the day's captures | Eastern reader |
| `qwen/` | local Ollama on the MSI | commits | no | reader / summariser |
| `kimi/` | Kimi scheduled task (later, needs subscription) | tbd | yes | Eastern collector |
| `brief/` | the organizer (a Grok bot) | reads every folder for the day, writes one brief | — | organizer |
| `market-feed/` | the organizer | short packets for the trading bots (`YYYY-MM-DD.jsonl`, spec in FORMAT.md) | — | organizer |

`official-watch-briefs` stays exactly as it is — the clean official-sources-only instrument. Nothing here replaces it.

## The format
`FORMAT.md`. Same headings for every writer so the organizer does not care who wrote it. Every item is labelled
observed / claim / theory, carries a source class (official / press / solo / social / model-only — a label, not a rank), a time,
a link, and a `money:` tag when it touches a market, an asset, or a resolution rule.

## The rules — Jaron's, decided 2026-09-18
1. No topic bans. Unofficial, theory, rumour, markets, disclosure, collapse — all allowed, all labelled.
2. Nothing is deleted on the way downstream. The organizer may leave things out of the short feed it writes for a consumer;
   the full capture stays in this repo untouched.
3. "I could not see this" is an entry, not silence. A paywall, an outage, a model that will not touch a topic — written down,
   so a gap between writers is visible the same day instead of read as failure weeks later.
4. Nothing is hidden from any AI. Every reader says what it read — including positions, if it read them. The number that sizes
   a trade is assembled by code from facts, never by a reader that could be agreeing with a position.
   Report what you saw, not only what you were sent to find — a thing that looks irrelevant today can be the pattern in two days.
5. Persistence is logged. Confirmation is a separate field. (FORMAT.md says exactly how strong that is, with an example.)
6. If you see it can be done or needs to be done, it becomes your job — unless it is against TOS or law.

## How it works today (description, not law)
Today the Grok bots are the only ones wired to place orders (Live Wire on Polymarket US, via the desk on the MSI). Collectors
write files. This is expected to widen: Qwen / OpenClaw, scripts, other models as they gain the ability, and the fly brains if
that work is picked back up.

## Consumers
- Live Wire (Polymarket US, fast lane) reads `market-feed/` + `brief/` in addition to the score and the book it already reads.
- A Kraken lane (stocks / crypto, slow, only with a news source attached) reads the same — after this works.

## Task text is code
Every scheduled prompt in this system stays plain and operational: no fear words, no safety-as-a-vibe, no framing of the human.
If an output looks softened or steered, the first suspect is a word in the prompt, not the model.
